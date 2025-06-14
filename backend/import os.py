import os
import soundfile as sf

root = "data/mi_voz/niko"  # Ajusta la ruta a tu carpeta de audios
for fname in os.listdir(root):
    if fname.endswith(".wav"):
        data, sr = sf.read(os.path.join(root, fname))
        if len(data.shape) > 1 and data.shape[1] == 2:
            print(f"{fname} es estéreo")