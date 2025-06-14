from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
import shutil
import subprocess
import uuid
import librosa
import soundfile as sf
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definir la raíz absoluta del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
RESULTS_DIR = DATA_DIR / "results"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload-song/")
async def upload_song(file: UploadFile = File(...)):
    # Guarda el archivo subido
    out_path = UPLOAD_DIR / file.filename
    with open(out_path, "wb") as f:
        f.write(await file.read())
    # Aquí deberías llamar al pipeline de separación y conversión de voz
    # Simulación de procesamiento
    return {"status": "uploaded", "filename": file.filename}

@app.get("/download/{filename}")
def download_result(filename: str):
    result_path = RESULTS_DIR / filename
    if not result_path.exists():
        return JSONResponse(status_code=404, content={"error": "Archivo no encontrado"})
    return FileResponse(result_path, media_type="audio/wav", filename=filename)

def mezclar_voces_instrumental(voz_path, instrumental_path, output_path, voz_gain=1.0, instrumental_gain=1.0):
    """
    Mezcla la voz clonada y el instrumental, ajustando volúmenes si es necesario.
    """
    voz, sr = librosa.load(voz_path, sr=None)
    instrumental, _ = librosa.load(instrumental_path, sr=sr)
    # Ajustar longitudes
    min_len = min(len(voz), len(instrumental))
    voz = voz[:min_len] * voz_gain
    instrumental = instrumental[:min_len] * instrumental_gain
    mezcla = voz + instrumental
    # Normalizar para evitar clipping
    mezcla = mezcla / max(1.01, abs(mezcla).max())
    sf.write(output_path, mezcla, sr)

@app.post("/process/")
async def process_song(file: UploadFile = File(...)):
    """
    Pipeline completo: recibe canción, separa voz, convierte, clona voz y devuelve resultado.
    """
    # 1. Guardar archivo temporal
    job_id = str(uuid.uuid4())
    temp_dir = UPLOAD_DIR / job_id
    temp_dir.mkdir(parents=True, exist_ok=True)
    input_path = temp_dir / file.filename
    with open(input_path, "wb") as f:
        f.write(await file.read())
    print("Archivo guardado en:", input_path, "¿Existe?", input_path.exists())
    input_path = input_path.resolve()

    # 2. Separar voz e instrumental (Demucs)
    vocals_path = (temp_dir / "vocals.wav").resolve()
    instrumental_path = (temp_dir / "instrumental.wav").resolve()
    demucs_cmd = [
        sys.executable, "separate_vocals.py",
        "--input", str(input_path),
        "--vocals", str(vocals_path),
        "--instrumental", str(instrumental_path)
    ]
    subprocess.run(demucs_cmd, check=True, cwd=os.path.dirname(__file__))

    # 3. Convertir voz a formato compatible (mono, 44.1kHz)
    converted_vocals = temp_dir / "vocals_mono.wav"
    convert_cmd = [
        sys.executable, "convert_audio.py",
        "--input", str(vocals_path),
        "--output", str(converted_vocals)
    ]
    subprocess.run(convert_cmd, check=True, cwd=os.path.dirname(__file__))

    # 4. Inferencia con So-VITS-SVC (clonación de voz)
    cloned_vocals = temp_dir / "cloned_vocals.wav"
    svc_script = PROJECT_ROOT / "so-vits-svc" / "inference_main.py"
    svc_config = PROJECT_ROOT / "so-vits-svc" / "configs" / "base.yaml"
    svc_model = PROJECT_ROOT / "models" / "model.pth"
    svc_raw_dir = PROJECT_ROOT / "so-vits-svc" / "raw"
    svc_results_dir = PROJECT_ROOT / "so-vits-svc" / "results"
    svc_raw_dir.mkdir(parents=True, exist_ok=True)
    svc_results_dir.mkdir(parents=True, exist_ok=True)
    # Copiar el archivo convertido a so-vits-svc/raw/
    raw_filename = converted_vocals.name
    raw_path = svc_raw_dir / raw_filename
    shutil.copy(str(converted_vocals), str(raw_path))
    # Ejecutar inferencia pasando solo el nombre del archivo
    svc_cmd = [
        sys.executable, str(svc_script),
        "-c", str(svc_config),
        "-m", str(svc_model),
        "-n", raw_filename
    ]
    subprocess.run(svc_cmd, check=True, cwd=str(PROJECT_ROOT / "so-vits-svc"))
    # Buscar el archivo generado en results/
    import glob
    result_pattern = f"{raw_filename.split('.')[0]}*.*"
    result_files = list(svc_results_dir.glob(result_pattern))
    if not result_files:
        raise FileNotFoundError(f"No se encontró el resultado de inferencia para {raw_filename}")
    # Tomar el archivo más reciente generado
    result_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    svc_result = result_files[0]
    shutil.copy(str(svc_result), str(cloned_vocals))

    # 5. Mezclar voz clonada con instrumental
    result_name = f"result_{job_id}.wav"
    result_path = RESULTS_DIR / result_name
    mezclar_voces_instrumental(cloned_vocals, instrumental_path, result_path)

    # Limpieza opcional de temporales
    shutil.rmtree(temp_dir)

    return {"status": "processed", "result": result_name}

# Endpoints adicionales y lógica de procesamiento se agregarán en los siguientes pasos.
