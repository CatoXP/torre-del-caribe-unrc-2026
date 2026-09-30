# Guía de estilo UNRC para el documento ejecutivo

Autor: **Brandon Uriel García Sánchez** · Proyecto Torre del Caribe

Fuente oficial: *Guía de Identidad Gráfica UNRC 2024-2030*, Universidad Nacional Rosario Castellanos
([PDF](https://www.rcastellanos.cdmx.gob.mx/storage/app/media/Identidad%20UNRC%202025/Manual_Institucional_UNRC.pdf),
consultado el 28-sep-2026). Los números de página se refieren a ese documento.

## 1. Colores institucionales (pág. 9)
| Uso | Nombre | Pantone | HEX | RGB |
|---|---|---|---|---|
| Color principal: títulos, barras de gráficas, encabezados de tabla | **Guinda** | 7420 C | `#9F2241` | 159, 34, 65 |
| Color secundario: acentos, líneas, segunda serie de gráficas | **Dorado** | 465 C | `#BC955C` | 188, 149, 92 |
| Logotipo a una tinta | Gris | Neutral Black C | — | — |

**Regla del manual (págs. 18–19):** *"Por ningún motivo deberán colocarse títulos o cuerpos de texto en color negro."*
Los títulos van en guinda y el cuerpo de texto en gris oscuro (`#3A3A3A`), nunca en negro puro.

Para gráficas con más de dos series se usan, en este orden, los colores de ilustración del manual (pág. 26):
`#9F2241`, `#BC955C`, `#565393`, `#58A65D`, `#8CAFDD`, `#F26E50`, `#465973`.

## 2. Tipografía (págs. 17–19)
- **Títulos:** Patria (la tipografía del imagotipo).
- **Texto e información complementaria:** Noto Sans. El manual sugiere usar de 2 a 3 estilos; aquí se usan Regular,
  SemiBold y Bold.
- Si Patria no está instalada en la computadora donde se edite, Word la reemplaza. En la versión final hay que
  instalarla o usar Noto Sans Bold para los títulos.

## 3. Cómo se escribe (reglas de redacción)
1. **Para alguien nuevo en el tema.** Cada término técnico se explica la primera vez que aparece, con una frase
   sencilla (por ejemplo, "Parquet: un formato de archivo que guarda tablas de forma comprimida y rápida de leer").
2. **Tono de informe, en tercera persona o impersonal:** "El sistema descarga...", "Se eligió... porque...".
   Nunca "ya decidimos", "como te dije", "vamos a", ni ninguna otra forma de conversación.
3. **Cada proceso responde tres preguntas:** qué hace, por qué se hizo así (con el dato que lo justifica) y qué
   resultado dio.
4. **Solo datos reales.** Cada cifra lleva su fuente entre paréntesis (por ejemplo, "SITUR-Q, 2024"). Lo que es
   estimado se dice explícitamente.
5. **Cada capítulo lleva al menos una gráfica o una captura**, con título y la línea "Fuente: ...".
6. **Párrafos cortos** (máximo 5 líneas) y viñetas para las listas.

## 4. Gráficas
- Se generan con `matplotlib` usando los colores de la sección 1, fondo blanco, sin cuadrícula pesada y con los ejes
  en gris.
- Cada gráfica se guarda en `docs/ejecutivo/figuras/` como PNG a 200 ppp, con un nombre que diga lo que muestra
  (por ejemplo, `f1_cobertura_siturq.png`).
- El título dice la conclusión, no solo el tema. Por ejemplo: "Tulum perdió 31 % de visitantes en 2026" en lugar de
  "Visitantes de Tulum".

## 5. Capturas
- Las capturas de la página web y del sistema se guardan en `docs/ejecutivo/capturas/`.
- Cada captura lleva un pie que explica qué se ve y por qué importa.
