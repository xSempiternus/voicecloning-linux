# voiceclonation-linux

Pipeline completo para clonación de voz artística usando **So-VITS-SVC**, **Demucs** y **FastAPI**.

> **Recomendado:** Entrena y ejecuta en **Linux/WSL** (Windows Subsystem for Linux) con Python 3.10+ y GPU Nvidia.  
> **No garantizado** en Windows nativo.

---

## Estructura del proyecto

- `backend/` — API FastAPI, scripts de entrenamiento y procesamiento, integración So-VITS-SVC y Demucs.
- `so-vits-svc/` — Código principal y scripts de So-VITS-SVC.
- `data/` — Audios de entrenamiento y procesados (**no incluidos en el repo**).
- `logs/` — Checkpoints y logs de entrenamiento (**no incluidos en el repo**).
- `frontend/`, `models/`, etc. — Otros módulos del proyecto.

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

3. **Preprocesa tus datos de voz:**
   ```bash
   python so-vits-svc/preprocess_flist_config.py --source_dir data/mi_voz
   python so-vits-svc/preprocess_hubert_f0.py
   ```

4. **Entrena el modelo:**
   ```bash
   python so-vits-svc/train.py -c so-vits-svc/configs/config.json -m svc
   ```

5. **Monitorea el entrenamiento con TensorBoard:**
   ```bash
   tensorboard --logdir=logs/svc
   # Abre http://localhost:6006 en tu navegador
   ```

---

## Notas y buenas prácticas

- **No subas** datos, audios, logs, checkpoints ni entornos virtuales al repositorio.
- Si trabajas en **Windows**, crea un entorno virtual nuevo y ejecuta `pip install -r requirements.txt`.  
  _Los entornos virtuales de Linux y Windows **no son compatibles** entre sí._
- Los archivos de entrenamiento, logs y checkpoints generados en Linux/WSL **no deben copiarse** directamente a Windows.
- Usa siempre `.gitignore` para mantener el repo limpio.
- Documenta cualquier cambio importante en este README.
- Si necesitas scripts distintos para Windows y Linux, sepáralos en carpetas o documenta su uso.

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

## Troubleshooting

- Si tienes errores de dependencias, revisa la versión de Python y reinstala el entorno virtual.
- Si el audio da error de canales, asegúrate de que todos los `.wav` sean **mono** (usa el script de conversión incluido).
- Para problemas de rutas, usa siempre rutas absolutas o relativas desde la raíz del proyecto.
- Consulta los logs y TensorBoard para monitorear el entrenamiento y detectar problemas.

---

## Créditos y licencias

- Basado en [So-VITS-SVC](https://github.com/svc-develop-team/so-vits-svc) y [Demucs](https://github.com/facebookresearch/demucs).
- Consulta las licencias originales en cada submódulo.

---

¿Listo para clonar tu voz?  
¡Sigue los pasos y documenta tu experiencia para mejorar este pipeline!

---

¿Quieres agregar ejemplos de inferencia, integración web o más troubleshooting?  
¡Edita este README y contribuye!