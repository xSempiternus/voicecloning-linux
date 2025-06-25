#!/usr/bin/env python3
"""
Script para mejorar la inferencia de So-Vits-SVC reduciendo los pitidos
"""

import sys
import os
import torch
import librosa
import soundfile as sf
import numpy as np
from scipy import signal

def enhance_audio_output(input_file, output_file=None, 
                        apply_lowpass=True, lowpass_cutoff=14000,
                        apply_denoising=True, denoise_amount=0.1,
                        apply_normalization=True):
    """
    Procesa el audio generado para reducir/eliminar pitidos y mejorar la calidad.
    
    Args:
        input_file: Ruta al archivo de audio generado por So-Vits-SVC
        output_file: Ruta de salida (si None, usa input_file_enhanced.wav)
        apply_lowpass: Si aplicar filtro paso bajo
        lowpass_cutoff: Frecuencia de corte del filtro paso bajo
        apply_denoising: Si aplicar reducción de ruido
        denoise_amount: Intensidad del denoising (0.0-1.0)
        apply_normalization: Si normalizar el audio
    
    Returns:
        Ruta del archivo procesado
    """
    if output_file is None:
        base = os.path.splitext(input_file)[0]
        output_file = f"{base}_enhanced.wav"
    
    # Cargar el audio
    audio, sr = librosa.load(input_file, sr=None)
    
    # 1. Aplicar filtro paso bajo para quitar pitidos de alta frecuencia
    if apply_lowpass:
        nyquist = 0.5 * sr
        cutoff_norm = lowpass_cutoff / nyquist
        b, a = signal.butter(4, cutoff_norm, btype='low')
        audio = signal.filtfilt(b, a, audio)
    
    # 2. Aplicar denoising espectral simple si se solicita
    if apply_denoising and denoise_amount > 0:
        # STFT
        D = librosa.stft(audio)
        mag, phase = librosa.magphase(D)
        
        # Estimar ruido del espectro (suponiendo que las frecuencias más altas tienden a contener más ruido)
        noise_estimate = np.median(mag[-int(mag.shape[0]*0.2):], axis=0, keepdims=True)
        noise_estimate = np.tile(noise_estimate, (mag.shape[0], 1))
        
        # Aplicar substracción espectral
        mag_denoised = np.maximum(mag - denoise_amount * noise_estimate, 0)
        
        # Reconstruir la señal
        D_denoised = mag_denoised * phase
        audio = librosa.istft(D_denoised)
    
    # 3. Normalizar el audio
    if apply_normalization:
        max_amp = np.max(np.abs(audio))
        if max_amp > 0:
            audio = audio * (0.95 / max_amp)  # Dejar un pequeño margen
            
            # Aplicar compresión muy suave para mejorar consistencia
            threshold = 0.6
            ratio = 0.8
            above_threshold = audio > threshold
            audio[above_threshold] = threshold + (audio[above_threshold] - threshold) * ratio
            below_threshold = audio < -threshold
            audio[below_threshold] = -threshold + (audio[below_threshold] + threshold) * ratio
    
    # Guardar el resultado
    sf.write(output_file, audio, sr)
    print(f"Audio mejorado guardado en: {output_file}")
    
    return output_file

# Script para mejorar el model_inference.py

def modify_inference_for_improved_quality():
    """
    Instrucciones para modificar la inferencia para mejorar la calidad
    """
    instructions = """
    INSTRUCCIONES PARA MEJORAR LA CALIDAD DE INFERENCIA EN SO-VITS-SVC:
    
    1. En el archivo inference_main.py, busca dónde se genera el audio final y añade:
    
       # Después de generar audio_opt
       # Limitar valores extremos para evitar pitidos
       audio_opt = torch.clamp(audio_opt, min=-0.95, max=0.95)
       
       # Si hay picos de volumen extremos, normalizarlos
       max_val = torch.max(torch.abs(audio_opt))
       if max_val > 0.9:
           audio_opt = audio_opt * (0.9 / max_val)
           
    2. Parámetros de inferencia a ajustar:
       - Reduce el "clustering_factor" a un valor entre 0.1 y 0.25
       - Utiliza un "slice_db" más alto (por ejemplo -32) si hay pitidos
       - Prueba diferentes valores de noise_scale (0.3-0.6) y noise_scale_w (0.4-0.8)
       
    3. Post-procesa los archivos generados con este script:
       python enhance_inference.py audio_generado.wav
    """
    print(instructions)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python enhance_inference.py <archivo_entrada> [<archivo_salida>]")
        print("\nO para mostrar las instrucciones de optimización:")
        print("python enhance_inference.py --help")
        sys.exit(1)
    
    if sys.argv[1] == "--help":
        modify_inference_for_improved_quality()
        sys.exit(0)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    enhance_audio_output(input_file, output_file)
