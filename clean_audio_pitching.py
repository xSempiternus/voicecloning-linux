"""
Este script modifica las muestras de audio para eliminar el pitido en archivos generados.

Uso:
1. Guardar este archivo en el directorio principal del proyecto
2. Ejecutarlo con: python clean_audio_pitching.py <ruta_al_archivo>
"""

import os
import sys
import numpy as np
import soundfile as sf
import librosa
from scipy import signal

def remove_high_pitch_noise(audio_path, output_path=None, lowpass_cutoff=12000):
    """
    Elimina ruidos de alta frecuencia (pitidos) de un archivo de audio usando un filtro paso bajo
    y normalización de audio.
    
    Args:
        audio_path: Ruta al archivo de audio
        output_path: Ruta para guardar el audio procesado (opcional)
        lowpass_cutoff: Frecuencia de corte para el filtro paso bajo (en Hz)
    
    Returns:
        Ruta al archivo procesado
    """
    if output_path is None:
        base_name = os.path.splitext(audio_path)[0]
        output_path = f"{base_name}_cleaned.wav"
    
    # Cargar el audio
    audio, sr = librosa.load(audio_path, sr=None)
    
    # Diseñar un filtro paso bajo para eliminar las frecuencias altas (pitidos)
    nyquist = 0.5 * sr
    cutoff_norm = lowpass_cutoff / nyquist
    b, a = signal.butter(4, cutoff_norm, btype='low')
    
    # Aplicar el filtro
    audio_filtered = signal.filtfilt(b, a, audio)
    
    # Normalizar el audio para evitar clipping
    audio_norm = librosa.util.normalize(audio_filtered, norm=np.inf, axis=None)
    
    # Para audios muy ruidosos, podemos aplicar una compresión dinámica suave
    # para reducir la diferencia entre partes altas y bajas
    threshold = 0.5
    ratio = 0.7
    above_threshold = audio_norm > threshold
    audio_norm[above_threshold] = threshold + (audio_norm[above_threshold] - threshold) * ratio
    below_threshold = audio_norm < -threshold
    audio_norm[below_threshold] = -threshold + (audio_norm[below_threshold] + threshold) * ratio
    
    # Guardar el resultado
    sf.write(output_path, audio_norm, sr)
    print(f"Audio procesado guardado en: {output_path}")
    
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python clean_audio_pitching.py <ruta_al_archivo>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    remove_high_pitch_noise(input_path)
