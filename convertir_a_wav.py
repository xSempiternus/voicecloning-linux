import os
import subprocess
from pathlib import Path

# Carpeta donde están los audios originales
AUDIO_DIR = Path('data/mi_voz')

# Extensiones a convertir
target_exts = ['.mp3', '.m4a', '.mp4']

convertidos = []

for audio_file in AUDIO_DIR.iterdir():
    if audio_file.suffix.lower() in target_exts:
        wav_file = audio_file.with_suffix('.wav')
        print(f"Convirtiendo {audio_file.name} -> {wav_file.name}")
        # ffmpeg: convertir a wav, mono, 44.1kHz
        cmd = [
            'ffmpeg', '-y',
            '-i', str(audio_file),
            '-ac', '1',
            '-ar', '44100',
            str(wav_file)
        ]
        subprocess.run(cmd, check=True)
        # Eliminar el archivo original
        os.remove(audio_file)
        print(f"Eliminado {audio_file.name}")
        convertidos.append(f"{audio_file.name} -> {wav_file.name}")

if convertidos:
    print("\nResumen de archivos convertidos:")
    for c in convertidos:
        print(c)
else:
    print("No se encontraron archivos .mp3, .m4a o .mp4 para convertir.")
print("Conversión finalizada.")
