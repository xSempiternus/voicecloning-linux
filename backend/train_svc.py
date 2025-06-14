# Script para preparar datos y entrenar So-VITS-SVC

"""
Este script facilita la preparación de datos y el entrenamiento del modelo So-VITS-SVC desde la línea de comandos.

Uso:
    python train_svc.py --prepare <ruta_a_datos> --config <ruta_config> --output <ruta_output>
    python train_svc.py --train --config <ruta_config>

Requiere que So-VITS-SVC esté correctamente instalado en backend/so-vits-svc y que las dependencias estén instaladas (ver instrucciones en README).
"""

import argparse
import os
import subprocess

SOVITS_DIR = os.path.join(os.path.dirname(__file__), 'so-vits-svc')

parser = argparse.ArgumentParser(description="Entrenamiento y preparación de datos para So-VITS-SVC")
parser.add_argument('--prepare', type=str, help='Ruta a la carpeta con datos de voz (wavs)')
parser.add_argument('--config', type=str, help='Ruta al archivo de configuración de So-VITS-SVC')
parser.add_argument('--output', type=str, help='Ruta de salida para los datos procesados')
parser.add_argument('--train', action='store_true', help='Iniciar entrenamiento')

args = parser.parse_args()

if args.prepare:
    # Preprocesamiento de datos
    preprocess_cmd = [
        'python', os.path.join(SOVITS_DIR, 'preprocess.py'),
        '--in_dir', args.prepare,
        '--config', args.config,
        '--out_dir', args.output or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dataset')
    ]
    print('Ejecutando:', ' '.join(preprocess_cmd))
    subprocess.run(preprocess_cmd, check=True)

if args.train:
    # Entrenamiento
    train_cmd = [
        'python', os.path.join(SOVITS_DIR, 'train.py'),
        '--config', args.config
    ]
    print('Ejecutando:', ' '.join(train_cmd))
    subprocess.run(train_cmd, check=True)
