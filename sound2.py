import numpy as np
import wavio
# imports
import matplotlib.pyplot as plt
import numpy as np
import wave, sys
import random
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import norm
# Parameters
samplerate = 44100   # samples per second
duration = 2
samples = duration*samplerate
t = np.linspace(0,duration, samples, endpoint=False)
x = (np.sin(2*np.pi*50*t)+np.sin(2*np.pi*100*t)+np.sin(2*np.pi*150*t)+np.sin(2*np.pi * 300 * t) +np.sin(2*np.pi * 400 * t)+np.sin(2*np.pi*500*t)+np.sin(2*np.pi*600*t)+np.sin(2*np.pi *700* t) +np.sin(2*np.pi * 1200 * t) )
# Write the samples to a file
wavio.write("sine.wav", x, samplerate, sampwidth=1)

#data = wavio.read("sine.wav")
#samplerate,data = wavfile.read("sine.wav")



       
      