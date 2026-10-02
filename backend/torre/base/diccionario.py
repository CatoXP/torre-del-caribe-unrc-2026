# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Genera el diccionario de datos (docs/datos/DICCIONARIO.md) leyendo el almacén DuckDB: por cada tabla
#                    de Silver, de Gold y del modelo estrella da su descripción, renglones, y por cada columna su tipo,
#                    % de vacíos, un ejemplo real y qué significa.
# Por qué así:       - Generado, no escrito a mano: si cambia una tabla, el diccionario cambia con ella y nunca queda viejo.
#                      Lo que sí se escribe a mano es el SIGNIFICADO (abajo, en TABLAS y COLUMNAS).
#                    - Toda columna de Silver debe tener significado; si falta, el proceso se detiene (lo vigila
#                      tests/test_silver_fase2.py). En Gold, las columnas que no están descritas remiten a la nota de
#                      decisión de su fase, donde se explica el modelo.
# Datos de entrada:  datos/gold/torre.duckdb (torre.base.almacen).
# Alimenta a:        El informe técnico (criterio 2 de la rúbrica: estructura y documenta los datos) y al equipo.

import duckdb

from torre.base.almacen import ALMACEN
from torre.base.entorno import RAIZ

SALIDA = RAIZ / "docs" / "datos" / "DICCIONARIO.md"

# ---------- Qué es cada tabla ----------
TABLAS = {
    # Silver (limpio y tipado)
    "silver_afac": "Pasajeros por aerolínea en México, por mes (AFAC vía DataTur, 2016 → jul-2026). Nacional.",
    "silver_clima_diario": "Clima diario de 8 puntos de Quintana Roo (Open-Meteo, 1950 → 2026).",
    "silver_clima_horario": "Clima por hora de 8 puntos (Open-Meteo, 2019 → 2026), con hora local.",
    "silver_cruceros": "Arribos y pasajeros de crucero por puerto y mes (DataTur, 2016 → jul-2026).",
    "silver_datatur_ocupacion": "Ocupación hotelera semanal y mensual por centro turístico (DataTur, 2022 → 2026).",
    "silver_denue": "Negocios del país con giro, tamaño y coordenadas (DENUE INEGI), con su categoría turística.",
    "silver_fred_diario": "Pesos por dólar por día (FRED, DEXMXUS).",
    "silver_fred_mensual": "Pesos por dólar promedio del mes e inflación de EE. UU. (FRED).",
    "silver_huracanes": "Posiciones de todas las tormentas del Atlántico cada 6 horas (HURDAT2, NOAA, 1851 → 2025).",
    "silver_inah": "Visitantes a museos y zonas arqueológicas por mes y tipo (INAH vía DataTur, 2016 → 2026).",
    "silver_iter": "Población y viviendas por localidad (Censo 2020, ITER Quintana Roo).",
    "silver_nacionalidad": "Llegadas de extranjeros por avión, por aeropuerto, país y sexo (UPM vía DataTur, 2012 → jul-2026).",
    "silver_restmex": "Reseñas de turistas con calificación de 1 a 5 (Rest-Mex 2025, CC-BY-4.0).",
    "silver_siturq": "Indicadores turísticos de Quintana Roo por destino y mes (SITUR-Q, API pública).",
    # Modelo estrella
    "dim_lugar": "Dimensión de lugares: cada lugar con su papel (promovido, referencia o comparación).",
    "dim_tiempo": "Dimensión de tiempo: un renglón por mes, de 2012 a 2027.",
    "hechos_mes": "Hechos: una medida por lugar, mes y variable, con su fuente. Un hueco no tiene renglón.",
    # Gold (salidas de los modelos)
    "gold_criterios_regiones": "Fase 3. Tabla de los 5 criterios por región (sargazo, cierres, saturación, fragilidad, datos).",
    "gold_lugares_clasificados": "Planeador. Negocios del DENUE clasificados por léxico (hospedaje, comida, qué hacer).",
    "gold_lugares_recomendados": "Planeador. Negocios recomendados por lugar y momento del día.",
    "gold_pronostico_backtest": "Fase 5. Cada pronóstico del origen móvil contra el dato real.",
    "gold_pronostico_calendario": "Fase 5. Calendario lugar × mes: temporada alta, tormenta, lluvia y otro mes u otro lugar.",
    "gold_pronostico_cobertura": "Fase 5. Qué tanto el rango del 90 % contuvo al dato real, por modelo y horizonte.",
    "gold_pronostico_eleccion": "Fase 5. Modelo elegido por serie (menor error con rango confiable).",
    "gold_pronostico_escenarios": "Fase 5. Monte Carlo: escenarios malo/probable/bueno por mes y riesgo de rebasar capacidad.",
    "gold_pronostico_escenarios_anual": "Fase 5. Escenarios sumados al año, por supuesto de golpe de tormenta.",
    "gold_pronostico_forma_anio": "Fase 5. Forma del año: índice estacional de cada mes por serie.",
    "gold_pronostico_fuerza_estacional": "Fase 5. Fuerza estacional por serie (clásica y STL).",
    "gold_pronostico_mes": "Fase 5. Pronóstico de los próximos 12 meses con su rango del 90 % (_est).",
    "gold_pronostico_metricas": "Fase 5. Errores (MAE, MAPE) de cada modelo por serie.",
    "gold_pronostico_poisson_tormentas": "Fase 5. Probabilidad de tormenta por mes (Poisson, 1966–2025).",
    "gold_pronostico_sensibilidad": "Fase 5. Efecto de lluvia y dólar en cada serie, con su p-valor.",
    "gold_pronostico_series": "Fase 5. Series mensuales que se pronostican, con huecos y tramos marcados.",
    "gold_radar_clusters_centros": "Fase 4. Agrupamiento Ward de los centros turísticos del país (DataTur).",
    "gold_radar_estado": "Fase 4. Índice de presión y estado (tranquilo/concurrido/saturado) por lugar y mes.",
    "gold_radar_indice_comparable": "Fase 4. Índice comparable (mismas medidas en todos los lugares).",
    "gold_radar_markov_backtest": "Fase 4. Prueba de la cadena de Markov semanal contra la persistencia.",
    "gold_radar_markov_matriz": "Fase 4. Matriz de transición semanal entre estados (norte, DataTur).",
    "gold_radar_markov_riesgo": "Fase 4. Probabilidad de cada estado a 1–8 semanas.",
    "gold_radar_modelos": "Fase 4. Comparación de clasificadores del estado del mes siguiente.",
    "gold_radar_panel_mensual": "Fase 4. Panel lugar × mes con todas las variables de presión.",
    "gold_radar_prediccion": "Fase 4. Estado esperado del mes siguiente por lugar (_est).",
    "gold_radar_sesgo": "Fase 4. Aciertos del modelo en los 5 lugares contra el norte (sesgo).",
    "gold_reconciliacion_cruceros": "Fase 2. Cruceristas: DataTur contra SITUR-Q, mes a mes, en Cozumel y Mahahual.",
}

# ---------- Qué significa cada columna (las que se repiten van una sola vez) ----------
COLUMNAS = {
    "anio": "Año.", "mes": "Mes (1–12).", "periodo": "Primer día del mes.", "fecha": "Fecha.",
    "archivo": "Archivo crudo de Bronze de donde salió el renglón (rastreo, regla de oro 2).",
    "es_qroo": "Verdadero si es de Quintana Roo.",
    "papel_campana": "Papel en la campaña: promovida, referencia, retirada o excluida (docs/regiones/REGIONES.md).",
    "region_campana": "Región de la campaña a la que pertenece.", "lugar_campana": "Lugar de la campaña al que pertenece.",
    "lat": "Latitud (grados).", "lon": "Longitud (grados).", "latitud": "Latitud (grados).", "longitud": "Longitud (grados).",
    "estado": "Entidad federativa.", "sin_dato_flag": "Verdadero si la fuente no trae dato (hueco; no se rellena).",
    "fuente": "Fuente oficial.", "fuente_tipo": "Tipo de dato de la fuente (observado o reanálisis).",
    "cve_mun": "Clave INEGI del municipio.", "municipio": "Municipio.", "cve_loc": "Clave INEGI de la localidad.",
    "localidad": "Localidad.", "tipo_fila": "Tipo de renglón en la fuente (dato, total o nota).",
    # AFAC
    "tipo_vuelo": "nacional o internacional.", "servicio": "regular o fletamento.",
    "region_aerolinea": "Región de origen de la aerolínea.", "aerolinea": "Aerolínea.",
    "pasajeros": "Pasajeros (AFAC: transportados; cruceros: pasajeros que llegaron en el mes).",
    "sumada_flag": "Verdadero si el renglón suma dos cifras de la misma etiqueta (Virgin America + Alaska, 2016–ene-2018).",
    # Clima
    "punto": "Punto de clima (8 puntos de Quintana Roo).", "temp_max_c": "Temperatura máxima del día (°C).",
    "lluvia_mm": "Lluvia (mm).", "viento_max_kmh": "Viento máximo del día (km/h).",
    "fecha_hora_utc": "Fecha y hora en UTC, como la entrega la fuente.", "fecha_hora_local": "Fecha y hora local (UTC − 5 h).",
    "temp_c": "Temperatura (°C).", "viento_kmh": "Viento (km/h).",
    # Cruceros
    "puerto": "Puerto de cruceros.", "arribos": "Barcos que llegaron en el mes.", "litoral": "Pacífico o Golfo-Caribe.",
    "puerto_sin_cruceros_flag": "Verdadero si el puerto tiene 0 pasajeros en toda la serie (catálogo sin cruceros).",
    # DataTur ocupación
    "centro": "Centro turístico (nombre limpio).", "centro_crudo": "Centro turístico tal como viene en el archivo.",
    "cuartos_disponibles": "Cuartos disponibles promedio diario.", "cuartos_ocupados": "Cuartos ocupados promedio diario.",
    "no_disponible_flag": "Verdadero si la fuente marca el dato como no disponible.",
    "nota_al_pie": "Nota al pie de la fuente (bandera de comparabilidad).", "ocupacion_pct": "Ocupación hotelera (%).",
    "semana": "Semana del año (ISO).", "n_versiones": "Cuántas veces se publicó la misma semana o mes.",
    "revisado_flag": "Verdadero si la cifra cambió entre publicaciones (se conserva la última).",
    "ocupacion_calc_pct": "Ocupación recalculada como ocupados ÷ disponibles × 100 (comprobación).",
    "frecuencia": "semanal o mensual.",
    # DENUE
    "id": "Identificador del negocio en el DENUE.", "nom_estab": "Nombre del establecimiento.",
    "codigo_act": "Código SCIAN de la actividad.", "nombre_act": "Actividad económica.",
    "per_ocu": "Personal ocupado (rango, como lo publica INEGI).", "tipoUniEco": "Tipo de unidad económica (fija o semifija).",
    "entidad": "Entidad federativa.", "cod_postal": "Código postal.", "fecha_alta": "Fecha de alta en el DENUE.",
    "scian_3": "Subsector SCIAN (3 dígitos).", "categoria_turistica": "Categoría turística (hospedaje, alimentos, etc.).",
    "es_turistico": "Verdadero si el giro es turístico.", "personas_min": "Límite inferior del rango de personal.",
    "personas_max": "Límite superior del rango de personal.",
    "coordenadas_flag": "Verdadero si las coordenadas caen fuera de su municipio o faltan.", "cve_ent": "Clave INEGI de la entidad.",
    # FRED
    "pesos_por_dolar": "Pesos mexicanos por dólar.", "n_dias_observados": "Días con cotización en el mes.",
    "n_dias_sin_dato": "Días hábiles sin cotización (feriados).",
    "mes_incompleto_flag": "Verdadero si el mes aún no termina.", "inflacion_eeuu_indice": "Índice de precios al consumidor de EE. UU.",
    # Huracanes
    "id_tormenta": "Identificador de la tormenta (HURDAT2).", "nombre": "Nombre (tormenta o sitio INAH).",
    "hora_utc": "Hora UTC (HHMM).", "marca": "Marca especial del registro (p. ej., L = toca tierra).",
    "estado_sistema": "Tipo de sistema (HU huracán, TS tormenta tropical, etc.).", "viento_kt": "Viento sostenido (nudos).",
    "presion_mb": "Presión central (mb); vacío si la fuente trae −999.", "km_chetumal": "Distancia a Chetumal (km).",
    "dentro_radio_flag": "Verdadero si pasa a ≤ 200 km de Chetumal.", "tormenta_o_huracan_flag": "Verdadero si el viento es ≥ 34 nudos.",
    "era_satelital_flag": "Verdadero desde 1966 (era satelital).", "afecta_sur_flag": "Verdadero si cumple las tres reglas anteriores.",
    "formato_irregular_flag": "Verdadero si la línea original venía mal formada.",
    # INAH
    "clasificacion": "Museo o zona arqueológica.", "tipo_visitante": "nacional o extranjero.",
    "visitantes": "Visitantes en el mes.", "sin_visitantes_flag": "Verdadero si el mes tiene 0 visitantes (suele ser cierre).",
    # ITER
    "poblacion": "Habitantes (Censo 2020).", "viviendas_habitadas": "Viviendas particulares habitadas.",
    "viviendas_con_agua": "Viviendas con agua entubada.", "viviendas_con_drenaje": "Viviendas con drenaje.",
    "viviendas_con_luz": "Viviendas con electricidad.", "reservado_flag": "Verdadero si INEGI reserva el dato por confidencialidad.",
    # Nacionalidad
    "aeropuerto": "Aeropuerto de llegada.", "pais": "País de nacionalidad.", "region_mundo": "Región del mundo.",
    "sexo": "hombre, mujer o no disponible.", "llegadas_extranjeros": "Extranjeros que llegaron por avión en el mes.",
    # Rest-Mex
    "titulo": "Título de la reseña.", "resena": "Texto de la reseña.", "calificacion": "Calificación de 1 a 5.",
    "pueblo": "Pueblo reseñado.", "tipo": "hotel, restaurante o atractivo.", "n_palabras": "Palabras de la reseña.",
    # SITUR-Q
    "unidad": "Destino o zona de SITUR-Q.", "tipo_unidad": "destino, zona o zona especial.",
    "variable": "Variable medida.", "valor": "Valor de la variable.", "n_registros_fuente": "Registros de la fuente que se sumaron.",
    "hueco_flag": "Verdadero si la fuente trae 0 o vacío donde debería haber dato (hueco declarado).",
    "indicador": "Indicador de SITUR-Q (ocupación, cruceristas, Tren Maya, etc.).",
    # Estrella
    "lugar": "Lugar.", "es_de_los_5": "Verdadero si es una de las 5 regiones de la campaña.",
    "papel": "promovido, referencia o comparación.", "trimestre": "Trimestre (1–4).",
    # Reconciliación
    "pasajeros_datatur": "Pasajeros de crucero según DataTur.", "cruceristas_siturq": "Cruceristas según SITUR-Q.",
    "diferencia": "SITUR-Q − DataTur.", "diferencia_pct": "Diferencia como % de DataTur.",
}


def _ejemplo(con, tabla: str, columna: str) -> str:
    v = con.execute(f'SELECT "{columna}" FROM {tabla} WHERE "{columna}" IS NOT NULL LIMIT 1').fetchone()
    if v is None:
        return "—"
    t = str(v[0]).replace("|", "/").replace("\n", " ")
    return t[:40] + ("…" if len(t) > 40 else "")


def describir(con, tabla: str) -> tuple[int, list[dict]]:
    n = con.execute(f"SELECT count(*) FROM {tabla}").fetchone()[0]
    filas = []
    for col, tipo, *_ in con.execute(f"DESCRIBE {tabla}").fetchall():
        vacios = con.execute(f'SELECT avg(CASE WHEN "{col}" IS NULL THEN 1 ELSE 0 END) FROM {tabla}').fetchone()[0] or 0
        filas.append({"columna": col, "tipo": tipo, "vacios_pct": 100 * vacios, "ejemplo": _ejemplo(con, tabla, col),
                      "significado": COLUMNAS.get(col)})
    return n, filas


def faltantes_silver(con) -> list[str]:
    """Columnas de Silver sin significado escrito (debe quedar vacía)."""
    falta = []
    for (t,) in con.execute("SELECT view_name FROM duckdb_views() WHERE view_name LIKE 'silver_%'").fetchall():
        falta += [f"{t}.{c}" for c, *_ in con.execute(f"DESCRIBE {t}").fetchall() if c not in COLUMNAS]
    return falta


def generar() -> str:
    with duckdb.connect(str(ALMACEN), read_only=True) as con:
        falta = faltantes_silver(con)
        if falta:
            raise ValueError(f"Columnas de Silver sin significado: {falta}")
        nombres = [r[0] for r in con.execute(
            "SELECT view_name FROM duckdb_views() WHERE NOT internal UNION ALL "
            "SELECT table_name FROM duckdb_tables()").fetchall()]
        orden = ([n for n in sorted(nombres) if n.startswith("silver_")] + ["dim_lugar", "dim_tiempo", "hechos_mes"]
                 + [n for n in sorted(nombres) if n.startswith("gold_")])
        sin_tabla = [n for n in orden if n not in TABLAS]
        if sin_tabla:
            raise ValueError(f"Tablas sin descripción: {sin_tabla}")
        md = ["# Diccionario de datos — Torre del Caribe", "",
              "Autor: **Brandon Uriel García Sánchez** · Generado por `python -m torre.base.diccionario` desde el almacén "
              "`datos/gold/torre.duckdb`. **No se edita a mano**: el significado de cada columna vive en "
              "`backend/torre/base/diccionario.py`.", "",
              "Capas: **Silver** = limpio y tipado (una vista por tabla) · **Estrella** = dim_lugar, dim_tiempo, hechos_mes "
              "· **Gold** = salidas de los modelos (su método está en la nota de decisión de su fase y en "
              "`docs/metodologia/ECUACIONES.md`). Sufijos: `_est` estimado, `_flag` bandera.", "",
              "| Tabla | Renglones | Qué es |", "|---|---:|---|"]
        detalle = []
        for t in orden:
            n, filas = describir(con, t)
            md.append(f"| [`{t}`](#{t}) | {n:,} | {TABLAS[t]} |")
            detalle += ["", f"## {t}", "", f"{TABLAS[t]} **{n:,} renglones.**", "",
                        "| Columna | Tipo | Vacíos | Ejemplo | Significado |", "|---|---|---:|---|---|"]
            for f in filas:
                s = f["significado"] or "Ver la nota de decisión de su fase."
                detalle.append(f"| `{f['columna']}` | {f['tipo']} | {f['vacios_pct']:.1f} % | {f['ejemplo']} | {s} |")
    texto = "\n".join(md + detalle) + "\n"
    SALIDA.write_text(texto, encoding="utf-8")
    print(f"Diccionario: {len(orden)} tablas → {SALIDA.relative_to(RAIZ)}")
    return texto


if __name__ == "__main__":
    generar()
