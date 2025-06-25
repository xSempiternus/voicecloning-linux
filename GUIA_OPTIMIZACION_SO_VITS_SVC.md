# Guía de Optimización para So-Vits-SVC

Este documento recopila información importante adicional y soluciones a problemas comunes que hemos identificado durante el uso de So-Vits-SVC para clonación de voz.

## Problemas de Pitidos y Soluciones

Uno de los problemas más comunes al usar So-Vits-SVC es la aparición de pitidos en el audio generado. Hemos identificado varias causas y soluciones:

### Causas principales de los pitidos

1. **Configuración inadecuada de parámetros mel**
   - Valores extremos de `mel_fmin` y `mel_fmax` (0.0 y 22050.0)
   - Ausencia de soporte para variaciones de volumen

2. **Procesamiento de F0 incorrecto**
   - El uso de `use_automatic_f0_prediction: true` puede causar problemas con datos limitados

3. **Cantidad insuficiente de datos de entrenamiento**
   - Menos de 30 minutos de audio puede resultar en calidad reducida

### Parámetros optimizados

Hemos encontrado que los siguientes valores podrían mejor para reducir los pitidos:

```json
{
  "train": {
    "learning_rate": 0.00008,
    "warmup_epochs": 2,
    "vol_aug": true
  },
  "data": {
    "mel_fmin": 40.0,
    "mel_fmax": 14000.0
  },
  "model": {
    "vol_embedding": true,
    "use_automatic_f0_prediction": false
  }
}
```

### Parámetros recomendados para inferencia

Para obtener mejores resultados durante la inferencia, se recomiendan estos parámetros:

```bash
python inference_main.py \
--model_path logs/niko/G_epoch_150.pth \
--config_path logs/niko/config.json \
--clean_names "audio_input.wav" \
--trans -1 \
--spk_list niko \
--f0_predictor harvest \
--noice_scale 0.1 \
--pad_seconds 0.7
```

## Flujo de trabajo recomendado

1. **Preparación de datos**
   - Usa archivos WAV mono de 44.1kHz
   - Aproximadamente 30 minutos o más de audio limpio
   - Realiza la separación de voz si es necesario

2. **Preprocesamiento**
   ```bash
   python preprocess_hubert_f0.py --in_dir ../data/mi_voz/nombre --f0_predictor harvest
   ```

3. **Verificación de archivos auxiliares**
   - Asegúrate de que se generen archivos .f0.npy, .hubert.npy y .vol.npy

4. **Entrenamiento con parámetros optimizados**
   ```bash
   python train.py -m nombre_modelo
   ```

5. **Monitoreo con TensorBoard**
   ```bash
   tensorboard --logdir=logs/nombre_modelo
   ```

6. **Post-procesamiento para mejorar calidad**
   - Aplica filtrado paso bajo (14kHz) al audio generado
   - Normaliza el volumen para evitar picos extremos
   - Usa compresión ligera para mejorar la consistencia

## Consejos adicionales

- Si el modelo sigue produciendo pitidos después de 50+ épocas, considera reiniciar el entrenamiento desde cero
- Utiliza el predictor de F0 "harvest" o "rmvpe" para mayor precisión
- Aumenta las épocas de entrenamiento gradualmente y monitorea los resultados
- Prueba diferentes valores de `noice_scale` durante la inferencia (0.1-0.4)

## Recursos y herramientas útiles

- Herramienta para separación de voz: [Demucs](https://github.com/facebookresearch/demucs)
- [Enhancer para audio generado](https://github.com/tumuyan/RealSR-NCNN-Android) para mejorar la calidad
- [MoeVoiceStudio](https://github.com/NaruseMioShirakana/MoeVoiceStudio) para edición avanzada
