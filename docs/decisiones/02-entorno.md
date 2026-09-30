# 02 — Entorno de trabajo (Fase 0: cimientos)

Autor: **Brandon Uriel García Sánchez** · 27-sep-2026 · *Escrita para que cualquier integrante la defienda en el coloquio.*

## Decisión
El proyecto corre en un entorno propio (`.venv`, Python 3.11.9) con **PySpark 3.5.6 + Java 17 (OpenJDK
17.0.20.1 de Microsoft) + winutils/hadoop.dll 3.3.6**. Todas las versiones están fijas en `requirements.txt`.

## Por qué (evidencia)
- **Java:** la máquina solo tenía **Java 1.8.0_481** (verificado el 26-sep-2026). PySpark 4.x, que es lo que instala
  pip por defecto, exige Java 17. Se instaló JDK 17 con `winget install Microsoft.OpenJDK.17`.
- **Java 8 queda intacto:** `backend/torre/base/entorno.py` apunta `JAVA_HOME` al JDK 17 **solo dentro del proceso
  del proyecto**, así que no se cambia nada más en Windows.
- **PySpark 3.5.6 y no 4.x:** es la línea compatible con los binarios de Hadoop 3.3.6 para Windows, que sí existen
  y se verificaron. Sin `winutils.exe` y `hadoop.dll`, Spark no puede escribir Parquet en Windows.
- **Entorno aislado:** Graphify (extra `[leiden]`) bajó el `numpy` del Python global a 1.26.4. El `.venv` evita que
  eso u otra instalación afecten al proyecto.
- **Binarios de Hadoop verificados:** están en `herramientas/hadoop/bin/` (fuente `github.com/cdarlint/winutils`,
  versión hadoop-3.3.6). Ambos son ejecutables PE32+ x86-64 y sus huellas SHA-256 son:
  - `winutils.exe`: `496a591eb1e67df2a620f710d529ba6ddfe1c19149e6647cc4e320bb0efd8553`
  - `hadoop.dll`: `d7ab36a68518748cef142be2da5069b4c763c2cd764c1d2e6ac48c7200405be3`

## Opciones descartadas
- **Spark dentro de Docker:** funciona, pero es más pesado de arrancar y de explicar el día del coloquio.
- **Cambiar el Java de todo Windows:** podría romper otros programas que usan Java 8.
- **Instalar en el Python global:** ya estaba alterado por otras herramientas.

## Resultado (gate de la Fase 0)
`tests/test_entorno.py` pasó en **22.93 s**. Spark leyó un CSV de 3 filas, escribió Parquet y, al leerlo de
nuevo, la suma fue 1 + 2 + 3 = **6**, igual a la esperada.

Cómo se reproduce:
```
.venv\Scripts\python -m pytest tests\test_entorno.py -v
```

## Consecuencia
Queda lista la base para la arquitectura Bronze → Silver → Gold (criterio 2, 12 %). La siguiente es la
**Fase 1**: descargar las fuentes oficiales D1–D13 con su manifiesto SHA-256 y el conteo real de filas.
