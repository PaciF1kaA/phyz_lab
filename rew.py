import re
import sys
import base64
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ STREAMLIT И АДАПТИВНЫЕ СТИЛИ
# =====================================================================
st.set_page_config(
    page_title="Физическая лаборатория: Термо-ЭДС и Эффект Зеебека",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Адаптивные стили для исключения горизонтального переполнения графиков на смартфонах (320–430 px)
st.markdown(
    """
    <style>
        .stPlotlyChart, .js-plotly-plot, .plot-container {
            max-width: 100% !important;
            overflow-x: hidden !important;
        }
        @media (max-width: 640px) {
            .block-container {
                padding-left: 0.65rem !important;
                padding-right: 0.65rem !important;
            }
            .stPlotlyChart {
                margin-left: 0 !important;
                margin-right: 0 !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================================
# 2. СПРАВОЧНЫЕ ТАБЛИЦЫ НСХ ТЕРМОПАР И БАЗА МЕТАЛЛОВ (С ПАСПОРТАМИ ДАННЫХ)
# =====================================================================

# 2.1. ТЖК (тип J, железо / константан), диапазон -210 ... 1200 °C, шаг 10 °C (142 точки)
TJK_TEMPS = np.arange(-210, 1210, 10, dtype=float)
TJK_MV = np.array([
    # -210 ... 150 °C
    -8.095, -7.890, -7.659, -7.403, -7.123, -6.821, -6.500, -6.159, -5.801, -5.426,
    -5.037, -4.633, -4.215, -3.786, -3.344, -2.893, -2.431, -1.961, -1.482, -0.995,
    -0.501,  0.000,  0.507,  1.019,  1.537,  2.059,  2.585,  3.116,  3.650,  4.187,
     4.726,  5.269,  5.814,  6.360,  6.909,  7.459,  8.010,
    # 160 ... 610 °C
     8.562,  9.115,  9.669, 10.224, 10.779, 11.334, 11.889, 12.445, 13.000, 13.555,
    14.110, 14.665, 15.219, 15.773, 16.327, 16.881, 17.434, 17.986, 18.538, 19.090,
    19.642, 20.194, 20.745, 21.297, 21.848, 22.400, 22.952, 23.504, 24.057, 24.610,
    25.164, 25.720, 26.276, 26.834, 27.393, 27.953, 28.516, 29.080, 29.647, 30.216,
    30.788, 31.362, 31.939, 32.519, 33.102, 33.689,
    # 620 ... 1070 °C
    34.279, 34.873, 35.470, 36.071, 36.675, 37.284, 37.896, 38.512, 39.132, 39.755,
    40.382, 41.012, 41.645, 42.281, 42.919, 43.559, 44.203, 44.848, 45.494, 46.141,
    46.786, 47.431, 48.074, 48.715, 49.353, 49.989, 50.622, 51.251, 51.877, 52.500,
    53.119, 53.735, 54.347, 54.956, 55.561, 56.164, 56.763, 57.360, 57.953, 58.545,
    59.134, 59.721, 60.307, 60.890, 61.473, 62.054,
    # 1080 ... 1200 °C
    62.634, 63.214, 63.792, 64.370, 64.948, 65.525, 66.102, 66.679, 67.255, 67.831,
    68.406, 68.980, 69.553
])

# 2.2. ТХА (тип K, хромель / алюмель), диапазон выборки -200 ... 1320 °C (56 точек из таблицы КИП-Сервис)
THA_TEMPS = np.concatenate([
    np.arange(-200, 550, 50, dtype=float),
    np.arange(520, 1340, 20, dtype=float)
])
THA_MV = np.array([
    # -200 ... 500 °C (шаг 50 °C)
    -5.891, -4.913, -3.554, -1.889,  0.000,  2.023,  4.096,  6.138,  8.138, 10.153,
    12.209, 14.293, 16.397, 18.516, 20.644,
    # 520 ... 700 °C (шаг 20 °C)
    21.497, 22.350, 23.203, 24.055, 24.905, 25.755, 26.602, 27.447, 28.289, 29.129,
    # 720 ... 900 °C (шаг 20 °C)
    29.965, 30.798, 31.628, 32.453, 33.275, 34.093, 34.908, 35.718, 36.524, 37.326,
    # 920 ... 1100 °C (шаг 20 °C)
    38.122, 38.918, 39.708, 40.494, 41.276, 42.053, 42.826, 43.595, 44.359, 45.119,
    # 1120 ... 1320 °C (шаг 20 °C)
    45.873, 46.623, 47.367, 48.105, 48.838, 49.565, 50.286, 51.000, 51.708, 52.410,
    53.106
])

# 2.3. ТХК (тип L, хромель / копель), диапазон -200 ... 800 °C, шаг 10 °C (101 точка из таблицы КИП-Сервис)
THK_TEMPS = np.arange(-200, 810, 10, dtype=float)
THK_MV = np.array([
    # -200 ... -110 °C
    -9.488, -9.203, -8.894, -8.562, -8.207, -7.831, -7.433, -7.014, -6.575, -6.118,
    # -100 ... -10 °C
    -5.641, -5.147, -4.636, -4.108, -3.564, -3.005, -2.431, -1.843, -1.242, -0.627,
    # 0 ... 90 °C
     0.000,  0.639,  1.290,  1.951,  2.624,  3.306,  3.999,  4.701,  5.413,  6.133,
    # 100 ... 190 °C
     6.862,  7.599,  8.344,  9.096,  9.857, 10.624, 11.398, 12.179, 12.967, 13.761,
    # 200 ... 290 °C
    14.560, 15.366, 16.177, 16.994, 17.818, 18.642, 19.474, 20.310, 21.150, 21.995,
    # 300 ... 390 °C
    22.843, 23.695, 24.550, 25.409, 26.271, 27.135, 28.002, 28.872, 29.743, 30.617,
    # 400 ... 490 °C
    31.492, 32.369, 33.247, 34.126, 35.007, 35.888, 36.769, 37.652, 38.534, 39.417,
    # 500 ... 590 °C
    40.299, 41.182, 42.064, 42.946, 43.828, 44.709, 45.590, 46.471, 47.350, 48.230,
    # 600 ... 690 °C
    49.108, 49.986, 50.864, 51.740, 52.617, 53.492, 54.367, 55.241, 56.114, 56.987,
    # 700 ... 800 °C
    57.859, 58.729, 59.599, 60.467, 61.333, 62.197, 63.058, 63.917, 64.771, 65.621,
    66.466
])

# Единый справочник расчётных табличных моделей термопар для Стенда №1
THERMOCOUPLES_DB = {
    "ТЖК (тип J, Железо-Константан, таблица с шагом 10 °C)": {
        "short_code": "J (ТЖК)",
        "temp_unit": "°C",
        "unit": "мВ",
        "min_t": -210,
        "max_t": 1200,
        "default_hot": 500,
        "temps": TJK_TEMPS,
        "values": TJK_MV,
        "grid_step": "Равномерный шаг 10 °C (142 узла, без пропусков)",
        "data_source": "Справочная таблица НСХ КИП-Сервис (kipia.pdf, выдержка на основе ГОСТ Р 8.585-2001)",
        "applicability": "Расчётная табличная модель в диапазоне −210…+1200 °C (на воздухе рабочий предел до 750 °C)",
        "color": "#80ed99",
        "electrodes": ("Железо (+)", "Константан (-)")
    },
    "ТХА (тип K, Хромель-Алюмель, справочная выборка 50/20 °C)": {
        "short_code": "K (ТХА)",
        "temp_unit": "°C",
        "unit": "мВ",
        "min_t": -200,
        "max_t": 1320,
        "default_hot": 500,
        "temps": THA_TEMPS,
        "values": THA_MV,
        "grid_step": "Неравномерный шаг: 50 °C (−200…500 °C) и 20 °C (520…1320 °C), всего 56 узлов",
        "data_source": "Сокращённая справочная выборка КИП-Сервис (по ГОСТ Р 8.585-2001 полный диапазон −270…+1372 °C)",
        "applicability": "Кусочно-линейная интерполяция по 56 узлам в диапазоне −200…+1320 °C (рабочий предел на воздухе до 1100–1200 °C)",
        "color": "#00b4d8",
        "electrodes": ("Хромель (+)", "Алюмель (-)")
    },
    "ТХК (тип L, Хромель-Копель, таблица с шагом 10 °C)": {
        "short_code": "L (ТХК)",
        "temp_unit": "°C",
        "unit": "мВ",
        "min_t": -200,
        "max_t": 800,
        "default_hot": 500,
        "temps": THK_TEMPS,
        "values": THK_MV,
        "grid_step": "Равномерный шаг 10 °C (101 узел, без пропусков)",
        "data_source": "Справочная таблица НСХ КИП-Сервис (выдержка на основе ГОСТ Р 8.585-2001)",
        "applicability": "Расчётная табличная модель в диапазоне −200…+800 °C",
        "color": "#f77f00",
        "electrodes": ("Хромель (+)", "Копель (-)")
    }
}

# База данных металлов и сплавов для Стенда №2 (приближённые коэффициенты при ~20 °C)
METALS_DB = {
    "Хромель (Ni90-Cr10)": {
        "seebeck": 24.0,
        "ref_temp": "≈ 20 °C (комнатная температура)",
        "color_hex": "#80ed99",
        "three_hex": "0x80ed99",
        "description": "Жаростойкий сплав никеля (90%) и хрома (10%), положительный термоэлектрод пар ТХА и ТХК."
    },
    "Железо (Fe)": {
        "seebeck": 16.0,
        "ref_temp": "≈ 20 °C (комнатная температура)",
        "color_hex": "#adb5bd",
        "three_hex": "0xadb5bd",
        "description": "Технически чистое железо, положительный электрод термопары ТЖК."
    },
    "Медь (Cu)": {
        "seebeck": 1.8,
        "ref_temp": "≈ 20 °C (комнатная температура)",
        "color_hex": "#f77f00",
        "three_hex": "0xf77f00",
        "description": "Электротехническая медь с малой абсолютной термо-ЭДС (в реферате указано около 2 мкВ/К)."
    },
    "Платина (Pt)": {
        "seebeck": -4.5,
        "ref_temp": "≈ 20 °C (комнатная температура)",
        "color_hex": "#e0e6ed",
        "three_hex": "0xe0e6ed",
        "description": "Благородный металл, используемый как эталон при построении термоэлектрических рядов."
    },
    "Алюмель (Ni95-Mn2-Al2-Si1)": {
        "seebeck": -17.0,
        "ref_temp": "≈ 20 °C (комнатная температура)",
        "color_hex": "#00b4d8",
        "three_hex": "0x00b4d8",
        "description": "Никелевый сплав, образующий с хромелем пару ТХА (при 20 °C S_пары ≈ 41 мкВ/°C)."
    },
    "Константан (Cu55-Ni45)": {
        "seebeck": -35.0,
        "ref_temp": "≈ 20 °C (комнатная температура)",
        "color_hex": "#e0aaff",
        "three_hex": "0xe0aaff",
        "description": "Медно-никелевый сплав, образующий с железом пару ТЖК (при 20 °C S_пары ≈ 51 мкВ/°C)."
    },
    "Копель (Cu56-Ni44-Mn)": {
        "seebeck": -40.5,
        "ref_temp": "≈ 20 °C (комнатная температура)",
        "color_hex": "#ff9f1c",
        "three_hex": "0xff9f1c",
        "description": "Термоэлектродный сплав, образующий с хромелем пару ТХК (при 20 °C S_пары ≈ 64.5 мкВ/°C)."
    }
}


def resolve_asset_path(rel_path: str) -> Path | None:
    """
    Находит путь к файлу из папки assets как при обычном запуске (локально или в Streamlit Cloud),
    так и внутри собранного через PyInstaller исполняемого файла (.exe, sys._MEIPASS).
    """
    search_roots = []
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        search_roots.append(Path(sys._MEIPASS))
    if "__file__" in globals():
        search_roots.append(Path(__file__).resolve().parent)
    search_roots.append(Path.cwd())

    filename = Path(rel_path).name
    for root in search_roots:
        for candidate in (root / rel_path, root / "assets" / filename, root / filename):
            if candidate.is_file():
                return candidate
    return None


def get_threejs_script_tags() -> str:
    """
    Проверяет наличие локальных копий three.min.js и OrbitControls.js по отдельности.
    Если локальный файл найден — встраивает его, иначе подключает внешний скрипт CDN.
    """
    local_three = resolve_asset_path("assets/three.min.js")
    local_orbit = resolve_asset_path("assets/OrbitControls.js")

    if local_three is not None:
        three_js_code = local_three.read_text(encoding="utf-8", errors="ignore")
        tag_three = f"<script>{three_js_code}</script>"
    else:
        tag_three = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'

    if local_orbit is not None:
        orbit_js_code = local_orbit.read_text(encoding="utf-8", errors="ignore")
        tag_orbit = f"<script>{orbit_js_code}</script>"
    else:
        tag_orbit = '<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>'

    return f"{tag_three}\n{tag_orbit}"


# =====================================================================
# 3. ФИЗИЧЕСКИЕ ФУНКЦИИ РАСЧЕТА ТЕРМО-ЭДС, КОЭФФИЦИЕНТА ЗЕЕБЕКА И ГРАФИКОВ
# =====================================================================
def calculate_nominal_emf(sensor_key: str, temp_c: float) -> float:
    """
    Возвращает табличное значение Термо-ЭДС E(T) при T_0 = 0 °C
    из встроенного массива выбранной термопары (с кусочно-линейной интерполяцией между узлами сетки).
    """
    spec = THERMOCOUPLES_DB[sensor_key]
    return float(np.interp(temp_c, spec["temps"], spec["values"]))


def calculate_seebeck_diff(sensor_key: str, temp_c: float) -> float:
    """
    Вычисляет дифференциальную термо-ЭДС S(T) = dE/dT в мкВ/°C
    методом центральной разности с шагом dt = 10 °C.
    """
    spec = THERMOCOUPLES_DB[sensor_key]
    dt = 10.0
    t_plus = min(float(spec["max_t"]), temp_c + dt)
    t_minus = max(float(spec["min_t"]), temp_c - dt)
    if t_plus == t_minus:
        return 0.0
    e_plus = calculate_nominal_emf(sensor_key, t_plus)
    e_minus = calculate_nominal_emf(sensor_key, t_minus)
    return float(((e_plus - e_minus) / (t_plus - t_minus)) * 1000.0)


def evaluate_circuit_physics(
    e_hot: float,
    e_cold: float,
    t_hot: float,
    t_cold: float,
    fault_mode: str,
    t_short_c: float | None = None,
    e_short: float | None = None,
    open_meter_mode: str = "Вторичный прибор с контролем обрыва (шунт входа)",
    r_cold_branch_ohm: float = 8.0,
    r_hot_loop_ohm: float = 7.0,
    r_bridge_ohm: float = 0.0,
    r_in_ohm: float = 1e6
) -> dict:
    """
    Физическая модель термоэлектрической цепи с независимыми сопротивлениями участков:
    - r_cold_branch_ohm (R_уч1): сопротивление проводов от холодного спая до точки КЗ, Ом;
    - r_hot_loop_ohm (R_уч2): сопротивление горячего участка от точки КЗ до рабочего спая, Ом;
    - r_bridge_ohm (R_кз): переходное сопротивление перемычки КЗ, Ом;
    - r_in_ohm (R_вх): входное сопротивление измерительного прибора, Ом.
    """
    r_total_tp_ohm = r_cold_branch_ohm + r_hot_loop_ohm
    e_generated_mv = e_hot - e_cold

    if fault_mode == "Норма":
        current_ua = (e_generated_mv * 1000.0) / (r_total_tp_ohm + r_in_ohm)
        u_meter_mv = e_generated_mv * (r_in_ohm / (r_total_tp_ohm + r_in_ohm))
        return {
            "circuit_state": f"Замкнута (исправна, R_тп = {r_total_tp_ohm:.1f} Ом)",
            "current_status": f"I = {current_ua:+.4f} мкА (термоток протекает)",
            "current_ua": current_ua,
            "i_loop_ma": 0.0,
            "e_gen_mv": e_generated_mv,
            "u_meter_mv": u_meter_mv,
            "u_meter_str": f"{u_meter_mv:+.3f} мВ",
            "measurement_state": "Достоверное измерение (R_вх ≫ R_тп, U_приб ≈ E_ген)",
            "active_point_t": t_hot,
            "active_point_e": u_meter_mv,
            "warning": None
        }

    if fault_mode == "Обрыв термоэлектрического контура":
        current_ua = 0.0
        if open_meter_mode.startswith("Идеальный"):
            u_meter_mv = e_generated_mv
            u_meter_str = f"{u_meter_mv:+.3f} мВ (режим U_хх)"
            meas_state = "Измерение ЭДС холостого хода U_хх на разомкнутых концах (I = 0 мкА)"
        else:
            u_meter_mv = None
            u_meter_str = "ОБРЫВ (0.000 мВ на входе)"
            meas_state = "Недостоверно: цепь разомкнута, источник ЭДС отсечён от входа прибора (I = 0 мкА)"

        return {
            "circuit_state": "Разомкнута (обрыв проводника)",
            "current_status": "I = 0.0000 мкА (ток отсутствует, R_контура → ∞)",
            "current_ua": 0.0,
            "i_loop_ma": 0.0,
            "e_gen_mv": e_generated_mv,
            "u_meter_mv": u_meter_mv,
            "u_meter_str": u_meter_str,
            "measurement_state": meas_state,
            "active_point_t": t_hot,
            "active_point_e": e_generated_mv,
            "warning": (
                f"Физическое состояние при обрыве: внутри термоэлектродов сохраняется разделение носителей заряда, "
                f"поэтому генерируемая термо-ЭДС холостого хода составляет E_ген = {e_generated_mv:+.3f} мВ. "
                f"Так как контур разомкнут, электрический ток равен нулю (I = 0 мкА). "
                f"Вход стандартного прибора с контролем обрыва отсечён от спая и сигнализирует об отказе линии."
            )
        }

    # Режим «Паразитный спай (КЗ)» с точным расчётом по теореме Тевенина для введённых R_уч1, R_уч2, R_кз
    t_kz = t_short_c if t_short_c is not None else t_cold
    e_kz = e_short if e_short is not None else e_cold

    # ЭДС холодного участка (от T_cold до T_кз) и горячего участка (от T_кз до T_hot)
    e_segment_cold_mv = e_kz - e_cold
    e_segment_hot_mv = e_hot - e_kz

    # Сопротивление контура горячей петли КЗ (R_уч2 + R_кз)
    r_loop_total = max(r_hot_loop_ohm + r_bridge_ohm, 1e-6)

    # Локальный циркулирующий ток в горячей петле КЗ: I_кз = (E(T_hot) - E(T_кз)) / (R_уч2 + R_кз) [мА]
    i_loop_ma = e_segment_hot_mv / r_loop_total

    # Эквивалентная ЭДС Тевенина и эквивалентное сопротивление со стороны прибора
    e_thevenin_mv = e_segment_cold_mv + i_loop_ma * r_bridge_ohm
    r_thevenin_ohm = r_cold_branch_ohm + (r_hot_loop_ohm * r_bridge_ohm) / r_loop_total

    # Ток во внешней цепи прибора (мкА) и напряжение на зажимах прибора (мВ)
    i_meter_ua = (e_thevenin_mv * 1000.0) / (r_thevenin_ohm + r_in_ohm)
    u_shunted_mv = e_thevenin_mv * (r_in_ohm / (r_thevenin_ohm + r_in_ohm))
    error_mv = u_shunted_mv - e_generated_mv

    return {
        "circuit_state": (
            f"Шунтирована перемычкой КЗ при T_кз = {t_kz:.0f} °C "
            f"(R_уч1={r_cold_branch_ohm:.1f} Ом, R_уч2={r_hot_loop_ohm:.1f} Ом, R_кз={r_bridge_ohm:.2f} Ом)"
        ),
        "current_status": f"I_приб = {i_meter_ua:+.4f} мкА | Локальный ток петли КЗ: I_кз = {i_loop_ma:+.3f} мА",
        "current_ua": i_meter_ua,
        "i_loop_ma": i_loop_ma,
        "e_gen_mv": e_generated_mv,
        "u_meter_mv": u_shunted_mv,
        "u_meter_str": f"{u_shunted_mv:+.3f} мВ (шунт при {t_kz:.0f} °C)",
        "measurement_state": (
            f"Искажено шунтированием: U_приб = {u_shunted_mv:+.3f} мВ, "
            f"методическая погрешность ΔE = {error_mv:+.3f} мВ"
        ),
        "active_point_t": t_kz,
        "active_point_e": u_shunted_mv,
        "warning": (
            f"Модель короткого замыкания (паразитного спая) при введённых сопротивлениях "
            f"R_уч1 = {r_cold_branch_ohm:.1f} Ом, R_уч2 = {r_hot_loop_ohm:.1f} Ом, R_кз = {r_bridge_ohm:.2f} Ом: "
            f"разность ЭДС горячего участка E(T_hot) − E(T_кз) = {e_segment_hot_mv:+.3f} мВ создаёт в замкнутой горячей петле "
            f"локальный паразитный ток I_кз = ({e_segment_hot_mv:+.3f} мВ) / ({r_hot_loop_ohm:.1f} + {r_bridge_ohm:.2f} Ом) = {i_loop_ma:+.3f} мА. "
            f"На вход прибора поступает напряжение U_приб = {u_shunted_mv:+.3f} мВ вместо полной ЭДС спая E_ген = {e_generated_mv:+.3f} мВ."
        )
    }


def hot_junction_rgb(temp_c: float) -> tuple[str, str, float]:
    """Преобразует температуру горячего спая T_hot в цвет свечения (красный/оранжевый/желтый)."""
    norm = float(np.clip((temp_c + 200.0) / 1400.0, 0.0, 1.0))
    r = int(180 + 75 * norm)
    g = int(35 + 145 * (norm ** 1.4))
    b = int(20 + 20 * norm)
    hex_col = f"0x{r:02x}{g:02x}{b:02x}"
    emissive = f"0x{int(r * 0.9):02x}{int(g * 0.6):02x}00"
    intensity = float(0.35 + 1.15 * norm)
    return hex_col, emissive, intensity


def cold_junction_rgb(temp_c: float) -> tuple[str, str, float]:
    """Преобразует температуру холодного спая T_cold в оттенки синего/голубого."""
    norm = float(np.clip((temp_c + 50.0) / 150.0, 0.0, 1.0))
    r = int(15 + 65 * norm)
    g = int(110 + 115 * norm)
    b = int(255 - 35 * norm)
    hex_col = f"0x{r:02x}{g:02x}{b:02x}"
    emissive = f"0x00{int(g * 0.7):02x}{int(b * 0.9):02x}"
    intensity = float(0.45 + 0.4 * (1.0 - norm))
    return hex_col, emissive, intensity


def configure_adaptive_plotly_layout(
    fig: go.Figure,
    x_main: np.ndarray,
    y_main: np.ndarray,
    all_y_arrays: list[np.ndarray],
    x_title: str,
    y_title: str,
    display_mode: str = "Адаптивный (ПК + смартфон)"
) -> tuple[dict, str]:
    """
    Настраивает адаптивное отображение графика Plotly под мобильные (320–430 px) и настольные экраны.
    Устанавливает равномерную линейную градуировку оси температуры с шагом 250 °C (tick0=0, dtick=250)
    и подбирает геометрию осей под визуальный наклон ~45° без изменения исходных физических данных.
    """
    x_arr = np.asarray(x_main, dtype=float)
    y_arr = np.asarray(y_main, dtype=float)

    # 1. Фактические физические диапазоны без модификации данных
    x_data_min, x_data_max = float(np.min(x_arr)), float(np.max(x_arr))
    dx_main = x_data_max - x_data_min
    dy_main_chord = abs(float(y_arr[-1]) - float(y_arr[0]))
    dy_main_span = float(np.max(y_arr) - np.min(y_arr))
    dy_main = max(dy_main_chord, dy_main_span)

    # Полный диапазон по Y с учётом всех отображаемых кривых и точек
    y_all_concat = np.concatenate([np.asarray(a, dtype=float).ravel() for a in all_y_arrays if len(a) > 0])
    y_all_min, y_all_max = float(np.min(y_all_concat)), float(np.max(y_all_concat))
    dy_all = y_all_max - y_all_min

    # Запас (padding) вокруг фактических границ, чтобы крайние маркеры и подписи не обрезались
    pad_x = max(0.06 * dx_main, 1.0)
    x_range = [x_data_min - pad_x, x_data_max + pad_x]

    if dy_all < 1e-6:
        y_range = [-1.0, 1.0]
    else:
        pad_y = 0.09 * dy_all
        y_range = [y_all_min - pad_y, y_all_max + pad_y]

    r_x = x_range[1] - x_range[0]
    r_y = y_range[1] - y_range[0]

    # 2. Параметры вёрстки для мобильного, адаптивного и десктопного режимов
    if display_mode == "Смартфон (320–430 px)":
        fig_height = 470
        margins = dict(l=54, r=14, t=28, b=145)
        y_nticks = 6
        x_tick_size, y_tick_size, title_size, legend_size = 10, 12, 13, 11
        legend_y = -0.28
        hover_mode = "closest"
        plotly_config = {
            "responsive": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d", "toggleSpikelines"]
        }
    elif display_mode == "Компьютер (широкий экран)":
        fig_height = 520
        margins = dict(l=64, r=24, t=32, b=115)
        y_nticks = 7
        x_tick_size, y_tick_size, title_size, legend_size = 12, 12, 13, 12
        legend_y = -0.21
        hover_mode = "x unified"
        plotly_config = {"responsive": True, "displaylogo": False}
    else:
        fig_height = 490
        margins = dict(l=58, r=16, t=30, b=135)
        y_nticks = 6
        x_tick_size, y_tick_size, title_size, legend_size = 11, 12, 13, 11
        legend_y = -0.25
        hover_mode = "closest"
        plotly_config = {
            "responsive": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"]
        }

    # 3. Градуировка горизонтальной оси температуры с равномерным шагом 250 °C (от 0 в обе стороны)
    xaxis_cfg = dict(
        title=dict(text=x_title, font=dict(size=title_size)),
        range=x_range,
        tickmode="linear",
        tick0=0,
        dtick=250,
        tickangle=0,
        ticks="outside",
        ticklen=5,
        tickfont=dict(size=x_tick_size),
        automargin=True,
        showgrid=True,
        gridcolor="rgba(255,255,255,0.14)",
        zerolinecolor="rgba(255,255,255,0.32)"
    )
    yaxis_cfg = dict(
        title=dict(text=y_title, font=dict(size=title_size)),
        range=y_range,
        nticks=y_nticks,
        tickfont=dict(size=y_tick_size),
        automargin=True,
        showgrid=True,
        gridcolor="rgba(255,255,255,0.10)",
        zerolinecolor="rgba(255,255,255,0.28)"
    )

    if dy_main < 1e-6 or dx_main < 1e-6:
        angle_note = (
            "Градуировка оси T: шаг 250 °C (от 0 °C). Визуальный угол основной линии: 0° "
            "(физически горизонтальная прямая, ΔE = 0 мВ) — график отображён без искажения."
        )
    else:
        target_scaleratio = dx_main / dy_main
        needed_box_aspect = (r_y * target_scaleratio) / r_x

        if 0.55 <= needed_box_aspect <= 1.75:
            xaxis_cfg["constrain"] = "domain"
            xaxis_cfg["constraintoward"] = "center"
            yaxis_cfg["scaleanchor"] = "x"
            yaxis_cfg["scaleratio"] = target_scaleratio
            yaxis_cfg["constrain"] = "domain"
            yaxis_cfg["constraintoward"] = "center"
            angle_sign = "−45°" if (float(y_arr[-1]) < float(y_arr[0])) else "+45°"
            angle_note = (
                f"Градуировка оси T: линейный шаг 250 °C (tick0=0, dtick=250). "
                f"Масштаб осей согласован (scaleratio = {target_scaleratio:.2f} °C/мВ): "
                f"расчётный визуальный наклон основной кривой {angle_sign} без изменения исходных данных."
            )
        else:
            angle_note = (
                "Градуировка оси T: линейный шаг 250 °C (tick0=0, dtick=250). "
                "Вспомогательная кривая существенно расширяет диапазон оси Y (расчётное соотношение сторон "
                f"{needed_box_aspect:.2f} вне интервала 0.55…1.75), поэтому принудительная фиксация 45° отключена."
            )

    fig.update_layout(
        autosize=True,
        height=fig_height,
        margin=margins,
        template="plotly_dark",
        hovermode=hover_mode,
        xaxis=xaxis_cfg,
        yaxis=yaxis_cfg,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=legend_y,
            xanchor="center",
            x=0.5,
            font=dict(size=legend_size),
            bgcolor="rgba(14, 17, 23, 0.0)",
            itemwidth=30
        )
    )

    # Совместимое подключение промежуточных делений (шаг 125 °C) без числовых подписей
    try:
        fig.update_xaxes(
            minor=dict(
                tickmode="linear",
                tick0=0,
                dtick=125,
                ticks="outside",
                ticklen=3,
                showgrid=True,
                gridcolor="rgba(255,255,255,0.04)"
            )
        )
    except Exception:
        # Если установлена старая версия Plotly без поддержки minor-делений, график работает с основными делениями 250 °C
        pass

    return plotly_config, angle_note


# =====================================================================
# 4. 3D-ВИЗУАЛИЗАЦИЯ С ПРОВЕРКОЙ THREE / ORBITCONTROLS И ПЕРЕХВАТОМ ОШИБОК WEBGL
# =====================================================================
def render_3d_stand1_gradient(
    t_hot: float,
    t_cold: float,
    sensor_title: str,
    e_gen_str: str,
    u_meter_str: str,
    seebeck_str: str,
    fault_state: str,
    t_kz_val: float | None = None
) -> str:
    """
    3D-модель термопары для Стенда №1.
    Проверяет наличие THREE и THREE.OrbitControls отдельно и перехватывает ошибки создания WebGLRenderer
    с автоматическим переходом на векторную 2D SVG-схему.
    """
    hot_hex, hot_emissive, hot_int = hot_junction_rgb(t_hot)
    cold_hex, cold_emissive, cold_int = cold_junction_rgb(t_cold)
    hot_css = "#" + hot_hex[2:]
    cold_css = "#" + cold_hex[2:]
    border_col = "#ff2a2a" if fault_state != "Норма" else "#00b4d8"
    is_open = "Обрыв" in fault_state
    is_short = "Паразитный" in fault_state
    kz_label = f"{t_kz_val:.0f} °C" if t_kz_val is not None else ""
    three_scripts = get_threejs_script_tags()

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; overflow: hidden; background-color: #0e1117; font-family: sans-serif; }}
            #hud {{
                position: absolute; top: 10px; left: 12px; color: #e0e6ed;
                background: rgba(20, 24, 33, 0.92); padding: 10px 14px;
                border-radius: 8px; border-left: 4px solid {border_col}; font-size: 12px;
                pointer-events: none; z-index: 10; line-height: 1.45;
            }}
            #legend {{
                position: absolute; bottom: 38px; left: 12px; color: #e0e6ed;
                background: rgba(20, 24, 33, 0.85); padding: 6px 10px;
                border-radius: 6px; font-size: 11px; pointer-events: none; z-index: 10;
            }}
            #hint {{
                position: absolute; bottom: 10px; left: 12px; color: #9aa5b1;
                background: rgba(14, 17, 23, 0.75); padding: 5px 10px;
                border-radius: 6px; font-size: 11px; pointer-events: none; z-index: 10;
            }}
            #fallback2d {{
                display: none; width: 100vw; height: 100vh;
                align-items: center; justify-content: center; flex-direction: column;
                background-color: #0e1117; color: #e0e6ed;
            }}
            .hot-badge {{ color: #ff6b35; font-weight: bold; }}
            .cold-badge {{ color: #4cc9f0; font-weight: bold; }}
            #hud b {{ color: #ff9f1c; }}
        </style>
        {three_scripts}
    </head>
    <body>
        <div id="hud">
            <div>Термопара: <b>{sensor_title}</b></div>
            <div>Горячий спай T_hot: <span class="hot-badge">{t_hot:.1f} °C</span> | Холодный спай T_cold: <span class="cold-badge">{t_cold:.1f} °C</span></div>
            <div>ЭДС холостого хода E_ген: <b>{e_gen_str}</b> | S(T_hot): <b>{seebeck_str}</b></div>
            <div>На приборе U_приб: <b>{u_meter_str}</b></div>
            <div>Состояние цепи: <b>{fault_state}</b></div>
        </div>
        <div id="legend">
            🔴 Внизу: Горячий спай (T_hot) &nbsp;|&nbsp; 🔵 Вверху: Холодный спай (T_cold)
        </div>
        <div id="hint">🖱️ ЛКМ: вращать 3D | Колесо: масштаб | ПКМ: панорама</div>

        <!-- Автономный 2D SVG-fallback при недоступности Three.js, OrbitControls или WebGL -->
        <div id="fallback2d">
            <svg width="320" height="360" viewBox="0 0 320 360">
                <defs>
                    <linearGradient id="gradWire" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" style="stop-color:{cold_css};stop-opacity:1" />
                        <stop offset="100%" style="stop-color:{hot_css};stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="85" y="45" width="150" height="36" rx="6" fill="{cold_css}" stroke="#ffffff" stroke-width="1.5"/>
                <text x="160" y="68" fill="#0e1117" font-size="12" font-weight="bold" text-anchor="middle">Холодный спай ({t_cold:.0f} °C)</text>
                <line x1="115" y1="81" x2="155" y2="290" stroke="url(#gradWire)" stroke-width="8" stroke-linecap="round"/>
                <line x1="205" y1="81" x2="165" y2="290" stroke="url(#gradWire)" stroke-width="8" stroke-linecap="round"/>
                {"<rect x='115' y='165' width='35' height='22' fill='#0e1117'/><circle cx='132' cy='176' r='10' fill='none' stroke='#ff2a2a' stroke-width='2' stroke-dasharray='3,3'/><text x='70' y='180' fill='#ff4d4d' font-size='11'>Обрыв I=0</text>" if is_open else ""}
                {"<line x1='128' y1='185' x2='192' y2='185' stroke='#ff2a2a' stroke-width='6'/><text x='235' y='189' fill='#ff4d4d' font-size='11'>КЗ (" + kz_label + ")</text>" if is_short else ""}
                <circle cx="160" cy="295" r="20" fill="{hot_css}" stroke="#ffffff" stroke-width="1.5"/>
                <text x="160" y="335" fill="{hot_css}" font-size="12" font-weight="bold" text-anchor="middle">Горячий спай ({t_hot:.0f} °C)</text>
            </svg>
        </div>

        <script>
            function activateFallback2D(reason) {{
                const fb = document.getElementById('fallback2d');
                const hintEl = document.getElementById('hint');
                if (fb) fb.style.display = 'flex';
                if (hintEl) hintEl.innerText = 'ℹ️ Автономная 2D SVG-схема (' + reason + ')';
            }}

            if (typeof window.THREE === 'undefined') {{
                activateFallback2D('библиотека THREE не загружена');
            }} else if (typeof window.THREE.OrbitControls === 'undefined') {{
                activateFallback2D('модуль THREE.OrbitControls не загружен');
            }} else {{
                try {{
                    const scene = new THREE.Scene();
                    scene.background = new THREE.Color(0x0e1117);

                    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
                    camera.position.set(0.0, 0.3, 6.8);

                    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
                    if (!renderer || !renderer.domElement) {{
                        throw new Error('WebGL контекст недоступен');
                    }}
                    renderer.setSize(window.innerWidth, window.innerHeight);
                    renderer.setPixelRatio(window.devicePixelRatio || 1);
                    document.body.appendChild(renderer.domElement);

                    const controls = new THREE.OrbitControls(camera, renderer.domElement);
                    controls.enableDamping = true;
                    controls.dampingFactor = 0.06;
                    controls.autoRotate = true;
                    controls.autoRotateSpeed = 0.8;
                    controls.addEventListener('start', function() {{ controls.autoRotate = false; }});

                    scene.add(new THREE.AmbientLight(0xffffff, 0.65));
                    const dirLight = new THREE.DirectionalLight(0xffffff, 0.85);
                    dirLight.position.set(5, 8, 6);
                    scene.add(dirLight);

                    const hotLight = new THREE.PointLight({hot_emissive}, {hot_int * 1.8}, 6);
                    hotLight.position.set(0, -2.1, 0.5);
                    scene.add(hotLight);

                    const coldLight = new THREE.PointLight({cold_emissive}, {cold_int * 1.6}, 6);
                    coldLight.position.set(0, 2.0, 0.5);
                    scene.add(coldLight);

                    const group = new THREE.Group();

                    const coldMat = new THREE.MeshStandardMaterial({{
                        color: {cold_hex}, emissive: {cold_emissive},
                        emissiveIntensity: {cold_int * 0.65}, metalness: 0.5, roughness: 0.25
                    }});
                    const coldBlock = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.55, 0.85), coldMat);
                    coldBlock.position.set(0, 2.05, 0);
                    group.add(coldBlock);

                    const termGeom = new THREE.CylinderGeometry(0.16, 0.16, 0.35, 24);
                    const leftTerm = new THREE.Mesh(termGeom, coldMat);
                    leftTerm.position.set(-0.65, 2.45, 0);
                    group.add(leftTerm);

                    const rightTerm = new THREE.Mesh(termGeom, coldMat);
                    rightTerm.position.set(0.65, 2.45, 0);
                    group.add(rightTerm);

                    const cCold = new THREE.Color({cold_hex});
                    const cHot = new THREE.Color({hot_hex});
                    const numSegs = 24;
                    const yTop = 1.75;
                    const yBot = -1.95;

                    for (let i = 0; i < numSegs; i++) {{
                        const tFrac = i / (numSegs - 1);
                        const segColor = cCold.clone().lerp(cHot, tFrac);
                        const segMat = new THREE.MeshStandardMaterial({{
                            color: segColor,
                            emissive: segColor,
                            emissiveIntensity: 0.22 + 0.35 * tFrac,
                            metalness: 0.7,
                            roughness: 0.25
                        }});

                        const yPos = yTop - tFrac * (yTop - yBot);
                        const xSpread = 0.65 * (1.0 - 0.82 * (tFrac * tFrac));
                        const segHeight = (yTop - yBot) / numSegs * 1.15;

                        if (!({str(is_open).lower()} && (i === 10 || i === 11))) {{
                            const segLeft = new THREE.Mesh(new THREE.CylinderGeometry(0.10, 0.10, segHeight, 16), segMat);
                            segLeft.position.set(-xSpread, yPos, 0);
                            segLeft.rotation.z = 0.22 * tFrac;
                            group.add(segLeft);
                        }}

                        const segRight = new THREE.Mesh(new THREE.CylinderGeometry(0.10, 0.10, segHeight, 16), segMat);
                        segRight.position.set(xSpread, yPos, 0);
                        segRight.rotation.z = -0.22 * tFrac;
                        group.add(segRight);
                    }}

                    const hotMat = new THREE.MeshStandardMaterial({{
                        color: {hot_hex}, emissive: {hot_emissive},
                        emissiveIntensity: {hot_int}, metalness: 0.4, roughness: 0.2
                    }});
                    const hotJunction = new THREE.Mesh(new THREE.SphereGeometry(0.34, 32, 24), hotMat);
                    hotJunction.position.set(0, -2.05, 0);
                    group.add(hotJunction);

                    const heaterRing = new THREE.Mesh(
                        new THREE.TorusGeometry(0.62, 0.07, 16, 48),
                        new THREE.MeshStandardMaterial({{ color: {hot_hex}, emissive: {hot_emissive}, emissiveIntensity: 0.8 }})
                    );
                    heaterRing.rotation.x = Math.PI / 2;
                    heaterRing.position.set(0, -2.05, 0);
                    group.add(heaterRing);

                    if ({str(is_short).lower()}) {{
                        const shortMat = new THREE.MeshStandardMaterial({{
                            color: 0xff2a2a, emissive: 0xff0000, emissiveIntensity: 0.85, metalness: 0.8
                        }});
                        const bridge = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 1.15, 16), shortMat);
                        bridge.rotation.z = Math.PI / 2;
                        bridge.position.set(0, 0.45, 0);
                        group.add(bridge);
                    }}

                    if ({str(is_open).lower()}) {{
                        const sparkMat = new THREE.MeshBasicMaterial({{ color: 0xff2a2a, wireframe: true }});
                        const breakSphere = new THREE.Mesh(new THREE.SphereGeometry(0.24, 12, 12), sparkMat);
                        breakSphere.position.set(-0.52, 0.22, 0);
                        group.add(breakSphere);
                    }}

                    scene.add(group);

                    function animate() {{
                        requestAnimationFrame(animate);
                        controls.update();
                        renderer.render(scene, camera);
                    }}
                    animate();

                    window.addEventListener('resize', () => {{
                        camera.aspect = window.innerWidth / window.innerHeight;
                        camera.updateProjectionMatrix();
                        renderer.setSize(window.innerWidth, window.innerHeight);
                    }});
                }} catch (err) {{
                    activateFallback2D('ошибка инициализации WebGL: ' + (err && err.message ? err.message : 'неизвестная ошибка'));
                }}
            }}
        </script>
    </body>
    </html>
    """


def render_3d_stand2_pair(
    metal1_name: str,
    metal2_name: str,
    col1_hex: str,
    col2_hex: str,
    s_pair: float,
    delta_t: float,
    e_gen_mv: float,
    u_meter_mv: float | None,
    u_meter_str: str,
    fault_state: str
) -> str:
    """
    3D-модель для Стенда №2 с раздельной проверкой THREE / THREE.OrbitControls
    и перехватом ошибок WebGLRenderer (автоматический переход на 2D SVG).
    """
    border_col = "#ff2a2a" if fault_state != "Норма" else "#80ed99"
    is_open = "Обрыв" in fault_state
    is_short = "Паразитный" in fault_state
    col1_css = "#" + col1_hex[2:]
    col2_css = "#" + col2_hex[2:]
    meter_val = 0.0 if u_meter_mv is None else u_meter_mv
    needle_angle = float(np.clip((meter_val / 50.0) * 0.9, -1.1, 1.1))
    three_scripts = get_threejs_script_tags()

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; overflow: hidden; background-color: #0e1117; font-family: sans-serif; }}
            #hud {{
                position: absolute; top: 10px; left: 12px; color: #e0e6ed;
                background: rgba(20, 24, 33, 0.92); padding: 10px 14px;
                border-radius: 8px; border-left: 4px solid {border_col}; font-size: 12px;
                pointer-events: none; z-index: 10; line-height: 1.45;
            }}
            #hint {{
                position: absolute; bottom: 10px; left: 12px; color: #9aa5b1;
                background: rgba(14, 17, 23, 0.75); padding: 5px 10px;
                border-radius: 6px; font-size: 11px; pointer-events: none; z-index: 10;
            }}
            #fallback2d {{
                display: none; width: 100vw; height: 100vh;
                align-items: center; justify-content: center; flex-direction: column;
                background-color: #0e1117; color: #e0e6ed;
            }}
            #hud b {{ color: #80ed99; }}
        </style>
        {three_scripts}
    </head>
    <body>
        <div id="hud">
            <div>Ветвь А: <b>{metal1_name}</b> | Ветвь B: <b>{metal2_name}</b></div>
            <div>S_пары (при ~20 °C): <b>{s_pair:+.1f} мкВ/°C</b> | ΔT: <b>{delta_t:+.0f} °C</b></div>
            <div>ЭДС холостого хода E_ген: <b>{e_gen_mv:+.3f} мВ</b></div>
            <div>Показание вольтметра U_приб: <b>{u_meter_str}</b></div>
            <div>Состояние контура: <b>{fault_state}</b></div>
        </div>
        <div id="hint">🖱️ ЛКМ: вращать 3D | Колесо: масштаб | ПКМ: панорама</div>

        <div id="fallback2d">
            <svg width="320" height="360" viewBox="0 0 320 360">
                <rect x="95" y="45" width="130" height="70" rx="8" fill="#1f2937" stroke="#9aa5b1" stroke-width="2"/>
                <text x="160" y="75" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">Милливольтметр</text>
                <text x="160" y="98" fill="#80ed99" font-size="11" text-anchor="middle">{u_meter_str}</text>
                <line x1="115" y1="115" x2="155" y2="290" stroke="{col1_css}" stroke-width="7" stroke-linecap="round"/>
                <line x1="205" y1="115" x2="165" y2="290" stroke="{col2_css}" stroke-width="7" stroke-linecap="round"/>
                {"<rect x='115' y='180' width='35' height='22' fill='#0e1117'/><text x='65' y='195' fill='#ff4d4d' font-size='11'>Обрыв I=0</text>" if is_open else ""}
                {"<line x1='130' y1='200' x2='190' y2='200' stroke='#ff2a2a' stroke-width='6'/><text x='225' y='204' fill='#ff4d4d' font-size='11'>Перемычка КЗ</text>" if is_short else ""}
                <circle cx="160" cy="295" r="18" fill="#ff5400" stroke="#ffffff" stroke-width="1.5"/>
            </svg>
        </div>

        <script>
            function activateFallback2D(reason) {{
                const fb = document.getElementById('fallback2d');
                const hintEl = document.getElementById('hint');
                if (fb) fb.style.display = 'flex';
                if (hintEl) hintEl.innerText = 'ℹ️ Автономная 2D SVG-схема (' + reason + ')';
            }}

            if (typeof window.THREE === 'undefined') {{
                activateFallback2D('библиотека THREE не загружена');
            }} else if (typeof window.THREE.OrbitControls === 'undefined') {{
                activateFallback2D('модуль THREE.OrbitControls не загружен');
            }} else {{
                try {{
                    const scene = new THREE.Scene();
                    scene.background = new THREE.Color(0x0e1117);

                    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
                    camera.position.set(0.0, 0.5, 7.2);

                    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
                    if (!renderer || !renderer.domElement) {{
                        throw new Error('WebGL контекст недоступен');
                    }}
                    renderer.setSize(window.innerWidth, window.innerHeight);
                    renderer.setPixelRatio(window.devicePixelRatio || 1);
                    document.body.appendChild(renderer.domElement);

                    const controls = new THREE.OrbitControls(camera, renderer.domElement);
                    controls.enableDamping = true;
                    controls.dampingFactor = 0.06;

                    scene.add(new THREE.AmbientLight(0xffffff, 0.75));
                    const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
                    dirLight.position.set(4, 7, 6);
                    scene.add(dirLight);

                    const group = new THREE.Group();

                    const meterBodyMat = new THREE.MeshStandardMaterial({{ color: 0x1f2937, metalness: 0.5, roughness: 0.4 }});
                    const meterBody = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.35, 0.7), meterBodyMat);
                    meterBody.position.set(0, 1.75, 0);
                    group.add(meterBody);

                    const dialMat = new THREE.MeshStandardMaterial({{ color: 0x0f172a, roughness: 0.2 }});
                    const dialFace = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.55, 0.08, 32), dialMat);
                    dialFace.rotation.x = Math.PI / 2;
                    dialFace.position.set(0, 1.72, 0.35);
                    group.add(dialFace);

                    const needlePivot = new THREE.Group();
                    needlePivot.position.set(0, 1.50, 0.42);
                    const needleMat = new THREE.MeshBasicMaterial({{ color: 0xff4d4d }});
                    const needle = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.48, 0.04), needleMat);
                    needle.position.set(0, 0.22, 0);
                    needlePivot.add(needle);
                    needlePivot.rotation.z = -{needle_angle};
                    group.add(needlePivot);

                    const coldMat = new THREE.MeshStandardMaterial({{
                        color: 0x00b4d8, emissive: 0x0077b6, emissiveIntensity: 0.5
                    }});
                    const termL = new THREE.Mesh(new THREE.SphereGeometry(0.18, 20, 20), coldMat);
                    termL.position.set(-0.85, 0.95, 0);
                    group.add(termL);

                    const termR = new THREE.Mesh(new THREE.SphereGeometry(0.18, 20, 20), coldMat);
                    termR.position.set(0.85, 0.95, 0);
                    group.add(termR);

                    const mat1 = new THREE.MeshStandardMaterial({{
                        color: {col1_hex}, metalness: 0.8, roughness: 0.22
                    }});
                    const mat2 = new THREE.MeshStandardMaterial({{
                        color: {col2_hex}, metalness: 0.8, roughness: 0.22
                    }});

                    if (!{str(is_open).lower()}) {{
                        const wire1 = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 3.1, 24), mat1);
                        wire1.position.set(-0.44, -0.45, 0);
                        wire1.rotation.z = 0.28;
                        group.add(wire1);
                    }} else {{
                        const wire1Top = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 1.2, 24), mat1);
                        wire1Top.position.set(-0.68, 0.35, 0);
                        wire1Top.rotation.z = 0.28;
                        group.add(wire1Top);

                        const wire1Bot = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 1.2, 24), mat1);
                        wire1Bot.position.set(-0.22, -1.25, 0);
                        wire1Bot.rotation.z = 0.28;
                        group.add(wire1Bot);
                    }}

                    const wire2 = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 3.1, 24), mat2);
                    wire2.position.set(0.44, -0.45, 0);
                    wire2.rotation.z = -0.28;
                    group.add(wire2);

                    const hotMat = new THREE.MeshStandardMaterial({{
                        color: 0xff5400, emissive: 0xff2a00, emissiveIntensity: 0.95, roughness: 0.2
                    }});
                    const hotJunction = new THREE.Mesh(new THREE.SphereGeometry(0.32, 32, 24), hotMat);
                    hotJunction.position.set(0, -1.9, 0);
                    group.add(hotJunction);

                    if ({str(is_short).lower()}) {{
                        const shortMat = new THREE.MeshStandardMaterial({{
                            color: 0xff2a2a, emissive: 0xcc0000, emissiveIntensity: 0.8
                        }});
                        const shortBar = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.15, 16), shortMat);
                        shortBar.rotation.z = Math.PI / 2;
                        shortBar.position.set(0, 0.1, 0);
                        group.add(shortBar);
                    }}

                    scene.add(group);

                    function animate() {{
                        requestAnimationFrame(animate);
                        controls.update();
                        renderer.render(scene, camera);
                    }}
                    animate();

                    window.addEventListener('resize', () => {{
                        camera.aspect = window.innerWidth / window.innerHeight;
                        camera.updateProjectionMatrix();
                        renderer.setSize(window.innerWidth, window.innerHeight);
                    }});
                }} catch (err) {{
                    activateFallback2D('ошибка инициализации WebGL: ' + (err && err.message ? err.message : 'неизвестная ошибка'));
                }}
            }}
        </script>
    </body>
    </html>
    """


# =====================================================================
# 5. БОКОВАЯ ПАНЕЛЬ: ВЫБОР СТЕНДА, МОДЕЛИ НЕИСПРАВНОСТЕЙ И ПРАКТИКУМ
# =====================================================================
st.sidebar.title("⚛️ Физическая лаборатория")
st.sidebar.caption("Тема: «Термо-ЭДС. Эффект Зеебека»")

lab_mode = st.sidebar.radio(
    "Выберите исследовательский стенд:",
    options=[
        "Стенд №1: Визуализация градиента температур и генерация Термо-ЭДС",
        "Стенд №2: Исследование эффекта Зеебека в разнородных металлах (Термоэлектрические пары)"
    ]
)

chart_display_mode = st.sidebar.selectbox(
    "📱 Режим отображения графиков:",
    options=[
        "Адаптивный (ПК + смартфон)",
        "Смартфон (320–430 px)",
        "Компьютер (широкий экран)"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Физические нарушения цепи")
circuit_fault_mode = st.sidebar.selectbox(
    "Состояние термоэлектрического контура:",
    options=[
        "Норма",
        "Обрыв термоэлектрического контура",
        "Паразитный спай (КЗ)"
    ]
)

open_circuit_meter_mode = "Вторичный прибор с контролем обрыва (шунт входа)"
if circuit_fault_mode == "Обрыв термоэлектрического контура":
    open_circuit_meter_mode = st.sidebar.radio(
        "Режим измерительного прибора при обрыве:",
        options=[
            "Вторичный прибор с контролем обрыва (шунт входа)",
            "Идеальный высокоомный вольтметр на разрыве (измерение U_хх)"
        ]
    )

# Независимые параметры сопротивлений участков цепи (п. 2 ревизии)
r_cold_branch_input = 8.0
r_hot_loop_input = 7.0
r_bridge_input = 0.0
if circuit_fault_mode == "Паразитный спай (КЗ)":
    st.sidebar.markdown("**Сопротивления участков цепи при КЗ:**")
    r_cold_branch_input = float(st.sidebar.number_input(
        "Сопротивление холодного участка R_уч1 (до КЗ), Ом:",
        min_value=0.1,
        max_value=500.0,
        value=8.0,
        step=0.5
    ))
    r_hot_loop_input = float(st.sidebar.number_input(
        "Сопротивление горячего участка R_уч2 (от КЗ до спая), Ом:",
        min_value=0.1,
        max_value=500.0,
        value=5.0,
        step=0.5
    ))
    r_bridge_input = float(st.sidebar.number_input(
        "Переходное сопротивление перемычки R_кз, Ом:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5
    ))

st.sidebar.markdown("---")
st.sidebar.subheader("🎓 Справочный практикум")
if st.sidebar.button("🧠 Случайный качественный вопрос"):
    physics_questions = [
        {
            "title": "Равенство температур спаев",
            "question": "Почему при равенстве температур горячего и холодного спаев (T_hot = T_cold) результирующая Термо-ЭДС равна нулю?",
            "hint": "Рассмотрите интеграл по замкнутому контуру и Второе начало термодинамики: возможен ли вечный двигатель второго рода?"
        },
        {
            "title": "Влияние длины проводников",
            "question": "Как изменится Термо-ЭДС термопары, если удлинить её провода в 3 раза при неизменных T_hot и T_cold?",
            "hint": "Зависит ли интеграл E = ∫ S(T) dT от геометрической длины пути, или меняется только внутреннее омическое сопротивление контура?"
        },
        {
            "title": "Закон Вольта (третьего металла)",
            "question": "Что такое закон Вольта для последовательной цепи металлов и почему медные щупы вольтметра не искажают измеряемую Термо-ЭДС?",
            "hint": "Запишите алгебраическую сумму потенциалов при условии, что оба контакта с третьим металлом имеют одинаковую температуру T_cold."
        }
    ]
    st.session_state["prof_question"] = np.random.choice(physics_questions)

if "prof_question" in st.session_state:
    pq = st.session_state["prof_question"]
    st.sidebar.info(f"**Тема: {pq['title']}**\n\n{pq['question']}")
    st.sidebar.caption(f"💡 *Подсказка:* {pq['hint']}")


# =====================================================================
# 6. СТЕНД №1: ВИЗУАЛИЗАЦИЯ ГРАДИЕНТА ТЕМПЕРАТУР И ГЕНЕРАЦИЯ ТЕРМО-ЭДС
# =====================================================================
if lab_mode.startswith("Стенд №1"):
    st.title("Стенд №1: Визуализация градиента температур и генерация Термо-ЭДС")

    sensor_name = st.sidebar.selectbox(
        "Выберите термопару из расчётной базы симулятора:",
        options=list(THERMOCOUPLES_DB.keys())
    )
    spec = THERMOCOUPLES_DB[sensor_name]

    t_hot = float(st.sidebar.slider(
        "Температура горячего спая (T_hot), °C:",
        min_value=int(spec["min_t"]),
        max_value=int(spec["max_t"]),
        value=int(spec["default_hot"]),
        step=10
    ))

    t_cold = float(st.sidebar.slider(
        "Температура холодного спая (T_cold), °C:",
        min_value=-50,
        max_value=100,
        value=20,
        step=10
    ))

    t_kz_stand1 = None
    e_kz_stand1 = None
    kz_contact_type = "Непосредственное соприкосновение электродов A и B"
    if circuit_fault_mode == "Паразитный спай (КЗ)":
        st.sidebar.markdown("**Температура и тип контакта КЗ:**")
        kz_min = int(min(t_cold, t_hot))
        kz_max = int(max(t_cold, t_hot))
        kz_default = int(round((t_cold + t_hot) / 2.0, -1))
        if kz_min == kz_max:
            t_kz_stand1 = float(kz_min)
        else:
            t_kz_stand1 = float(st.sidebar.slider(
                "Температура в точке перемычки (T_кз), °C:",
                min_value=kz_min,
                max_value=kz_max,
                value=int(np.clip(kz_default, kz_min, kz_max)),
                step=10
            ))
        kz_contact_type = st.sidebar.selectbox(
            "Характер паразитного контакта:",
            options=[
                "Непосредственное соприкосновение электродов A и B",
                "Перемычка из третьего металла C (изотермическая при T_кз)"
            ]
        )
        e_kz_stand1 = calculate_nominal_emf(sensor_name, t_kz_stand1)

    e_hot = calculate_nominal_emf(sensor_name, t_hot)
    e_cold = calculate_nominal_emf(sensor_name, t_cold)
    delta_t = t_hot - t_cold
    seebeck_hot = calculate_seebeck_diff(sensor_name, t_hot)

    phys = evaluate_circuit_physics(
        e_hot=e_hot,
        e_cold=e_cold,
        t_hot=t_hot,
        t_cold=t_cold,
        fault_mode=circuit_fault_mode,
        t_short_c=t_kz_stand1,
        e_short=e_kz_stand1,
        open_meter_mode=open_circuit_meter_mode,
        r_cold_branch_ohm=r_cold_branch_input,
        r_hot_loop_ohm=r_hot_loop_input,
        r_bridge_ohm=r_bridge_input
    )

    if circuit_fault_mode == "Норма":
        st.latex(
            rf"E_{{\text{{ген}}}} = E(T_{{\text{{hot}}}}) - E(T_{{\text{{cold}}}}) = "
            rf"E({t_hot:.0f}^\circ\text{{C}}) - E({t_cold:.0f}^\circ\text{{C}}) = "
            rf"{e_hot:.3f} - ({e_cold:.3f}) = {phys['e_gen_mv']:+.3f}\text{{ мВ}}, \quad "
            rf"U_{{\text{{приб}}}} \approx E_{{\text{{ген}}}} = {phys['u_meter_mv']:+.3f}\text{{ мВ}}"
        )
    elif circuit_fault_mode == "Обрыв термоэлектрического контура":
        st.latex(
            rf"E_{{\text{{ген (х.х.)}}}} = E({t_hot:.0f}^\circ\text{{C}}) - E({t_cold:.0f}^\circ\text{{C}}) = "
            rf"{e_hot:.3f} - ({e_cold:.3f}) = {phys['e_gen_mv']:+.3f}\text{{ мВ}}, \quad "
            rf"R_{{\text{{контура}}}} \to \infty \implies I = 0\text{{ мкА}}"
        )
    else:
        st.latex(
            rf"I_{{\text{{кз}}}} = \frac{{E(T_{{\text{{hot}}}}) - E(T_{{\text{{кз}}}})}}{{R_{{\text{{уч2}}}} + R_{{\text{{кз}}}}}} = "
            rf"\frac{{{e_hot:.3f} - ({e_kz_stand1:.3f})}}{{{r_hot_loop_input:.1f} + {r_bridge_input:.2f}}} = {phys['i_loop_ma']:+.3f}\text{{ мА}}, \quad "
            rf"U_{{\text{{приб}}}} \approx \left[E(T_{{\text{{кз}}}}) - E(T_{{\text{{cold}}}})\right] + I_{{\text{{кз}}}} R_{{\text{{кз}}}} = "
            rf"{phys['u_meter_mv']:+.3f}\text{{ мВ}}"
        )

    if phys["warning"]:
        st.warning(f"⚠️ **Физическая диагностика цепи:** {phys['warning']}")
        if circuit_fault_mode == "Паразитный спай (КЗ)" and "третьего" in kz_contact_type:
            st.caption(
                "ℹ️ По закону промежуточных металлов Вольта, если перемычка из третьего металла C находится "
                "при единой температуре T_кз, сумма контактных ЭДС на её краях равна нулю, и измеряемый сигнал "
                "определяется температурой T_кз и делителем сопротивлений R_уч2 и R_кз."
            )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "1. Генерируемая Термо-ЭДС E_ген",
        f"{phys['e_gen_mv']:+.3f} мВ",
        delta=f"E(T_hot)={e_hot:.3f} мВ | E(T_cold)={e_cold:.3f} мВ"
    )
    m2.metric(
        "2. Напряжение на приборе U_приб",
        phys["u_meter_str"],
        delta=phys["circuit_state"]
    )
    m3.metric(
        "3. Ток в цепи и S(T_hot)",
        f"S = {seebeck_hot:.2f} мкВ/°C",
        delta=phys["current_status"]
    )
    m4.metric(
        "4. Градиент температур (ΔT)",
        f"{delta_t:+.1f} °C",
        delta=f"T_hot ({t_hot:.0f} °C) − T_cold ({t_cold:.0f} °C)"
    )

    st.caption(
        f"**Состояние цепи:** {phys['circuit_state']} | "
        f"**Ток в контуре:** {phys['current_status']} | "
        f"**Статус измерения:** {phys['measurement_state']}"
    )

    col_plot, col_3d = st.columns([3, 2])

    with col_plot:
        st.subheader("Формирование Термо-ЭДС на характеристике НСХ")
        t_curve = spec["temps"]
        e_curve_abs = spec["values"]
        e_curve_rel = e_curve_abs - e_cold
        is_mobile_view = (chart_display_mode == "Смартфон (320–430 px)")

        fig_stand1 = go.Figure()
        all_y_stand1 = [e_curve_rel, e_curve_abs, np.array([0.0, phys["e_gen_mv"]])]

        fig_stand1.add_trace(go.Scatter(
            x=t_curve, y=e_curve_rel, mode="lines",
            name=f"E(T) − E({t_cold:.0f} °C)",
            line=dict(color=spec["color"], width=3),
            hovertemplate="T = %{x:.0f} °C<br>E_ген = %{y:+.3f} мВ<extra>Основная НСХ</extra>"
        ))

        fig_stand1.add_trace(go.Scatter(
            x=t_curve, y=e_curve_abs, mode="lines+markers",
            name="Таблица E(T) при T₀ = 0 °C",
            line=dict(color="#adb5bd", width=1.5, dash="dash"),
            marker=dict(size=3.5 if is_mobile_view else 4, color="#ffffff"),
            hovertemplate="T = %{x:.0f} °C<br>E_табл = %{y:+.3f} мВ<extra>При T₀ = 0 °C</extra>"
        ))

        fig_stand1.add_trace(go.Scatter(
            x=[t_cold], y=[0.0],
            mode="markers+text", name="Холодный спай (T_cold)",
            text=[f" T_cold ({t_cold:.0f}°C)"] if is_mobile_view else [f"  T_cold = {t_cold:.0f} °C"],
            textposition="bottom right",
            textfont=dict(size=11, color="#4cc9f0"),
            marker=dict(size=10, color="#00b4d8", symbol="circle", line=dict(width=1.5, color="white")),
            hovertemplate=(
                f"Холодный спай T_cold = {t_cold:.0f} °C<br>"
                f"E_табл(T_cold) = {e_cold:.3f} мВ<br>E_отн = 0.000 мВ<extra></extra>"
            )
        ))

        fig_stand1.add_trace(go.Scatter(
            x=[t_hot], y=[phys["e_gen_mv"]],
            mode="markers+text", name="Рабочий спай (E_ген)",
            text=[f"T_hot ({phys['e_gen_mv']:+.1f} мВ)"] if is_mobile_view else [f"  T_hot = {t_hot:.0f} °C ({phys['e_gen_mv']:+.2f} мВ)"],
            textposition="top left",
            textfont=dict(size=11, color="#ff6b6b"),
            marker=dict(size=12, color="#ff4d4d", symbol="diamond", line=dict(width=1.5, color="white")),
            hovertemplate=(
                f"Горячий спай T_hot = {t_hot:.0f} °C<br>"
                f"E_ген = {phys['e_gen_mv']:+.3f} мВ<br>"
                f"E_табл(T_hot) = {e_hot:.3f} мВ<extra></extra>"
            )
        ))

        if circuit_fault_mode == "Паразитный спай (КЗ)" and t_kz_stand1 is not None:
            all_y_stand1.append(np.array([phys["u_meter_mv"]]))
            fig_stand1.add_trace(go.Scatter(
                x=[t_kz_stand1], y=[phys["u_meter_mv"]],
                mode="markers+text", name="Точка КЗ (U_приб)",
                text=[f"T_кз ({phys['u_meter_mv']:+.1f} мВ)"],
                textposition="bottom right",
                textfont=dict(size=11, color="#ff9f1c"),
                marker=dict(size=12, color="#ff9f1c", symbol="x", line=dict(width=2, color="white")),
                hovertemplate=(
                    f"Паразитный спай T_кз = {t_kz_stand1:.0f} °C<br>"
                    f"U_приб = {phys['u_meter_mv']:+.3f} мВ<extra></extra>"
                )
            ))

        if "ai_alloy" in st.session_state:
            ai = st.session_state["ai_alloy"]
            a1, a2, a3 = ai["coeffs"]["a1"], ai["coeffs"]["a2"], ai["coeffs"]["a3"]
            e_ai_cold = a1 * t_cold + a2 * (t_cold ** 2) + a3 * (t_cold ** 3)
            e_ai_curve = (a1 * t_curve + a2 * (t_curve ** 2) + a3 * (t_curve ** 3)) - e_ai_cold
            all_y_stand1.append(e_ai_curve)
            fig_stand1.add_trace(go.Scatter(
                x=t_curve, y=e_ai_curve, mode="lines",
                name=f"Условная НСХ ({ai['s_target']} мкВ/°C)",
                line=dict(color="#ff9f1c", width=2.5, dash="dot"),
                hovertemplate="T = %{x:.0f} °C<br>E_мод = %{y:+.3f} мВ<extra>Условная НСХ</extra>"
            ))

        plotly_cfg1, angle_note1 = configure_adaptive_plotly_layout(
            fig=fig_stand1,
            x_main=t_curve,
            y_main=e_curve_rel,
            all_y_arrays=all_y_stand1,
            x_title="Температура T, °C",
            y_title="Термо-ЭДС E, мВ",
            display_mode=chart_display_mode
        )
        st.plotly_chart(fig_stand1, use_container_width=True, config=plotly_cfg1)
        st.caption(f"📐 {angle_note1}")

    with col_3d:
        st.subheader("3D-модель теплового градиента спаев")
        short_title = spec["short_code"]
        components.html(
            render_3d_stand1_gradient(
                t_hot=t_hot,
                t_cold=t_cold,
                sensor_title=short_title,
                e_gen_str=f"{phys['e_gen_mv']:+.3f} мВ",
                u_meter_str=phys["u_meter_str"],
                seebeck_str=f"{seebeck_hot:.2f} мкВ/°C",
                fault_state=circuit_fault_mode,
                t_kz_val=t_kz_stand1
            ),
            height=430
        )

    with st.expander("📊 Паспорт набора данных НСХ и справочная таблица (Аудит источников данных)"):
        st.markdown(
            f"- **Наименование в базе:** `{sensor_name}`\n"
            f"- **Единицы измерения:** Температура — `{spec['temp_unit']}`, Термо-ЭДС — `{spec['unit']}`\n"
            f"- **Шаг температурной сетки:** {spec['grid_step']}\n"
            f"- **Источник данных:** {spec['data_source']}\n"
            f"- **Область применимости:** {spec['applicability']}\n"
            f"- **Примечание о полноте:** Для ТХА (тип K) массив содержит 56 опорных точек с шагом 50 °C / 20 °C "
            f"(частичная справочная выборка, а не полная таблица ГОСТ Р 8.585-2001 с шагом 1 °C). "
            f"Для типов T, E, N, S, R, B и вольфрам-рениевых пар в приложении реализован справочный подбор (раздел 10), "
            f"но табличная расчётная модель на Стенде №1 для них не включена."
        )
        df_gost = pd.DataFrame({
            "Температура раб. конца, °C": spec["temps"].astype(int),
            "Табличная Термо-ЭДС E(T) при T₀=0 °C, мВ": [f"{v:.3f}" for v in spec["values"]],
            f"Генерируемая ЭДС E_ген при T_cold={t_cold:.0f} °C, мВ": [f"{(v - e_cold):+.3f}" for v in spec["values"]]
        })
        st.dataframe(df_gost, use_container_width=True, height=240)


# =====================================================================
# 7. СТЕНД №2: ИССЛЕДОВАНИЕ ЭФФЕКТА ЗЕЕБЕКА В РАЗНОРОДНЫХ МЕТАЛЛАХ
# =====================================================================
else:
    st.title("Стенд №2: Исследование эффекта Зеебека в разнородных металлах (Термоэлектрические пары)")

    st.info(
        "ℹ️ **Об используемом приближении (п. 3.4 ТЗ):** Абсолютные коэффициенты Зеебека металлов $S_1$ и $S_2$ "
        "в данной модели являются **приближёнными справочными значениями при комнатной температуре ($\\approx 20\\text{ }^\\circ\\text{C}$)**. "
        "Расчёт по формуле $E = S_{\\text{пары}} \\cdot \\Delta T$ использует **линейное приближение с постоянным коэффициентом Зеебека**, "
        "которое физически строго справедливо только при малых перепадах температур $\\Delta T$. На широком интервале температур "
        "коэффициент Зеебека зависит от температуры $S(T)$, и точная ЭДС определяется интегралом "
        "$E = \\int_{T_{\\text{cold}}}^{T_{\\text{hot}}} [S_A(T) - S_B(T)]\\,dT$."
    )

    metal_names = list(METALS_DB.keys())
    metal_1 = st.sidebar.selectbox(
        "Металл / сплав ветви А (Термоэлектрод 1):",
        options=metal_names,
        index=0  # Хромель
    )
    metal_2 = st.sidebar.selectbox(
        "Металл / сплав ветви B (Термоэлектрод 2):",
        options=metal_names,
        index=6  # Копель
    )

    t_hot_s2 = float(st.sidebar.slider(
        "Температура горячего спая (T_hot), °C:",
        min_value=-100,
        max_value=800,
        value=520,
        step=10
    ))
    t_cold_s2 = float(st.sidebar.slider(
        "Температура холодного спая (T_cold), °C:",
        min_value=-100,
        max_value=200,
        value=20,
        step=10
    ))

    delta_t_val = t_hot_s2 - t_cold_s2
    s_metal1 = METALS_DB[metal_1]["seebeck"]
    s_metal2 = METALS_DB[metal_2]["seebeck"]
    s_pair = s_metal1 - s_metal2  # мкВ/°C

    e_hot_lin = (s_pair * t_hot_s2) / 1000.0
    e_cold_lin = (s_pair * t_cold_s2) / 1000.0

    t_kz_s2 = None
    e_kz_lin = None
    if circuit_fault_mode == "Паразитный спай (КЗ)":
        kz_min2 = int(min(t_cold_s2, t_hot_s2))
        kz_max2 = int(max(t_cold_s2, t_hot_s2))
        kz_def2 = int(round((t_cold_s2 + t_hot_s2) / 2.0, -1))
        if kz_min2 == kz_max2:
            t_kz_s2 = float(kz_min2)
        else:
            t_kz_s2 = float(st.sidebar.slider(
                "Температура перемычки КЗ (T_кз), °C:",
                min_value=kz_min2,
                max_value=kz_max2,
                value=int(np.clip(kz_def2, kz_min2, kz_max2)),
                step=10
            ))
        e_kz_lin = (s_pair * t_kz_s2) / 1000.0

    phys_s2 = evaluate_circuit_physics(
        e_hot=e_hot_lin,
        e_cold=e_cold_lin,
        t_hot=t_hot_s2,
        t_cold=t_cold_s2,
        fault_mode=circuit_fault_mode,
        t_short_c=t_kz_s2,
        e_short=e_kz_lin,
        open_meter_mode=open_circuit_meter_mode,
        r_cold_branch_ohm=r_cold_branch_input,
        r_hot_loop_ohm=r_hot_loop_input,
        r_bridge_ohm=r_bridge_input
    )

    if metal_1 == metal_2:
        st.info("ℹ️ Выбраны одинаковые металлы ($S_1 = S_2$). По закону однородной цепи в контуре из одного металла термо-ЭДС равна нулю ($S_{\\text{пары}} = 0$).")

    st.latex(
        rf"S_{{\text{{пары}}}} \approx S_A(20^\circ\text{{C}}) - S_B(20^\circ\text{{C}}) = "
        rf"({s_metal1:+.1f}) - ({s_metal2:+.1f}) = {s_pair:+.1f}\text{{ мкВ/}}^\circ\text{{C}}, \quad "
        rf"E_{{\text{{лин}}}} = S_{{\text{{пары}}}} \cdot (T_{{\text{{hot}}}} - T_{{\text{{cold}}}}) = "
        rf"{phys_s2['e_gen_mv']:+.3f}\text{{ мВ}}"
    )

    if phys_s2["warning"]:
        st.warning(f"⚠️ **Физическая диагностика цепи:** {phys_s2['warning']}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        f"S₁ ({metal_1.split('(')[0].strip()})",
        f"{s_metal1:+.1f} мкВ/°C",
        delta="Приближённо при ~20 °C"
    )
    c2.metric(
        f"S₂ ({metal_2.split('(')[0].strip()})",
        f"{s_metal2:+.1f} мкВ/°C",
        delta=f"S_пары = {s_pair:+.1f} мкВ/°C"
    )
    c3.metric(
        "Генерируемая ЭДС E_ген (лин.)",
        f"{phys_s2['e_gen_mv']:+.3f} мВ",
        delta=f"ΔT = {delta_t_val:+.0f} °C ({t_hot_s2:.0f} − {t_cold_s2:.0f} °C)"
    )
    c4.metric(
        "Напряжение на приборе U_приб",
        phys_s2["u_meter_str"],
        delta=phys_s2["current_status"]
    )

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.subheader("Сравнение линейного приближения и нелинейной табличной НСХ")
        t_grid_s2 = np.linspace(-100, 800, 91)
        e_lin_arr = (s_pair * (t_grid_s2 - t_cold_s2)) / 1000.0
        is_mobile_view = (chart_display_mode == "Смартфон (320–430 px)")

        fig_stand2 = go.Figure()
        all_y_stand2 = [e_lin_arr, np.array([0.0, phys_s2["e_gen_mv"]])]

        fig_stand2.add_trace(go.Scatter(
            x=t_grid_s2, y=e_lin_arr, mode="lines",
            name=f"Линейная (S = {s_pair:+.1f} мкВ/°C)",
            line=dict(color="#80ed99", width=3.2),
            hovertemplate="T_hot = %{x:.0f} °C<br>E_лин = %{y:+.3f} мВ<extra>Линейное приближение</extra>"
        ))

        pair_tuple = (metal_1.split("(")[0].strip(), metal_2.split("(")[0].strip())
        gost_match_key = None
        gost_sign = 1.0
        if pair_tuple == ("Хромель", "Копель"):
            gost_match_key, gost_sign = "ТХК (тип L, Хромель-Копель, таблица с шагом 10 °C)", 1.0
        elif pair_tuple == ("Копель", "Хромель"):
            gost_match_key, gost_sign = "ТХК (тип L, Хромель-Копель, таблица с шагом 10 °C)", -1.0
        elif pair_tuple == ("Хромель", "Алюмель"):
            gost_match_key, gost_sign = "ТХА (тип K, Хромель-Алюмель, справочная выборка 50/20 °C)", 1.0
        elif pair_tuple == ("Алюмель", "Хромель"):
            gost_match_key, gost_sign = "ТХА (тип K, Хромель-Алюмель, справочная выборка 50/20 °C)", -1.0
        elif pair_tuple == ("Железо", "Константан"):
            gost_match_key, gost_sign = "ТЖК (тип J, Железо-Константан, таблица с шагом 10 °C)", 1.0
        elif pair_tuple == ("Константан", "Железо"):
            gost_match_key, gost_sign = "ТЖК (тип J, Железо-Константан, таблица с шагом 10 °C)", -1.0

        comparison_caption = None
        if gost_match_key is not None:
            e_ref_cold = gost_sign * calculate_nominal_emf(gost_match_key, t_cold_s2)
            e_gost_arr = np.array([gost_sign * calculate_nominal_emf(gost_match_key, t_val) - e_ref_cold for t_val in t_grid_s2])
            e_gost_hot = gost_sign * calculate_nominal_emf(gost_match_key, t_hot_s2) - e_ref_cold
            all_y_stand2.append(e_gost_arr)
            fig_stand2.add_trace(go.Scatter(
                x=t_grid_s2, y=e_gost_arr, mode="lines",
                name=f"Табличная НСХ ({THERMOCOUPLES_DB[gost_match_key]['short_code']})",
                line=dict(color="#00b4d8", width=2.5, dash="dash"),
                hovertemplate="T_hot = %{x:.0f} °C<br>E_табл = %{y:+.3f} мВ<extra>Табличная НСХ</extra>"
            ))
            comparison_caption = (
                f"📌 **Сравнение моделей при $T_{{\\text{{hot}}}} = {t_hot_s2:.0f}\\text{{ }}^\\circ\\text{{C}}$, "
                f"$T_{{\\text{{cold}}}} = {t_cold_s2:.0f}\\text{{ }}^\\circ\\text{{C}}$:** "
                f"линейное приближение даёт $E_{{\\text{{лин}}}} = {phys_s2['e_gen_mv']:+.3f}\\text{{ мВ}}$, "
                f"табличная нелинейная характеристика даёт $E_{{\\text{{табл}}}} = {e_gost_hot:+.3f}\\text{{ мВ}}$ "
                f"(расхождение из-за зависимости $S(T)$ составляет ${abs(phys_s2['e_gen_mv'] - e_gost_hot):.3f}\\text{{ мВ}}$)."
            )

        fig_stand2.add_trace(go.Scatter(
            x=[t_cold_s2], y=[0.0],
            mode="markers+text", name="Холодный спай (T_cold)",
            text=[f"T_cold ({t_cold_s2:.0f}°C)"],
            textposition="bottom right",
            textfont=dict(size=11, color="#4cc9f0"),
            marker=dict(size=10, color="#00b4d8", symbol="circle", line=dict(width=1.5, color="white")),
            hovertemplate=f"Холодный спай T_cold = {t_cold_s2:.0f} °C<br>E = 0.000 мВ<extra></extra>"
        ))

        fig_stand2.add_trace(go.Scatter(
            x=[t_hot_s2], y=[phys_s2["e_gen_mv"]],
            mode="markers+text", name="Рабочая точка (E_ген)",
            text=[f"T_hot ({phys_s2['e_gen_mv']:+.1f} мВ)"] if is_mobile_view else [f"  T_hot = {t_hot_s2:.0f} °C ({phys_s2['e_gen_mv']:+.2f} мВ)"],
            textposition="top left",
            textfont=dict(size=11, color="#ff6b6b"),
            marker=dict(size=12, color="#ff4d4d", symbol="diamond", line=dict(width=1.5, color="white")),
            hovertemplate=(
                f"Горячий спай T_hot = {t_hot_s2:.0f} °C<br>"
                f"ΔT = {delta_t_val:+.0f} °C<br>"
                f"E_ген (лин.) = {phys_s2['e_gen_mv']:+.3f} мВ<extra></extra>"
            )
        ))

        if circuit_fault_mode == "Паразитный спай (КЗ)" and t_kz_s2 is not None:
            all_y_stand2.append(np.array([phys_s2["u_meter_mv"]]))
            fig_stand2.add_trace(go.Scatter(
                x=[t_kz_s2], y=[phys_s2["u_meter_mv"]],
                mode="markers+text", name="Точка КЗ (U_приб)",
                text=[f"T_кз ({phys_s2['u_meter_mv']:+.1f} мВ)"],
                textposition="bottom right",
                textfont=dict(size=11, color="#ff9f1c"),
                marker=dict(size=12, color="#ff9f1c", symbol="x", line=dict(width=2, color="white")),
                hovertemplate=(
                    f"Паразитный спай T_кз = {t_kz_s2:.0f} °C<br>"
                    f"U_приб = {phys_s2['u_meter_mv']:+.3f} мВ<extra></extra>"
                )
            ))

        if "ai_alloy" in st.session_state:
            ai = st.session_state["ai_alloy"]
            a1, a2, a3 = ai["coeffs"]["a1"], ai["coeffs"]["a2"], ai["coeffs"]["a3"]
            e_ai_c = a1 * t_cold_s2 + a2 * (t_cold_s2 ** 2) + a3 * (t_cold_s2 ** 3)
            e_ai_arr = (a1 * t_grid_s2 + a2 * (t_grid_s2 ** 2) + a3 * (t_grid_s2 ** 3)) - e_ai_c
            all_y_stand2.append(e_ai_arr)
            fig_stand2.add_trace(go.Scatter(
                x=t_grid_s2, y=e_ai_arr, mode="lines",
                name=f"Условная НСХ ({ai['s_target']} мкВ/°C)",
                line=dict(color="#ff9f1c", width=2.5, dash="dot"),
                hovertemplate="T_hot = %{x:.0f} °C<br>E_мод = %{y:+.3f} мВ<extra>Условная НСХ</extra>"
            ))

        plotly_cfg2, angle_note2 = configure_adaptive_plotly_layout(
            fig=fig_stand2,
            x_main=t_grid_s2,
            y_main=e_lin_arr,
            all_y_arrays=all_y_stand2,
            x_title="Температура T_hot, °C",
            y_title=f"Термо-ЭДС (отн. {t_cold_s2:.0f} °C), мВ",
            display_mode=chart_display_mode
        )
        st.plotly_chart(fig_stand2, use_container_width=True, config=plotly_cfg2)
        st.caption(f"📐 {angle_note2}")
        if comparison_caption:
            st.caption(comparison_caption)

        st.caption(
            f"**Справка по материалам:** 1) *{metal_1}*: {METALS_DB[metal_1]['description']} "
            f"2) *{metal_2}*: {METALS_DB[metal_2]['description']}"
        )

    with col_r:
        st.subheader("3D-схема термоэлектрического контура")
        components.html(
            render_3d_stand2_pair(
                metal1_name=metal_1.split("(")[0].strip(),
                metal2_name=metal_2.split("(")[0].strip(),
                col1_hex=METALS_DB[metal_1]["three_hex"],
                col2_hex=METALS_DB[metal_2]["three_hex"],
                s_pair=s_pair,
                delta_t=delta_t_val,
                e_gen_mv=phys_s2["e_gen_mv"],
                u_meter_mv=phys_s2["u_meter_mv"],
                u_meter_str=phys_s2["u_meter_str"],
                fault_state=circuit_fault_mode
            ),
            height=430
        )

st.markdown("---")


# =====================================================================
# 8. СПРАВОЧНЫЙ ПОМОЩНИК И ГЕНЕРАТОР УСЛОВНОЙ НСХ
# =====================================================================
st.subheader("📘 Справочный помощник по термоэлектрическим явлениям и Генератор условной НСХ")
st.caption(
    "Раздел работает на основе локальной базы проверенных физических разборов и расчётных формул "
    "(внешняя генеративная языковая модель не используется)."
)


def build_hypothetical_thermoelectric(target_s_uv: float) -> dict:
    """
    Генератор условной НСХ: формирует учебную полиномиальную модель E(T) = a1*T + a2*T^2 + a3*T^3
    с заданным начальным наклоном S_0 (мкВ/°C) и фиксированными модельными коэффициентами нелинейности.
    """
    a1 = target_s_uv / 1000.0
    sign = 1.0 if target_s_uv >= 0 else -1.0
    a2 = sign * 1.45e-5
    a3 = -sign * 4.20e-9
    t_vec = np.linspace(0, 1000, 200)
    e_vec = a1 * t_vec + a2 * (t_vec ** 2) + a3 * (t_vec ** 3)
    return {
        "name": f"Условная-НСХ-S{int(abs(target_s_uv))}",
        "s_target": round(target_s_uv, 2),
        "coeffs": {"a1": a1, "a2": a2, "a3": a3},
        "t": t_vec,
        "e": e_vec
    }


with st.expander("📐 Генератор условной НСХ (расчёт учебной полиномиальной модели)", expanded=False):
    st.warning(
        "⚠️ **Предупреждение:** Полученная характеристика является математической моделью "
        "и не подтверждает существование реального термоэлектрического материала с такими свойствами."
    )
    col_gen1, col_gen2 = st.columns([2, 1])
    with col_gen1:
        desired_s = st.number_input(
            "Задайте начальный коэффициент Зеебека S₀ при 0 °C (мкВ/°C):",
            min_value=-250.0,
            max_value=250.0,
            value=75.0,
            step=5.0
        )
    with col_gen2:
        st.write("")
        st.write("")
        if st.button("Построить условную НСХ"):
            st.session_state["ai_alloy"] = build_hypothetical_thermoelectric(desired_s)
            st.rerun()

    if "ai_alloy" in st.session_state:
        ai_cur = st.session_state["ai_alloy"]
        c_a1 = ai_cur["coeffs"]["a1"]
        c_a2 = ai_cur["coeffs"]["a2"]
        c_a3 = ai_cur["coeffs"]["a3"]
        st.info(
            f"Построена условная математическая модель **{ai_cur['name']}** ($S_0 = {ai_cur['s_target']}$ мкВ/°C, "
            f"где $a_1 = S_0 / 1000$, а коэффициенты $a_2, a_3$ заданы как учебные константы нелинейности)."
        )
        st.latex(
            rf"E(T) = a_1 T + a_2 T^2 + a_3 T^3 = "
            rf"{c_a1:.5f}\,T + ({c_a2:.2e})\,T^2 + ({c_a3:.2e})\,T^3 \text{{ [мВ]}}"
        )

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "Добро пожаловать в **Справочный помощник по термоэлектрическим явлениям**!\n\n"
                "Выберите или введите интересующий вопрос по физике эффекта Зеебека (ответы формируются по базе знаний практикума):\n"
                "- *«Почему при равенстве температур спаев Термо-ЭДС равна нулю?»*\n"
                "- *«Как изменится ЭДС, если удлинить провода?»*\n"
                "- *«Что такое закон Вольта для последовательной цепи металлов?»*\n"
                "- *«Построй условную НСХ для 85 мкВ/°C»*"
            )
        }
    ]

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input(
    "Введите вопрос по теме (например: 'Что такое закон Вольта?' или 'Модель НСХ 90 мкВ/°C')..."
)

if user_query:
    st.session_state["messages"].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    q_low = user_query.lower()
    num_match = re.search(r"([-+]?\d+(?:[.,]\d+)?)", q_low)

    if any(k in q_low for k in ["равенств", "нулю", "ноль", "одинаков"]):
        reply = (
            "**Физическое объяснение (Равенство температур спаев $T_{\\text{hot}} = T_{\\text{cold}}$):**\n\n"
            "В замкнутом контуре из двух металлов $A$ и $B$ результирующая Термо-ЭДС определяется интегралом:\n"
            "$$E = \\int_{T_{\\text{cold}}}^{T_{\\text{hot}}} \\left(S_A(T) - S_B(T)\\right) dT$$\n"
            "При $T_{\\text{hot}} = T_{\\text{cold}}$ верхний и нижний пределы интегрирования совпадают, поэтому интеграл "
            "тождественно равен нулю ($E = 0$). Термодинамически это прямое следствие **Второго начала термодинамики**: "
            "в изотермическом контуре невозможно непрерывное преобразование теплоты в электрическую работу без перепада температур."
        )
    elif any(k in q_low for k in ["удлин", "длин", "провод", "сечен"]):
        reply = (
            "**Физическое объяснение (Влияние длины и сечения проводников):**\n\n"
            "Если проводники термопары однородны по химическому составу, то **генерируемая Термо-ЭДС не изменится** при удлинении проводов. "
            "Причина в том, что $E = \\int_{T_{\\text{cold}}}^{T_{\\text{hot}}} S_{AB}(T)\\,dT$ является функцией только граничных температур "
            "концов $T_{\\text{hot}}$ и $T_{\\text{cold}}$, а не градиента $\\nabla T$ по отдельности. Однако при увеличении длины $l$ возрастает "
            "внутреннее омическое сопротивление контура $R_{\\text{тп}} = \\rho \\frac{l}{S_{\\text{сеч}}}$, что увеличивает падение напряжения "
            "при протекании тока через низкоомный прибор."
        )
    elif any(k in q_low for k in ["вольт", "третьего", "третий", "последоват"]):
        reply = (
            "**Физическое объяснение (Закон Вольта / Закон промежуточных металлов):**\n\n"
            "Согласно закону промежуточных металлов, включение в термоэлектрический контур любого третьего проводника $C$ (например, медных выводов "
            "и входной цепи вольтметра) **не изменяет результирующую Термо-ЭДС**, если оба конца этого третьего проводника находятся "
            "при одинаковой температуре $T_{\\text{cold}}$:\n"
            "$$\\int_{T_{\\text{cold}}}^{T_{\\text{cold}}} S_C(T)\\,dT = 0$$\n"
            "Дополнительные термо-ЭДС на контактах «Металл А — Медь» и «Медь — Металл B» взаимно компенсируют друг друга."
        )
    elif num_match and any(k in q_low for k in ["модел", "нсх", "сплав", "зеебек", "мкв", "коэфф", "постро"]):
        s_val = float(num_match.group(1).replace(",", "."))
        s_val = float(np.clip(s_val, -300.0, 300.0))
        alloy_data = build_hypothetical_thermoelectric(s_val)
        st.session_state["ai_alloy"] = alloy_data
        c1, c2, c3 = alloy_data["coeffs"]["a1"], alloy_data["coeffs"]["a2"], alloy_data["coeffs"]["a3"]

        reply = (
            f"Построена условная математическая характеристика **`{alloy_data['name']}`** для $S_0 = {alloy_data['s_target']}$ мкВ/°C "
            f"(кривая добавлена на графики Стенда №1 и Стенда №2):\n\n"
            f"- **Линейный коэффициент $a_1 = S_0 / 1000$:** `{c1:.5f}` мВ/°C\n"
            f"- **Заданный модельный коэффициент $a_2$:** `{c2:.2e}` мВ/°C²\n"
            f"- **Заданный модельный коэффициент $a_3$:** `{c3:.2e}` мВ/°C³\n\n"
            f"$$E(T) = {c1:.5f}\\,T + ({c2:.2e})\\,T^2 + ({c3:.2e})\\,T^3\\text{{ [мВ]}}$$\n\n"
            f"> *Предупреждение: полученная характеристика является математической моделью и не подтверждает "
            f"существование реального термоэлектрического материала с такими свойствами.*"
        )
    else:
        reply = (
            "В справочной базе помощника доступны разборы тем: **равенство температур спаев**, **влияние длины проводников**, "
            "**закон промежуточных металлов (Вольта)**, а также расчёт **условной полиномиальной модели НСХ** по заданному "
            "коэффициенту Зеебека (например: *«Модель НСХ 65 мкВ/°C»*)."
        )

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)


# =====================================================================
# 9. ТЕОРЕТИЧЕСКИЙ РАЗДЕЛ: «ТЕРМО-ЭДС. ЭФФЕКТ ЗЕЕБЕКА»
# =====================================================================
st.markdown("---")


def render_theory_image(rel_path: str, caption: str) -> None:
    """
    Отображает иллюстрацию из папки assets с сохранением пропорций, без растягивания
    и с поддержкой мобильных и настольных экранов.
    """
    found_path = resolve_asset_path(rel_path)
    if found_path is not None:
        img_bytes = found_path.read_bytes()
        b64_encoded = base64.b64encode(img_bytes).decode("utf-8")
        st.markdown(
            f"""
            <div style="text-align: center; margin: 1.0rem auto; max-width: 760px;">
                <img src="data:image/png;base64,{b64_encoded}"
                     alt="{caption}"
                     style="max-width: 100%; height: auto; object-fit: contain; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12);" />
                <div style="font-style: italic; color: #adb5bd; font-size: 0.92rem; margin-top: 0.45rem;">
                    {caption}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(
            f"🖼️ Изображение `{rel_path}` не найдено. "
            f"Поместите папку `assets` рядом с `fasd.py` (или в репозиторий GitHub)."
        )
        st.markdown(f"*{caption}*")


def render_stage_1() -> None:
    st.markdown("## Этап 1. Введение и история открытия эффекта Зеебека")

    st.markdown("### 1.1. Что такое термоэлектрические явления")
    st.markdown(
        "Термоэлектрические явления — это группа эффектов, связывающих тепловые и электрические процессы "
        "в проводниках и полупроводниках.\n\n"
        "Одно из наиболее известных явлений этой группы — **эффект Зеебека**. В замкнутой цепи из двух "
        "разнородных проводников, если места их соединения (спаи) имеют разную температуру, возникает "
        "электродвижущая сила. Её называют **термоэлектродвижущей силой**, или **термо-ЭДС**.\n\n"
        "Эффект был открыт в 1821 году. Сегодня он лежит в основе одного из распространённых способов "
        "измерения температуры — с помощью термопар."
    )

    st.markdown("### 1.2. Почему тема имеет практическое значение")
    st.markdown(
        "Термопары применяются в металлургии, энергетике, химической промышленности, авиации и научных "
        "исследованиях. В реферате отмечено, что они могут работать в широком диапазоне температур — от "
        "значений, близких к абсолютному нулю, до температур свыше двух тысяч градусов. Термопары имеют "
        "малые размеры и не нуждаются во внешнем питании.\n\n"
        "Эффект Зеебека и обратный ему эффект Пельтье также лежат в основе термоэлектрических генераторов "
        "и охладителей."
    )

    render_theory_image(
        "assets/00_thermoelectric_circuit_illustration.png",
        "Рисунок 1. Иллюстрация термоэлектрической цепи. Конкретные материалы и количественные значения в изображении условны; физический смысл поясняется текстом ниже."
    )

    st.markdown("### 1.3. Научная обстановка начала XIX века")
    st.markdown(
        "В 1800 году Алессандро Вольта создал «вольтов столб» — первый источник постоянного тока. Это дало "
        "физикам возможность систематически изучать электрические явления. В то время учёные по-разному "
        "объясняли происхождение тока: одни связывали его с контактом разнородных металлов, другие — "
        "с химическими реакциями.\n\n"
        "В 1820 году Ханс Кристиан Эрстед обнаружил, что проводник с током отклоняет магнитную стрелку. "
        "Это открытие усилило интерес к связи электричества и магнетизма."
    )

    st.markdown("### 1.4. Томас Зеебек и его опыт")
    st.markdown(
        "Опыты, приведшие к открытию эффекта, Томас Зеебек проводил в Берлине в 1821–1823 годах. В известном "
        "опыте он спаял висмутовый и медный проводники в замкнутое кольцо, а внутрь кольца поместил магнитную "
        "стрелку компаса.\n\n"
        "Когда оба спая имели одинаковую температуру, стрелка оставалась неподвижной. При нагревании одного "
        "спая стрелка отклонялась. Чем больше была разность температур, тем сильнее становилось отклонение. "
        "При перестановке горячего и холодного спаев направление отклонения менялось.\n\n"
        "Сначала Зеебек объяснял результат намагничиванием металлов и называл явление термомагнитным эффектом. "
        "В 1823 году Эрстед дал верное объяснение: разность температур создаёт в цепи электрический ток, а этот "
        "ток отклоняет магнитную стрелку."
    )

    render_theory_image(
        "assets/01_experiment_seebeck.png",
        "Рисунок 2. Упрощённая схема опыта Зеебека, описанного в реферате."
    )

    st.markdown("### 1.5. Дальнейшее развитие термоэлектричества")
    st.markdown(
        "В реферате отмечены следующие этапы развития исследований:\n\n"
        "- **1823 год:** Ж. Фурье и Х. Эрстед построили термоэлектрическую батарею из чередующихся сурьмяных и висмутовых пластин.\n"
        "- **1829 год:** Л. Нобили собрал термостолбик из последовательно соединённых термопар; позднее он применялся для изучения теплового (инфракрасного) излучения.\n"
        "- **1834 год:** Жан Шарль Пельтье обнаружил обратное явление — нагревание или охлаждение спая при пропускании тока.\n"
        "- **1838 год:** Э. Х. Ленц продемонстрировал тепловое действие эффекта Пельтье.\n"
        "- **1851 год:** Г. Магнус установил, что термо-ЭДС не зависит от распределения температуры вдоль проводников между спаями.\n"
        "- **1851–1857 годы:** У. Томсон связал эффекты Зеебека и Пельтье и предсказал эффект, получивший его имя.\n"
        "- **1886 год:** А. Л. Ле Шателье предложил термопару платина–платинородий.\n"
        "- **1930-е годы:** школа А. Ф. Иоффе показала перспективность полупроводников для термоэлектрических генераторов и холодильников.\n\n"
        "**Главная мысль этапа:** эффект Зеебека был обнаружен по магнитному действию тока, возникающего в цепи при разности температур спаев. Позднее явление стало основой практических температурных измерений.\n\n"
        "*Материал по реферату: введение и глава 1, страницы 1–4.*"
    )


def render_stage_2() -> None:
    st.markdown("## Этап 2. Эффект Зеебека и физическая природа термо-ЭДС")

    st.markdown("### 2.1. Условие возникновения термо-ЭДС")
    st.markdown(
        "Эффект Зеебека состоит в возникновении ЭДС в цепи из разнородных проводников, если места их соединения "
        "(спаи) имеют разные температуры. В замкнутой цепи возникающий ток называют **термотоком**.\n\n"
        "При небольшой разности температур термо-ЭДС приблизительно пропорциональна разности температур спаев:"
    )
    st.latex(r"E = \alpha \cdot (T_1-T_2),")
    st.markdown(
        "где:\n\n"
        "- $E$ — термо-ЭДС;\n"
        "- $T_1$ и $T_2$ — температуры спаев;\n"
        "- $\\alpha$ — коэффициент термо-ЭДС (коэффициент Зеебека) данной пары проводников.\n\n"
        "Коэффициент Зеебека измеряется в вольтах на кельвин; на практике часто используют микровольты на кельвин.\n\n"
        "В общем случае коэффициент Зеебека зависит от температуры. Поэтому для пары проводников A и B термо-ЭДС "
        "определяют интегрированием:"
    )
    st.latex(r"E = \int_{T_2}^{T_1}[\alpha_B(T)-\alpha_A(T)]\,dT,")
    st.markdown("где $\\alpha_A$ и $\\alpha_B$ — коэффициенты Зеебека соответствующих проводников.")

    render_theory_image(
        "assets/04_seebeck_graph.png",
        "Рисунок 3. Схематическая линейная зависимость для небольшого диапазона температур, когда коэффициент можно считать приблизительно постоянным. Числовой масштаб не задан."
    )

    st.markdown("### 2.2. Физическая причина эффекта")
    st.markdown(
        "Физическая причина эффекта — **диффузия носителей заряда**. В нагретой части проводника электроны или "
        "дырки обладают большей энергией и концентрацией, поэтому диффундируют к холодному концу.\n\n"
        "На холодном конце накапливается заряд. Возникающее электрическое поле в стационарном состоянии "
        "уравновешивает диффузионный поток. Разность потенциалов зависит от материала проводника. Поэтому в цепи "
        "из двух разных проводников соответствующие разности потенциалов не компенсируют друг друга полностью, "
        "и возникает итоговая термо-ЭДС.\n\n"
        "В реферате также отмечены дополнительные вклады: температурная зависимость контактной разности потенциалов "
        "и, при низких температурах, увлечение электронов фононами, движущимися от горячего конца к холодному."
    )

    render_theory_image(
        "assets/02_carrier_diffusion.png",
        "Рисунок 4. Пояснение диффузии носителей заряда. Схема показывает общее направление процесса, описанного в реферате."
    )

    st.markdown("### 2.3. Коэффициент Зеебека и материалы")
    st.markdown(
        "Знак коэффициента Зеебека зависит от типа носителей заряда: у электронных проводников он отрицателен, "
        "у дырочных — положителен.\n\n"
        "Величина коэффициента сильно различается у разных материалов. В реферате приведены ориентировочные значения:\n\n"
        "- у большинства металлов — единицы и десятки мкВ/К;\n"
        "- у меди — около 2 мкВ/К;\n"
        "- у висмута — несколько десятков мкВ/К по модулю;\n"
        "- у полупроводников — сотни мкВ/К;\n"
        "- для обычных материалов при комнатной температуре приводится широкий примерный интервал от −100 до +1000 мкВ/К.\n\n"
        "**Главная мысль этапа:** термо-ЭДС возникает из-за температурного движения носителей заряда и зависит от разности температур, а также от свойств материалов проводников.\n\n"
        "*Материал по реферату: глава 2.1, страницы 5–6.*"
    )


def render_stage_3() -> None:
    st.markdown("## Этап 3. Связанные термоэлектрические явления: эффекты Пельтье и Томсона")

    st.markdown("### 3.1. Эффект Пельтье")
    st.markdown(
        "Эффект Пельтье — обратное по отношению к эффекту Зеебека явление. Если пропустить электрический ток "
        "через контакт двух разнородных проводников, то помимо джоулева тепла в контакте выделяется или "
        "поглощается дополнительная тепловая мощность $\\dot{Q}$:"
    )
    st.latex(r"\dot{Q} = \Pi \cdot I, \qquad Q = \dot{Q} \cdot t = \Pi \cdot I \cdot t,")
    st.markdown(
        "где:\n\n"
        "- $\\dot{Q}$ — тепловая мощность Пельтье, выделяемая или поглощаемая в контакте в единицу времени, **Вт** (Дж/с);\n"
        "- $Q$ — количество теплоты за время $t$ при постоянном токе, **Дж**;\n"
        "- $I$ — сила электрического тока, **А**;\n"
        "- $\\Pi$ — коэффициент Пельтье данной пары проводников, **В**.\n\n"
        "**Условия применимости и знак:** формула описывает обратимый тепловой эффект в спае отдельно от "
        "необратимого джоулева нагрева ($\\dot{Q}_{\\text{Дж}} = I^2 R$). В отличие от закона Джоуля–Ленца, "
        "мощность Пельтье линейна по току $I$: при изменении направления тока знак $\\dot{Q}$ меняется "
        "(нагрев спая сменяется охлаждением). На этом явлении основаны термоэлектрические охладители — модули Пельтье."
    )

    st.markdown("### 3.2. Эффект Томсона")
    st.markdown(
        "Эффект Томсона — выделение или поглощение дополнительной тепловой мощности в однородном проводнике, "
        "по которому течёт ток при наличии градиента температуры:"
    )
    st.latex(r"\dot{Q} = \tau \cdot I \cdot \Delta T, \qquad Q = \tau \cdot I \cdot \Delta T \cdot t,")
    st.markdown(
        "где:\n\n"
        "- $\\dot{Q}$ — тепловая мощность Томсона на участке с перепадом температур $\\Delta T$, **Вт**;\n"
        "- $Q$ — соответствующее количество теплоты за время $t$, **Дж**;\n"
        "- $\\tau$ — коэффициент Томсона материала, **В/К**;\n"
        "- $I$ — сила тока, **А**;\n"
        "- $\\Delta T$ — разность температур на концах участка проводника, **К** (или °C).\n\n"
        "**Условия применимости и знак:** соотношение применимо для участка со слабо меняющимся коэффициентом $\\tau$; "
        "знак эффекта (выделение или поглощение теплоты) меняется на противоположный при смене направления тока $I$ "
        "относительно направления градиента температуры."
    )

    st.markdown("### 3.3. Связь коэффициентов")
    st.markdown("В реферате приведены соотношения Кельвина, связывающие все три коэффициента через абсолютную температуру $T$ (в К):")
    st.latex(r"\Pi = \alpha T, \qquad \tau = T\frac{d\alpha}{dT}.")
    st.markdown(
        "Таким образом, эффекты Зеебека, Пельтье и Томсона рассматриваются как связанные термоэлектрические "
        "явления. В дальнейшем основной практический акцент сделан на эффекте Зеебека как основе работы термопар."
    )

    render_theory_image(
        "assets/05_peltier_thomson.png",
        "Рисунок 5. Иллюстративное сопоставление явлений, описанных в реферате."
    )

    st.markdown(
        "**Главная мысль этапа:** эффект Зеебека связан с возникновением электрического сигнала из-за разности "
        "температур, эффект Пельтье — с выделением или поглощением тепловой мощности при прохождении тока через контакт, "
        "эффект Томсона — с тепловой мощностью тока в однородном проводнике при градиенте температуры.\n\n"
        "*Материал по реферату: глава 2.2, страницы 6–7.*"
    )


def render_stage_4() -> None:
    st.markdown("## Этап 4. Термопары: устройство и принцип действия")

    st.markdown("### 4.1. Устройство термопары")
    st.markdown(
        "**Термопара** (термоэлектрический преобразователь) — датчик температуры, состоящий из двух разнородных "
        "проводников, называемых термоэлектродами и соединённых с одного конца.\n\n"
        "- Соединение, помещаемое в зону измерения, называется рабочим (горячим) спаем.\n"
        "- Свободные концы термоэлектродов подключаются к измерительному прибору.\n"
        "- Прибор измеряет термо-ЭДС, а температуру рабочего спая определяют по градуировочной таблице или "
        "формуле, установленной для данного типа термопары."
    )

    render_theory_image(
        "assets/03_thermocouple_measurement.png",
        "Рисунок 6. Упрощённая схема измерения термо-ЭДС термопарой."
    )

    st.markdown("### 4.2. Измерение и компенсация холодного спая")
    st.markdown(
        "Термо-ЭДС зависит не от одной абсолютной температуры рабочего спая, а от разности температур рабочего "
        "спая и свободных концов. Поэтому температуру свободных концов, называемых холодным спаем, необходимо знать.\n\n"
        "Раньше свободные концы помещали в сосуд с тающим льдом при 0 °C. В современных приборах температуру клемм "
        "измеряют термистором или термометром сопротивления и автоматически вводят поправку. Это называется "
        "**компенсацией холодного спая**.\n\n"
        "Если измерительный прибор удалён от места измерения, для удлинения термопары применяют компенсационные "
        "провода. В области невысоких температур их термо-ЭДС практически такая же, как у основных термоэлектродов.\n\n"
        "ЭДС стандартных термопар невелика: в реферате приведено значение порядка 10–70 мкВ на градус. Поэтому "
        "используют чувствительные вольтметры или усилители. Для увеличения сигнала термопары могут соединять "
        "последовательно, получая термобатарею (термостолбик)."
    )

    st.markdown("### 4.3. Законы термоэлектрических цепей")
    st.markdown(
        "Работа термопар описывается несколькими правилами.\n\n"
        "**Закон однородной цепи.** В цепи из одного однородного проводника нагревом нельзя создать термоток. "
        "Для разнородной пары важны температуры спаев; распределение температуры вдоль термоэлектродов между "
        "спаями не определяет термо-ЭДС.\n\n"
        "**Закон промежуточных металлов.** Включение в цепь третьего проводника не меняет ЭДС, если оба его "
        "конца находятся при одинаковой температуре. Это позволяет подключать к термопаре измерительный прибор.\n\n"
        "**Закон промежуточных температур.** ЭДС термопары между температурами $T_1$ и $T_3$ равна сумме ЭДС "
        "между $T_1$ и $T_2$, а также между $T_2$ и $T_3$.\n\n"
        "**Главная мысль этапа:** термопара преобразует температурную разность в небольшую термо-ЭДС. Для "
        "определения температуры учитывают характеристику конкретного типа термопары и температуру свободных концов.\n\n"
        "*Материал по реферату: глава 3.1–3.2, страницы 7–8.*"
    )


def render_stage_5() -> None:
    st.markdown("## Этап 5. Материалы и стандартные типы термопар")

    st.markdown("### 5.1. Требования к материалам")
    st.markdown(
        "К материалам термоэлектродов предъявляют следующие требования:\n\n"
        "- достаточно большая и воспроизводимая термо-ЭДС;\n"
        "- по возможности близкая к линейной зависимость от температуры;\n"
        "- стабильность градуировки при длительной работе;\n"
        "- жаростойкость и коррозионная стойкость;\n"
        "- высокая температура плавления;\n"
        "- пластичность, позволяющая получать проволоку и соединять спаи;\n"
        "- малое электрическое сопротивление;\n"
        "- воспроизводимость свойств от партии к партии;\n"
        "- приемлемая стоимость.\n\n"
        "Универсального материала, который одинаково хорошо удовлетворяет всем требованиям, нет. Поэтому "
        "используют разные пары материалов для разных температурных диапазонов и условий эксплуатации."
    )

    st.markdown("### 5.2. Основные стандартные типы")
    st.markdown(
        "В реферате приведена таблица типов термопар, их материалов, табличных температурных диапазонов "
        "и ориентировочной чувствительности."
    )

    tc_types_df = pd.DataFrame([
        {
            "Тип": "K",
            "Обозначение по ГОСТ Р 8.585-2001": "ТХА",
            "Положительный / отрицательный электрод": "Хромель (Ni–Cr) / алюмель (Ni–Al–Mn–Si)",
            "Диапазон по таблицам, °C": "−270…+1372",
            "Чувствительность, мкВ/°C": "около 41"
        },
        {
            "Тип": "J",
            "Обозначение по ГОСТ Р 8.585-2001": "ТЖК",
            "Положительный / отрицательный электрод": "Железо / константан",
            "Диапазон по таблицам, °C": "−210…+1200",
            "Чувствительность, мкВ/°C": "около 55"
        },
        {
            "Тип": "T",
            "Обозначение по ГОСТ Р 8.585-2001": "ТМК",
            "Положительный / отрицательный электрод": "Медь / константан",
            "Диапазон по таблицам, °C": "−270…+400",
            "Чувствительность, мкВ/°C": "около 43"
        },
        {
            "Тип": "E",
            "Обозначение по ГОСТ Р 8.585-2001": "ТХКн",
            "Положительный / отрицательный электрод": "Хромель / константан",
            "Диапазон по таблицам, °C": "−270…+1000",
            "Чувствительность, мкВ/°C": "около 68"
        },
        {
            "Тип": "N",
            "Обозначение по ГОСТ Р 8.585-2001": "ТНН",
            "Положительный / отрицательный электрод": "Нихросил (Ni–Cr–Si) / нисил (Ni–Si–Mg)",
            "Диапазон по таблицам, °C": "−270…+1300",
            "Чувствительность, мкВ/°C": "около 39"
        },
        {
            "Тип": "S",
            "Обозначение по ГОСТ Р 8.585-2001": "ТПП",
            "Положительный / отрицательный электрод": "Платина + 10 % родия / платина",
            "Диапазон по таблицам, °C": "−50…+1768",
            "Чувствительность, мкВ/°C": "около 10"
        },
        {
            "Тип": "R",
            "Обозначение по ГОСТ Р 8.585-2001": "ТПП",
            "Положительный / отрицательный электрод": "Платина + 13 % родия / платина",
            "Диапазон по таблицам, °C": "−50…+1768",
            "Чувствительность, мкВ/°C": "около 10"
        },
        {
            "Тип": "B",
            "Обозначение по ГОСТ Р 8.585-2001": "ТПР",
            "Положительный / отрицательный электрод": "Платина + 30 % родия / платина + 6 % родия",
            "Диапазон по таблицам, °C": "0…+1820",
            "Чувствительность, мкВ/°C": "около 10 при высоких температурах"
        }
    ])
    st.dataframe(tc_types_df, use_container_width=True, hide_index=True)

    st.markdown(
        "> Важно: в реферате указано, что приведённые диапазоны — это границы стандартных таблиц. "
        "Реальные рабочие диапазоны обычно уже и зависят от диаметра электродов, атмосферы и защитной арматуры. "
        "Например, тип J на воздухе применяют до 750 °C, тип K — примерно до 1100–1200 °C, типы S и R — до 1600 °C. "
        "Тип B практически не даёт сигнала при температурах ниже 50 °C."
    )

    st.markdown("### 5.3. Основные группы материалов")
    st.markdown(
        "**Платина и сплавы с родием.** Термопары типов S, R и B характеризуются стабильностью и применяются "
        "при высоких температурах и в эталонных измерениях. Их недостатки — высокая стоимость и сравнительно "
        "малая чувствительность, около 10 мкВ/°C. Для защиты от загрязнения такие термопары помещают "
        "в керамические чехлы.\n\n"
        "**Никелевые сплавы.** В промышленной термометрии широко применяется термопара типа K — хромель–алюмель. "
        "В реферате указано, что она недорогая, имеет почти линейную характеристику и чувствительность около 41 мкВ/°C. "
        "Среди её недостатков отмечены изменения характеристики при длительной работе в определённых температурных "
        "условиях и чувствительность к составу атмосферы.\n\n"
        "Пара нихросил–нисил (тип N) описана как улучшенная замена типа K: она лучше сопротивляется окислению и "
        "меньше изменяет характеристику при высоких температурах. Тип E (хромель–константан) имеет наибольшую "
        "чувствительность среди перечисленных стандартных пар — около 68 мкВ/°C.\n\n"
        "**Константан, железо и медь.** Константан входит в пары J, T и E. Пара железо–константан (тип J) имеет "
        "чувствительность около 55 мкВ/°C, но железо подвержено ржавлению. Пара медь–константан (тип T) применяется "
        "для низких температур; в реферате для неё указан примерный диапазон от −200 до +350 °C.\n\n"
        "**Вольфрам-рениевые термопары.** Используются для измерения очень высоких температур — порядка 2200–2500 °C, "
        "но только в вакууме, инертной или восстановительной среде, поскольку вольфрам быстро окисляется на воздухе.\n\n"
        "**Полупроводниковые термоэлектрические материалы.** Для термоэлектрических генераторов и охладителей "
        "используют полупроводники, у которых коэффициент Зеебека может достигать сотен мкВ/К. В реферате качество "
        "материала описывается безразмерной добротностью:"
    )
    st.latex(r"ZT = \frac{\alpha^2\sigma T}{\kappa},")
    st.markdown(
        "где $\\sigma$ — электропроводность, $\\kappa$ — теплопроводность, $T$ — абсолютная температура. "
        "Хороший термоэлектрик должен иметь большой коэффициент Зеебека и высокую электропроводность, "
        "но низкую теплопроводность."
    )

    render_theory_image(
        "assets/06_applications.png",
        "Рисунок 7. Области применения, перечисленные в реферате: металлургия, энергетика, химическая промышленность, авиация и научные исследования."
    )

    st.markdown(
        "**Главная мысль этапа:** выбор термопары определяется необходимым диапазоном температур, "
        "чувствительностью, стабильностью и условиями эксплуатации.\n\n"
        "*Материал по реферату: глава 3.3 и глава 4, страницы 8–13.*"
    )


def render_stage_6() -> None:
    st.markdown("## Этап 6. Применение термоэлектрических явлений и основные выводы")

    st.markdown("### 6.1. Измерение температуры")
    st.markdown(
        "Термопары являются распространёнными контактными датчиками температуры. В реферате перечислены "
        "металлургия, энергетика, химическая и стекольная промышленность, авиационные двигатели и научные приборы. "
        "Среди преимуществ отмечены небольшие размеры, прочность, быстродействие и широкий температурный диапазон."
    )

    st.markdown("### 6.2. Измерение теплового излучения")
    st.markdown(
        "Термобатареи, состоящие из последовательно соединённых термопар, применяются для регистрации теплового "
        "потока. Они входят в состав приёмников излучения и пирометров — бесконтактных измерителей температуры."
    )

    st.markdown("### 6.3. Термоэлектрические генераторы")
    st.markdown(
        "Термоэлектрические генераторы преобразуют тепло в электрическую энергию без движущихся частей. "
        "В реферате упоминается генератор ТГ-1 («партизанский котелок»), созданный в начале 1940-х годов для "
        "питания полевых радиостанций. Его мощность составляла несколько ватт, а КПД — около 2 %. Для современных "
        "генераторов в реферате приведён КПД порядка 8–10 %.\n\n"
        "Отдельный класс составляют радиоизотопные термоэлектрические генераторы (РИТЭГ), в которых источником "
        "тепла служит распад радиоактивных изотопов. В реферате в качестве примера названы космические аппараты «Вояджер»."
    )

    st.markdown("### 6.4. Термоэлектрическое охлаждение")
    st.markdown(
        "На эффекте Пельтье основаны малогабаритные холодильники и термостаты, системы охлаждения электронных "
        "компонентов и медицинские приборы. В реферате также отмечено начало серийного выпуска советского "
        "термоэлектрического холодильника «Морозко» в 1956 году."
    )

    st.markdown("### 6.5. Итог")
    st.markdown(
        "Эффект Зеебека, открытый в 1821 году, прошёл путь от лабораторного опыта с висмутом, медью и магнитной "
        "стрелкой до основы практической технологии.\n\n"
        "Термо-ЭДС возникает из-за диффузии носителей заряда от горячей части проводника к холодной. Её величина "
        "зависит от коэффициента Зеебека и свойств материалов. Важнейшее практическое применение эффекта — "
        "термопары, преобразующие разность температур в электрический сигнал, который можно измерить и "
        "использовать для определения температуры.\n\n"
        "Эффекты Зеебека, Пельтье и Томсона относятся к одной группе взаимосвязанных термоэлектрических явлений. "
        "Различные материалы термоэлектродов позволяют применять термопары в разных температурных диапазонах и условиях.\n\n"
        "**Главная мысль этапа:** эффект Зеебека связывает разность температур с электрическим сигналом; "
        "термопара использует это явление для измерения температуры в технике и промышленности.\n\n"
        "*Материал по реферату: глава 5 и заключение, страницы 14–16.*"
    )


def render_theory_section() -> None:
    """Главный учебный модуль «Теория: Термо-ЭДС. Эффект Зеебека»."""
    st.header("📚 Теория: Термо-ЭДС. Эффект Зеебека")
    st.markdown(
        "**Теоретический материал для KIP Simulator**  \n"
        "**Основа:** загруженный реферат «Термо-ЭДС. Эффект Зеебека» (17 страниц).  \n"
        "**Принцип подготовки:** текст сокращён и структурирован для изучения внутри приложения. "
        "Физические положения, формулы, исторические сведения и числовые данные взяты из реферата. "
        "Внешние сведения не добавлялись."
    )
    st.markdown(
        "> Иллюстрации в файле служат поясняющими схемами к материалу. Подписи к рисункам не заменяют "
        "текст и не вводят дополнительные числовые данные."
    )

    stages_list = [
        ("Этап 1. Введение и история открытия эффекта Зеебека", render_stage_1),
        ("Этап 2. Эффект Зеебека и физическая природа термо-ЭДС", render_stage_2),
        ("Этап 3. Связанные термоэлектрические явления: эффекты Пельтье и Томсона", render_stage_3),
        ("Этап 4. Термопары: устройство и принцип действия", render_stage_4),
        ("Этап 5. Материалы и стандартные типы термопар", render_stage_5),
        ("Этап 6. Применение термоэлектрических явлений и основные выводы", render_stage_6),
    ]

    if "theory_stage_idx" not in st.session_state:
        st.session_state["theory_stage_idx"] = 0

    view_mode = st.radio(
        "Режим отображения этапов теории:",
        options=[
            "Пошаговое изучение (с навигацией между этапами)",
            "Все этапы списком (раскрывающиеся карточки)"
        ],
        horizontal=True
    )

    if view_mode.startswith("Пошаговое"):
        stage_titles = [s[0] for s in stages_list]
        selected_title = st.selectbox(
            "Выберите этап для изучения:",
            options=stage_titles,
            index=st.session_state["theory_stage_idx"]
        )
        st.session_state["theory_stage_idx"] = stage_titles.index(selected_title)
        curr_idx = st.session_state["theory_stage_idx"]

        st.progress((curr_idx + 1) / len(stages_list), text=f"Этап {curr_idx + 1} из {len(stages_list)}")

        with st.container(border=True):
            stages_list[curr_idx][1]()

        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
        with nav_col1:
            if st.button("⬅️ Предыдущий этап", disabled=(curr_idx == 0), use_container_width=True):
                st.session_state["theory_stage_idx"] -= 1
                st.rerun()
        with nav_col3:
            if st.button("Следующий этап ➡️", disabled=(curr_idx == len(stages_list) - 1), use_container_width=True):
                st.session_state["theory_stage_idx"] += 1
                st.rerun()
    else:
        for idx, (title, render_fn) in enumerate(stages_list):
            with st.expander(title, expanded=(idx == 0)):
                render_fn()

    st.markdown("---")

    st.subheader("✅ Самопроверка по материалу")
    qa_pairs = [
        (
            "1. Что называют термо-ЭДС?",
            "Электродвижущая сила, возникающая в цепи из разнородных проводников при разных температурах спаев."
        ),
        (
            "2. Какие условия необходимы для возникновения эффекта Зеебека в цепи из двух разнородных проводников?",
            "Нужны два разнородных проводника и разная температура мест их соединения."
        ),
        (
            "3. Какие проводники использовал Зеебек в известном опыте и что наблюдал при нагревании одного спая?",
            "Висмутовый и медный проводники; при нагревании одного спая магнитная стрелка отклонялась, а при перестановке горячего и холодного спаев направление отклонения менялось."
        ),
        (
            "4. Как объясняется физическая причина возникновения термо-ЭДС в реферате?",
            "Из-за диффузии носителей заряда от нагретой части к холодной, накопления заряда и возникновения электрического поля."
        ),
        (
            "5. Что обозначают $T_1$, $T_2$ и $\\alpha$ в приближённой формуле термо-ЭДС?",
            "$T_1$ и $T_2$ — температуры спаев; $\\alpha$ — коэффициент термо-ЭДС данной пары проводников."
        ),
        (
            "6. Чем эффект Пельтье отличается от эффекта Зеебека?",
            "Эффект Пельтье проявляется как выделение или поглощение дополнительной тепловой мощности ($\\dot{Q} = \\Pi I$) при прохождении тока через контакт разнородных проводников."
        ),
        (
            "7. Что называют горячим и холодным спаями термопары?",
            "Горячий (рабочий) спай находится в зоне измерения; холодный спай образован свободными концами, подключаемыми к измерительному прибору."
        ),
        (
            "8. Для чего нужна компенсация холодного спая?",
            "Чтобы учитывать температуру свободных концов, поскольку измеряемая термо-ЭДС зависит от разности температур спаев."
        ),
        (
            "9. Какие три закона термоэлектрических цепей перечислены в реферате?",
            "Закон однородной цепи, закон промежуточных металлов и закон промежуточных температур."
        ),
        (
            "10. Где применяются термопары и другие термоэлектрические устройства согласно реферату?",
            "В измерении температуры, регистрации теплового излучения, термоэлектрических генераторах и охладителях, а также в перечисленных промышленных и научных областях."
        )
    ]

    for q_text, a_text in qa_pairs:
        with st.expander(q_text):
            st.markdown(f"**Ответ для проверки:** {a_text}")

    with st.expander("📋 Ответы для проверки (полный список)"):
        st.markdown("### Ответы для проверки")
        for idx, (_, a_text) in enumerate(qa_pairs, start=1):
            st.markdown(f"{idx}. {a_text}")

    st.markdown("---")

    st.subheader("📖 Словарь терминов")
    glossary_data = [
        {
            "Термин": "Термоэлектрические явления",
            "Значение по материалу реферата": "Группа эффектов, связывающих тепловые и электрические процессы в проводниках и полупроводниках."
        },
        {
            "Термин": "Эффект Зеебека",
            "Значение по материалу реферата": "Возникновение ЭДС в цепи из разнородных проводников при разной температуре спаев."
        },
        {
            "Термин": "Термо-ЭДС",
            "Значение по материалу реферата": "Электродвижущая сила, возникающая при эффекте Зеебека."
        },
        {
            "Термин": "Спай",
            "Значение по материалу реферата": "Место соединения двух термоэлектродов."
        },
        {
            "Термин": "Термоэлектрод",
            "Значение по материалу реферата": "Проводник, входящий в состав термопары."
        },
        {
            "Термин": "Коэффициент Зеебека",
            "Значение по материалу реферата": "Коэффициент, характеризующий термо-ЭДС пары проводников."
        },
        {
            "Термин": "Термоток",
            "Значение по материалу реферата": "Ток в замкнутой цепи, возникающий вследствие термо-ЭДС."
        },
        {
            "Термин": "Термопара",
            "Значение по материалу реферата": "Термоэлектрический преобразователь температуры из двух разнородных проводников."
        },
        {
            "Термин": "Компенсация холодного спая",
            "Значение по материалу реферата": "Учёт температуры свободных концов термопары при измерении."
        },
        {
            "Термин": "Термобатарея (термостолбик)",
            "Значение по материалу реферата": "Последовательное соединение нескольких термопар."
        },
        {
            "Термин": "Эффект Пельтье",
            "Значение по материалу реферата": "Выделение или поглощение дополнительной теплоты при прохождении тока через контакт разнородных проводников."
        },
        {
            "Термин": "Эффект Томсона",
            "Значение по материалу реферата": "Выделение или поглощение теплоты в однородном проводнике при прохождении тока и наличии градиента температуры."
        }
    ]

    search_term = st.text_input("🔍 Поиск по словарю терминов:", "")
    filtered_glossary = [
        row for row in glossary_data
        if search_term.lower() in row["Термин"].lower()
        or search_term.lower() in row["Значение по материалу реферата"].lower()
    ]
    st.dataframe(
        pd.DataFrame(filtered_glossary if filtered_glossary else glossary_data),
        use_container_width=True,
        hide_index=True
    )

    with st.expander("ℹ️ Примечание для интеграции в приложение"):
        st.markdown(
            "Материал разбит на шесть самостоятельных этапов. Каждый этап можно разместить отдельной "
            "раскрывающейся карточкой или вкладкой. Изображения находятся в папке `assets`; пути к ним "
            "указаны непосредственно в этом Markdown-файле. Таблицу типов термопар, формулы, самопроверку "
            "и словарь терминов следует переносить как структурированные элементы, а не как сплошной текст."
        )


render_theory_section()


# =====================================================================
# 10. МОДУЛЬ ПОДБОРА ТЕРМОПАРЫ ПО УСЛОВИЯМ ЭКСПЛУАТАЦИИ
# =====================================================================
st.markdown("---")

SELECTOR_TC_SPECS = {
    "K": {
        "code": "K",
        "gost": "ТХА",
        "title": "Тип K (ТХА — Хромель / Алюмель)",
        "electrodes": "Хромель (Ni–Cr) (+) / Алюмель (Ni–Al–Mn–Si) (−)",
        "table_min": -270.0,
        "table_max": 1372.0,
        "confirmed_work_min": -200.0,
        "confirmed_work_max": 1200.0,
        "table_range_str": "−270…+1372 °C (по таблице п. 5.2 реферата)",
        "sim_nsh_str": "Реализована на Стенде №1: выборка −200…+1320 °C (56 точек, шаг 50/20 °C)",
        "work_range_str": "Практическое применение на воздухе: примерно до +1100…1200 °C (при табличном пределе до +1372 °C)",
        "sensitivity_str": "около 41 мкВ/°C",
        "sensitivity_val": 41.0,
        "limitations": (
            "Чувствительна к составу атмосферы (при низком содержании кислорода и в восстановительной среде "
            "возникает селективное окисление хрома и дрейф НСХ); изменения характеристики при длительной работе; "
            "практический предел на воздухе (1100–1200 °C) ниже табличного (1372 °C)."
        )
    },
    "J": {
        "code": "J",
        "gost": "ТЖК",
        "title": "Тип J (ТЖК — Железо / Константан)",
        "electrodes": "Железо (+) / Константан (−)",
        "table_min": -210.0,
        "table_max": 1200.0,
        "confirmed_work_min": -210.0,
        "confirmed_work_max": 750.0,
        "table_range_str": "−210…+1200 °C (по таблице п. 5.2 реферата)",
        "sim_nsh_str": "Реализована на Стенде №1: таблица −210…+1200 °C (142 точки, шаг 10 °C)",
        "work_range_str": "Практическое применение на воздухе: до +750 °C (при табличном пределе до +1200 °C)",
        "sensitivity_str": "около 55 мкВ/°C",
        "sensitivity_val": 55.0,
        "limitations": (
            "Железо подвержено ржавлению (коррозии при конденсации влаги) и интенсивному окислению на воздухе выше 750 °C."
        )
    },
    "T": {
        "code": "T",
        "gost": "ТМК",
        "title": "Тип T (ТМК — Медь / Константан)",
        "electrodes": "Медь (+) / Константан (−)",
        "table_min": -270.0,
        "table_max": 400.0,
        "confirmed_work_min": -200.0,
        "confirmed_work_max": 350.0,
        "table_range_str": "−270…+400 °C (по таблице п. 5.2 реферата)",
        "sim_nsh_str": "Только справочная рекомендация (расчётная таблица на Стенде №1 не реализована)",
        "work_range_str": "Подтверждённый в реферате (п. 5.3) практический диапазон: примерно от −200 до +350 °C",
        "sensitivity_str": "около 43 мкВ/°C",
        "sensitivity_val": 43.0,
        "limitations": (
            "Низкий верхний температурный предел (практически до +350 °C, по таблице до +400 °C)."
        )
    },
    "E": {
        "code": "E",
        "gost": "ТХКн",
        "title": "Тип E (ТХКн — Хромель / Константан)",
        "electrodes": "Хромель (+) / Константан (−)",
        "table_min": -270.0,
        "table_max": 1000.0,
        "confirmed_work_min": None,
        "confirmed_work_max": None,
        "table_range_str": "−270…+1000 °C (по таблице п. 5.2 реферата)",
        "sim_nsh_str": "Только справочная рекомендация (расчётная таблица на Стенде №1 не реализована)",
        "work_range_str": (
            "В реферате указан только табличный диапазон −270…+1000 °C "
            "(отдельный численный рабочий предел не приведён; реальный рабочий диапазон уже табличного)"
        ),
        "sensitivity_str": "около 68 мкВ/°C (наибольшая среди стандартных пар)",
        "sensitivity_val": 68.0,
        "limitations": (
            "Точный практический верхний предел в реферате численно не выделен (указано, что реальный рабочий "
            "диапазон уже табличного −270…+1000 °C и зависит от диаметра электродов, атмосферы и арматуры); "
            "содержит хромель, чувствительный к средам с низким содержанием кислорода и восстановительной атмосфере."
        )
    },
    "N": {
        "code": "N",
        "gost": "ТНН",
        "title": "Тип N (ТНН — Нихросил / Нисил)",
        "electrodes": "Нихросил (Ni–Cr–Si) (+) / Нисил (Ni–Si–Mg) (−)",
        "table_min": -270.0,
        "table_max": 1300.0,
        "confirmed_work_min": None,
        "confirmed_work_max": None,
        "table_range_str": "−270…+1300 °C (по таблице п. 5.2 реферата)",
        "sim_nsh_str": "Только справочная рекомендация (расчётная таблица на Стенде №1 не реализована)",
        "work_range_str": (
            "В реферате указан табличный диапазон −270…+1300 °C и повышенная стойкость к окислению "
            "(отдельный численный рабочий предел в реферате не приведён; реальный рабочий диапазон уже табличного)"
        ),
        "sensitivity_str": "около 39 мкВ/°C",
        "sensitivity_val": 39.0,
        "limitations": (
            "Точный практический верхний предел в реферате численно не выделен (указана табличная граница +1300 °C, "
            "при этом реальный рабочий предел уже табличного и требует проверки по паспорту датчика); "
            "чувствительность немного ниже типа K (39 мкВ/°C)."
        )
    },
    "S": {
        "code": "S",
        "gost": "ТПП",
        "title": "Тип S (ТПП — Платина + 10 % родия / Платина)",
        "electrodes": "Платина + 10 % родия (+) / Платина (−)",
        "table_min": -50.0,
        "table_max": 1768.0,
        "confirmed_work_min": -50.0,
        "confirmed_work_max": 1600.0,
        "table_range_str": "−50…+1768 °C (по таблице п. 5.2 реферата)",
        "sim_nsh_str": "Только справочная рекомендация (расчётная таблица на Стенде №1 не реализована)",
        "work_range_str": "Подтверждённый в реферате (п. 5.2) практический рабочий диапазон: до +1600 °C",
        "sensitivity_str": "около 10 мкВ/°C",
        "sensitivity_val": 10.0,
        "limitations": (
            "Высокая стоимость и малая чувствительность (около 10 мкВ/°C); для защиты от загрязнения "
            "(особенно в восстановительных и технологических средах) необходимо помещать в керамические чехлы."
        )
    },
    "R": {
        "code": "R",
        "gost": "ТПП",
        "title": "Тип R (ТПП — Платина + 13 % родия / Платина)",
        "electrodes": "Платина + 13 % родия (+) / Платина (−)",
        "table_min": -50.0,
        "table_max": 1768.0,
        "confirmed_work_min": -50.0,
        "confirmed_work_max": 1600.0,
        "table_range_str": "−50…+1768 °C (по таблице п. 5.2 реферата)",
        "sim_nsh_str": "Только справочная рекомендация (расчётная таблица на Стенде №1 не реализована)",
        "work_range_str": "Подтверждённый в реферате (п. 5.2) практический рабочий диапазон: до +1600 °C",
        "sensitivity_str": "около 10 мкВ/°C",
        "sensitivity_val": 10.0,
        "limitations": (
            "Высокая стоимость и малая чувствительность (около 10 мкВ/°C); требует обязательной защиты керамическими чехлами."
        )
    },
    "B": {
        "code": "B",
        "gost": "ТПР",
        "title": "Тип B (ТПР — Платина + 30 % родия / Платина + 6 % родия)",
        "electrodes": "Платина + 30 % родия (+) / Платина + 6 % родия (−)",
        "table_min": 0.0,
        "table_max": 1820.0,
        "confirmed_work_min": 50.0,
        "confirmed_work_max": None,
        "table_range_str": "0…+1820 °C (по таблице п. 5.2 реферата)",
        "sim_nsh_str": "Только справочная рекомендация (расчётная таблица на Стенде №1 не реализована)",
        "work_range_str": (
            "Нижний рабочий предел: от +50 °C (ниже 50 °C не даёт сигнала); "
            "верхний численный рабочий предел в реферате не выделен (таблица до +1820 °C, реальный рабочий диапазон уже табличного)"
        ),
        "sensitivity_str": "около 10 мкВ/°C при высоких температурах",
        "sensitivity_val": 10.0,
        "limitations": (
            "Практически не даёт сигнала при температурах ниже +50 °C; точный верхний практический предел "
            "в реферате численно не указан (указана только граница таблицы +1820 °C); высокая стоимость, "
            "малая чувствительность, обязательна защита керамическими чехлами."
        )
    },
    "W-Re": {
        "code": "W-Re",
        "gost": "Вольфрам-рениевые (конкретная марка в реферате не указана)",
        "title": "Вольфрам-рениевые термопары",
        "electrodes": "Вольфрам-рениевые сплавы (конкретный состав электродов в источнике не детализирован)",
        "table_min": 2200.0,
        "table_max": 2500.0,
        "confirmed_work_min": 2200.0,
        "confirmed_work_max": 2500.0,
        "table_range_str": "В таблице п. 5.2 не приведены; в тексте п. 5.3 указан диапазон порядка 2200–2500 °C",
        "sim_nsh_str": "Только справочная рекомендация (расчётная таблица на Стенде №1 не реализована)",
        "work_range_str": "Порядка 2200–2500 °C ТОЛЬКО в вакууме, инертной или восстановительной среде",
        "sensitivity_str": "Численное значение чувствительности в источнике не приведено",
        "sensitivity_val": None,
        "limitations": (
            "КАТЕГОРИЧЕСКИ НЕДОПУСТИМЫ НА ВОЗДУХЕ (вольфрам быстро окисляется в окислительной атмосфере); "
            "применимы только в вакууме, инертной или восстановительной среде."
        )
    }
}


def evaluate_thermocouple_selection(
    t_min: float,
    t_max: float,
    environment: str,
    priority: str
) -> dict:
    """
    Выполняет строгий многокритериальный подбор термопары по полному интервалу [t_min, t_max],
    рабочей среде и приоритету.
    """
    if t_min >= t_max:
        return {
            "status": "error",
            "message": (
                f"Некорректный ввод температурного интервала: минимальная температура ({t_min:.1f} °C) "
                f"должна быть строго меньше максимальной температуры ({t_max:.1f} °C)."
            ),
            "warnings": [],
            "primary": None,
            "alternatives": [],
            "rejected_reasons": {}
        }

    warnings_list = []
    rejected_reasons = {}
    candidates = []

    for code, sp in SELECTOR_TC_SPECS.items():
        if code == "W-Re":
            if t_min >= 2200.0 and t_max <= 2500.0:
                if environment == "воздушная / окислительная":
                    rejected_reasons[code] = (
                        "Недопустима в воздушной/окислительной среде: вольфрам быстро окисляется на воздухе."
                    )
                elif environment == "среда с пониженным содержанием кислорода":
                    rejected_reasons[code] = (
                        "Недопустима при наличии остаточного кислорода: вольфрам быстро окисляется, "
                        "требуется вакуум, чистая инертная или восстановительная среда."
                    )
                elif environment == "неизвестная":
                    rejected_reasons[code] = (
                        "Не может быть рекомендована при неизвестной рабочей среде: вольфрам быстро окисляется "
                        "на воздухе, поэтому без подтверждения вакуума, инертной или восстановительной среды выбор небезопасен."
                    )
                else:
                    candidates.append(code)
            else:
                rejected_reasons[code] = (
                    f"В теоретическом источнике (п. 5.3) применение вольфрам-рениевых термопар подтверждено "
                    f"только для области очень высоких температур порядка 2200–2500 °C (задано: {t_min:.0f}…{t_max:.0f} °C)."
                )
            continue

        lower_bound = sp["confirmed_work_min"] if sp["confirmed_work_min"] is not None else sp["table_min"]
        if t_min < lower_bound:
            if code == "B" and t_min >= 0.0:
                rejected_reasons[code] = (
                    f"Нижняя температура ({t_min:.0f} °C) ниже +50 °C: согласно п. 5.2 реферата, "
                    "тип B практически не даёт сигнала при температурах ниже 50 °C."
                )
            else:
                rejected_reasons[code] = (
                    f"Нижняя температура ({t_min:.0f} °C) выходит за допустимый нижний предел ({lower_bound:.0f} °C; "
                    f"граница стандартной таблицы {sp['table_min']:.0f} °C)."
                )
            continue

        upper_bound = sp["confirmed_work_max"] if sp["confirmed_work_max"] is not None else sp["table_max"]
        if t_max > upper_bound:
            if sp["confirmed_work_max"] is not None and t_max <= sp["table_max"]:
                rejected_reasons[code] = (
                    f"Верхняя температура ({t_max:.0f} °C) укладывается в справочную таблицу ({sp['table_range_str']}), "
                    f"но превышает подтверждённый в реферате практический рабочий предел ({sp['confirmed_work_max']:.0f} °C)."
                )
            else:
                rejected_reasons[code] = (
                    f"Верхняя температура ({t_max:.0f} °C) превышает предел стандартной таблицы ({sp['table_max']:.0f} °C)."
                )
            continue

        candidates.append(code)

    if not candidates:
        if t_max > 1820.0 and t_min < 2200.0:
            err_msg = (
                f"Для температурного интервала **{t_min:.0f}…{t_max:.0f} °C** (среда: *{environment}*) в предоставленном "
                "теоретическом материале нет подтверждённого типа термопары: верхний табличный предел платинородиевой "
                "термопары типа B заканчивается на **+1820 °C**, а для вольфрам-рениевых термопар в реферате "
                "указан только диапазон порядка **2200–2500 °C** (без характеристик для промежуточной зоны 1820–2200 °C)."
            )
        elif t_min >= 2200.0 and t_max <= 2500.0 and environment in (
            "воздушная / окислительная",
            "среда с пониженным содержанием кислорода",
            "неизвестная"
        ):
            err_msg = (
                f"В диапазоне **{t_min:.0f}…{t_max:.0f} °C** при рабочей среде **«{environment}»** безопасный выбор невозможен: "
                "вольфрам-рениевые термопары (2200–2500 °C) быстро окисляются при наличии кислорода и допускаются "
                "**только в вакууме, инертной или восстановительной среде**."
            )
        else:
            err_msg = (
                f"Для заданного интервала **{t_min:.0f}…{t_max:.0f} °C** и среды **«{environment}»** не найден тип термопары, "
                "рабочий диапазон которого полностью перекрывает весь заданный интервал от минимальной до максимальной температуры."
            )
        return {
            "status": "error",
            "message": err_msg,
            "warnings": warnings_list,
            "primary": None,
            "alternatives": [],
            "rejected_reasons": rejected_reasons
        }

    status_code = "ok"
    if environment == "неизвестная":
        status_code = "conditional"
        warnings_list.append(
            "РАБОЧАЯ СРЕДА НЕ ОПРЕДЕЛЕНА («неизвестная»): выдана условная оценка только по температурному интервалу. "
            "Безусловная рекомендация невозможна без уточнения атмосферы (тип K чувствителен к составу атмосферы, "
            "железо в типе J ржавеет во влажной среде, а платиновые пары S, R, B требуют керамических чехлов)."
        )
    elif environment == "восстановительная" and candidates != ["W-Re"]:
        status_code = "conditional"
        warnings_list.append(
            "УСЛОВНАЯ РЕКОМЕНДАЦИЯ ДЛЯ ВОССТАНОВИТЕЛЬНОЙ СРЕДЫ: в предоставленном реферате работа непосредственно "
            "в восстановительной атмосфере подтверждена только для вольфрам-рениевых термопар (при 2200–2500 °C). "
            "Для стандартных термопар точные допустимые пределы в восстановительной атмосфере в источнике не приведены: "
            "тип K чувствителен к составу атмосферы, а платинородиевые пары (S, R, B) требуют герметичной защиты "
            "керамическими чехлами от загрязнения. Необходима проверка по паспорту датчика."
        )
    elif environment == "среда с пониженным содержанием кислорода":
        status_code = "conditional"
        warnings_list.append(
            "УСЛОВНАЯ РЕКОМЕНДАЦИЯ ДЛЯ СРЕДЫ С ПОНИЖЕННЫМ СОДЕРЖАНИЕМ КИСЛОРОДА: никель-хромовые термопары (особенно тип K) "
            "чувствительны к составу атмосферы и при дефиците кислорода подвержены селективному окислению хрома с уходом градуировки; "
            "пара нихросил–нисил (тип N) лучше сопротивляется окислению, однако точные рабочие границы для данной среды "
            "в реферате не приведены — требуется проверка паспорта и выбор защитного чехла."
        )
    elif environment in ("инертная", "вакуум") and candidates != ["W-Re"]:
        status_code = "conditional"
        warnings_list.append(
            f"Выбрана среда «{environment}»: в реферате числовые рабочие пределы стандартных пар (J до 750 °C, K до 1100–1200 °C, "
            "S и R до 1600 °C) приведены для обычных (воздушных) условий, поэтому применение в инертной среде или вакууме "
            "требует проверки по паспорту датчика и учёта защитной арматуры (керамических чехлов для S, R, B)."
        )

    if candidates == ["W-Re"]:
        warnings_list.append(
            "В теоретическом материале (п. 5.3) для вольфрам-рениевых термопар приведён только ориентировочный "
            "рабочий диапазон (2200–2500 °C) и требование к среде (вакуум, инертная или восстановительная). "
            "Конкретная градуировка по ГОСТ и численная чувствительность в реферате не указаны."
        )
        return {
            "status": "conditional",
            "primary": SELECTOR_TC_SPECS["W-Re"],
            "justification": (
                f"Интервал **{t_min:.0f}…{t_max:.0f} °C** превышает табличный предел всех стандартных пар (максимум +1820 °C у типа B). "
                f"Поскольку задана допустимая безокислительная среда (*{environment}*), по данным п. 5.3 реферата "
                "условно рекомендуются **вольфрам-рениевые термопары** (с обязательной проверкой паспорта конкретной марки)."
            ),
            "alternatives": [],
            "warnings": warnings_list,
            "rejected_reasons": rejected_reasons
        }

    scored = []
    for code in candidates:
        score = 0.0
        reasons = []

        if t_max > 1600.0:
            if code == "B":
                score += 95.0
                reasons.append(
                    f"единственная стандартная термопара из таблицы п. 5.2 со справочным пределом до +1820 °C "
                    f"(у типов S и R практический рабочий предел ограничен +1600 °C)"
                )
        elif t_max > 1200.0:
            if code in ("S", "R"):
                score += 96.0
                reasons.append(
                    f"имеет явно подтверждённый в реферате (п. 5.2) практический рабочий предел до +1600 °C "
                    f"и высокую стабильность в диапазоне {t_min:.0f}…{t_max:.0f} °C"
                )
                if code == "S":
                    score += 1.5
            elif code == "B":
                score += 84.0
                reasons.append("высокотемпературная платинородиевая пара со справочным диапазоном 0…+1820 °C")
            elif code == "N":
                score += 70.0
                reasons.append(
                    "укладывается в верхнюю часть справочной таблицы типа N (−270…+1300 °C), "
                    "но точный практический предел выше 1200 °C в реферате не подтверждён"
                )
        elif t_max > 900.0:
            if code == "N":
                score += 92.0
                reasons.append(
                    "согласно п. 5.3 реферата, тип N (нихросил–нисил) является улучшенной заменой типа K: "
                    "лучше сопротивляется окислению и меньше изменяет характеристику при высоких температурах"
                )
            elif code == "K":
                score += 84.0
                reasons.append("широко распространённая промышленная пара с рабочим пределом на воздухе до 1100–1200 °C")
            elif code in ("S", "R"):
                score += 78.0
                reasons.append("эталонная стабильность при высоких температурах (рабочий предел до +1600 °C)")
            elif code == "E":
                score += 70.0
                reasons.append("высокая чувствительность (около 68 мкВ/°C), но работа вблизи табличного предела +1000 °C")
            elif code == "B":
                score += 65.0
        elif t_min < 0.0 and t_max <= 350.0:
            if code == "T":
                score += 94.0
                reasons.append(
                    "в п. 5.3 реферата пара медь–константан (тип T) прямо указана для низких температур "
                    "с подтверждённым примерным диапазоном от −200 до +350 °C"
                )
            elif code == "E":
                score += 88.0
                reasons.append("обладает максимальной чувствительность среди стандартных пар (около 68 мкВ/°C)")
            elif code == "K":
                score += 85.0
                reasons.append("универсальная промышленная термопара с почти линейной характеристикой")
            elif code == "N":
                score += 82.0
                reasons.append("стабильная никель-хромовая пара со справочным диапазоном от −270 °C")
            elif code == "J":
                score += 65.0
                reasons.append("чувствительность около 55 мкВ/°C, но железо подвержено ржавлению при конденсации влаги")
            elif code in ("S", "R"):
                score += 45.0
        else:
            if code == "K":
                score += 90.0
                reasons.append(
                    "недорогая и наиболее универсальная промышленная пара с почти линейной характеристикой "
                    "и чувствительностью около 41 мкВ/°C"
                )
            elif code == "E":
                score += 87.0
                reasons.append("наибольшая чувствительность среди стандартных термопар (около 68 мкВ/°C)")
            elif code == "N":
                score += 86.0
                reasons.append("повышенная стабильность характеристики и стойкость к окислению по сравнению с типом K")
            elif code == "J":
                score += 84.0
                reasons.append("высокая чувствительность (около 55 мкВ/°C) при работе на воздухе до +750 °C")
            elif code == "T":
                score += 82.0
                reasons.append("хорошая воспроизводимость в области умеренных температур до +350 °C")
            elif code in ("S", "R"):
                score += 50.0
            elif code == "B":
                score += 40.0

        if environment in ("восстановительная", "среда с пониженным содержанием кислорода"):
            if code == "K":
                score -= 12.0
            elif code == "N":
                score += 4.0

        if priority == "повышенная чувствительность":
            sens = SELECTOR_TC_SPECS[code]["sensitivity_val"] or 0.0
            score += sens * 0.45
            if code == "E":
                reasons.append("приоритет «повышенная чувствительность»: максимальный сигнал около 68 мкВ/°C")
            elif code == "J":
                reasons.append("приоритет «повышенная чувствительность»: повышенный сигнал около 55 мкВ/°C")
        elif priority == "стабильность и точность":
            if code == "N":
                score += 18.0
                reasons.append("приоритет «стабильность и точность»: меньший дрейф характеристики при нагреве, чем у типа K")
            elif code in ("S", "R"):
                score += 24.0 if t_max >= 600.0 else 10.0
                reasons.append("приоритет «стабильность и точность»: благородные металлы для точных и эталонных измерений")
            elif code == "T" and t_max <= 350.0:
                score += 14.0
        elif priority == "универсальность":
            if t_min < 0.0 and t_max <= 350.0:
                if code == "T":
                    score += 12.0
                    reasons.append("приоритет «универсальность» в низкотемпературной зоне: оптимальная пара для области −200…+350 °C")
                elif code == "K":
                    score += 8.0
            else:
                if code == "K" and t_max <= 1100.0:
                    score += 15.0
                    reasons.append("приоритет «универсальность»: стандартное решение для общепромышленной термометрии")
                elif code == "K" and t_max > 1100.0:
                    score += 8.0
                elif code == "N" and 900.0 < t_max <= 1200.0:
                    score += 14.0

        scored.append((score, code, reasons))

    scored.sort(key=lambda item: item[0], reverse=True)
    _, best_code, best_reasons = scored[0]
    primary_spec = SELECTOR_TC_SPECS[best_code]

    if primary_spec["confirmed_work_max"] is None or primary_spec["confirmed_work_min"] is None:
        status_code = "conditional"
        warnings_list.append(
            f"УСЛОВНАЯ РЕКОМЕНДАЦИЯ ПО РАБОЧЕМУ ДИАПАЗОНУ ({primary_spec['title']}): в предоставленном реферате "
            f"для типа {best_code} приведены границы стандартной таблицы ({primary_spec['table_range_str']}), "
            "но не выделено отдельное численное значение гарантированного практического верхнего предела "
            "(при этом в п. 5.2 указано, что реальные рабочие диапазоны обычно уже табличных и зависят от диаметра "
            "электродов, атмосферы и защитной арматуры). Перед применением обязательна сверка с паспортом датчика."
        )

    if (best_code == "K" or "K" in candidates) and t_max > 1100.0:
        warnings_list.append(
            f"Примечание по типу K (ТХА): температура {t_max:.0f} °C находится на верхнем краю указанного в реферате "
            "практического рабочего диапазона типа K на воздухе (1100–1200 °C)."
        )
    if best_code in ("S", "R"):
        warnings_list.append(
            "Термопары типов S (Платина + 10 % родия / Платина) и R (Платина + 13 % родия / Платина) имеют "
            "одинаковые табличные (−50…+1768 °C) и рабочие (до +1600 °C) границы и чувствительность около 10 мкВ/°C."
        )

    alternatives = []
    for _, alt_code, alt_reasons in scored[1:3]:
        alt_spec = SELECTOR_TC_SPECS[alt_code]
        alt_note = "; ".join(alt_reasons) if alt_reasons else (
            f"Перекрывает заданный интервал ({alt_spec['work_range_str']}), чувствительность: {alt_spec['sensitivity_str']}."
        )
        if alt_spec["confirmed_work_max"] is None:
            alt_note += " (Точный рабочий предел в реферате не выделен — требуется сверка с паспортом)."
        alternatives.append({"spec": alt_spec, "note": alt_note})

    justification_text = (
        f"Для полного температурного интервала **{t_min:.0f}…{t_max:.0f} °C** "
        f"(рабочая среда: *{environment}*, приоритет: *{priority}*) выбран **{primary_spec['title']}**, поскольку он: "
        + "; ".join(best_reasons) + "."
    )

    return {
        "status": status_code,
        "primary": primary_spec,
        "justification": justification_text,
        "alternatives": alternatives,
        "warnings": warnings_list,
        "rejected_reasons": rejected_reasons
    }


def render_thermocouple_selector() -> None:
    """Интерактивный модуль «Подбор термопары по условиям эксплуатации»."""
    st.header("🧭 Подбор термопары по условиям эксплуатации")
    st.markdown(
        "Инженерный модуль для выбора типа термопары по полному диапазону температур $[T_{\\min}, T_{\\max}]$, "
        "характеру рабочей среды и приоритету измерения. Алгоритм разделяет **справочный диапазон таблиц НСХ**, "
        "**фактический рекомендуемый рабочий диапазон** и выдаёт условную рекомендацию с предупреждением, если "
        "для выбранного типа или среды в реферате не указан точный гарантированный рабочий предел."
    )

    if "sel_t_min" not in st.session_state:
        st.session_state["sel_t_min"] = 20.0
    if "sel_t_max" not in st.session_state:
        st.session_state["sel_t_max"] = 300.0
    if "sel_env" not in st.session_state:
        st.session_state["sel_env"] = "воздушная / окислительная"
    if "sel_prio" not in st.session_state:
        st.session_state["sel_prio"] = "универсальность"
    if "selector_committed" not in st.session_state:
        st.session_state["selector_committed"] = None

    scenarios_preset = [
        ("1. −50…+100 °C, воздушная среда", -50.0, 100.0, "воздушная / окислительная", "универсальность"),
        ("2. 20…300 °C, воздушная среда", 20.0, 300.0, "воздушная / окислительная", "универсальность"),
        ("3. 1000…1150 °C, воздушная среда", 1000.0, 1150.0, "воздушная / окислительная", "универсальность"),
        ("4. 1200…1500 °C, воздушная среда", 1200.0, 1500.0, "воздушная / окислительная", "универсальность"),
        ("5. 1700…1800 °C, инертная среда", 1700.0, 1800.0, "инертная", "стабильность и точность"),
        ("6. 2200…2500 °C, вакуум", 2200.0, 2500.0, "вакуум", "универсальность"),
        ("7. 2200…2500 °C, неизвестная среда", 2200.0, 2500.0, "неизвестная", "универсальность"),
        ("8. 1800…2000 °C, вакуум (вне подтверждённых зон)", 1800.0, 2000.0, "вакуум", "универсальность"),
        ("9. −250…+1700 °C, воздушная (вне диапазонов)", -250.0, 1700.0, "воздушная / окислительная", "универсальность"),
        ("10. Ошибка ввода: T_min = 400 °C > T_max = 100 °C", 400.0, 100.0, "воздушная / окислительная", "универсальность"),
    ]

    with st.expander("⚡ Контрольные тестовые сценарии (10 сценариев + автоматическая верификация)", expanded=False):
        st.caption("Нажмите на кнопку любого сценария для загрузки в форму или запустите сводную таблицу исполнения всех 10 тестов:")
        sc_cols = st.columns(2)
        for idx, (label, s_min, s_max, s_env, s_prio) in enumerate(scenarios_preset):
            with sc_cols[idx % 2]:
                if st.button(label, key=f"preset_btn_{idx}", use_container_width=True):
                    st.session_state["sel_t_min"] = s_min
                    st.session_state["sel_t_max"] = s_max
                    st.session_state["sel_env"] = s_env
                    st.session_state["sel_prio"] = s_prio
                    st.session_state["selector_committed"] = {
                        "t_min": s_min,
                        "t_max": s_max,
                        "env": s_env,
                        "prio": s_prio
                    }
                    st.rerun()

        if st.button("🧪 Выполнить все 10 сценариев и показать сводный протокол", use_container_width=True):
            protocol_rows = []
            for label, s_min, s_max, s_env, s_prio in scenarios_preset:
                res = evaluate_thermocouple_selection(s_min, s_max, s_env, s_prio)
                prim_title = res["primary"]["title"] if res["primary"] else "Отказ (не найден)"
                alt_titles = ", ".join(a["spec"]["code"] for a in res["alternatives"]) if res["alternatives"] else "—"
                protocol_rows.append({
                    "Сценарий": label,
                    "Статус": res["status"],
                    "Фактический результат": prim_title,
                    "Альтернативы": alt_titles,
                    "Предупреждения": "Да (" + str(len(res["warnings"])) + ")" if res["warnings"] else ("Ошибка/Отказ" if res["status"] == "error" else "Нет")
                })
            st.dataframe(pd.DataFrame(protocol_rows), use_container_width=True, hide_index=True)

    with st.form("thermocouple_selector_form"):
        col_in1, col_in2, col_in3, col_in4 = st.columns(4)
        with col_in1:
            t_min_in = st.number_input(
                "Минимальная температура, °C:",
                min_value=-270.0,
                max_value=3000.0,
                value=float(st.session_state["sel_t_min"]),
                step=10.0
            )
        with col_in2:
            t_max_in = st.number_input(
                "Максимальная температура, °C:",
                min_value=-270.0,
                max_value=3000.0,
                value=float(st.session_state["sel_t_max"]),
                step=10.0
            )
        with col_in3:
            env_options = [
                "воздушная / окислительная",
                "инертная",
                "восстановительная",
                "среда с пониженным содержанием кислорода",
                "вакуум",
                "неизвестная"
            ]
            current_env = st.session_state["sel_env"] if st.session_state["sel_env"] in env_options else env_options[0]
            env_in = st.selectbox(
                "Рабочая среда:",
                options=env_options,
                index=env_options.index(current_env)
            )
        with col_in4:
            prio_options = [
                "универсальность",
                "стабильность и точность",
                "повышенная чувствительность"
            ]
            prio_in = st.selectbox(
                "Приоритет выбора:",
                options=prio_options,
                index=prio_options.index(st.session_state["sel_prio"])
            )

        run_selection = st.form_submit_button(
            "🔍 Подобрать термопару",
            type="primary",
            use_container_width=True
        )

    if run_selection:
        st.session_state["sel_t_min"] = t_min_in
        st.session_state["sel_t_max"] = t_max_in
        st.session_state["sel_env"] = env_in
        st.session_state["sel_prio"] = prio_in
        st.session_state["selector_committed"] = {
            "t_min": t_min_in,
            "t_max": t_max_in,
            "env": env_in,
            "prio": prio_in
        }

    if st.session_state["selector_committed"] is None:
        st.info("👆 Задайте параметры эксплуатации и нажмите кнопку **«🔍 Подобрать термопару»**, чтобы выполнить расчёт.")
        return

    committed = st.session_state["selector_committed"]
    result = evaluate_thermocouple_selection(
        committed["t_min"],
        committed["t_max"],
        committed["env"],
        committed["prio"]
    )

    if result["status"] == "error":
        st.error(f"🚫 **Подходящий тип термопары не найден (отказ в рекомендации):**\n\n{result['message']}")
        for w in result["warnings"]:
            st.warning(f"⚠️ {w}")
    else:
        p = result["primary"]
        header_prefix = (
            "⚠️ Условная рекомендация (требуется проверка паспорта датчика / условий среды)"
            if result["status"] in ("warning", "conditional")
            else "🏆 Рекомендуемый тип термопары"
        )
        with st.container(border=True):
            st.subheader(f"{header_prefix}: {p['title']}")
            k1, k2, k3 = st.columns(3)
            k1.metric("Обозначение по ГОСТ Р 8.585-2001", p["gost"])
            k2.metric("Ориентировочная чувствительность", p["sensitivity_str"])
            k3.metric("Справочный диапазон таблицы", p["table_range_str"].split("(")[0].strip())

            st.markdown(f"- **1. Материалы электродов:** {p['electrodes']}")
            st.markdown(f"- **2. Практический рабочий диапазон (по источнику):** {p['work_range_str']}")
            st.markdown(f"- **3. Справочный диапазон стандартной таблицы:** {p['table_range_str']}")
            st.markdown(f"- **4. Статус в расчётной базе симулятора (Стенд №1):** {p['sim_nsh_str']}")
            st.markdown(f"- **5. Обоснование выбора:** {result['justification']}")
            st.markdown(f"- **6. Ограничения применения и возможные проблемы:** {p['limitations']}")

        for w in result["warnings"]:
            st.warning(f"⚠️ **Предупреждение:** {w}")

        if result["alternatives"]:
            st.subheader("🔄 Возможные альтернативные варианты")
            alt_cols = st.columns(len(result["alternatives"]))
            for idx, alt_item in enumerate(result["alternatives"]):
                alt_sp = alt_item["spec"]
                with alt_cols[idx]:
                    with st.container(border=True):
                        st.markdown(f"#### {alt_sp['title']}")
                        st.markdown(f"- **Обозначение ГОСТ:** `{alt_sp['gost']}`")
                        st.markdown(f"- **Материалы электродов:** {alt_sp['electrodes']}")
                        st.markdown(f"- **Рабочий диапазон:** {alt_sp['work_range_str']}")
                        st.markdown(f"- **Табличный диапазон:** {alt_sp['table_range_str']}")
                        st.markdown(f"- **Статус в симуляторе:** {alt_sp['sim_nsh_str']}")
                        st.markdown(f"- **Чувствительность:** {alt_sp['sensitivity_str']}")
                        st.markdown(f"- **Пояснение:** {alt_item['note']}")
                        st.caption(f"*Ограничения:* {alt_sp['limitations']}")

    if result.get("rejected_reasons"):
        with st.expander("📋 Причины отклонения остальных типов термопар для заданного режима"):
            rej_rows = [
                {
                    "Тип термопары": SELECTOR_TC_SPECS[k]["title"],
                    "Причина отказа / неприменимости": reason
                }
                for k, reason in result["rejected_reasons"].items()
            ]
            st.dataframe(pd.DataFrame(rej_rows), use_container_width=True, hide_index=True)

    st.info(
        "📌 **Примечание о достоверности:** Выбор выполнен по учебно-справочным данным реферата. "
        "При реальном промышленном внедрении необходимо свериться с паспортом конкретного датчика, "
        "требованиями ГОСТ Р 8.585-2001, диаметром термоэлектродов, конструкцией защитной арматуры (чехла) "
        "и характеристиками вторичного измерительного прибора."
    )


render_thermocouple_selector()
