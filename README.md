# Thermal_Onset_Auto_En

This is a one if the first alpha version of this software. Basically what it starts from and the only version I can post legally.

Automation of raw thermogravimetric data processing from .csv files and collected melting temperatures of metal standards obtained from laboratory thermal analyzers (specifically Chinese models with inconvenient/missing software). The script automatically extracts required data for calculations, manages folder paths defined in code, performs filtering, smoothing, identifies DTA peaks and temperature onset points, and generates clear visualizations.

## Key Features

- Processing raw .csv files exported from thermal analyzers
- Automatic extraction and renaming of required columns for calculations
- Temperature data smoothing using Savitzky-Golay filter
- Automatic DTA peak detection
- Temperature onset determination via tangent intersection method
- Automated folder handling for input/output data (paths defined in code)
- Export of processed data to new .csv files
- Results visualization with essential dependency plots

## Example Input/Output Files

- Repository contains test input file:  
  `In_6.2 mg_RT-172 deg_10 oC-min_koeff 0-1_argon_DTA 25 uV_TG 10 mg.csv`  
  Example raw data for test runs and input format demonstration.
- First two sample plots (`Figure_1.png`, `Figure_2.png`) demonstrate script output:

![Figure_1](https://github.com/user-attachments/assets/7c968356-6f94-4004-889b-9af01bc35949)

![Figure_2](https://github.com/user-attachments/assets/15e8a2cf-a9eb-4ef9-9483-dd622f98a07b)

## Quick Start

1. Install dependencies:
    ```bash
    pip install pandas numpy matplotlib scipy
    ```
2. Download `Auto_Thermal_Onset.py` to your working directory
3. Specify your .csv file path in the script's `file_path` variable and output path in `output_file_path`
4. Input your actual measured melting temperatures in `T_measured` and corresponding standard reference temperatures in `T_ref`
5. Run script:
    ```bash
    python Auto_Thermal_Onset.py
    ```
6. Review results in terminal and generated plots

# Replace file paths in script with your preferred locations:
file_path = r'C:\Users\UserName\Desktop\raw_data\In_6.2 mg_RT-172 deg_10 oC-min_koeff 0-1_argon_DTA 25 uV_TG 10 mg.csv'
output_file_path = r'C:\Users\UserName\Desktop\Filtered_Data\output_Grapf_filtered.csv'
# Insert your measured melting temperatures and corresponding reference standard temperatures (default testing set shown):
T_measured = np.array([156.83, 230.5, 267.76, 412.07, 651.6, 964.53, 1071.31])
T_ref = np.array([156.7, 232.05, 271.4, 419.56, 660.0, 961.8, 1064.2])



# Thermal_Onset_Auto

Это одна из самых ранних альфа версий, с чего вся разработка и начиналась. Эта версия, которую я могу легально опубликовать.

Автоматизация обработки сырых данных термоанализа из .csv-файлов и собранных температур плавления металлов-стандартов, полученных с лабораторных термоанализаторов (в частности китайских моделей с неудобным, отсутствующим ПО). Скрипт автоматически извлекает необходимые данные для расчетов, манипулирует указанными в коде папками, выполняет фильтрацию, сглаживание, определяет пик и температурный онсет, а также строит наглядные графики.

## Основные возможности

- Работа с сырыми .csv-файлами, экспортированными с термоанализатора
- Автоматическое выделение нужных столбцов и переименование для расчетов
- Сглаживание температурных данных с помощью фильтра Савицкого-Голея
- Автоматический поиск пика DTA
- Определение температурного онсета через пересечение касательных
- Автоматическая работа с папками для входных и выходных данных (пути указываются в коде)
- Экспорт обработанных данных в новый .csv-файл
- Визуализация результатов с построением основных графиков зависимостей

## Пример входных и выходных файлов

- В репозитории присутствует тестовый входной файл:  
  `In_6.2 mg_RT-172 deg_10 oC-min_koeff 0-1_argon_DTA 25 uV_TG 10 mg.csv`  
  Это пример сырых данных для пробных запусков и демонстрации формата входных файлов.
- Для наглядности приложены первые два графика (`Figure_1.png`, `Figure_2.png`), чтобы показать, как выглядит результат работы скрипта.

![Figure_1](https://github.com/user-attachments/assets/7c968356-6f94-4004-889b-9af01bc35949)

![Figure_2](https://github.com/user-attachments/assets/15e8a2cf-a9eb-4ef9-9483-dd622f98a07b)

## Быстрый старт

1. Установите зависимости:
    ```bash
    pip install pandas numpy matplotlib scipy
    ```
2. Скачайте скрипт `Auto_Thermal_Onset.py` и поместите его в рабочую папку
3. Укажите путь к вашему .csv-файлу в переменной `file_path` внутри скрипта и путь к выходному рабочему файлу `output_file_path`
4. Внесите в `T_measured` ваши фактические температуры плавления и в `T_ref` соответствующие им температуры по стандарту
5. Запустите скрипт:
    ```bash
    python Auto_Thermal_Onset.py
    ```
6. Ознакомьтесь с результатами в терминале и графиками

# В скрипте замените пути к файлам на удобные для вас:
file_path = r'C:\Users\UserName\Desktop\raw_data\In_6.2 mg_RT-172 deg_10 oC-min_koeff 0-1_argon_DTA 25 uV_TG 10 mg.csv'
output_file_path = r'C:\Users\UserName\Desktop\Filtered_Data\output_Grapf_filtered.csv'
# Вставьте свои температуры плавления и соответствующие им температуры по стандарту, дефолтно указан стандартный набор тестирования в T_ref:
T_measured = np.array([156.83, 230.5, 267.76, 412.07, 651.6, 964.53, 1071.31])
T_ref = np.array([156.7, 232.05, 271.4, 419.56, 660.0, 961.8, 1064.2])
