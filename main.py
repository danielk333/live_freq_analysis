
import time
import unittest

import numpy as n
from scipy.io import wavfile
from scipy.fftpack import fft, ifft, fftfreq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def running_mean(x, N):
    cumsum = n.cumsum(n.insert(x, 0, 0)) 
    cmsum = n.zeros(len(x),dtype = x.dtype)
    cumsum = (cumsum[N:] - cumsum[:-N]) / float(N)
    for i in range(len(cumsum)):
        cmsum[i] = cumsum[i]
    for i in range(0,N):
        cmsum[N+i] = (cumsum[N+i] - cumsum[-(N+i)]) / float(N-i)
    return cmsum
    
def band_pass(y, x, xmin, xmax):
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

    if window > wav_data.shape[0]:
        window = wav_data.shape[0]

    if overlap > 0:
        integ_range = list(range(0, wav_data.shape[0] - window, overlap))
    else:
        integ_range = list(range(0, wav_data.shape[0] - window, window))
    
    if len(integ_range) == 0:
        integ_range = [0]

    # generate time dependant specturm
    data_ampl = []
    data_freq = []
    data_db = []

    for i in integ_range:
        sub_data = wav_data[i:(i + window)]
        tmp_ampl = fft(sub_data)
        tmp_freq = fftfreq(sub_data.size, d=T_s)
        pos = tmp_freq > 0

        data_ampl.append(tmp_ampl)
        data_freq.append(tmp_freq)
        data_db.append(10.0 * n.log10(n.abs(tmp_ampl)))

    return n.array(data_ampl), n.array(data_freq), n.array(data_db), n.array(integ_range)

def run_fft2wave(data_ampl, integ_range, window, rate, filename, bit_num = 1, volume = 1.0):
    data = n.empty((max(integ_range) + window, 1), dtype=n.int16)

    for i, data_ch in zip(integ_range, data_ampl):
        tmp_data = n.real(ifft(data_ch))
        tmp_data = n.int16(tmp_data*(bit_num+1)*volume)
        data[i:(i + window), 0] = tmp_data

    wavfile.write(filename, rate, data)

def frequency_shift(ampl_data, freq_data, shift):
    #assume linear freq data space
    num = freq_data.size
    dfreq = (n.max(freq_data) - n.min(freq_data))/float(num)

    if shift < 0:
        shift_num = int((-shift)//dfreq)+1
        n.copyto(ampl_data[:-shift_num], ampl_data[shift_num:])
        #ampl_data[-shift_num:] = 0.0
    else:
        shift_num = int(shift//dfreq)+1
        n.copyto(ampl_data[shift_num:], ampl_data[:-shift_num])
        #ampl_data[:shift_num] = 0.0

    return ampl_data

def main(plot=False):
    fs, data_raw = wavfile.read('./test.wav')
    T_s = 1.0 / float(fs)

    if data_raw.dtype == 'int16':
        nb_bits = 16 # -> 16-bit wav files
    elif data_raw.dtype == 'int32':
        nb_bits = 32 # -> 32-bit wav files
    max_nb_bit = float(2 ** (nb_bits - 1))
    data = n.float64(data_raw.copy())
    data = data / (max_nb_bit + 1.0)

    window = 2000
    window_T = window * T_s
    overlap = window // 2  # this is the step the window moves by in the FFT analysis

    data_ampl, data_freq, data_db, integ_range = THE_FUNCTION_THAT_EXTRACTS_FREQUENCY_STUFF(wav_data=data[:, 0], T_s=T_s, window=window, overlap=overlap)

    #this runs filter on the data

    #gaussian
    for ind in range(data_ampl.shape[0]):
        data_ampl[ind,:] = gaussian_filter(data_ampl[ind,:], data_freq[ind,:], 1000, 300)
    #Bandpass
    #for ind in range(data_ampl.shape[0]):
        #data_ampl[ind,:] = band_pass(data_ampl[ind,:], data_freq[ind,:], 300, 700)
    #shift down
    for ind in range(data_ampl.shape[0]):
        data_ampl[ind,:] = frequency_shift(data_ampl[ind,:], data_freq[ind,:], -400.0)

    

    #this saves to wav file
    run_fft2wave(data_ampl, integ_range, window, fs, 'modified_gbp_shifted.wav', bit_num = max_nb_bit, volume = 0.25)

    if plot:
        # generate animatioon
        def update_text(i):
            return 't={:.4f} s'.format(integ_range[i] * T_s)

        fig, ax = plt.subplots()
        ln, = ax.plot([], [])
        titl = fig.text(0.5, 0.94, update_text(0), size=22, horizontalalignment='center')

        def init():
            ax.set_xlim(0, 2000)
            ax.set_ylim(20, 100)
            return ln,

        def update(i):
            t0 = time.time()
            titl.set_text(update_text(i))
            ln.set_data(data_freq[i,:], 10.0 * n.log10(n.abs(data_ampl[i,:]*(max_nb_bit + 1.0))))
            time.sleep(window_T)
            while time.time() - t0 < window_T:
                time.sleep(0.001)
            return ln,

        ani = FuncAnimation(fig, update, frames=range(len(integ_range)),
                            init_func=init)

        plt.show()


if __name__ == '__main__':
    main(plot=False)
    #unittest.main()
