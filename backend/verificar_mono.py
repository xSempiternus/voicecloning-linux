import os
import librosa
from pathlib import Path

folder = "data/mi_voz/niko"
exts = {'.wav', '.mp3', '.flac', '.ogg', '.m4a'}

print(f"Verificando archivos en: {folder}\n")
for fname in os.listdir(folder):
    fpath = os.path.join(folder, fname)
    if not os.path.isfile(fpath):
        continue
    if Path(fname).suffix.lower() not in exts:
        continue
    try:
        y, _ = librosa.load(fpath, sr=None, mono=False)
        if y.ndim == 1:
            print(f"[OK] {fname} es mono.")
        else:
            print(f"[WARN] {fname} es estéreo.")
    except Exception as e:
        print(f"[ERROR] No se pudo procesar {fname}: {e}")
