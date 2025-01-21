import numpy as np


# специальные сигналы
def single_pulse(T, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    s[t < T] = 1
    return t, s


def delta_function(A, T, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    s[np.abs(t - T) < delta_t / 2] = A
    return t, s


def unit_step(T, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    s[t >= T] = 1
    return t, s


# импульсы
def generate_unipolar_pulses(signal_duration, pulse_duration, step):
    t = np.arange(0.0, signal_duration, step)
    signal = np.zeros_like(t)
    for pulse_num in range(int(signal_duration / pulse_duration) + 1):
        start = int(pulse_num * pulse_duration / step)
        end = int(start + pulse_duration / 2 / step) + 1
        signal[start:end] = 1
    return t, signal


def generate_bipolar_pulses(signal_duration, pulse_duration, step):
    t = np.arange(0.0, signal_duration, step)
    signal = np.empty_like(t)
    for pulse_num in range(int(signal_duration / pulse_duration) + 1):
        start = int(pulse_num * pulse_duration / step)
        end_pulse = int(start + pulse_duration / 2 / step)
        end = int(start + pulse_duration / step) + 1
        signal[start:end_pulse] = 1
        signal[end_pulse:end] = -1
    return t, signal


# функция генерации синусоидального сигнала
def generate_harmonic(frequency, duration, step, shift):
    t = np.arange(0.0, duration + 0.001, step)
    if shift != 0:
        signal = np.sin(2 * np.pi * frequency * t + shift)
    else:
        signal = np.sin(2 * np.pi * frequency * t)
    return t, signal


# функция генерации полигармонического сигнала
def generate_poliharmonic(frequencies, duration, step):
    t = np.arange(0.0, duration + 0.001, step)
    signal = sum(np.sin(2 * np.pi * f * t) for f in frequencies)
    return t, signal


# Функция генерации затухающей синусоиды
def generate_damped_sine(alpha, frequency, duration, step):
    t = np.arange(0.0, duration + 0.001, step)
    signal = np.exp(-alpha * t) * np.sin(2 * np.pi * frequency * t)
    return t, signal