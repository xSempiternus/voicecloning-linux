import requests
import os

audio_path = "data/ghost_town.wav"
url = "http://localhost:8000/process/"

with open(audio_path, "rb") as f:
    files = {"file": (os.path.basename(audio_path), f, "audio/mpeg")}
    response = requests.post(url, files=files)
    print("Status:", response.status_code)
    print("Respuesta:", response.text)
