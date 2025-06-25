#!/usr/bin/env python
"""
Script para post-procesar audio generado y eliminar pitidos de alta frecuencia.
"""

import os
import sys
import numpy as np
import librosa
import soundfile as sf
from scipy import signal

def process_audio(input_file, output_file=None, lowpass_cutoff=14000, 
                  apply_compression=True, normalize=True):
    """
    Post-procesa el audio generado para eliminar pitidos y mejorar la calidad.
    
    Args:
        input_file: Ruta al archivo de audio a procesar
        output_file: Ruta donde guardar el resultado (si None, usa input_file_processed.wav)
        lowpass_cutoff: Frecuencia de corte para el filtro paso bajo
        apply_compression: Si aplicar compresión dinámica
        normalize: Si normalizar el audio
    
    Returns:
        Ruta al archivo procesado
    """
    if output_file is None:
        base = os.path.splitext(input_file)[0]
        output_file = f"{base}_processed.wav"
    
    # Cargar el audio
    audio, sr = librosa.load(input_file, sr=None)
    
    # Aplicar filtro paso bajo para eliminar pitidos de alta frecuencia
    nyquist = 0.5 * sr
    cutoff_norm = lowpass_cutoff / nyquist
    b, a = signal.butter(4, cutoff_norm, btype='low')
    audio_filtered = signal.filtfilt(b, a, audio)
    
    # Aplicar compresión suave para controlar picos
    if apply_compression:
        # Threshold en dB
        threshold_db = -20
        ratio = 4.0  # Ratio de compresión 4:1
        attack = 0.005  # Tiempo de ataque en segundos
        release = 0.1  # Tiempo de liberación en segundos
        
        # Convertir el audio a dB
        audio_db = librosa.amplitude_to_db(np.abs(audio_filtered))
        
        # Calcular la ganancia de compresión
        mask = audio_db > threshold_db
        compressed_db = np.copy(audio_db)
        compressed_db[mask] = threshold_db + (audio_db[mask] - threshold_db) / ratio
        
        # Calcular la diferencia y aplicar suavizado para controlar ataque/liberación
        gain_db = compressed_db - audio_db
        
        # Aplicar el suavizado de ataque/liberación (simplificado)
        smoothed_gain = np.zeros_like(gain_db)
        for i in range(1, len(gain_db)):
            if gain_db[i] < smoothed_gain[i-1]:
                # Ataque (ganancia disminuyendo)
                smoothed_gain[i] = attack * gain_db[i] + (1 - attack) * smoothed_gain[i-1]
            else:
                # Liberación (ganancia aumentando)
                smoothed_gain[i] = release * gain_db[i] + (1 - release) * smoothed_gain[i-1]
        
        # Aplicar la ganancia suavizada al audio
        audio_filtered = audio_filtered * librosa.db_to_amplitude(smoothed_gain)
    
    # Normalizar el volumen
    if normalize:
        max_amp = np.max(np.abs(audio_filtered))
        if max_amp > 0:
            audio_filtered = audio_filtered * (0.9 / max_amp)
    
    # Guardar el resultado
    sf.write(output_file, audio_filtered, sr)
    print(f"Audio procesado guardado como: {output_file}")
    
    return output_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python post_process_audio.py <archivo_entrada> [<archivo_salida>]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_audio(input_file, output_file)
