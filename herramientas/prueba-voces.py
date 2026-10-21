# Prueba de voces en español para Abecé (21/10/2026).
# Genera las mismas frases con cada voz candidata y arma prueba/index.html para escucharlas en el teléfono.
#   Silero v3_es (es_0, es_1, es_2): licencia CC BY-NC 4.0, la misma familia que las voces rusas de Azbuka.
#   Piper es_ES (davefx, sharvard hombre y mujer): plan B, para comparar; licencia de cada voz a confirmar.
# Lo corre GitHub Actions (Actions → «Prueba de voces» → Run workflow); no hace falta correrlo a mano.
import html, os, re, subprocess, urllib.request, wave

SALIDA = "prueba"
FRASES = [
    ("Presentarse", "Hola, me llamo Ana. Soy de Moscú y vivo en Barcelona."),
    ("Z, C y S (distinción)", "La caza y la casa no suenan igual. Cocer y coser, tampoco."),
    ("Z, C y S en frase", "Gracias. ¿Cerramos la ventana? Hace mucho frío esta mañana."),
    ("Vosotros", "¿Vosotros sois de aquí? ¿Queréis un zumo de naranja?"),
    ("Pregunta", "Perdona, ¿dónde está la estación de metro?"),
    ("R y RR", "Perro y pero. Carro y caro. El tren llega a las ocho."),
    ("J, G y LL", "Julio y Gerardo llevan el coche al taller."),
    ("Vocales átonas", "Hola, cómo estás. Todo bien, gracias. Hasta mañana."),
    ("Narración", "Los domingos por la tarde, Ana pasea por el parque con su amiga Lucía. Después toman un café y hablan de la semana."),
    ("Palabras sueltas", "la mesa. el árbol. jamón. pequeño. el miércoles."),
    ("Profesor", "Muy bien. Ahora repite conmigo: yo hablo, tú hablas, él habla."),
]

def m4a(wav, destino):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-ac", "1", "-ar", "24000", "-c:a", "aac", "-b:a", "48k", destino], check=True)
    os.remove(wav)

def guardar_wav(muestras, sr, ruta):
    import numpy as np
    datos = (np.clip(muestras, -1, 1) * 32767).astype("int16")
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(datos.tobytes())

def silero(voces):
    import torch
    modelo, _ = torch.hub.load(repo_or_dir="snakers4/silero-models", model="silero_tts", language="es", speaker="v3_es", trust_repo=True, skip_validation=True)
    for v in ["es_0", "es_1", "es_2"]:
        clave = "silero-" + v
        os.makedirs(os.path.join(SALIDA, clave), exist_ok=True)
        for i, (_, t) in enumerate(FRASES, 1):
            texto = re.sub(r"[¿¡]", "", t)
            try:
                audio = modelo.apply_tts(text=texto, speaker=v, sample_rate=48000)
                wav = os.path.join(SALIDA, clave, f"{i:02}.wav")
                guardar_wav(audio.numpy(), 48000, wav)
                m4a(wav, wav[:-4] + ".m4a")
            except Exception as e:
                print("✗", clave, i, e)
        voces.append((clave, f"Silero · {v}", "Silero v3_es · CC BY-NC 4.0"))

PIPER = [
    ("piper-davefx", "Piper · davefx", "es/es_ES/davefx/medium/es_ES-davefx-medium", None),
    ("piper-sharvard-0", "Piper · sharvard (voz 0)", "es/es_ES/sharvard/medium/es_ES-sharvard-medium", 0),
    ("piper-sharvard-1", "Piper · sharvard (voz 1)", "es/es_ES/sharvard/medium/es_ES-sharvard-medium", 1),
]

def piper(voces):
    base = "https://huggingface.co/rhasspy/piper-voices/resolve/main/"
    for clave, nombre, ruta, hablante in PIPER:
        modelo = os.path.basename(ruta) + ".onnx"
        try:
            if not os.path.exists(modelo):
                urllib.request.urlretrieve(base + ruta + ".onnx", modelo)
                urllib.request.urlretrieve(base + ruta + ".onnx.json", modelo + ".json")
            os.makedirs(os.path.join(SALIDA, clave), exist_ok=True)
            for i, (_, t) in enumerate(FRASES, 1):
                wav = os.path.join(SALIDA, clave, f"{i:02}.wav")
                cmd = ["piper", "--model", modelo, "--output_file", wav]
                if hablante is not None:
                    cmd += ["--speaker", str(hablante)]
                subprocess.run(cmd, input=t.encode("utf-8"), check=True, capture_output=True)
                m4a(wav, wav[:-4] + ".m4a")
            voces.append((clave, nombre, "Piper · plan B, licencia a confirmar"))
        except Exception as e:
            print("✗", clave, e)

def pagina(voces):
    filas = []
    for clave, nombre, nota in voces:
        items = "".join(
            f'<div class="f"><div class="t"><b>{html.escape(tit)}</b><br>{html.escape(t)}</div>'
            f'<audio controls preload="none" src="{clave}/{i:02}.m4a"></audio></div>'
            for i, (tit, t) in enumerate(FRASES, 1) if os.path.exists(os.path.join(SALIDA, clave, f"{i:02}.m4a")))
        filas.append(f'<section><h2>{html.escape(nombre)}</h2><p class="n">{html.escape(nota)} · ¿hombre o mujer? ¿España o América?</p>{items}</section>')
    doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>Abecé · prueba de voces</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#0F0F14;color:#F0EEE8;font:15px/1.5 system-ui,sans-serif;padding:max(24px,env(safe-area-inset-top)) 16px 48px}}
h1{{color:#C9A84C;font-size:24px;margin:0 0 6px}}h2{{color:#C9A84C;font-size:18px;margin:28px 0 4px}}.n{{color:#888080;font-size:13px;margin:0 0 10px}}
.f{{background:#1A1A24;border:1px solid #2A2A38;border-radius:12px;padding:12px;margin:8px 0}}.t{{color:#B8B0A8;font-size:14px;margin-bottom:8px}}.t b{{color:#F0EEE8}}
audio{{width:100%}}p{{max-width:640px}}</style></head><body>
<h1>Abecé · prueba de voces</h1><p>Las mismas frases con cada voz. Para elegir el elenco: quién suena de España (distingue «caza» y «casa»), quién es hombre y quién mujer, y cuál se entiende mejor.</p>
{''.join(filas)}</body></html>"""
    open(os.path.join(SALIDA, "index.html"), "w", encoding="utf-8").write(doc)

if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    voces = []
    try:
        silero(voces)
    except Exception as e:
        print("✗ Silero:", e)
    piper(voces)
    pagina(voces)
    print("✓", len(voces), "voces")
