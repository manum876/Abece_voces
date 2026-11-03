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

Desde el 03/11/2026 (Manu, tras la prueba de palabras: Piper pronunciaba mal las palabras sueltas, Silero bien):

| Voz (carpeta) | Quién | Modelo |
|---|---|---|
| `es2` | La narración (palabras, frases, ejercicios, Diccionario, Verbos…) y Pablo | Silero v3_es es_2 |
| `es1` | Javier, el profesor | Silero v3_es es_1 |
| `es0` | Hombres secundarios (recepcionista…) | Silero v3_es es_0 |
| `ana`, `lucia`, `mujer` | Ana, Lucía y las mujeres secundarias, solo en sus líneas de diálogo (Silero no tiene voces de mujer) | Piper es_ES sharvard, voz 1 (Ana ×1,08, Lucía ×0,93, las demás en su tono) |

La **prueba de palabras** (Actions → «Prueba de palabras») está en `prueba-palabras/`.

## Licencias

- [Piper](https://github.com/rhasspy/piper), voz es_ES sharvard: datos del corpus Sharvard, **CC BY 3.0**.
- [Silero TTS](https://github.com/snakers4/silero-models), modelo v3_es: **CC BY-NC 4.0**, solo uso no comercial.
