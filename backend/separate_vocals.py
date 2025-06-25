import sys
import subprocess
from pathlib import Path
import argparse
import librosa
import soundfile as sf
import os
import shutil

def check_and_convert_wav(input_path, output_path, sr=44100):
    # Verificar extensión
    ext = Path(input_path).suffix.lower()
    if ext != '.wav':
        print(f"[INFO] {input_path} no es .wav. Convirtiendo a wav...")
        y, _ = librosa.load(input_path, sr=sr, mono=False)
        sf.write(output_path, y, sr)
        input_path = output_path
    else:
        print(f"[OK] {input_path} ya es .wav.")
    # Verificar si es mono
    y, _ = librosa.load(input_path, sr=sr, mono=False)
    if y.ndim == 1:
        print(f"[OK] {input_path} ya es mono. No se modifica.")
        if input_path != output_path:
            sf.write(output_path, y, sr)
    else:
        print(f"[INFO] {input_path} es estéreo. Convirtiendo a mono...")
        y_mono = librosa.to_mono(y)
        sf.write(output_path, y_mono, sr)
        print(f"[OK] {output_path} convertido a mono.")

def separate_and_convert(input_audio, vocals_path, instrumental_path, sr=44100, keep_instrumental=False):
    # Carpeta de salida temporal
    output_dir = Path(vocals_path).parent
    # Ejecutar Demucs
    cmd = [
        sys.executable, "-m", "demucs",
        "--two-stems", "vocals",
        "--out", str(output_dir),
        str(input_audio)
    ]
    subprocess.run(cmd, check=True)
    # Buscar carpeta del modelo (ej: htdemucs)
    model_folders = [d for d in output_dir.iterdir() if d.is_dir() and d.name.startswith('htdemucs')]
    if not model_folders:
        raise RuntimeError("No se encontró la carpeta temporal generada por Demucs.")
    model_folder = model_folders[0]
    vocals_file = model_folder / Path(input_audio).stem / "vocals.wav"
    instrumental_file = model_folder / Path(input_audio).stem / "no_vocals.wav"
    # Verificar y convertir a wav mono
    check_and_convert_wav(vocals_file, vocals_path, sr)
    if keep_instrumental:
        check_and_convert_wav(instrumental_file, instrumental_path, sr)
    # Eliminar carpeta temporal de Demucs
    try:
        shutil.rmtree(model_folder)
        print(f"[INFO] Carpeta temporal {model_folder} eliminada.")
    except Exception as e:
        print(f"[WARN] No se pudo eliminar {model_folder}: {e}")
    # Eliminar archivo instrumental si no se desea conservar
    if not keep_instrumental and Path(instrumental_path).exists():
        try:
            Path(instrumental_path).unlink()
            print(f"[INFO] Archivo instrumental {instrumental_path} eliminado.")
        except Exception as e:
            print(f"[WARN] No se pudo eliminar {instrumental_path}: {e}")

def process_folder(input_folder, output_folder, sr=44100, keep_instrumental=False):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    exts = {'.wav', '.mp3', '.flac', '.ogg', '.m4a'}
    for f in input_folder.iterdir():
        if not f.is_file() or f.suffix.lower() not in exts:
            continue
        print(f"\nProcesando: {f.name}")
        vocals_out = output_folder / f"{f.stem}_voz.wav"
        instr_out = output_folder / f"{f.stem}_inst.wav"
        separate_and_convert(str(f), str(vocals_out), str(instr_out), sr, keep_instrumental=keep_instrumental)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Separar voz e instrumental usando Demucs y convertir a wav mono 44.1kHz, verificando requisitos. Puede procesar un archivo o una carpeta completa.")
    parser.add_argument('--input', help='Archivo de entrada (.mp3, .wav, etc)')
    parser.add_argument('--vocals', help='Ruta de salida para la voz (wav mono)')
    parser.add_argument('--instrumental', help='Ruta de salida para el instrumental (wav mono)')
    parser.add_argument('--input_folder', help='Carpeta con archivos a procesar')
    parser.add_argument('--output_folder', help='Carpeta donde guardar los resultados')
    parser.add_argument('--keep_instrumental', action='store_true', help='Conservar archivos instrumentales')
    args = parser.parse_args()

    if args.input_folder and args.output_folder:
        process_folder(args.input_folder, args.output_folder, keep_instrumental=args.keep_instrumental)
    elif args.input and args.vocals and args.instrumental:
        separate_and_convert(args.input, args.vocals, args.instrumental, keep_instrumental=args.keep_instrumental)
    else:
        print("Debes especificar --input y --vocals y --instrumental, o --input_folder y --output_folder.")
