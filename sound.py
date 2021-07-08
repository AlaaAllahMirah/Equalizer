import math
import wave
import struct



#audio is a global variable containing a list of all samples
audio = []

# 44100 is the industry standard sample rate - CD quality.
sample_rate = 44100



def create_signal(f1 = 500, f2 = 600, f3 = 880, f4 = 700 , f5 = 1050, duration_seconds = 1):
    global audio
    num_samples = duration_seconds * sample_rate

    for x in range(int(num_samples)):
        sig1 = math.sin(2 * math.pi * f1 * ( x / sample_rate ))
        sig2 = math.sin(2 * math.pi * f2 * ( x / sample_rate ))
        sig3 = math.sin(2 * math.pi * f3 * ( x / sample_rate ))
        sig4 = math.sin(2 * math.pi * f4 * ( x / sample_rate ))
        sig5 = math.sin(2 * math.pi * f5 * ( x / sample_rate ))
        audio.append(sig1 + sig2 + sig3 + sig4 + sig5)
    
    return


def save_wav(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))


    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 1000.0 )))

    wav_file.close()

    return


create_signal()
    
save_wav("soundfile.wav")