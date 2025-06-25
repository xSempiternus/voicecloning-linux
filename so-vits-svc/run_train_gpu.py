#!/usr/bin/env python
"""
Script para forzar el uso de GPU para So-Vits-SVC
"""

import os
import sys
import torch

# Forzar el uso de CUDA
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Usa la primera GPU
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"

# Verificar la GPU disponible
if not torch.cuda.is_available():
    print("CUDA no está disponible. Asegúrate de que tienes una GPU compatible y los drivers adecuados.")
    sys.exit(1)

print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"Dispositivo actual: {torch.cuda.current_device()}")
print(f"Nombre del dispositivo: {torch.cuda.get_device_name(0)}")
print(f"Memoria total: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# Ejecutar el entrenamiento
train_command = "python train.py -m niko"
os.system(train_command)
