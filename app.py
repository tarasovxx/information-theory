import streamlit as st
import numpy as np
import math
import plotly.graph_objects as go
import plotly.io as pio

# функции включения и отключения нажатия кнопок
def buttons_off():
    st.session_state.button_1 = False
    st.session_state.button_2 = False
    
def button_1_on():
    st.session_state.button_1 = True

def button_1_off():
    st.session_state.button_1 = False
    
def button_2_on():
    st.session_state.button_2 = True

def button_2_off():
    st.session_state.button_2 = False
    
def new_image(images):
    images += 1   
        
# функция генерации синусоидального сигнала
def generate_harmonic(frequency, duration, step, shift):
    t = np.arange(0.0, duration, step)
    if shift != 0: signal = np.sin(2 * np.pi * frequency * t + shift)
    else: signal = np.sin(2 * np.pi * frequency * t)
    return t, signal

# функция генерации полигармонического сигнала
def generate_poliharmonic(frequencies, duration, points):
    t = np.arange(0.0, duration, step)
    signal = sum(np.sin(2 * np.pi * f * t) for f in frequencies)
    return t, signal

# основная часть 
if 'button_1' not in st.session_state:
    st.session_state.button_1 = False
    
if 'button_2' not in st.session_state:
    st.session_state.button_2 = False

if 'image_count' not in st.session_state:
    st.session_state.image_count = 1
    
#st.title('Временное и частотное представление сигналов')
st.markdown('## Временное и частотное представление сигналов')
# ввод параметров
signal_type = st.selectbox('Тип сигнала', ('Периодический', 'Апериодический', 'Специальный'), on_change = buttons_off)
# сигналы    
signal = [0]; t = [0]; points = 0; flag = 0
if signal_type == 'Периодический':
    signal_kind = st.selectbox('Вид сигнала', ('Гармонический', 'Полигармонический', 'Однополярные импульсы', 'Разнополярные импульсы'), on_change = buttons_off)
    
    if signal_kind == 'Гармонический':
        period = st.number_input('Период 0,628 ≤ T ≤ 6,28 (с)', min_value = 0.628, max_value = 6.28, value = 0.628, step = 0.001, format = "%0.3f")
        duration = st.selectbox('Интервал задания сигнала (с)', ('1,2 * T', '10 * T'))
        step = st.number_input('Шаг дискретизации 0,001 ≤ Δt ≤ 2,0 (c)', min_value = 0.001, max_value = 2.0, value = 0.030, step = 0.001, format = "%0.3f")
        shift = st.number_input('Фазовый сдвиг 0,0 ≤ phi ≤ 6,28 (рад)', min_value = 0.0, max_value = 6.28, value = 0.0, step = 0.01, format = "%0.2f")
        frequency = round(1 / period, 3)
        if duration == '1,2 * T': duration = round(1.2 * period, 3)
        else: duration = 10 * period
        y_tick = 0.2; x_tick = round(duration / 12, 1)
        points = math.floor(duration / step) + 1
        t, signal = generate_harmonic(frequency, duration + step, step, shift)
        
    elif signal_kind == 'Полигармонический':
        frequencies = st.text_input('Частоты гармоник через ";"', '1; 2; 3')
        frequencies = frequencies.replace(',', '.')
        try: 
            frequencies = list(map(float, frequencies.split('; ')))            
            duration = st.number_input('Интервал задания сигнала 0,001 ≤ TN ≤ 10 (с)', min_value = 0.001, max_value = 10.0, value = 2.0, step = 0.001, format = "%0.3f")
            step = st.number_input('Шаг дискретизации 0,001 ≤ Δt ≤ 2,0 (c)', min_value = 0.001, max_value = 2.0, value = 0.030, step = 0.001, format = "%0.3f")
            points = math.floor(duration / step) + 1
            y_tick = 0.5; x_tick = round(duration / 12, 1)
            t, signal = generate_poliharmonic(frequencies, duration + step, points)  
        except Exception as e: 
            st.warning("Ошибка ввода параметров")
            frequencies = [0]  

elif signal_type == 'Апериодический':
    signal_kind = st.selectbox('Вид сигнала', ('Затухающая синусоида'), on_change = button_1_off)

else: # cпециальный
    signal_kind = st.selectbox('Вид сигнала', ('Одиночный импульс', 'Единичный скачок', 'Дельта-функция'), on_change = button_1_off)

# формирование сигнала             
st.button('Выполнить формирование сигнала', on_click = button_1_on)
if st.session_state.button_1: # кнопка нажата
    fig = go.Figure()  
    fig.add_trace(go.Scatter(x = t, y = signal, mode = 'lines'))
    fig.update_layout(title = 'Вид сигнала\n', title_x = 0.5, margin = dict(l=15, r=30, t=60, b=20), template = 'plotly', width = 1200, height = 500)
    fig.update_xaxes(title_text = 'Время (c)', showgrid = True, title_font_color = 'black', linecolor = 'black', dtick = x_tick, mirror = True)
    fig.update_yaxes(title_text = 'Амплитуда', showgrid = True, title_font = dict(color = 'black'), linecolor = 'black', dtick = y_tick, mirror = True)                           
    # сохранение и копирование
    write_p, save, copy = st.columns([8, 1, 1])  
    write_p.write(f'Количество точек = {points}')
    with save:
        if st.button(label = '', icon = ":material/download:", on_click = button_1_on):
            pio.write_image(fig, f"График_сигнала_{st.session_state.image_count}.jpg", format = 'jpg', width = 1050, height = 675)
            st.session_state.image_count += 1            
    with copy:
        st.button(label = '', icon = ":material/file_copy:", on_click = button_1_on)
            #write_p.success('График скопирован')
    # график сигнала     
    fig.show()
    st.plotly_chart(fig)                
    # спектры
    st.button('Спектр сигнала', on_click = button_2_on)
    if st.session_state.button_2:
        signal_type = st.selectbox('Число БПФ', ('128', '256', '256', '512', '1024', '2048', '4096'), index = 4, on_change = button_2_on)    
        spectrum = st.radio("**Спектры:**", ["Вещественный", "Мнимый", "Комплексный", "Амплитудный", "Фазовый"])
