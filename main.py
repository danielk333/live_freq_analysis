from scipy.io import wavfile
from scipy.fftpack import fft 
from scipy.fftpack import fftfreq 
from matplotlib.animation import FuncAnimation
import numpy as n
import matplotlib.pyplot as plt
import time

fs, data = wavfile.read('./test.wav')

T_s = 1.0/float(fs)

window = 2000
window_T = window*T_s
overlap = window//2 #this is the step the window moves by in the FFT analysis

integ_range = list(range(0, data.shape[0]-window, overlap))
#remove last elements just for safty
del integ_range[-1]

#generate time dependant specturm
data_ampl = []
data_freq = []
data_db = []

for i in integ_range:
    sub_data = data[i:(i+window),0]

    tmp_ampl = fft(sub_data)
    tmp_freq = fftfreq(sub_data.size,d=T_s)
    pos = tmp_freq > 0

    data_ampl.append( tmp_ampl[pos] ) 
    data_freq.append( tmp_freq[pos] )
    data_db.append( 10.0*n.log10(n.abs(tmp_ampl[pos])) )
    
#generate animatioon
def update_text(i):
    return 't={:.4f} s'.format(integ_range[i]*T_s)

fig, ax = plt.subplots()
ln, = ax.plot([], [])
titl = fig.text(0.5,0.94,update_text(0),size=22,horizontalalignment='center')

def init():
    ax.set_xlim(0, 5000)
    ax.set_ylim(20, 100)
    return ln,

def update(i):
    t0 = time.time()
    titl.set_text(update_text(i))
    ln.set_data(data_freq[i], data_db[i])
    time.sleep(window_T)
    while time.time() - t0 < window_T:
        time.sleep(0.001)
    return ln,

ani = FuncAnimation(fig, update, frames=range(len(integ_range)),
                    init_func=init)

plt.show()
