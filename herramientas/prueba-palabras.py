# Prueba de palabras sueltas (03/11/2026). Con las voces de producción, Manu oyó «ojo» como «dogo»,
# «ocho» como «oyo» y «gato» como «ato»: las palabras sueltas salían de 0,3 s, apuradas y cortadas.
# Esta prueba genera las mismas palabras con varios ajustes de Piper para elegir de oído cuál se usa.
# Se corre a mano: Actions → «Prueba de palabras» → Run workflow. Se escucha en
# https://manum876.github.io/Abece_voces/prueba-palabras/
import html, os, subprocess, urllib.request, wave

SALIDA = "prueba-palabras"
BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/sharvard/medium/es_ES-sharvard-medium"
MODELO = "es_ES-sharvard-medium.onnx"
PALABRAS = ["ojo", "ocho", "gato", "año", "hola", "casa", "perro", "jamón", "ciudad", "guitarra", "llave", "cinco", "el gato", "¿Cómo te llamas?"]
# (clave, nombre, hablante, tono, punto, length_scale, noise_scale, noise_w)
VARIANTES = [
    ("a-actual", "A · Como ahora", 1, 1.08, False, None, None, None),
    ("b-punto", "B · Con punto final", 1, 1.08, True, None, None, None),
    ("c-lento", "C · Punto y más lento (×1,25)", 1, 1.08, True, 1.25, None, None),
    ("d-estable", "D · Punto, más lento y más estable", 1, 1.08, True, 1.25, 0.4, 0.6),
    ("e-sin-tono", "E · Como D, sin cambiar el tono", 1, 1.0, True, 1.25, 0.4, 0.6),
    ("f-javier", "F · Como D, con la voz de Javier", 0, 1.0, True, 1.25, 0.4, 0.6),
]
# Silero v3_es (03/11/2026, Manu: «¿y si volvemos a Silero?»): solo tiene voces de hombre.
SILERO = [
    ("g-silero-es2", "G · Silero es_2 (hombre, la mejor de Silero)", "es_2", False),
    ("h-silero-es2-punto", "H · Silero es_2 con punto final", "es_2", True),
    ("i-silero-es1-punto", "I · Silero es_1 con punto final", "es_1", True),
]

def m4a(wav, sr, tono, destino):
    filtro = ["-af", f"asetrate={sr}*{tono},aresample=24000,atempo={1 / tono:.4f}"] if tono != 1.0 else []
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav] + filtro +
                   ["-ac", "1", "-ar", "24000", "-c:a", "aac", "-b:a", "48k", "-movflags", "+faststart", destino], check=True)
    os.remove(wav)

def duracion(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except Exception: return 0.0

if __name__ == "__main__":
    from piper.voice import PiperVoice
    if not os.path.exists(MODELO):
        urllib.request.urlretrieve(BASE + ".onnx", MODELO)
        urllib.request.urlretrieve(BASE + ".onnx.json", MODELO + ".json")
    voz = PiperVoice.load(MODELO)
    sr = voz.config.sample_rate
    os.makedirs(SALIDA, exist_ok=True)
    filas = []
    for clave, nombre, hablante, tono, punto, ls, ns, nw in VARIANTES:
        os.makedirs(os.path.join(SALIDA, clave), exist_ok=True)
        items = []
        for i, p in enumerate(PALABRAS, 1):
            texto = p if (not punto or p[-1] in ".?!") else p + "."
            wav = os.path.join(SALIDA, clave, f"{i:02}.wav")
            with wave.open(wav, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
                for b in voz.synthesize_stream_raw(texto, speaker_id=hablante, length_scale=ls, noise_scale=ns, noise_w=nw):
                    w.writeframes(b)
            dest = wav[:-4] + ".m4a"
            m4a(wav, sr, tono, dest)
            items.append(f'<div class="f"><div class="t"><b>{html.escape(p)}</b> · {duracion(dest):.2f} s</div>'
                         f'<audio controls preload="none" src="{clave}/{i:02}.m4a"></audio></div>')
        filas.append(f'<section><h2>{html.escape(nombre)}</h2>{"".join(items)}</section>')
    # Silero
    import re, torch
    modelo, _ = torch.hub.load(repo_or_dir="snakers4/silero-models", model="silero_tts", language="es", speaker="v3_es", trust_repo=True, skip_validation=True)
    for clave, nombre, hablante, punto in SILERO:
        os.makedirs(os.path.join(SALIDA, clave), exist_ok=True)
        items = []
        for i, p in enumerate(PALABRAS, 1):
            texto = re.sub(r"[¿¡]", "", p if (not punto or p[-1] in ".?!") else p + ".")
            wav = os.path.join(SALIDA, clave, f"{i:02}.wav")
            audio = modelo.apply_tts(text=texto, speaker=hablante, sample_rate=48000)
            pcm = (audio.clamp(-1, 1) * 32767).to(torch.int16).numpy().tobytes()
            with wave.open(wav, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000); w.writeframes(pcm)
            dest = wav[:-4] + ".m4a"
            m4a(wav, 48000, 1.0, dest)
            items.append(f'<div class="f"><div class="t"><b>{html.escape(p)}</b> · {duracion(dest):.2f} s</div>'
                         f'<audio controls preload="none" src="{clave}/{i:02}.m4a"></audio></div>')
        filas.append(f'<section><h2>{html.escape(nombre)}</h2>{"".join(items)}</section>')
    doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>Abecé · prueba de palabras</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#0F0F14;color:#F0EEE8;font:15px/1.5 system-ui,sans-serif;padding:max(24px,env(safe-area-inset-top)) 16px 48px}}
h1{{color:#C9A84C;font-size:24px;margin:0 0 6px}}h2{{color:#C9A84C;font-size:18px;margin:28px 0 4px}}
.f{{background:#1A1A24;border:1px solid #2A2A38;border-radius:12px;padding:12px;margin:8px 0}}.t{{color:#B8B0A8;font-size:14px;margin-bottom:8px}}.t b{{color:#F0EEE8}}
audio{{width:100%}}p{{max-width:640px}}</style></head><body>
<h1>Abecé · prueba de palabras</h1><p>Las mismas palabras con Piper (A–F: A es como suenan hoy en la app) y con Silero (G–I, solo voces de hombre). ¿Cuál dice bien «ojo», «ocho», «gato» y «año»?</p>
{''.join(filas)}</body></html>"""
    open(os.path.join(SALIDA, "index.html"), "w", encoding="utf-8").write(doc)
    print("✓", len(VARIANTES) + len(SILERO), "variantes ·", len(PALABRAS), "palabras")
