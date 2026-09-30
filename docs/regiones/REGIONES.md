# Regiones de Quintana Roo — selección con evidencia 2026

Autor: **Brandon Uriel García Sánchez** · extraído del plan v3 aprobado (`docs/plan/PLAN_v3.md`) el 27-sep-2026.

## D.1 Criterios de selección (calculados con datos en la Fase 3: `datos/gold/criterios_regiones.parquet`, ver `docs/decisiones/05-planteamiento.md`)
1. **Sargazo:** fuera de la franja en rojo.
2. **Crisis económica o cierres** reportados en 2026.
3. **Saturación:** ocupación o presión de visitantes ya alta.
4. **Fragilidad ambiental o de servicios** (agua, basura, ecosistema).
5. **Hay datos confirmados** para medirla (SITUR-Q, DataTur, INAH, Tren Maya, aeropuerto).

## D.2 Situación 2026 (noticias verificadas)
- **Sargazo récord:** más de **104,700 t** recogidas y se prevén ~130,000 t (+35 % vs 2025); **56 de 140 playas
  en rojo** (agosto); la franja más afectada va **de Tulum a Xcalak** (incluye Mahahual). Solo 5 playas libres.
  [Cadena Política](https://cadenapolitica.com/2026/08/12/sargazo-quintana-roo-2026-record-historico-playas-afectadas/) ·
  [Ámbito](https://www.ambito.com/mexico/lifestyle/56-las-140-playas-del-litoral-quintana-roo-estanm-roja-abundante-presencia-sargazo-agosto-2026-n6308181) ·
  [PorEsto](https://www.poresto.com/quintana-roo/2026/5/16/sargazo-golpea-el-caribe-mexicano-32-playas-afectadas-y-solo-cinco-libres-en-2026.html)
- **Caribe en general:** ocupación de 59.6 % en la semana del 4 al 10 de julio de 2026; quiebran hoteles pequeños.
  [Infobae](https://www.infobae.com/america/agencias/2026/07/14/sargazo-falta-de-vuelos-y-crisis-global-tienen-al-caribe-mexicano-con-ocupacion-del-60/) ·
  [Reportur](https://www.reportur.com/estados-unidos/2026/07/15/qroo-quiebran-muchos-pequenos-hoteles-por-sargazo-y-flojo-mundial/)

## D.3 Regiones EXCLUIDAS como destino a promover
| Región | Motivo 2026 | Evidencia |
|---|---|---|
| **Tulum** | Crisis por sargazo: ventas −60 %, cierres de negocios, ocupación ene–may 69.88 % vs 76.86 % en 2025; conflicto por el Parque del Jaguar | [La Jornada](https://www.jornada.com.mx/noticia/2026/07/16/estados/sargazo-hunde-la-actividad-turistica-en-tulum-ventas-caen-hasta-60-y-cierran-negocios) · [El Quintanarroense](https://elquintanarroense.com.mx/2026/04/17/empresarios-de-tulum-advierten-de-cierres-de-negocios-y-caida-de-visitantes-por-restricciones-en-el-parque-del-jaguar/) |
| **Playa del Carmen, Puerto Morelos** | Sargazo severo; en Puerto Morelos rebasa la limpieza (ocupación 48.9 %) | [Reportur](https://www.reportur.com/mexico/2026/08/11/puerto-morelos-sargazo-rebasa-la-limpieza-de-playas-de-los-hoteles/) |
| **Mahahual y Xcalak** | Dentro de la franja roja Tulum–Xcalak; "situación crítica" según empresarios | [PorEsto](https://www.poresto.com/quintana-roo/2026/5/16/sargazo-golpea-el-caribe-mexicano-32-playas-afectadas-y-solo-cinco-libres-en-2026.html) |
| **Cozumel** | Sin sargazo en la costa oeste, pero **saturado por cruceros**: más de 1 millón de pasajeros en 330 barcos en 59 días; "se declara lleno" | [Reportur](https://www.reportur.com/cruceros/2026/03/15/cozumel-desbordada-con-330-cruceros-en-solo-59-dias/) · [Reportur](https://www.reportur.com/cruceros/2026/02/25/cozumel-se-declara-lleno-por-aeropuerto-cruceros-y-el-ferry/) |
| **Isla Mujeres** | Poco sargazo, pero ocupación de 93.5–95 %; carencias de agua y drenaje en la parte continental | [Quintana Roo Hoy](https://quintanaroohoy.com/quintanaroo/islamujeres/isla-mujeres-ocupacion-hotelera-febrero-2026/) · [Canal 10](https://noticias.canal10.tv/nota/empresarial-turismo/isla-mujeres-mantiene-ocupacion-del-95-por-ciento-en-hoteles-la-isla-llena-de-visitantes-2026-04-16) |
| **Holbox** | "Colapso crónico de infraestructura": basura (más de 90,000 t acumuladas), agua tratada fuera de norma, drenaje obsoleto | [Tribuna de México](https://tribunademexico.com/basura-holbox/) · [Un Mundo Sustentable](https://unmundosustentable.com/noticias/holbox-se-ahoga-fallas-electricas-e-ineficiencia-de-la-capa-afectan-al-turismo/) |
| **Cancún / Costa Mujeres** | Destino saturado de referencia; la zona norte con sargazo excesivo. **Entra como región emisora** (ver D.5) | [Excélsior](https://www.excelsior.com.mx/nacional/sargazo-quintana-roo-record-historico-playas-afectadas-2026) |
| **Bacalar** (condicionada) | Sin sargazo, pero la laguna está en **deterioro ecológico** (estromatolitos, pérdida del color turquesa; turismo +300 % entre 2009 y 2019). Si entra, es solo con tope estricto y sin actividades en la laguna | [UNAM Global](https://unamglobal.unam.mx/global_revista/laguna-bacalar-microbialitos-contaminacion/) · [El Quintanarroense](https://elquintanarroense.com.mx/2025/02/03/en-riesgo-el-color-azul-turquesa-de-la-laguna-de-bacalar/) |

## D.4 Evidencia oficial: visitantes del INAH en Quintana Roo

Fuente: DataTur `BdINAH.zip` (`Bd_INAH.xlsx`), descargado el 27-sep-2026. Cálculo: suma de `Visitantes`
(nacionales + extranjeros) por `Nombre` y `Año`, filtrando `Estado = Quintana Roo`. Las ecuaciones y un ejemplo
resuelto a mano están en `docs/metodologia/ECUACIONES.md` §1. En la Fase 1 la ingesta formal reproduce estas cifras.

| Sitio | 2019 | 2024 | 2025 | Var. ene–jul 2026 vs 2025 | % extranjeros 2025 |
|---|---:|---:|---:|---:|---:|
| Z.A. Tulum (referencia saturada) | 1,996,544 | 1,245,294 | 1,031,443 | **−31.3 %** | 62 % |
| Z.A. Cobá | 750,113 | 207,812 | 191,815 | −3.7 % | 67 % |
| Z.A. Chacchoben | 176,427 | 195,357 | 237,039 | +1.1 % | 92 % (crucero) |
| Z.A. San Gervasio (Cozumel) | 134,346 | 121,326 | 143,541 | −20.7 % | 91 % (crucero) |
| Z.A. Ichkabal (abrió en 2025) | — | — | 38,186 | −27.5 % | 19 % |
| Z.A. Kohunlich | 42,813 | 6,222 | 21,850 | **+13.5 %** | 66 % |
| Z.A. Oxtankah | 13,772 | 1,603 | 11,017 | −4.6 % | 5 % |
| Z.A. Dzibanché-Kinichná | 21,326 | 945 | 6,592 | **+69.2 %** | 44 % |
| Z.A. Muyil | 18,131 | 10,751 | 0 (cerrada) | 13,654 en ene–jul 2026 | — |

Muyil estuvo cerrada del 4-jun-2024 al 10-feb-2026 por obras del PROMEZA
([INAH](https://inah.gob.mx/boletines/gracias-al-promeza-reabre-al-publico-la-zona-arqueologica-de-muyil-en-quintana-roo));
por eso su 2025 vale 0 y no es un error de datos.

## D.5 Foco final: 5 regiones (decidido por Brandon el 28-sep-2026)

El 27-sep se eligieron 8 destinos. El 28-sep Brandon pidió **quitar todo lo que tenga sargazo, cierres o relación con
Tulum y enfocarse en 5**. Salieron Cobá, Muyil y Ribera del Río Hondo, y la quinta región elegida fue Laguna
Milagros–Xul-Ha.

### Destinos que promueve la campaña (5)
| # | Región | Municipio | Por qué sí | Condición / riesgo | Cómo se mide |
|---|---|---|---|---|---|
| 1 | **Chetumal (ciudad)** | Othón P. Blanco | Ocupación de 58.0 % en ene-2024 (SITUR-Q); el turismo beliceño cayó hasta 60 % en 2026 → capacidad ociosa; 1,836 negocios turísticos en el municipio (DENUE) | 🟡 Sargazo en los canales de entrada de la bahía (ver abajo) | SITUR-Q Chetumal (habitaciones, Tren Maya, Belice), aeropuerto Chetumal (D3), DENUE |
| 2 | **Bahía: Calderitas–Oxtankah** | Othón P. Blanco | Oxtankah: 11,017 visitantes en 2025, 95 % nacionales; Calderitas es la "capital gastronómica del sur" | 🟡 Mismo riesgo de la bahía | INAH Oxtankah, DENUE, ITER |
| 3 | **Ruta arqueológica del sur** (Kohunlich, Dzibanché, Ichkabal) | Othón P. Blanco | 66,628 visitantes en 2025; Kohunlich (+13.5 %) y Dzibanché (+69.2 %) crecen en 2026 | Bajo | INAH, Tren Maya |
| 4 | **Maya Ka'an interior + Kantemó** (Felipe Carrillo Puerto, Ocom, Tihosuco, Señor, Chunhuhub, José María Morelos) | Felipe Carrillo Puerto y José María Morelos | 8 experiencias comunitarias promovidas en 2026; estación del Tren Maya; 76 comunidades | Poca oferta (402 y 169 negocios turísticos): **tope por capacidad** | SITUR-Q "Maya Ka'an", ITER, DENUE |
| 5 | **Laguna Milagros–Xul-Ha** | Othón P. Blanco | Producto turístico consolidado por Othón P. Blanco en 2026; sin sargazo; forma ruta con Chetumal | Sistema lagunar frágil (el mismo de Bacalar) → **tope estricto**, sin actividades invasivas | DENUE, ITER (sin serie turística propia: hueco declarado) |

Fuentes: [Heraldo: productos de Othón P. Blanco](https://quintanaroo.heraldodemexico.com.mx/local/2026/2/24/consolidan-othon-p-blanco-siete-productos-turisticos-con-identidad-propia-13326.html) ·
[Gob. Q. Roo: Maya Ka'an](https://qroo.gob.mx/con-8-experiencias-de-turismo-comunitario-de-maya-kaan-quintana-roo-muestra-la-riqueza-del-caribe-mexicano-en-la-feria-turistica-del-mundo-maya-2026/) ·
[El Universal: Kantemó](https://www.eluniversal.com.mx/destinos/kantemo-la-cueva-de-las-serpientes-colgantes-en-quintana-roo/) ·
[INAH: Kohunlich](https://inah.gob.mx/boletines/reabrira-al-publico-la-zona-arqueologica-de-kohunlich-en-quintana-roo)

### Referencia (no se promueve ni aparece en la portada ni en las piezas)
| Región | Para qué se usa | Por qué no se promueve |
|---|---|---|
| **Cancún** | Origen del turista al que se le habla y punto de comparación de la saturación (única ocupación hotelera medida en 2025–2026: DataTur semanal) | Sargazo y saturación en 2026 |
| **Riviera Maya** (incluye Playa del Carmen) | Origen del turista y punto de comparación | Sargazo en rojo |
| **Tulum** | Punto de comparación de la saturación (visitas INAH) | Sargazo, caída de ventas de hasta 60 % y cierres de negocios |

### Retiradas el 28-sep-2026
| Región | Motivo |
|---|---|
| Cobá + Punta Laguna | Pertenece al municipio de Tulum (sargazo y cierres en 2026) |
| Muyil | Estuvo cerrada del 4-jun-2024 al 10-feb-2026 y colinda con Tulum |
| Ribera del Río Hondo | Sin ninguna serie turística propia |

### Descartadas antes
- **Chacchoben:** 92 % de sus visitantes son de crucero y llegan por Mahahual (franja roja de sargazo).
- **Kantunilkín–Chiquilá:** evidencia débil; es la puerta de entrada a Holbox.

**Consecuencia para el plan:** la campaña es una **ruta sur–Maya Ka'an de cultura, bahía, laguna y comunidad**.
Cuatro de las cinco regiones están en Othón P. Blanco, así que la campaña puede venderse como un solo viaje. En la
Fase 3 se calcula la tabla de criterios D.1 para las 5 regiones, con Cancún, Riviera Maya y Tulum como referencia.

### Verificación del 28-sep-2026: sargazo en la Bahía de Chetumal
ECOSUR confirma sargazo en los canales de entrada de la bahía (Canal de Zaragoza y río Bacalar Chico). No hay reporte
en la costa de Chetumal ni en Calderitas. Las regiones 1, 2 y 5 (todas en la bahía o junto a ella) siguen como destinos, con vigilancia. La evidencia
(HTML, capturas y párrafos) está en `datos/bronze/evidencia_sargazo/2026-09-28/` y el detalle en
`docs/decisiones/03-ingesta.md`.

### Revisión con datos oficiales (Fase 2, 28-sep-2026): Isla Mujeres
La ocupación de 93.5–95 % que usamos para excluir a Isla Mujeres venía de noticias. DataTur registra **74.7 % (febrero)
y 43.2 % (abril) de 2026**. Ya no se reevalúa: con el foco en 5 regiones queda fuera de todos modos. El caso se
conserva como ejemplo de fuentes que no coinciden. Detalle en `docs/decisiones/04-silver.md`.
