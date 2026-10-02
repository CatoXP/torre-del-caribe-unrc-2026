# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Arma el almacén de consulta del proyecto en DuckDB (datos/gold/torre.duckdb):
#                    1. Una vista por cada tabla de Silver (silver_<tabla>) y por cada salida de Gold (gold_<tabla>).
#                    2. El modelo estrella del plan (Fase 2, punto 2):
#                       - dim_lugar: los lugares con su papel (promovido, referencia o comparación).
#                       - dim_tiempo: un renglón por mes de 2012 a 2027.
#                       - hechos_mes: una medida por lugar y mes, en formato largo (lugar, periodo, variable, valor,
#                         fuente), para cruzar fuentes sin tener que saber en qué archivo está cada una.
# Por qué así:       - Spark limpia y escribe (Bronze → Silver), pero para responder una pregunta en milisegundos a la
#                      página o al equipo no hace falta levantar Spark: DuckDB lee los mismos Parquet sin copiarlos.
#                    - Vistas y no copias: si se reconstruye Silver, el almacén ve el dato nuevo sin volver a cargarlo.
#                      Solo las tres tablas de la estrella se materializan, porque son chicas y se consultan mucho.
#                    - Formato largo en hechos_mes: cada fuente aporta las variables que tiene. Un hueco simplemente no
#                      tiene renglón; nunca se rellena con cero.
#                    - Alternativa descartada: una base de datos con servidor (PostgreSQL). Exige instalar y levantar un
#                      servicio, y el proyecto debe correr sin internet en cualquier computadora.
# Datos de entrada:  datos/silver/* (Parquet particionado) y datos/gold/*.parquet.
# Alimenta a:        La página y el informe (consultas rápidas y rastreables), el diccionario de datos
#                    (torre.base.diccionario) y la Fase 9 (endpoint de consulta de solo lectura).

from pathlib import Path

import duckdb

from torre.base.entorno import RAIZ

SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"
ALMACEN = GOLD / "torre.duckdb"

# Variables del panel del Radar que entran a hechos_mes, con su fuente oficial.
VARIABLES_PANEL = {
    "llegadas_tren": "SITUR-Q (Tren Maya)",
    "cruceristas": "SITUR-Q",
    "cruces_belice": "SITUR-Q",
    "visitantes_inah": "INAH (DataTur BdINAH)",
    "ocupacion_pct": "SITUR-Q o DataTur (una sola por lugar, Fase 4)",
    "cuartos": "SITUR-Q",
    "hoteles": "SITUR-Q",
}
# Lugares de referencia (regla de oro 9). Los 5 lugares salen del panel (es_de_los_5).
REFERENCIA = ("Cancún", "Playa del Carmen", "Tulum")


def tablas_silver() -> list[Path]:
    return sorted(p for p in SILVER.iterdir() if p.is_dir() and any(p.rglob("*.parquet")))


def tablas_gold() -> list[Path]:
    return sorted(GOLD.glob("*.parquet"))


def _ruta(p: Path) -> str:
    return p.as_posix().replace("'", "''")


def crear_vistas(con: duckdb.DuckDBPyConnection) -> None:
    for p in tablas_silver():
        con.execute(f"CREATE OR REPLACE VIEW silver_{p.name} AS SELECT * FROM "
                    f"read_parquet('{_ruta(p)}/**/*.parquet', hive_partitioning = true, union_by_name = true)")
    for p in tablas_gold():
        con.execute(f"CREATE OR REPLACE VIEW gold_{p.stem} AS SELECT * FROM read_parquet('{_ruta(p)}')")


def crear_estrella(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("""
        CREATE OR REPLACE TABLE dim_tiempo AS
        SELECT CAST(p AS DATE) AS periodo, year(p) AS anio, month(p) AS mes, quarter(p) AS trimestre
        FROM range(DATE '2012-01-01', DATE '2028-01-01', INTERVAL 1 MONTH) t(p)""")
    con.execute(f"""
        CREATE OR REPLACE TABLE dim_lugar AS
        SELECT lugar, bool_or(es_de_los_5) AS es_de_los_5,
               CASE WHEN bool_or(es_de_los_5) THEN 'promovido'
                    WHEN lugar IN {REFERENCIA} THEN 'referencia' ELSE 'comparación' END AS papel
        FROM gold_radar_panel_mensual GROUP BY lugar""")
    partes = [f"SELECT lugar, CAST(periodo AS DATE) AS periodo, '{v}' AS variable, CAST({v} AS DOUBLE) AS valor, "
              f"'{f}' AS fuente FROM gold_radar_panel_mensual WHERE {v} IS NOT NULL" for v, f in VARIABLES_PANEL.items()]
    # Extranjeros por avión: el aeropuerto se asigna a su lugar (Chetumal, Cancún, Tulum, Cozumel).
    partes.append("""SELECT lugar_campana, CAST(periodo AS DATE), 'llegadas_extranjeros_avion',
                            CAST(sum(llegadas_extranjeros) AS DOUBLE), 'DataTur BD_Nacionalidad (UPM)'
                     FROM silver_nacionalidad WHERE es_qroo GROUP BY ALL""")
    # Pasajeros de crucero según DataTur, solo de los puertos que sí reciben cruceros.
    partes.append("""SELECT puerto, CAST(periodo AS DATE), 'pasajeros_crucero_datatur', CAST(pasajeros AS DOUBLE),
                            'DataTur BaseDatosCruceros'
                     FROM silver_cruceros WHERE es_qroo AND NOT puerto_sin_cruceros_flag""")
    con.execute("CREATE OR REPLACE TABLE hechos_mes AS " + "\nUNION ALL\n".join(partes))
    # Un lugar que aparece en los hechos y no en dim_lugar (p. ej., Mahahual por cruceros) entra como comparación.
    con.execute("""INSERT INTO dim_lugar SELECT DISTINCT h.lugar, false, 'comparación' FROM hechos_mes h
                   WHERE h.lugar NOT IN (SELECT lugar FROM dim_lugar)""")


def construir_almacen(ruta: Path = ALMACEN) -> Path:
    if ruta.exists():
        ruta.unlink()
    with duckdb.connect(str(ruta)) as con:
        crear_vistas(con)
        crear_estrella(con)
        n_s, n_g = len(tablas_silver()), len(tablas_gold())
        n_h = con.execute("SELECT count(*) FROM hechos_mes").fetchone()[0]
        print(f"Almacén DuckDB: {n_s} vistas de Silver, {n_g} de Gold; hechos_mes con {n_h:,} renglones")
        print(con.execute("""SELECT variable, count(DISTINCT lugar) AS lugares, min(periodo) AS desde, max(periodo) AS hasta,
                                    count(*) AS renglones FROM hechos_mes GROUP BY variable ORDER BY variable""").df()
              .to_string(index=False))
    return ruta


def consultar(sql: str):
    """Consulta de SOLO LECTURA al almacén (para la página o el equipo). Devuelve un DataFrame."""
    with duckdb.connect(str(ALMACEN), read_only=True) as con:
        return con.execute(sql).df()


if __name__ == "__main__":
    construir_almacen()
