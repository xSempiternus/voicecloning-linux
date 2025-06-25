# voiceclonation-linux

Pipeline completo y optimizado para clonación de voz artística usando **So-VITS-SVC**, **Demucs** y **FastAPI**.

> **Recomendado:** Entrena y ejecuta en **Linux/WSL** (Windows Subsystem for Linux) con Python 3.10+ y GPU Nvidia.  
> **No garantizado** en Windows nativo.

---

## Estructura del proyecto

- `backend/` — API FastAPI, scripts de entrenamiento y procesamiento, integración So-VITS-SVC y Demucs.
- `so-vits-svc/` — Código principal y scripts de So-VITS-SVC.
- `data/` — Audios de entrenamiento y procesados (**no incluidos en el repo**).
- `logs/` — Checkpoints y logs de entrenamiento (**no incluidos en el repo**).
- `frontend/`, `models/`, etc. — Otros módulos del proyecto.
- Scripts de automatización y optimización en la raíz del proyecto.

---

## Instalación y uso rápido (Linux/WSL)

1. **Clona el repositorio y entra a la carpeta:**
   ```bash
   git clone https://github.com/xSempiternus/voicecloning-linux.git
   cd voicecloning-linux
   ```

2. **Crea y activa el entorno virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Preprocesa y optimiza tus datos de voz:**
   ```bash
   # Verifica que todos los audios sean mono
   python backend/verificar_mono.py data/mi_voz/niko/

   # Chequea la calidad del dataset
   python check_audio_quality.py data/mi_voz/niko/

   # Limpia los audios para evitar pitidos
   python clean_audio_pitching.py data/mi_voz/niko/

   # Preprocesa los datos para So-VITS-SVC
   python so-vits-svc/preprocess_hubert_f0.py --in_dir data/mi_voz/niko --f0_predictor harvest
   ```

4. **Entrena el modelo (GPU):**
   ```bash
   python so-vits-svc/run_train_gpu.py
   # o para CPU
   python so-vits-svc/train_cpu.py
   ```

5. **Monitorea el entrenamiento con TensorBoard:**
   ```bash
   tensorboard --logdir=logs/niko
   # Abre http://localhost:6006 en tu navegador
   ```

6. **Post-procesa el audio generado:**
   ```bash
   python post_process_audio.py so-vits-svc/results/mi_inferencia.wav
   ```

---

## Optimización y mejores prácticas

- Usa `mel_fmin: 40.0` y `mel_fmax: 14000.0` en tu config para evitar artefactos.
- Activa `vol_aug` y `vol_embedding` para mayor robustez.
- Prueba el predictor de F0 `harvest` o `rmvpe` para mejores resultados.
- Si aparecen pitidos, aplica el post-procesado y revisa la calidad de los datos originales.
- Consulta la guía avanzada: `GUIA_OPTIMIZACION_SO_VITS_SVC.md`.

---

## Ejemplo de inferencia

```bash
python so-vits-svc/inference_main.py \
  -m logs/niko/G_epoch_270.pth \
  -c logs/niko/config.json \
  -n Thinking\ Out\ Loud_only_vocals_mono.wav \
  -s niko \
  --device cuda \
  -f0p harvest \
  --noice_scale 0.1
```

El archivo generado estará en `so-vits-svc/results/` con un nombre similar a:
`Thinking Out Loud_only_vocals_mono.wav_0key_niko_sovits_harvest.flac`

---

## Troubleshooting

- Si tienes errores de dependencias, revisa la versión de Python y reinstala el entorno virtual.
- Si el audio da error de canales, asegúrate de que todos los `.wav` sean **mono** (usa el script de conversión incluido).
- Para problemas de rutas, usa siempre rutas absolutas o relativas desde la raíz del proyecto.
- Consulta los logs y TensorBoard para monitorear el entrenamiento y detectar problemas.
- Si el modelo produce pitidos, revisa la guía de optimización y aplica el post-procesado.

---

## Buenas prácticas: exclusión de archivos con `.gitignore`

Este repositorio incluye un archivo `.gitignore` robusto para mantener el historial limpio y evitar subir archivos innecesarios o pesados.

**¿Qué se excluye?**
- Entornos virtuales (`.venv/`, `env/`, etc.) tanto en la raíz como en subcarpetas.
- Datos de entrenamiento, audios, resultados y archivos generados por el pipeline.
- Checkpoints, logs, archivos de TensorBoard y modelos entrenados.
- Archivos temporales y de caché de Python, Jupyter, editores y sistemas operativos.
- Configuraciones de IDEs y archivos de lock de gestores de dependencias (opcional).
- Submódulos y archivos internos de So-VITS-SVC y Demucs que no deben subirse.

**¿Por qué es importante?**
- Evita subir archivos grandes o privados.
- Facilita la colaboración y la replicabilidad.
- Mantiene el repositorio profesional y fácil de clonar.

Si necesitas compartir datos o modelos, usa servicios externos (Google Drive, HuggingFace, etc.) y documenta los pasos de descarga en el README.

---

## Créditos y licencias

- Basado en [So-VITS-SVC](https://github.com/svc-develop-team/so-vits-svc) y [Demucs](https://github.com/facebookresearch/demucs).
- Consulta las licencias originales en cada submódulo.

---

## Nota importante sobre So-VITS-SVC

A partir de la versión actual, la carpeta `so-vits-svc` ya **no es un submódulo**: ahora forma parte integral de este repositorio y puedes modificar libremente cualquier archivo de su interior (por ejemplo, `utils.py` y `train.py` para entrenamiento single GPU).

**¿Por qué este cambio?**
- Permite personalizar y versionar scripts internos sin depender del repositorio original.
- Facilita la replicabilidad y el soporte a largo plazo.

**¿Qué debes saber?**
- Si ya habías clonado el repo antes, elimina cualquier referencia a submódulos con:
  ```bash
  git submodule deinit -f so-vits-svc
  git rm --cached so-vits-svc
  rm -rf .git/modules/so-vits-svc
  rm -f .gitmodules
  ```
- Ahora, al clonar el repo, tendrás acceso directo a todo el código de `so-vits-svc` y sus modificaciones.

Si necesitas restaurar la versión original de So-VITS-SVC, puedes volver a agregarlo como submódulo o clonar el repo oficial por separado.
---

## Resultados de inferencia y observaciones

Se realizaron inferencias utilizando el último modelo entrenado. Los resultados obtenidos fueron unos pitidos graves, aunque se logra percibir la voz de fondo. Se probó con la voz entrenada intentando cantar "Thinking Out Loud" de Ed Sheeran.
