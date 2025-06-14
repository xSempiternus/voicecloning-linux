import argparse
import librosa
import soundfile as sf

def mp3_to_wav(input_path, output_path, sr=44100):
    y, _ = librosa.load(input_path, sr=sr, mono=True)
    sf.write(output_path, y, sr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convertir audio a wav mono 44.1kHz")
    parser.add_argument('--input', required=True, help='Archivo de entrada')
    parser.add_argument('--output', required=True, help='Archivo de salida')
    args = parser.parse_args()
    mp3_to_wav(args.input, args.output)
