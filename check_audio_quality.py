#!/usr/bin/env python
"""
Script para analizar la calidad de los archivos de audio de entrenamiento.
"""

import os
import sys
import numpy as np
import librosa
import matplotlib.pyplot as plt
from glob import glob

def analyze_audio_file(file_path):
    """
    Analiza un archivo de audio y devuelve estadísticas importantes.
    """
    try:
        # Cargar el audio
        audio, sr = librosa.load(file_path, sr=None)
        
        # Duración
        duration = librosa.get_duration(y=audio, sr=sr)
        
        # Análisis de amplitud
        mean_amplitude = np.mean(np.abs(audio))
        max_amplitude = np.max(np.abs(audio))
        
        # Detectar clipping
        clipping_threshold = 0.99
        samples_clipping = np.sum(np.abs(audio) > clipping_threshold)
        clipping_percentage = 100 * samples_clipping / len(audio)
        
        # Detectar silencios
        silence_threshold = 0.01
        samples_silence = np.sum(np.abs(audio) < silence_threshold)
        silence_percentage = 100 * samples_silence / len(audio)
        
        # Análisis espectral
        D = librosa.stft(audio)
        D_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        
        # Frecuencia promedio de energía
        freqs = librosa.fft_frequencies(sr=sr)
        energy = np.sum(np.abs(D), axis=1)
        mean_freq = np.sum(freqs * energy) / np.sum(energy) if np.sum(energy) > 0 else 0
        
        # Detección de ruido de alta frecuencia
        high_freq_range = (freqs > 10000)
        low_freq_range = (freqs < 4000) & (freqs > 80)
        high_freq_energy = np.sum(np.mean(np.abs(D[high_freq_range]), axis=1))
        low_freq_energy = np.sum(np.mean(np.abs(D[low_freq_range]), axis=1))
        high_to_low_ratio = high_freq_energy / low_freq_energy if low_freq_energy > 0 else 0
        
        return {
            'file': os.path.basename(file_path),
            'duration': duration,
            'mean_amplitude': mean_amplitude,
            'max_amplitude': max_amplitude,
            'clipping_percentage': clipping_percentage,
            'silence_percentage': silence_percentage,
            'mean_frequency': mean_freq,
            'high_to_low_ratio': high_to_low_ratio
        }
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return None

def analyze_dataset(file_list):
    """
    Analiza un conjunto de archivos de audio y genera un informe.
    """
    results = []
    total_duration = 0
    
    for file_path in file_list:
        print(f"Analyzing: {os.path.basename(file_path)}")
        stats = analyze_audio_file(file_path)
        if stats:
            results.append(stats)
            total_duration += stats['duration']
    
    if not results:
        print("No valid audio files found!")
        return
    
    # Mostrar estadísticas generales
    print("\n===== Análisis del Dataset =====")
    print(f"Total de archivos: {len(results)}")
    print(f"Duración total: {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    
    # Mostrar problemas potenciales
    print("\n===== Problemas Potenciales =====")
    
    # Archivos con clipping
    clipping_files = [r for r in results if r['clipping_percentage'] > 0.1]
    if clipping_files:
        print("\nArchivos con posible clipping:")
        for r in clipping_files:
            print(f"  - {r['file']}: {r['clipping_percentage']:.2f}% de muestras")
    
    # Archivos con demasiado silencio
    silence_files = [r for r in results if r['silence_percentage'] > 20]
    if silence_files:
        print("\nArchivos con exceso de silencios:")
        for r in silence_files:
            print(f"  - {r['file']}: {r['silence_percentage']:.2f}% de muestras")
    
    # Archivos con alto ruido de alta frecuencia
    noisy_files = [r for r in results if r['high_to_low_ratio'] > 0.1]
    if noisy_files:
        print("\nArchivos con posible ruido de alta frecuencia:")
        for r in sorted(noisy_files, key=lambda x: x['high_to_low_ratio'], reverse=True):
            print(f"  - {r['file']}: ratio {r['high_to_low_ratio']:.4f}")
    
    # Archivos muy cortos
    short_files = [r for r in results if r['duration'] < 3.0]
    if short_files:
        print("\nArchivos muy cortos (<3s):")
        for r in short_files:
            print(f"  - {r['file']}: {r['duration']:.2f}s")
    
    # Archivos con volumen bajo
    low_vol_files = [r for r in results if r['max_amplitude'] < 0.1]
    if low_vol_files:
        print("\nArchivos con volumen bajo:")
        for r in low_vol_files:
            print(f"  - {r['file']}: max amplitud {r['max_amplitude']:.4f}")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python check_audio_quality.py <directorio_o_archivo_lista>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    if os.path.isdir(input_path):
        # Buscar todos los archivos WAV en el directorio
        file_list = glob(os.path.join(input_path, "*.wav"))
    elif input_path.endswith(".txt"):
        # Leer lista de archivos
        with open(input_path, 'r') as f:
            file_list = [line.strip() for line in f if line.strip()]
    else:
        # Considerar como un solo archivo
        file_list = [input_path]
    
    analyze_dataset(file_list)
