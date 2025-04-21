import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

# Укажите путь к вашему CSV файлу
file_path = r'C:\Users\UserName\Desktop\raw_data\In_6.2_10_2 нагрева.csv'

# Проверка существования файла
if os.path.exists(file_path):
    try:
        # Импорт данных из CSV файла, пропуская первые 45 строк
        data = pd.read_csv(file_path, sep=',', encoding='utf-8', skiprows=45)

        # Удаляем столбцы и создаем копию
        columns_to_keep = [0, 1, 4]
        data_filtered = data.iloc[:, columns_to_keep].copy()  # Make a copy here

        # Переименовываем столбцы для удобства
        data_filtered.columns = ['Time', 'Temperature', 'DTA']  # Установите нужные названия

        # Выводим оставшиеся данные в терминал
        print("Оставшиеся данные:")
        print(data_filtered)

        # Сохранение оставшихся данных в новый CSV файл
        output_file_path = r'C:\Users\UserName\Desktop\Filtered_Data\output_Grapf_filtered.csv'  # Измените путь при необходимости
        data_filtered.to_csv(output_file_path, index=False)
        print(f"\nОставшиеся данные сохранены в файл: {output_file_path}")

        # Построение графика с полиномиальной линией тренда
        T_measured = np.array([156.83, 230.5, 267.76, 412.07, 651.6, 964.53, 1071.31])
        T_ref = np.array([156.7, 232.05, 271.4, 419.56, 660.0, 961.8, 1064.2])
        Difference = T_measured - T_ref

        plt.figure(figsize=(10, 6))
        plt.gca().xaxis.set_major_locator(AutoLocator())
        plt.gca().yaxis.set_major_locator(AutoLocator())

        plt.plot(T_measured, Difference, 'o', color='blue', label='Точки построения графика')
        plt.plot(T_measured, Difference, color='blue', label='Изменение температуры', linewidth=2)

        coefficients = np.polyfit(T_measured, Difference, 4)
        polynomial = np.poly1d(coefficients)
        y_fit = polynomial(T_measured)

        plt.plot(T_measured, y_fit, color='red', linestyle='--', label='Полиномиальная линия тренда')

        plt.xlabel('T_measured, ℃')
        plt.ylabel('Difference, ℃')
        plt.title('График с полиномиальной линией тренда')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Параметры сглаживания для температуры
        window_length = 51  # Длина окна (должна быть нечетной)
        polyorder = 3       # Степень полинома

        # Применение Savitzky-Golay фильтра для сглаживания температуры с использованием .loc
        data_filtered.loc[:, 'Temperature_Smooth'] = savgol_filter(data_filtered['Temperature'], window_length=window_length, polyorder=polyorder)

        # Поиск отрицательных пиков в DTA ниже -3
        peaks, properties = find_peaks(-data_filtered['DTA'], height=3)

        if len(peaks) > 0:
            last_peak_index = peaks[-1]  # Индекс последнего отрицательного пика
            last_peak_time = data_filtered['Time'].iloc[last_peak_index]
            last_peak_value = data_filtered['DTA'].iloc[last_peak_index]
            print(f"Последний отрицательный пик DTA ниже -3: Время: {last_peak_time}, Значение: {last_peak_value}")

            # Вычисление первой производной DTA с использованием .loc
            data_filtered.loc[:, 'DTA_Derivative'] = np.gradient(data_filtered['DTA'])

            # Определение границ пика
            left_boundary_index = np.where(data_filtered['DTA_Derivative'][:last_peak_index] > 0)[0][-1] if np.any(data_filtered['DTA_Derivative'][:last_peak_index] > 0) else 0
            right_boundary_index = np.where(data_filtered['DTA_Derivative'][last_peak_index:] < 0)[0][0] + last_peak_index if np.any(data_filtered['DTA_Derivative'][last_peak_index:] < 0) else len(data_filtered) - 1
            
            left_boundary_time = data_filtered['Time'].iloc[left_boundary_index]
            right_boundary_time = data_filtered['Time'].iloc[right_boundary_index]
            
            print(f"Границы пика: Слева: {left_boundary_time}, Справа: {right_boundary_time}")

            ### Построение графика с максимальным размером для первого графика ###
            plt.figure(figsize=(18, 9.5))  # Увеличиваем размер графика
            
            ax1 = plt.gca()  # Получаем текущую ось
            
            ax1.scatter(data_filtered['Time'], data_filtered['DTA'], marker='.', color='b', alpha=0.5, s=2, label='DTA')  
            ax1.plot(data_filtered['Time'], data_filtered['DTA'], color='b', linewidth=1)  
            
            ax1.plot(last_peak_time, last_peak_value, 'ro', markersize=10, label='Последний пик')  
            
            ax1.axvline(x=left_boundary_time, color='green', linestyle='--', label='Левая граница')
            ax1.axvline(x=right_boundary_time, color='orange', linestyle='--', label='Правая граница')
            
            ax1.set_xlabel('Время (Сек.)', fontsize=16)
            ax1.set_ylabel('DTA', fontsize=16, color='b')
            ax1.tick_params(axis='y', labelcolor='b')
            
            ax2 = ax1.twinx()  
            
            ax2.plot(data_filtered['Time'], data_filtered['Temperature_Smooth'], color='r', linewidth=1)  
            
            ax2.set_ylabel('Температура (°C)', fontsize=16, color='r')
            ax2.tick_params(axis='y', labelcolor='r')

            plt.title('График зависимости DTA и Сглаженной Температуры от времени', fontsize=20)
            
            ax1.grid(True)
            
            plt.legend()  
            
            plt.show()

            ### Создание второго графика ###
            
            peak_data = data_filtered.iloc[left_boundary_index:right_boundary_index + 1]

            plt.figure(figsize=(18, 9.5))  
            
            plt.plot(peak_data['Temperature_Smooth'], peak_data['DTA'], color='purple', linewidth=2)

            ### Определение базовой линии и касательных ###
            
            base_level = np.mean(data_filtered['DTA'][:left_boundary_index])  # Базовая линия перед пиком
            
            # Найдем производные в границах пика для касательных
            slope_left = peak_data['DTA_Derivative'].iloc[0]   # Наклон на левой границе пика
            slope_right = peak_data['DTA_Derivative'].iloc[-1] # Наклон на правой границе пика
            
            x_left = peak_data['Temperature_Smooth'].iloc[0]   # Температура на левой границе пика
            x_right = peak_data['Temperature_Smooth'].iloc[-1]  # Температура на правой границе пика
            
            # Касательная слева (y - base_level)
            y_left_func = lambda x: slope_left * (x - x_left) + peak_data['DTA'].iloc[0]
            
            # Касательная справа (y - base_level)г
            y_right_func = lambda x: slope_right * (x - x_right) + peak_data['DTA'].iloc[-1]
            
            # Определяем диапазон для построения касательных
            temp_range = np.linspace(peak_data['Temperature_Smooth'].min(), peak_data['Temperature_Smooth'].max(), num=100)
            
            left_tangent_values = y_left_func(temp_range)
            right_tangent_values = y_right_func(temp_range)

            plt.plot(temp_range, left_tangent_values, color='orange', linestyle='--', label='Касательная слева')
            plt.plot(temp_range, right_tangent_values, color='green', linestyle='--', label='Касательная справа')

            ### Находим точку пересечения касательных ###
            
            intersection_xs = np.linspace(peak_data['Temperature_Smooth'].min(), peak_data['Temperature_Smooth'].max(), num=100)
            
            intersection_ys_left = y_left_func(intersection_xs)
            intersection_ys_right = y_right_func(intersection_xs)

            intersection_points_x = []
            intersection_points_y = []

            for i in range(len(intersection_xs) - 1):
                if (intersection_ys_left[i] - intersection_ys_right[i]) * (intersection_ys_left[i + 1] - intersection_ys_right[i + 1]) < 0:
                    intersection_xs_val = (intersection_xs[i] + intersection_xs[i + 1]) / 2
                    intersection_ys_val = y_left_func(intersection_xs_val)
                    intersection_points_x.append(intersection_xs_val)
                    intersection_points_y.append(intersection_ys_val)

                    plt.plot(intersection_xs_val, intersection_ys_val, 'ro', markersize=8, label='Температурный онсет')

                    break

                if len(intersection_points_x) > 0:
                    break
            
            plt.xlabel('Сглаженная Температура (°C)', fontsize=16)
            plt.ylabel('DTA', fontsize=16)
            
            plt.title('График зависимости DTA от Сглаженной Температуры с температурным онсетом', fontsize=20)
            
            plt.legend()
            
            plt.grid(True)
            
            plt.show()

    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
else:
    print("Файл не найден. Проверьте путь к файлу.")