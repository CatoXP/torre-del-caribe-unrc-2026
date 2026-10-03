# 09 — Auditoría de las Fases 1 a 4 contra el plan (29-sep-2026)

Autor: **Brandon Uriel García Sánchez** · *Escrita para que cualquier integrante la defienda en el coloquio.*

Brandon pidió "volver a revisar la Fase 4 auditando todo del 1 al 4 y, si todo está bien según el plan, seguir". La
auditoría revisa tres cosas:
1. Si cada punto del plan (`docs/plan/PLAN_v3.md`, B.7) está hecho y dónde está la evidencia.
2. Si los resultados se **reproducen** al volver a correr el código.
3. Si las **cifras escritas** en los documentos coinciden con lo que calcula el código.

## 1. Reproducibilidad y cifras

**Reproducibilidad.** Se volvieron a correr desde cero el panel, el índice, la predicción, la cadena de Markov y la
tabla de criterios. Las **8 tablas de Gold salieron idénticas** a las guardadas:
`radar_panel_mensual`, `radar_estado`, `radar_indice_comparable`, `radar_modelos`, `radar_prediccion`,
`radar_markov_matriz`, `radar_markov_riesgo` y `criterios_regiones`. Los modelos usan semilla fija (`SEMILLA = 0`).

**Cifras de los documentos.** Hay una prueba nueva, `tests/test_documentos.py`, con 21 comprobaciones. Recalcula con el
código las cifras clave (cortes, IPT de Cancún, aciertos del modelo, cortes y Brier de Markov, HHI, cuotas y total de
cuartos) y revisa que `ECUACIONES.md`, `05-planteamiento.md`, `08-radar.md` y el documento ejecutivo digan exactamente
eso. **Las 21 coinciden.** Si en el futuro una fuente se vuelve a descargar y una cifra cambia, la prueba falla.

**Conteo de la Fase 1.** El manifiesto tiene 377 archivos:

| Concepto | Archivos | Registros |
|---|---:|---:|
| Manifiesto completo | 377 | 8,135,278 |
| − Evidencia de sargazo (capturas) | 15 | 70 |
| − Benchmarks de publicidad (capturas y tablas) | 9 | 406 |
| **Fuentes oficiales** | **353** | **8,134,802** |

El resultado coincide con lo que dicen `03-ingesta.md` y el documento ejecutivo.

## 2. Punto por punto contra el plan

### Fase 1 — Ingesta (Bronze) · ✅ completa
| Punto del plan | Estado | Evidencia |
|---|---|---|
| SITUR-Q (indicadores por destino y mes) | ✅ | 14 archivos; `ingesta_siturq.py` |
| DataTur: semanales, mensuales, Nacionalidad, INAH, AFAC, Cruceros, Compendio | ✅ | 166 zips de ocupación; Nacionalidad 521,364 filas; Compendio 2024 (`CETM2024.zip`, 295,191 filas) |
| Rest-Mex, DENUE (32 estados), ITER, clima, huracanes, FRED, geo, ENDUTIH | ✅ | `ingesta_abiertas.py`; DENUE en 33 archivos (el estado 15 viene en 2 partes) |
| D13 benchmarks con captura | ✅ | `ingesta_benchmarks.py` |
| Manifiesto SHA-256 y conteo por fuente | ✅ | `datos/bronze/MANIFIESTO.csv`; prueba de huellas en `tests/test_ingesta.py` |

### Fase 2 — Almacén y calidad (Silver/Gold) · ⚠️ incompleta
| Punto del plan | Estado | Evidencia o falta |
|---|---|---|
| Silver de SITUR-Q, DataTur ocupación, DENUE, INAH e ITER | ✅ | 5 tablas en `datos/silver/` con pruebas |
| Silver de Nacionalidad, AFAC, Cruceros, clima, huracanes, Rest-Mex y FRED | ❌ | Están en Bronze, sin limpiar |
| Modelo estrella en Gold y diccionario de datos automático | ❌ | Gold solo tiene salidas del Radar y los criterios |
| Reconciliación SITUR-Q contra DataTur | ⚠️ | **Hecha en esta auditoría** (sección 3), falta el reporte formal de calidad |
| DuckDB sobre Gold | ❌ | Pendiente (se usa en la Fase 9) |
| Prueba de corte "85,993 reseñas de Q. Roo" | ❌ | Rest-Mex no está en Silver |

**Por qué se avanzó sin cerrar la Fase 2.** Brandon decidió trabajar la página en paralelo (28-sep) y abrir las Fases 3
y 4 con las fuentes que ya estaban limpias. Las que faltan no las usan esas fases: clima, huracanes y tipo de cambio
son de la Fase 5; nacionalidades y reseñas, de la Fase 8. **Consecuencia:** antes de la Fase 5 hay que terminar la
Silver de clima, huracanes y FRED.

### Fase 3 — Planteamiento · ✅ completa (falta el visto bueno formal)
| Punto del plan | Estado | Evidencia |
|---|---|---|
| Notebook de variables, actores y relaciones | ✅ | `notebooks/01_planteamiento.ipynb`, 17 variables, 7 actores, HHI |
| Lugares que promueve la campaña (con la tabla de criterios D.1) | ✅ | 5 regiones; `criterios.py`; las 5 pasan |
| Cómo tratar el sur sin ocupación 2025–2026 | ✅ | Presión de llegada medida (`05-planteamiento.md`) |

### Fase 4 — Radar · ⚠️ hecha, con tres diferencias contra el plan
| Punto del plan | Estado | Evidencia o diferencia |
|---|---|---|
| IPT con ocupación, llegadas por habitación, turistas por residente, densidad de oferta (DENUE) y visitas INAH | ⚠️ | Entraron ocupación, llegadas por residente (tren, cruceros) y visitas INAH por residente. **No entraron** "llegadas por habitación" ni "densidad de oferta"; no se decidió explícitamente |
| Pesos definidos con Brandon y sensibilidad | ✅ | Iguales; sensibilidad ±50 % (0–8.4 % cambian) |
| **Clustering jerárquico de los 54 centros del país (DataTur mensual)** | ❌ | **No se hizo.** Es la parte de minería del Radar en el plan |
| Umbrales tranquilo / concurrido / saturado con Brandon | ✅ | Percentiles comunes p50/p90 |
| Clasificador: logística, Random Forest y Gradient Boosting; validación temporal; F1-macro; importancia de variables | ✅ | `prediccion.py`, origen móvil, importancias |
| **Sesgo** entre norte y sur | ⚠️ | **Medido en esta auditoría** (sección 3): el modelo no puede validarse en los 5 lugares |
| Markov semanal a 1–8 semanas | ✅ | `markov.py` (239 semanas; el plan decía 135 porque se contaba solo 2024–2026) |
| Salidas en Gold, notebook `02_radar` y nota de decisión | ✅ | 6 tablas `radar_*`; notebook; `08-radar.md` (el plan la llamaba `04-radar.md`) |

## 3. Hallazgos nuevos de la auditoría

### 3.1 DataTur y SITUR-Q no miden lo mismo
Ocupación mensual de 2022–2024 en los meses con ambas fuentes:

| Lugar | Meses | DataTur − SITUR-Q (promedio) | Diferencia absoluta media | Correlación |
|---|---:|---:|---:|---:|
| Cancún | 36 | −1.6 puntos | 2.4 | 0.94 |
| Playa del Carmen | 12 | −5.3 | 5.3 | 0.97 |
| Cozumel | 36 | −14.5 | 14.5 | 0.97 |
| Isla Mujeres | 36 | −19.3 | 19.3 | 0.68 |

Las dos fuentes se mueven juntas (correlación de 0.68 a 0.97), pero en niveles distintos. DataTur probablemente mide
otro conjunto de hoteles.
- **Consecuencia para el Radar:** con la opción D, esos 4 lugares usan DataTur y se ven menos ocupados de lo que
  diría SITUR-Q. Es el sentido conservador: si se usara SITUR-Q, el norte saldría todavía más presionado y la
  conclusión "el sur tiene espacio" se sostiene igual.
- Dentro de cada lugar no hay problema, porque cada uno usa una sola fuente en toda su historia.
- La diferencia sí afecta la comparación entre lugares y se declara como limitación.

### 3.2 El modelo no se puede validar en los 5 lugares
En los 12 meses de prueba, los 5 lugares nunca cambiaron de estado: 48 de 48 casos fueron "tranquilo".
- En los 5 lugares, el modelo y la persistencia aciertan el 100 %, pero no hubo ningún cambio que anticipar.
- En el resto del estado, el modelo acierta el 81.5 % contra el 78.7 % de la persistencia y anticipa 7 de 23 cambios.

**Consecuencia:** la afirmación correcta es "el modelo anticipa cambios en los lugares de referencia; en los 5 lugares
de la campaña no ha habido cambios que probar". No se puede decir que el modelo haya probado que anticipa saturaciones
del sur.

## 4. Veredicto
- **Fases 1 y 3:** completas según el plan.
- **Fase 4:** los resultados son reproducibles y las cifras de los documentos son correctas. Pero **no está completa
  según el plan**:
  - falta el clustering de los 54 centros;
  - dos componentes del índice que marca el plan (llegadas por habitación y densidad de oferta) no entraron sin una
    decisión explícita;
  - el sesgo quedó medido, pero debe declararse en la página y en el documento.
- **Fase 2:** incompleta. Hay que terminarla antes de la Fase 5 (clima, huracanes y FRED son insumos del Pronóstico).

Las decisiones que requieren a Brandon quedan en la sección 5 de esta nota.

## 5. Decisiones de Brandon y cómo se resolvieron (29-sep-2026)
| Hallazgo | Decisión de Brandon | Resultado |
|---|---|---|
| El índice no tenía "llegadas por habitación" ni "densidad de oferta" | Agregar llegadas por cuarto (tren + cruceros); la densidad no entra porque es fija en el tiempo | Hecho en `indice.py`. Se le mostró que con cruceros el componente queda dominado por los puertos (Mahahual: 432 por cuarto al mes; mes típico en 0.003 de la escala; con solo tren, 0.12) y decidió mantener tren + cruceros. Se declara |
| Faltaba el clustering de los centros del país | Hacerlo ahora y elegir k con la silueta | `clustering.py`: 55 centros completos, k = 2 (silueta 0.450). Descartado k = 7 (0.317) |
| DataTur mide menos que SITUR-Q | Declararlo, sin ajustar | En la página ("¿Cómo lo sabemos?"), en `ECUACIONES.md` §2.1 y en el documento ejecutivo |
| "Sube la p…" | Subir a GitHub | Primer commit del repositorio (datos crudos fuera, por `.gitignore`) |

**Consecuencia del nuevo componente.** Las cifras del Radar cambiaron:
- Cortes del índice comparable: 0.186 / 0.756.
- Julio de 2026: Cancún pasa a 0.193, "concurrido" en el índice comparable.
- Los 5 lugares siguen tranquilos.

El criterio de elección del modelo, que es de Brandon (más aciertos y, a igualdad, más cambios anticipados), ahora da la
**regresión logística**: 130 de 156 y 8 de 30 cambios, contra 130 y 6 de Random Forest y 126 de la persistencia. El
código elige solo con ese criterio. La página, los documentos y las pruebas leen o comprueban el resultado vigente.

**Pruebas:** 104 en verde. Son nuevas `test_documentos.py` (20 cifras), `test_radar_clustering.py` y la prueba de
sesgo.

**Veredicto final:**
- Fases 1, 3 y 4: completas según el plan, con las limitaciones declaradas.
- Fase 2: incompleta. Lo siguiente es terminar su Silver (clima, huracanes y FRED primero, porque los necesita la
  Fase 5) y después abrir el Pronóstico.
