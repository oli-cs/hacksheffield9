import numpy as np
import librosa, librosa.display
import noisereduce as nr
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
    

#calculate note envelopes

#Imports

## Visualization
import seaborn
import matplotlib.pyplot as plt
import IPython.display as ipd
from ipywidgets import interactive_output #http://ipywidgets.readthedocs.io/en/latest/index.html
from ipywidgets import IntSlider, FloatSlider, fixed, Checkbox
from ipywidgets import VBox, Label

#%matplotlib notebook

## Matplotlib
plt.rc("figure", figsize=(16, 8))
# Parameters
## Signal Processing 
fs = 44100                               # Sampling Frequency
nfft = 2048                              # length of the FFT window
overlap = 0.5                            # Hop overlap percentage
hop_length = int(nfft*(1-overlap))       # Number of samples between successive frames
n_bins = 72                              # Number of frequency bins
mag_exp = 4                              # Magnitude Exponent
pre_post_max = 6                         # Pre- and post- samples for peak picking
cqt_threshold = -61                      # Threshold for CQT dB levels, all values below threshold are set to -120 dB

# Load Audio
# Loadinging audio file
filename = 'notes/here comes the sun extract.wav'
x, fs = librosa.load(filename, sr=None, mono=True, duration=12)
# Notes Center Frequencies
notes_freqs = 440*2**(np.arange(-57, (128-57))/12)

cqt_freqs = librosa.core.cqt_frequencies(n_bins=128, fmin=librosa.note_to_hz('C0'), bins_per_octave=12)
# CQT
## Function
def calc_cqt(x,fs=fs,hop_length=hop_length, n_bins=n_bins, mag_exp=mag_exp):
    C = librosa.cqt(x, sr=fs, hop_length=hop_length, fmin=None, n_bins=n_bins)
    C_mag = librosa.magphase(C)[0]**mag_exp
    CdB = librosa.core.amplitude_to_db(C_mag ,ref=np.max)
    return CdB
# CQT Threshold
def cqt_thresholded(cqt,thres=cqt_threshold):
    new_cqt=np.copy(cqt)
    new_cqt[new_cqt<thres]=-130
    return new_cqt

# Onset Envelope from Cqt
def calc_onset_env(cqt):
    return librosa.onset.onset_strength(S=cqt, sr=fs, aggregate=np.mean, hop_length=hop_length)
# Onset from Onset Envelope
def calc_onset(cqt, pre_post_max=pre_post_max, backtrack=True):
    onset_env=calc_onset_env(cqt)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env,
                                           sr=fs, units='frames', 
                                           hop_length=hop_length, 
                                           backtrack=backtrack,
                                           pre_max=pre_post_max,
                                           post_max=pre_post_max)
    onset_boundaries = np.concatenate([[0], onset_frames, [cqt.shape[1]]])
    onset_times = librosa.frames_to_time(onset_boundaries, sr=fs, hop_length=hop_length)
    return [onset_times, onset_boundaries, onset_env]

# Fine Tuning UI
style = {'description_width': 'initial'}
mag_exp_slider=IntSlider(value=mag_exp, min=1, max=32, step=1, 
                         description='mag_exp:',continuous_update=False)

thres_slider=IntSlider(value=cqt_threshold, min=-120, max=0, step=1, 
                                                     description='Threshold:',continuous_update=False)

pre_post_slider=IntSlider(value=pre_post_max, min=1, max=32, step=1, 
                         description='Pre_post_max:',continuous_update=False, style=style)

backtrack_box=Checkbox(value=False,description='backtrack',disabled=False)

thres=thres_slider.value
mag_exp=mag_exp_slider.value
pre_post_max=pre_post_slider.value
backtrack=backtrack_box.value

CdB = calc_cqt(x,fs,hop_length, n_bins, mag_exp)
new_cqt=cqt_thresholded(CdB,thres)

#array of note locations!!
onsets = calc_onset(new_cqt,pre_post_max, backtrack)


#loop through audio file note by note (using envelopes) and calculate the list of notes

notes = []

for i in range(len(onsets[0])):
    if len(onsets[0]) == i+1:
        pass
    else:
        slice = calc_freq("notes/here comes the sun extract.wav",(onsets[0][i]*1000),(onsets[0][i+1]*1000))
    notes.append(calc_note(slice,frequencies))

print(notes)



# 

'''
def inter_cqt_tuning(mag_exp,thres,pre_post_max, backtrack):
    thres=thres_slider.value
    mag_exp=mag_exp_slider.value
    pre_post_max=pre_post_slider.value
    backtrack=backtrack_box.value
    global CdB
    CdB = calc_cqt(x,fs,hop_length, n_bins, mag_exp)
    #plt.figure()
    new_cqt=cqt_thresholded(CdB,thres)
    #librosa.display.specshow(new_cqt, sr=fs, hop_length=hop_length, x_axis='time', y_axis='cqt_note', cmap='coolwarm')
    #plt.ylim([librosa.note_to_hz('B2'),librosa.note_to_hz('B6')])
    global onsets
    onsets=calc_onset(new_cqt,pre_post_max, backtrack)
    print(onsets[0])
    #plt.vlines(onsets[0], 0, fs/2, color='k', alpha=0.8)
    #plt.title("Here comes Oli, doo doo doo doo")
    #plt.colorbar()
    #plt.show()'''
    
'''    
# Display UI
out = interactive_output(inter_cqt_tuning,  {'mag_exp': mag_exp_slider, 'thres': thres_slider, 
                                             'pre_post_max': pre_post_slider, 'backtrack':backtrack_box})
ui = VBox([mag_exp_slider, thres_slider, pre_post_slider, backtrack_box])
display(ui, out)'''

