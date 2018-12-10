
import time
import unittest

from scipy.io import wavfile
from scipy.fftpack import fft
from scipy.fftpack import fftfreq
from matplotlib.animation import FuncAnimation
import numpy as n
import matplotlib.pyplot as plt

def running_mean(x, N):
    cumsum = n.cumsum(n.insert(x, 0, 0)) 
    cmsum = n.zeros(len(x),dtype = x.dtype)
    cumsum = (cumsum[N:] - cumsum[:-N]) / float(N)
    for i in range(len(cumsum)):
        cmsum[i] = cumsum[i]
    for i in range(0,N):
        cmsum[N+i] = (cumsum[N+i] - cumsum[-(N+i)]) / float(N-i)
    return cmsum
    
def band_pass(x, y, xmin, xmax):
    for i,data in enumerate(x):
        if data <= xmin or data >= xmax:
            y[i]=0
    return y

def gaussian_filter(ampl_data, freq_data, f_mu, f_std):
    filtering = n.exp(-0.5*((freq_data-f_mu)/f_std)**2)
    ampl_data = ampl_data*filtering
    return ampl_data

class MyTests(unittest.TestCase):
    def test_freq_sin(x):
        T_s = 1e-6
        t = n.arange(0, 1, T_s, dtype=n.float)
        f0 = 3000  # Hz

        wav_data = n.sin(n.pi * 2.0 * f0 * t)

        data_ampl, data_freq, data_db, integ_range = THE_FUNCTION_THAT_EXTRACTS_FREQUENCY_STUFF(wav_data, T_s=T_s, window=wav_data.size, overlap=0)
        mean_freq = n.sum(n.abs(data_ampl) * data_freq[0]) / n.sum(n.abs(data_ampl))
        assert n.abs(mean_freq - f0) < 100


def THE_FUNCTION_THAT_EXTRACTS_FREQUENCY_STUFF(wav_data, T_s, window, overlap):
    print(wav_data.shape, window, overlap)

    # remove last elements just for safty
    if overlap > 0:
        integ_range = list(range(0, wav_data.shape[0] - window, overlap))
        del integ_range[-1]
    else:
        integ_range = list(range(0, wav_data.shape[0] - window, window))

    # generate time dependant specturm
    data_ampl = []
    data_freq = []
    data_db = []

    for i in integ_range:
        sub_data = wav_data[i:(i + window)]
        tmp_ampl = fft(sub_data)
        tmp_freq = fftfreq(sub_data.size, d=T_s)
        pos = tmp_freq > 0

        data_ampl.append(tmp_ampl[pos])
        data_freq.append(tmp_freq[pos])
        data_db.append(10.0 * n.log10(n.abs(tmp_ampl[pos])))

    return n.array(data_ampl), n.array(data_freq), n.array(data_db), n.array(integ_range)


def main():
    fs, data = wavfile.read('./test.wav')
    T_s = 1.0 / float(fs)

    window = 2000
    window_T = window * T_s
    overlap = window // 2  # this is the step the window moves by in the FFT analysis

    data_ampl, data_freq, data_db, integ_range = THE_FUNCTION_THAT_EXTRACTS_FREQUENCY_STUFF(wav_data=data[:, 0], T_s=T_s, window=window, overlap=overlap)

    # generate animatioon
    def update_text(i):
        return 't={:.4f} s'.format(integ_range[i] * T_s)

    fig, ax = plt.subplots()
    ln, = ax.plot([], [])
    titl = fig.text(0.5, 0.94, update_text(0), size=22, horizontalalignment='center')

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


if __name__ == '__main__':
    # main()
    unittest.main()
