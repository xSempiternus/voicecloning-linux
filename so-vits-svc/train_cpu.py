#!/usr/bin/env python3

"""
Script para forzar el uso de CPU en el entrenamiento de So-Vits-SVC
cuando hay problemas con la GPU
"""

import os

# Configura CUDA_VISIBLE_DEVICES como -1 para forzar CPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Mensaje informativo
print("==========================================================")
print("INICIANDO ENTRENAMIENTO EN MODO CPU")
print("Este script desactiva todas las GPUs para entrenar con CPU")
print("==========================================================")

# Importa el script train.py y ejecuta la función main()
import train
train.main()
