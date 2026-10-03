# 00 — Fundación del proyecto

Autor: **Brandon Uriel García Sánchez** · 27-sep-2026 · *Escrita para quien no estuvo cuando se decidió.*

## Decisión 1: empezar desde cero
- **Qué:** no se reutiliza código, modelos, salidas ni cifras del proyecto anterior.
- **Por qué:** Brandon revisó los flujos anteriores y no los aprobó; además, la carpeta del proyecto anterior
  ya no existe en disco (verificado el 27-sep-2026).
- **Descartado:** portar el paquete `cauce` y reentrenar.
- **Consecuencia:** cada técnica se diseña y valida de nuevo, con Brandon, fase por fase.

## Decisión 2: Quintana Roo y la fusión A1 + A3 + A5
- **Qué:** estado Quintana Roo; sistema de tres horizontes: Radar (hoy), Pronóstico (1–12 meses), Torre en vivo (semana).
- **Por qué:** entre las 5 alternativas, Brandon eligió combinar estas tres. Se reparten las técnicas para que
  no se encimen (ver `docs/plan/PLAN_v3.md`, secciones B.1 y B.2).
- **Evidencia de datos:** DataTur publica **135 archivos semanales** de ocupación (2024-S01 → 2026-S31) con 7
  centros de Q. Roo; SITUR-Q responde por API con 45 indicadores; HURDAT2 cubre de 1851 a 2025.
- **Descartado:** A2 (Voz del viajero) y A4 (Portafolio) como ejes; la minería de texto de A2 se conserva
  para el buyer persona.

## Decisión 3: no promover playa en 2026
- **Qué:** las regiones propuestas son Chetumal, Bahía Calderitas-Oxtankah, Ruta arqueológica del sur, Maya
  Ka'an interior y Muyil.
- **Por qué:** sargazo récord (más de 104,700 t; 56 de 140 playas en rojo), crisis de Tulum (ventas −60 %),
  Cozumel saturado por cruceros, Isla Mujeres al 93–95 % de ocupación y Holbox sin infraestructura suficiente.
  Detalle y fuentes en `docs/regiones/REGIONES.md`.
- **Pendiente:** confirmar con una tabla de criterios calculada con datos en la Fase 3; verificar sargazo en
  la Bahía de Chetumal en la Fase 1.

## Decisión 4: herramientas de trabajo
- **Git local** (`git init`, sin subir nada) para tener historial y habilitar los hooks.
- **Graphify** como mapa de conocimiento del proyecto; `nucleo/` queda excluido del grafo.
