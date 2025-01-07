import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# функция генерации синусоидального сигнала
def generate_harmonic(frequency, duration, step):
    t = np.arange(0.0, duration, step)
    signal = np.sin(2 * np.pi * frequency * t)
    return t, signal

# функция генерации полигармонического сигнала
def generate_poliharmonic(frequencies, duration, points):
    t = np.arange(0.0, duration, step)
    signal = sum(np.sin(2 * np.pi * f * t) for f in frequencies)
    return t, signal

# основная часть 
st.title('Временное и частотное представление сигналов')
# ввод параметров
signal_type = st.selectbox('Тип сигнала', ('Периодический', 'Апериодический', 'Специальный'))
# сигналы
if signal_type == 'Периодический':
    signal_kind = st.selectbox('Вид сигнала', ('Гармонический', 'Полигармонический', 'Однополярные импульсы', 'Разнополярные импульсы'))
    
    if signal_kind == 'Гармонический':
        period = st.number_input('Период 0,628 <= T <= 6,28 (с)', min_value = 0.628, max_value = 6.28, value = 0.628, step = 0.001, format = "%0.3f")
        duration = st.selectbox('Интервал задания сигнала (с)', ('1,2 * T', '20 * T'))
        step = st.number_input('Шаг дискретизации 0,001 <= Δt <= 1,0 (c)', min_value = 0.001, max_value = 1.0, value = 0.01, step = 0.001, format = "%0.3f")
        frequency = 1 / period
        if duration == '1,2 * T': duration = round(1.2 * period, 3)
        else: duration = 20 * period
        points = math.floor(duration / step) + 1
        t, signal = generate_harmonic(frequency, duration + step, step)
        
    elif signal_kind == 'Полигармонический':
        frequencies = st.text_input('Частоты гармоник через "; "', '1; 2; 3')
        frequencies = list(map(float, frequencies.split('; '))) # + обработать ввод
        duration = st.number_input('Интервал задания сигнала (с)', min_value = 0.001, max_value = 10.0, value = 2.0, step = 0.001, format = "%0.3f")
        step = st.number_input('Шаг дискретизации 0,001 <= Δt <= 1,0 (c)', min_value = 0.001, max_value = 1.0, value = 0.01, step = 0.001, format = "%0.3f")
        points = math.floor(duration / step) + 1
        t, signal = generate_poliharmonic(frequencies, duration + step, points) 
           
    # график сигнала
    if st.button('Выполнить формирование сигнала'):
        st.write(f'Количество точек = {points}')
        plt.figure(figsize = (14, 8))
        plt.plot(t, signal)
        plt.title('Вид сигнала\n')
        plt.xlabel('\nВремя (с)')
        plt.ylabel('Амплитуда')
        plt.grid()
        st.pyplot(plt)

elif signal_type == 'Апериодический':
    signal_kind = st.selectbox('Вид сигнала', ('Затухающая синусоида'))

else: # Специальный
    signal_kind = st.selectbox('Вид сигнала', ('Одиночный импульс', 'Единичный скачок', 'Дельта-функция'))
