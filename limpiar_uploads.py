# Script para limpiar la carpeta uploads y dejar solo la última subcarpeta
import os
import shutil
from pathlib import Path

uploads_dir = Path("c:/Users/nikoa/Documents/PROJECTS/VoiceClonation/data/uploads")
subdirs = sorted([d for d in uploads_dir.iterdir() if d.is_dir()], key=os.path.getmtime)
if len(subdirs) > 1:
    for d in subdirs[:-1]:
        shutil.rmtree(d)
print(f"Carpetas eliminadas: {[str(d) for d in subdirs[:-1]]}")
print(f"Carpeta conservada: {subdirs[-1] if subdirs else 'Ninguna'}")
