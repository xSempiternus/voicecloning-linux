import soundfile as sf
import numpy as np
sf.write("test.wav", np.zeros(44100), 44100)