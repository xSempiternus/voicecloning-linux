import sys
import subprocess
from pathlib import Path
import argparse

def separate_with_demucs(input_mp3, vocals_path, instrumental_path):
    # Carpeta de salida temporal
    output_dir = Path(vocals_path).parent
    # Llama a demucs vía línea de comandos (requiere demucs instalado)
    cmd = [
        sys.executable, "-m", "demucs",
        "--two-stems", "vocals",
        "--out", str(output_dir),
        str(input_mp3)
    ]
    subprocess.run(cmd, check=True)
    # Buscar carpeta del modelo (ej: htdemucs)
    model_folder = [d for d in output_dir.iterdir() if d.is_dir()][0]
    vocals_file = model_folder / Path(input_mp3).stem / "vocals.wav"
    instrumental_file = model_folder / Path(input_mp3).stem / "no_vocals.wav"
    # Copiar a los destinos solicitados
    Path(vocals_path).write_bytes(vocals_file.read_bytes())
    Path(instrumental_path).write_bytes(instrumental_file.read_bytes())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Separar voz e instrumental usando Demucs")
    parser.add_argument('--input', required=True, help='Archivo de entrada (.mp3, .wav, etc)')
    parser.add_argument('--vocals', required=True, help='Ruta de salida para la voz')
    parser.add_argument('--instrumental', required=True, help='Ruta de salida para el instrumental')
    args = parser.parse_args()
    separate_with_demucs(args.input, args.vocals, args.instrumental)
