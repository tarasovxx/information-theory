import numpy as np
from scipy.signal import butter, lfilter


def white_noise(size, mean=0, std_dev=1):
    return np.random.normal(mean, std_dev, size)


def pink_noise(size):
    white = np.random.normal(0, 1, size)
    freq = np.fft.fftfreq(size)
    freq[0] = 1e-6
    spectrum = np.fft.fft(white)
    spectrum /= np.sqrt(np.abs(freq))
    pink = np.fft.ifft(spectrum)

    return pink.real


def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order)
    return lfilter(b, a, data)


def white_noise_filtered(size, cutoff, fs):
    white = np.random.normal(0, 1, size)
    return lowpass_filter(white, cutoff, fs)


def impulse_noise(size, density=0.1, magnitude=5):
    noise = np.zeros(size)
    num_impulses = int(size * density)
    for _ in range(num_impulses):
        index = np.random.randint(0, size)
        noise[index] = np.random.choice([magnitude, -magnitude])
    return noise
