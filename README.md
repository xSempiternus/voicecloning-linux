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

## Nota sobre la integración de So-VITS-SVC

- La carpeta `so-vits-svc` ahora forma parte integral de este repositorio y **ya no es un submódulo**.
- Se eliminó el submódulo y el repositorio interno (`.git`) para que todo el código y las modificaciones personalizadas sean visibles y versionables directamente aquí.
- Si necesitas hacer este proceso en otro proyecto, sigue estos pasos:
  1. Elimina el submódulo:
     ```bash
     git rm --cached so-vits-svc
     rm -rf so-vits-svc/.git
     rm -f .gitmodules
     ```
  2. Agrega la carpeta como normal:
     ```bash
     git add so-vits-svc
     git commit -m "Eliminar submódulo y agregar so-vits-svc como carpeta normal"
     git push
     ```
- Ahora puedes modificar cualquier archivo de `so-vits-svc` y compartir tus cambios con otros colaboradores.

**Checklist final para dejar el repo listo y profesional:**
- [x] `.gitignore` robusto y actualizado
- [x] README claro, con advertencias y buenas prácticas
- [x] Submódulos eliminados y carpetas integradas
- [x] Documentación de pasos especiales (como este)
- [x] Estructura de carpetas limpia y replicable
- [x] Instrucciones para clonar y usar el repo desde cero

¡El repositorio está listo para producción, colaboración y replicabilidad!

---

¿Listo para clonar tu voz?  
¡Sigue los pasos y documenta tu experiencia para mejorar este pipeline!

---

¿Quieres agregar ejemplos de inferencia, integración web o más troubleshooting?  
¡Edita este README y contribuye!