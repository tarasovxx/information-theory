import numpy as np
import matplotlib.pyplot as plt


def harmonic_signal(A, T, T_N, delta_t=None):
    if delta_t is None:
        delta_t = T / 1000
    t = np.arange(0, T_N, delta_t)
    s = A * np.sin((2 * np.pi / T) * t)
    return t, s


def polyharmonic_signal(T, T_N, delta_t=None, A_list=[1]):
    if delta_t is None:
        delta_t = T / 1000
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    for i, A in enumerate(A_list, start=1):
        s += A * np.sin((2 * np.pi * i / T) * t)
    return t, s


def unipolar_pulses(T, n, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    for i in range(n):
        start = int(i * T / delta_t)
        end = int((i + 1) * T / delta_t)
        s[start:end] = 1
    return t, s


def bipolar_pulses(T, n, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    for i in range(n):
        start = int(i * T / delta_t)
        end = int((i + 1) * T / delta_t)
        s[start:end] = 1 if i % 2 == 0 else -1
    return t, s


def damped_sine_wave(A, alpha, f, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = A * np.exp(-alpha * t) * np.sin(2 * np.pi * f * t)
    return t, s


def single_pulse(T, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    s[t < T] = 1
    return t, s


def single_rectangular_pulse(A, T, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    s[np.abs(t - T_N / 2) <= T / 2] = A
    return t, s


def single_exponential_pulse(A, beta, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = A * np.exp(-beta * t)
    return t, s


def unit_step(T, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    s[t >= T] = 1
    return t, s


def delta_function(A, T, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    s[np.abs(t - T) < delta_t / 2] = A
    return t, s


def triangular_signal(A, T, T_N, delta_t):
    t = np.arange(0, T_N, delta_t)
    s = np.zeros_like(t)
    for i, time in enumerate(t):
        phase = (time % T) / T
        if phase < 0.5:
            s[i] = 4 * A * phase
        else:
            s[i] = 4 * A * (1 - phase)
    return t, s


def plot_signals():
    plt.figure(figsize=(15, 20))

    # Гармонический сигнал
    t, s = harmonic_signal(A=1, T=2, T_N=10)
    plt.subplot(6, 2, 1)
    plt.plot(t, s)
    plt.title("Гармонический сигнал")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    # Полигармонический сигнал
    t, s = polyharmonic_signal(A_list=[1, 0.5, 0.3], T=2, T_N=10)
    plt.subplot(6, 2, 2)
    plt.plot(t, s)
    plt.title("Полигармонический сигнал")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    # Однополярные импульсы
    t, s = unipolar_pulses(T=1, n=5, T_N=10, delta_t=0.01)
    plt.subplot(6, 2, 3)
    plt.step(t, s, where='post')
    plt.title("Однополярные импульсы")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    # Разнополярные импульсы
    t, s = bipolar_pulses(T=1, n=5, T_N=10, delta_t=0.01)
    plt.subplot(6, 2, 4)
    plt.step(t, s, where='post')
    plt.title("Разнополярные импульсы")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    # Затухающая синусоида
    t, s = damped_sine_wave(A=1, alpha=0.5, f=2, T_N=10, delta_t=0.01)
    plt.subplot(6, 2, 5)
    plt.plot(t, s)
    plt.title("Затухающая синусоида")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    # Одиночный импульс
    t, s = single_pulse(T=2, T_N=10, delta_t=0.01)
    plt.subplot(6, 2, 6)
    plt.step(t, s, where='post')
    plt.title("Одиночный импульс")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    # Одиночный прямоугольный импульс
    t, s = single_rectangular_pulse(A=1, T=2, T_N=10, delta_t=0.01)
    plt.subplot(6, 2, 7)
    plt.plot(t, s)
    plt.title("Одиночный прямоугольный импульс")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    # Одиночный экспоненциальный импульс
    t, s = single_exponential_pulse(A=1, beta=1, T_N=10, delta_t=0.01)
    plt.subplot(6, 2, 8)
    plt.plot(t, s)
    plt.title("Одиночный экспоненциальный импульс")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    # Единичный скачок
    t, s = unit_step(T=5, T_N=10, delta_t=0.01)
    plt.subplot(6, 2, 9)
    plt.step(t, s, where='post')
    plt.title("Единичный скачок")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    # Дельта-функция
    t, s = delta_function(A=1, T=5, T_N=10, delta_t=0.01)
    plt.subplot(6, 2, 10)
    plt.stem(t, s, basefmt=" ")
    plt.title("Дельта-функция")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    # Треугольный сигнал
    t, s = triangular_signal(A=1, T=2, T_N=10, delta_t=0.01)
    plt.subplot(6, 2, 11)
    plt.plot(t, s)
    plt.title("Треугольный сигнал")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")

    plt.tight_layout()
    plt.show()
