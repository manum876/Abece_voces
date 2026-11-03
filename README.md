# Abecé — voces

Audios en español de **Abecé**, la dirección de [Азбука](https://github.com/manum876/Azbuka_v3) para aprender español desde cero.

- **Se generan con GitHub Actions: Actions → «Voces» → Run workflow.** Solo se hacen los audios que faltan, y se borran los de textos que ya no están en la app. Cuando la app suma algo (una unidad, lecturas, la charla con Lucía), alcanza con volver a correrlo.
  - `todo` (por defecto): unidades, diálogos, frases, Alfabeto, Gramática, el Diccionario, las formas y las tablas de los verbos más frecuentes y de los que enseñan las unidades. Unos 300 MB.
  - `completo`: además, las tablas de todos los verbos. Unos 750 MB, cerca del límite de 1 GB de GitHub Pages. Si después se corre `todo`, esas tablas se borran.
- La lista de textos y el generador viven en el repo de la app (`herramientas/voces/inventario-es.js` y `generar-voces-es.py`).
- `v1/<voz>/<clave>.m4a`: AAC 48 kbps, mono, 24 kHz, el mismo formato que Azbuka. `v1/indice.json`: qué audios hay. `v1/paginas/`: qué audios usa cada página.
- Repo aparte de `Azbuka_voces` a propósito: cada workflow corre por su cuenta y el índice de uno nunca borra los audios del otro. Además, cada repo tiene su propio límite de 1 GB en GitHub Pages.
- **Prueba de voces** (21 y 22/10/2026): Actions → «Prueba de voces». Las muestras están en `prueba/` y se escuchan en `https://manum876.github.io/Abece_voces/prueba/`.

## Elenco

| Voz (carpeta) | Quién | Modelo |
|---|---|---|
| `ana` | Ana y la narración | Piper es_ES sharvard, voz 1, tono más agudo (×1,08) |
| `lucia` | Lucía | Piper sharvard, voz 1, tono más grave (×0,93) |
| `javier` | Javier, el profesor | Piper sharvard, voz 0 |
| `mujer` | Personajes secundarios mujeres | Piper sharvard, voz 1 |
| `hombre`, `hombre2` | Personajes secundarios hombres | Silero v3_es es_2 y es_1 |
| `mayor` | Personas mayores (reservada) | Silero v3_es es_0 |

## Licencias

- [Piper](https://github.com/rhasspy/piper), voz es_ES sharvard: datos del corpus Sharvard, **CC BY 3.0**.
- [Silero TTS](https://github.com/snakers4/silero-models), modelo v3_es: **CC BY-NC 4.0**, solo uso no comercial.
