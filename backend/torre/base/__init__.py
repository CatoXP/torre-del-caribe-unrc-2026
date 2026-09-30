# Autor: Brandon Uriel García Sánchez
# Módulo: Base de datos
# Qué hace:          Ingesta de fuentes oficiales (Bronze) y transformación con PySpark (Silver/Gold).
# Por qué así:       Arquitectura medallón en Parquet: separa crudo inmutable de datos limpios y del modelo estrella (criterio 2 de la rúbrica).
# Datos de entrada:  D1–D13 de docs/datos/INVENTARIO.md
# Alimenta a:        Todas: sin datos confiables no hay decisión
