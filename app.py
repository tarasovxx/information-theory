import io

import streamlit as st
import numpy as np
import math
import plotly.graph_objects as go
import plotly.io as pio
import signal_noise_generator  # модуль генерации сигналов у Артема и Саши
from signal_noise_generator.signal_generator.signals import single_pulse, unit_step, delta_function
import base64
from PIL import Image


# добавление кнопок
if 'button_2' not in st.session_state: st.session_state.button_1 = False  # Выполнить формирование сигнала

if 'button_2' not in st.session_state: st.session_state.button_2 = False  # Спектр сигнала

if 'image_count' not in st.session_state: st.session_state.image_count = 1


# функции включения и отключения нажатия кнопок
def buttons_off():
    st.session_state.button_1 = False
    st.session_state.button_2 = False


def button_1_on(): st.session_state.button_1 = True


def button_1_off(): st.session_state.button_1 = False


def button_2_on(): st.session_state.button_2 = True


def button_2_off(): st.session_state.button_2 = False


# def single_pulse(T, T_N, delta_t):
#    t = np.arange(0, T_N, delta_t)
#    s = np.zeros_like(t)
#    s[t < T] = 1
#    return t, s

# def delta_function(A, T, T_N, delta_t):
#    t = np.arange(0, T_N, delta_t)
#    s = np.zeros_like(t)
#   s[np.abs(t - T) < delta_t / 2] = A
#    return t, s

# def unit_step(T, T_N, delta_t):
#    t = np.arange(0, T_N, delta_t)
#    s = np.zeros_like(t)
#    s[t >= T] = 1
#    return t, s

# импульсы
def generate_unipolar_pulses(signal_duration, pulse_duration, step):
    t = np.arange(0.0, signal_duration, step)
    signal = np.zeros_like(t)
    for pulse_num in range(int(signal_duration / pulse_duration)):
        start = int(pulse_num * pulse_duration / step)
        end = int(start + pulse_duration / 2 / step)
        signal[start:end] = 1
    return t, signal


def generate_bipolar_pulses(signal_duration, pulse_duration, step):
    t = np.arange(0.0, signal_duration, step)
    signal = np.empty_like(t)
    for pulse_num in range(int(signal_duration / pulse_duration)):
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


# основная часть
st.markdown('## Временное и частотное представление сигналов')
# ввод параметров
signal_type = st.selectbox('Тип сигнала', ('Периодический', 'Апериодический', 'Специальный'), on_change=buttons_off)
# сигналы
signal = [0];
t = [0];
points = 0
if signal_type == 'Периодический':
    signal_kind = st.selectbox('Вид сигнала', (
    'Гармонический', 'Полигармонический', 'Однополярные импульсы', 'Разнополярные импульсы'), on_change=buttons_off)

    if signal_kind == 'Гармонический':
        period = st.number_input('Период 0,628 ≤ T ≤ 6,28 (с)', min_value=0.628, max_value=6.28, value=0.628,
                                 step=0.001, format="%0.3f")
        duration = st.selectbox('Интервал задания сигнала (с)', ('1,2 * T', '10 * T'))
        if duration == '1,2 * T':
            duration = round(1.2 * period, 3)
        else:
            duration = 10 * period
        step = st.number_input('Шаг дискретизации 0,001 ≤ Δt ≤ 2,0 (c)', min_value=0.001, max_value=2.0,
                               value=round(period / 62.8, 3), step=0.001, format="%0.3f")
        shift = st.number_input('Фазовый сдвиг 0,0 ≤ phi ≤ 6,28 (рад)', min_value=0.0, max_value=6.28, value=0.0,
                                step=0.01, format="%0.2f")
        frequency = round(1 / period, 3)
        y_tick = 0.2;
        x_tick = round(duration / 12, 1)
        t, signal = generate_harmonic(frequency, duration, step, shift)
        points = len(signal)

    elif signal_kind == 'Полигармонический':
        st.write('Количество гармоник 1 ≤ KG ≤ 7')
        frequencies = st.text_input('Частоты гармоник через " ;"', '1; 2; 3')
        frequencies = frequencies.replace(',', '.')
        try:
            frequencies = list(map(float, frequencies.split(';')))
            if (len(frequencies) < 8):
                duration = st.number_input('Интервал задания сигнала 0,001 ≤ TN ≤ 10 (с)', min_value=0.001,
                                           max_value=10.0, value=1.2, step=0.001, format="%0.3f")
                step = st.number_input('Шаг дискретизации 0,001 ≤ Δt ≤ 2,0 (c)', min_value=0.001, max_value=2.0,
                                       value=round((1 / min(frequencies)) / 62.8, 3), step=0.001, format="%0.3f")
                y_tick = 0.5;
                x_tick = round(duration / 12, 1)
                t, signal = generate_poliharmonic(frequencies, duration, step)
                points = len(signal)
            else:
                st.warning('Количество гармоник превышает 7')
                frequencies = [0]
        except Exception as e:
            st.warning('Ошибка ввода параметров')
            frequencies = [0]

    elif signal_kind == 'Однополярные импульсы' or signal_kind == 'Разнополярные импульсы':
        pulses_count = st.number_input('Количество импульсов в последовательности 3 ≤ KG ≤ 7', min_value=3, max_value=7,
                                       value=3, step=1, format="%d")
        pulse_duration = st.number_input('Длительность импульса 0,628 ≤ T ≤ 6,28 (с)', min_value=0.628, max_value=6.28,
                                         value=0.628, step=0.001, format="%0.3f")
        signal_interval = st.selectbox('Интервал задания сигнала (с)', ('KG * T', '5 * KG * T'))
        step = st.number_input('Шаг дискретизации 0,001 ≤ Δt ≤ 2,0 (c)', min_value=0.001, max_value=2.0, value=0.030,
                               step=0.001, format="%0.3f")

        signal_duration = pulse_duration * pulses_count;
        if signal_interval == '5 * KG * T': signal_duration *= 5
        if signal_kind == 'Однополярные импульсы':
            t, signal = generate_unipolar_pulses(signal_duration, pulse_duration, step)
        else:
            t, signal = generate_bipolar_pulses(signal_duration, pulse_duration, step)
        y_tick = 0.2;
        x_tick = round(signal_duration / 12, 1)
        points = len(signal)

elif signal_type == 'Апериодический':
    signal_kind = st.selectbox('Вид сигнала', ('Затухающая синусоида'), on_change=buttons_off)

else:  # cпециальный
    signal_kind = st.selectbox('Вид сигнала', ('Одиночный импульс', 'Единичный скачок', 'Дельта-функция'),
                               on_change=buttons_off)
    if signal_kind == 'Одиночный импульс':
        duration = st.number_input('Длительность импульса 1,57 ≤ T ≤ 6,28 (с)', min_value=1.57, max_value=6.28,
                                   value=1.57,
                                   step=0.01, format="%0.2f")
        interval = st.selectbox('Интервал задания сигнала (с)', ('1,2 * T', '10 * T'))
        step = st.number_input('Шаг дискретизации 0,001 ≤ Δt ≤ 2,0 (c)', min_value=0.001, max_value=2.0,
                               value=round(duration / 62.8, 3),
                               step=0.001, format="%0.3f")
        if interval == '1,2 * T':
            interval = round(1.2 * duration, 3)
        else:
            interval = 10 * duration
        y_tick = 0.1;
        x_tick = round(interval / 10, 1)
        t, signal = single_pulse(duration, interval, step)
        points = len(signal)
    elif signal_kind == 'Единичный скачок':
        moment = st.number_input('Момент скачка 1 <= T <= 20 (c)', min_value=1, max_value=20, value=2, step=1,
                                 format="%d")
        step = st.number_input('Шаг дискретизации 0,001 ≤ Δt ≤ 2,0 (c)', min_value=0.001, max_value=2.0,
                               value=0.050,
                               step=0.001, format="%0.3f")
        y_tick = 1;
        x_tick = round(moment / 20, 1)
        t, signal = unit_step(0, moment + 0.001, step)
        points = len(signal)
    else:
        amplitude = st.selectbox('Амплитуда',
                                 ('1000', '2000', '3000', '4000', '5000', '6000', '7000', '8000', '9000', '10000'))
        moment = st.selectbox('Момент скачка (c)', ('0,01', '0,1'))
        duration = st.selectbox('Интервал задания сигнала (с)', ('1,2 * T', '10 * T'))
        step = st.number_input('Шаг дискретизации 0,001 ≤ Δt ≤ 2,0 (c)', min_value=0.001, max_value=2.0,
                               value=0.001,
                               step=0.001, format="%0.3f")
        if moment == '0,01':
            moment = 0.01
        else:
            moment = 0.1
        if duration == '1,2 * T':
            duration = 1.2 * moment
        else:
            duration = 10 * moment
        y_tick = 1000;
        x_tick = round(duration / 20, 1)
        t, signal = delta_function(amplitude, moment, duration + 0.001, step)
        points = len(signal)

# формирование сигнала
st.button('Выполнить формирование сигнала', on_click=button_1_on)
if st.session_state.button_1:  # кнопка нажата
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=signal, mode='lines'))
    fig.update_layout(title='Вид сигнала\n', title_x=0.49, margin=dict(l=15, r=30, t=60, b=20), template='plotly',
                      width=1200, height=500)
    fig.update_xaxes(title_text='Время (c)', showgrid=True, title_font_color='black', linecolor='black', dtick=x_tick,
                     mirror=True)
    fig.update_yaxes(title_text='Амплитуда', showgrid=True, title_font=dict(color='black'), linecolor='black',
                     dtick=y_tick, mirror=True)
    # сохранение и копирование
    print_points, save, copy = st.columns([8, 1, 1])
    print_points.write(f'Количество точек = {points}')
    with save:
        image = pio.to_image(fig, format='jpg', width=1050, height=675)
        if st.download_button(label='', icon=':material/download:', data=image,
                              file_name=f'График_сигнала_{st.session_state.image_count}.jpg'):
            st.session_state.image_count += 1
    with copy:
        st.button(label='', icon=":material/file_copy:")
        # write_p.success('График скопирован')

    # график сигнала
    # fig.show()
    # st.plotly_chart(fig)
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

    # спектры
    st.button('Спектр сигнала', on_click=button_2_on)
    if st.session_state.button_2:
        bpf_select = st.selectbox('Число БПФ', ('128', '256', '256', '512', '1024', '2048', '4096'), index=4)
        bpf = int(bpf_select)
        spectrum = None
        # FFT сигнала
        # if bpf > points: fft_signal = np.pad(signal, (0, bpf - points), mode = 'constant') # дозаполнение отчетов '0'
        # else: fft_signal = signal[:bpf]
        # fft_val = np.fft.fft(fft_signal, n = bpf)
        fft_val = np.fft.fft(signal, n=bpf)
        fft_freq = np.fft.fftfreq(bpf, step)
        indexes = (fft_freq >= 0)  # только неотрицательные частоты
        fft_val = fft_val[indexes]
        fft_freq = fft_freq[indexes]
        fft_freq = fft_freq * 2 * np.pi  # перевод в рад/с
        spectrum = st.radio('**Спектры:**', ['Вещественный', 'Мнимый', 'Комплексный', 'Амплитудный', 'Фазовый'],
                            index=None)
        if spectrum == 'Вещественный':
            y_val = np.real(fft_val)
        else:  # elif spectrum == 'Мнимый':
            y_val = np.imag(fft_val)
            # график спектра
        if spectrum != None:
            fig_1 = go.Figure()
            fig_1.add_trace(go.Scatter(x=fft_freq, y=y_val, mode='lines'))
            fig_1.update_layout(title=f'{spectrum} спектр\n', title_x=0.45, margin=dict(l=15, r=30, t=60, b=20),
                                template='ggplot2', width=1200, height=500)
            fig_1.update_xaxes(title_text='Частота (рад/c)', showgrid=True, title_font_color='black', linecolor='black',
                               mirror=True)
            fig_1.update_yaxes(showgrid=True, title_font=dict(color='black'), linecolor='black', mirror=True)
            # сохранение и копирование
            print_points_1, save_1, copy_1 = st.columns([8, 1, 1])
            print_points_1.write('')
            with save_1:
                image = pio.to_image(fig_1, format='jpg', width=1050, height=675)
                if st.download_button(label='', icon=':material/download:', data=image,
                                      file_name=f'{spectrum}_спектр_сигнала_{st.session_state.image_count}.jpg'):
                    st.session_state.image_count += 1
            with copy_1:
                st.button(label='', icon=":material/file_copy:", key='copy_1')
                # write_p.success('График скопирован')
            # fig_1.show()
            st.plotly_chart(fig_1)