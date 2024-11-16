import numpy as np
import librosa, librosa.display
from scipy.fft import *
from scipy.io import wavfile

frequencies = [
    [[213.5,226.55],"A"],
    [[226.56,240],"A#Bb"],
    [[240.01,254.25],"B"],
    [[254.26,269.4],"C"],
    [[269.41,285.45],"C#Db"],
    [[285.46,302.4],"D"],
    [[302.41,320.35],"D#Eb"],
    [[320.36,339.4],"E"],
    [[339.41,359.6],"F"],
    [[359.6,381],"F#Gb"],
    [[381.1,403.6],"G"],
    [[403.61,427.6],"G#Ab"]
]

def calc_freq(file, start_time, end_time):

    # Open the file and convert to mono
    sr, data = wavfile.read(file)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    # Return a slice of the data from start_time to end_time
    dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]

    # Fourier Transform
    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / sr)

    # Uncomment these to see the frequency spectrum as a plot
    # plt.plot(xf, np.abs(yf))
    # plt.show()

    # Get the most dominant frequency and return it
    idx = np.argmax(np.abs(yf))
    freq = xf[idx]
    return freq

def calc_note(raw, notes):

    normal = (raw % 213.5) + 213.5
    for i in range(len(notes)):
        if normal > notes[i][0][0] and normal < notes[i][0][1]:
            return notes[i][1]
    


nowfreq = calc_freq("notes/A.wav",0000,10000)
print("raw: ",nowfreq,"note: ",calc_note(nowfreq, frequencies))

nowfreq = calc_freq("notes/C.wav",0000,10000)
print("raw: ",nowfreq,"note: ",calc_note(nowfreq, frequencies))

nowfreq = calc_freq("notes/E.wav",0000,10000)
print("raw: ",nowfreq,"note: ",calc_note(nowfreq, frequencies))

nowfreq = calc_freq("notes/G.wav",0000,10000)
print("raw: ",nowfreq,"note: ",calc_note(nowfreq, frequencies))

nowfreq = calc_freq("notes/C chord.wav",0000,10000)
print("raw: ",nowfreq,"note: ",calc_note(nowfreq, frequencies))

