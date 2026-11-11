import re
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ STREAMLIT
# =====================================================================
st.set_page_config(
    page_title="Физическая лаборатория: Термо-ЭДС и Эффект Зеебека",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 2. ТОЧНЫЕ ТАБЛИЦЫ НСХ ТЕРМОПАР ИЗ ПРЕДОСТАВЛЕННЫХ ФАЙЛОВ (ГОСТ Р 8.585-2001)
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

# 2.2. ТХА (тип K, хромель / алюмель), диапазон -200 ... 1320 °C (56 точек из таблицы КИП-Сервис)
# От -200 до 500 °C шаг 50 °C; от 520 до 1320 °C шаг 20 °C
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

# Единый справочник стандартных термопар
THERMOCOUPLES_DB = {
    "ТЖК (тип J, Железо-Константан, ГОСТ Р 8.585-2001)": {
        "unit": "мВ",
        "min_t": -210,
        "max_t": 1200,
        "default_hot": 500,
        "temps": TJK_TEMPS,
        "values": TJK_MV,
        "color": "#80ed99",
        "electrodes": ("Железо (+)", "Константан (-)")
    },
    "ТХА (тип K, Хромель-Алюмель, ГОСТ Р 8.585-2001)": {
        "unit": "мВ",
        "min_t": -200,
        "max_t": 1320,
        "default_hot": 500,
        "temps": THA_TEMPS,
        "values": THA_MV,
        "color": "#00b4d8",
        "electrodes": ("Хромель (+)", "Алюмель (-)")
    },
    "ТХК (тип L, Хромель-Копель, ГОСТ Р 8.585-2001)": {
        "unit": "мВ",
        "min_t": -200,
        "max_t": 800,
        "default_hot": 500,
        "temps": THK_TEMPS,
        "values": THK_MV,
        "color": "#f77f00",
        "electrodes": ("Хромель (+)", "Копель (-)")
    }
}

# База данных металлов и сплавов для Стенда №2 (абсолютный коэффициент Зеебека при ~20 °C)
METALS_DB = {
    "Хромель (Ni90-Cr10)": {
        "seebeck": 24.0,
        "color_hex": "#80ed99",
        "three_hex": "0x80ed99",
        "description": "Жаростойкий сплав никеля (90%) и хрома (10%), положительный термоэлектрод пар ТХА и ТХК."
    },
    "Железо (Fe)": {
        "seebeck": 16.0,
        "color_hex": "#adb5bd",
        "three_hex": "0xadb5bd",
        "description": "Технически чистое железо, положительный электрод термопары ТЖК."
    },
    "Медь (Cu)": {
        "seebeck": 1.8,
        "color_hex": "#f77f00",
        "three_hex": "0xf77f00",
        "description": "Электротехническая медь с малой абсолютной термо-ЭДС."
    },
    "Платина (Pt)": {
        "seebeck": -4.5,
        "color_hex": "#e0e6ed",
        "three_hex": "0xe0e6ed",
        "description": "Благородный металл, используемый как эталон при построении термоэлектрических рядов."
    },
    "Алюмель (Ni95-Mn2-Al2-Si1)": {
        "seebeck": -17.0,
        "color_hex": "#00b4d8",
        "three_hex": "0x00b4d8",
        "description": "Никелевый сплав, образующий с хромелем пару ТХА (при 20 °C S_пара ≈ 41 мкВ/°C)."
    },
    "Константан (Cu55-Ni45)": {
        "seebeck": -35.0,
        "color_hex": "#e0aaff",
        "three_hex": "0xe0aaff",
        "description": "Медно-никелевый сплав, образующий с железом пару ТЖК (при 20 °C S_пара ≈ 51 мкВ/°C)."
    },
    "Копель (Cu56-Ni44-Mn)": {
        "seebeck": -40.5,
        "color_hex": "#ff9f1c",
        "three_hex": "0xff9f1c",
        "description": "Термоэлектродный сплав, образующий с хромелем пару ТХК (при 20 °C S_пара ≈ 64.5 мкВ/°C)."
    }
}


# =====================================================================
# 3. ФИЗИЧЕСКИЕ ФУНКЦИИ РАСЧЕТА ТЕРМО-ЭДС И КОЭФФИЦИЕНТА ЗЕЕБЕКА
# =====================================================================
def calculate_nominal_emf(sensor_key: str, temp_c: float) -> float:
    """
    Возвращает точное табличное значение Термо-ЭДС E(T) по ГОСТ Р 8.585-2001
    из загруженных массивов (с линейной интерполяцией только между узлами сетки).
    """
    spec = THERMOCOUPLES_DB[sensor_key]
    return float(np.interp(temp_c, spec["temps"], spec["values"]))


def calculate_seebeck_diff(sensor_key: str, temp_c: float) -> float:
    """
    Вычисляет дифференциальную термо-ЭДС S(T) = dE/dT в мкВ/°C
    по соседним табличным узлам с шагом dt = 10 °C.
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


# =====================================================================
# 4. 3D-ВИЗУАЛИЗАЦИЯ СТЕНДА №1 И СТЕНДА №2 (THREE.JS + ORBITCONTROLS)
# =====================================================================
def render_3d_stand1_gradient(
    t_hot: float,
    t_cold: float,
    sensor_title: str,
    emf_str: str,
    seebeck_str: str,
    fault_state: str
) -> str:
    """
    3D-модель термопары для Стенда №1:
    Подсвечивает горячий спай красным/оранжевым (T_hot), а холодный спай — синим/голубым (T_cold).
    """
    hot_hex, hot_emissive, hot_int = hot_junction_rgb(t_hot)
    cold_hex, cold_emissive, cold_int = cold_junction_rgb(t_cold)
    border_col = "#ff2a2a" if fault_state != "Норма" else "#00b4d8"
    is_open = "Обрыв" in fault_state
    is_short = "Паразитный" in fault_state

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
                border-radius: 8px; border-left: 4px solid {border_col}; font-size: 12.5px;
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
            .hot-badge {{ color: #ff6b35; font-weight: bold; }}
            .cold-badge {{ color: #4cc9f0; font-weight: bold; }}
            #hud b {{ color: #ff9f1c; }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
        <div id="hud">
            <div>Термопара: <b>{sensor_title}</b></div>
            <div>Горячий спай T_hot: <span class="hot-badge">{t_hot:.1f} °C</span></div>
            <div>Холодный спай T_cold: <span class="cold-badge">{t_cold:.1f} °C</span></div>
            <div>Результирующая ЭДС: <b>{emf_str}</b> | S(T): <b>{seebeck_str}</b></div>
            <div>Цепь: <b>{fault_state}</b></div>
        </div>
        <div id="legend">
            🔴 Внизу: Горячий спай (T_hot) &nbsp;|&nbsp; 🔵 Вверху: Холодный спай (T_cold)
        </div>
        <div id="hint">🖱️ ЛКМ: вращать 3D | Колесо: масштаб | ПКМ: панорама</div>
        <script>
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0e1117);

            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0.0, 0.3, 6.8);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
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

            // 1. ХОЛОДНЫЙ СПАЙ (синий/голубой изотермический блок вверху)
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

            // 2. ДВА ПРОВОДНИКА С ТЕПЛОВЫМ ГРАДИЕНТОМ ОТ T_cold К T_hot
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

            // 3. ГОРЯЧИЙ СПАЙ (сфера сварного соединения внизу)
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

            // 4. ВИЗУАЛИЗАЦИЯ ФИЗИЧЕСКИХ НАРУШЕНИЙ ЦЕПИ
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
    emf_mv: float,
    fault_state: str
) -> str:
    """
    3D-модель для Стенда №2:
    Два соединенных разнородных проводника (Металл 1 и Металл 2), подключенных к вольтметру.
    """
    border_col = "#ff2a2a" if fault_state != "Норма" else "#80ed99"
    is_open = "Обрыв" in fault_state
    is_short = "Паразитный" in fault_state
    needle_angle = float(np.clip((emf_mv / 50.0) * 0.9, -1.1, 1.1))
    emf_label = "0.000 мВ (Обрыв)" if is_open else f"{emf_mv:+.3f} мВ"

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
                border-radius: 8px; border-left: 4px solid {border_col}; font-size: 12.5px;
                pointer-events: none; z-index: 10; line-height: 1.45;
            }}
            #hint {{
                position: absolute; bottom: 10px; left: 12px; color: #9aa5b1;
                background: rgba(14, 17, 23, 0.75); padding: 5px 10px;
                border-radius: 6px; font-size: 11px; pointer-events: none; z-index: 10;
            }}
            #hud b {{ color: #80ed99; }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
        <div id="hud">
            <div>Ветвь А: <b>{metal1_name}</b> | Ветвь B: <b>{metal2_name}</b></div>
            <div>Коэффициент пары S_пара: <b>{s_pair:+.1f} мкВ/°C</b> | ΔT: <b>{delta_t:.0f} °C</b></div>
            <div>Показание вольтметра: <b>{emf_label}</b></div>
            <div>Состояние контура: <b>{fault_state}</b></div>
        </div>
        <div id="hint">🖱️ ЛКМ: вращать 3D | Колесо: масштаб | ПКМ: панорама</div>
        <script>
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0e1117);

            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0.0, 0.5, 7.2);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
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
        </script>
    </body>
    </html>
    """


# =====================================================================
# 5. БОКОВАЯ ПАНЕЛЬ: ВЫБОР СТЕНДА, НАРУШЕНИЯ ЦЕПИ И ЗАДАЧИ ПО ФИЗИКЕ
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

st.sidebar.markdown("---")
st.sidebar.subheader("🎓 Практикум Профессора")
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
        "Выберите стандартную термопару (ГОСТ Р 8.585-2001):",
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

    # Расчет физических величин строго по таблицам из PDF-файлов
    e_hot = calculate_nominal_emf(sensor_name, t_hot)
    e_cold = calculate_nominal_emf(sensor_name, t_cold)
    delta_t = t_hot - t_cold
    seebeck_hot = calculate_seebeck_diff(sensor_name, t_hot)

    if circuit_fault_mode == "Обрыв термоэлектрического контура":
        st.error("⚠️ Нарушение цепи: Обрыв термоэлектрического контура! Замкнутая цепь разомкнута, ток носителей заряда равен нулю.")
        e_result = 0.0
        emf_display = "0.000 мВ (Обрыв)"
    elif circuit_fault_mode == "Паразитный спай (КЗ)":
        t_parasitic = t_cold + 0.25 * delta_t
        e_result = calculate_nominal_emf(sensor_name, t_parasitic) - e_cold
        st.warning(
            f"⚠️ Нарушение цепи: Паразитный спай (КЗ) в точке с температурой T_кз ≈ {t_parasitic:.1f} °C! "
            f"Рабочий участок шунтирован, измеряемая ЭДС занижена."
        )
        emf_display = f"{e_result:.3f} мВ (Шунт КЗ)"
    else:
        e_result = e_hot - e_cold
        emf_display = f"{e_result:.3f} мВ"

    # Отображение физической формулы с точными табличными числами
    st.latex(
        rf"E_{{\text{{рез}}}} = E(T_{{\text{{hot}}}}) - E(T_{{\text{{cold}}}}) = "
        rf"E({t_hot:.0f}^\circ\text{{C}}) - E({t_cold:.0f}^\circ\text{{C}}) = "
        rf"{e_hot:.3f} - ({e_cold:.3f}) = {e_hot - e_cold:.3f}\text{{ мВ}}"
    )

    # Метрики Стенда №1
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "Результирующая Термо-ЭДС (E)",
        emf_display,
        delta=f"E(T_hot)={e_hot:.3f} мВ | E(T_cold)={e_cold:.3f} мВ"
    )
    m2.metric(
        "Дифференциальная термо-ЭДС S(T)",
        f"{seebeck_hot:.2f} мкВ/°C",
        delta=f"При T_hot = {t_hot:.0f} °C"
    )
    m3.metric(
        "Градиент температур (ΔT)",
        f"{delta_t:+.1f} °C",
        delta=f"T_hot ({t_hot:.0f} °C) − T_cold ({t_cold:.0f} °C)"
    )
    m4.metric(
        "Термоэлектродная пара",
        f"{spec['electrodes'][0]} / {spec['electrodes'][1]}",
        delta=f"Режим: {circuit_fault_mode}"
    )

    col_plot, col_3d = st.columns([3, 2])

    with col_plot:
        st.subheader("Формирование результирующей Термо-ЭДС на кривой НСХ")
        t_curve = spec["temps"]
        e_curve_abs = spec["values"]
        e_curve_rel = e_curve_abs - e_cold

        fig_stand1 = go.Figure()

        # Кривая E(T) - E(T_cold)
        fig_stand1.add_trace(go.Scatter(
            x=t_curve, y=e_curve_rel, mode="lines",
            name=f"E(T) − E({t_cold:.0f} °C)",
            line=dict(color=spec["color"], width=3)
        ))

        # Табличные кривые E(T) при T_cold = 0 °C (пунктиром для сверки с ГОСТ)
        fig_stand1.add_trace(go.Scatter(
            x=t_curve, y=e_curve_abs, mode="lines+markers",
            name="Таблица ГОСТ E(T) при T₀ = 0 °C",
            line=dict(color="#adb5bd", width=1.5, dash="dash"),
            marker=dict(size=4, color="#ffffff")
        ))

        # Точка холодного спая
        fig_stand1.add_trace(go.Scatter(
            x=[t_cold], y=[0.0],
            mode="markers+text", name="Холодный спай (T_cold)",
            text=[f"  T_cold = {t_cold:.0f} °C (E_табл = {e_cold:.3f} мВ)"],
            textposition="bottom right",
            marker=dict(size=11, color="#00b4d8", symbol="circle", line=dict(width=2, color="white"))
        ))

        # Точка горячего спая (результирующая и табличная)
        fig_stand1.add_trace(go.Scatter(
            x=[t_hot], y=[e_result],
            mode="markers+text", name="Рабочая точка E_рез",
            text=[f"  T_hot = {t_hot:.0f} °C (E_рез = {emf_display}, E_табл = {e_hot:.3f} мВ)"],
            textposition="top left",
            marker=dict(size=13, color="#ff4d4d", symbol="diamond", line=dict(width=2, color="white"))
        ))

        if "ai_alloy" in st.session_state:
            ai = st.session_state["ai_alloy"]
            a1, a2, a3 = ai["coeffs"]["a1"], ai["coeffs"]["a2"], ai["coeffs"]["a3"]
            e_ai_cold = a1 * t_cold + a2 * (t_cold ** 2) + a3 * (t_cold ** 3)
            e_ai_curve = (a1 * t_curve + a2 * (t_curve ** 2) + a3 * (t_curve ** 3)) - e_ai_cold
            fig_stand1.add_trace(go.Scatter(
                x=t_curve, y=e_ai_curve, mode="lines",
                name=f"Гипотетический сплав ({ai['s_target']} мкВ/°C)",
                line=dict(color="#ff9f1c", width=2.5, dash="dot")
            ))

        fig_stand1.update_layout(
            xaxis_title="Температура T, °C",
            yaxis_title="Термо-ЭДС E, мВ",
            template="plotly_dark",
            height=430,
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified"
        )
        st.plotly_chart(fig_stand1, use_container_width=True)

    with col_3d:
        st.subheader("3D-модель теплового градиента спаев")
        short_title = sensor_name.split("(")[0].strip()
        components.html(
            render_3d_stand1_gradient(
                t_hot=t_hot,
                t_cold=t_cold,
                sensor_title=short_title,
                emf_str=emf_display,
                seebeck_str=f"{seebeck_hot:.2f} мкВ/°C",
                fault_state=circuit_fault_mode
            ),
            height=430
        )

    # Таблица для быстрой проверки точных значений из файла ГОСТ Р 8.585-2001
    with st.expander("📋 Справочная таблица НСХ выбранной термопары (данные из PDF ГОСТ Р 8.585-2001)"):
        df_gost = pd.DataFrame({
            "Температура раб. конца, °C": spec["temps"].astype(int),
            "Термо-ЭДС E(T) при T₀=0 °C, мВ": [f"{v:.3f}" for v in spec["values"]],
            f"Результирующая ЭДС при T_cold={t_cold:.0f} °C, мВ": [f"{(v - e_cold):.3f}" for v in spec["values"]]
        })
        st.dataframe(df_gost, use_container_width=True, height=260)


# =====================================================================
# 7. СТЕНД №2: ИССЛЕДОВАНИЕ ЭФФЕКТА ЗЕЕБЕКА В РАЗНОРОДНЫХ МЕТАЛЛАХ
# =====================================================================
else:
    st.title("Стенд №2: Исследование эффекта Зеебека в разнородных металлах (Термоэлектрические пары)")

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

    delta_t_val = float(st.sidebar.slider(
        "Разность температур спаев ΔT = T_hot − T_cold (°C):",
        min_value=0,
        max_value=800,
        value=500,
        step=10
    ))

    s_metal1 = METALS_DB[metal_1]["seebeck"]
    s_metal2 = METALS_DB[metal_2]["seebeck"]
    s_pair = s_metal1 - s_metal2  # мкВ/°C

    nominal_pair_emf_mv = (s_pair * delta_t_val) / 1000.0

    if circuit_fault_mode == "Обрыв термоэлектрического контура":
        st.error("⚠️ Нарушение цепи: Обрыв термоэлектрического контура! Измерительная цепь разомкнута.")
        measured_pair_emf_mv = 0.0
    elif circuit_fault_mode == "Паразитный спай (КЗ)":
        measured_pair_emf_mv = 0.25 * nominal_pair_emf_mv
        st.warning("⚠️ Нарушение цепи: Паразитный спай (КЗ)! Проводники замкнуты в промежуточной температурной зоне.")
    else:
        measured_pair_emf_mv = nominal_pair_emf_mv

    if metal_1 == metal_2:
        st.info("ℹ️ Выбраны одинаковые металлы (S_металл1 = S_металл2). В однородной цепи эффект Зеебека не создает результирующей ЭДС (S_пара = 0).")

    st.latex(
        rf"S_{{\text{{пара}}}} = S_{{\text{{металл1}}}} - S_{{\text{{металл2}}}} = "
        rf"({s_metal1:+.1f}) - ({s_metal2:+.1f}) = {s_pair:+.1f}\text{{ мкВ/}}^\circ\text{{C}}, \quad "
        rf"E(\Delta T) = S_{{\text{{пара}}}} \cdot \Delta T = {nominal_pair_emf_mv:+.3f}\text{{ мВ}}"
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"S₁ ({metal_1.split('(')[0].strip()})", f"{s_metal1:+.1f} мкВ/°C")
    c2.metric(f"S₂ ({metal_2.split('(')[0].strip()})", f"{s_metal2:+.1f} мкВ/°C")
    c3.metric("Итоговый коэфф. Зеебека S_пара", f"{s_pair:+.1f} мкВ/°C")
    c4.metric(
        "Термо-ЭДС пары E(ΔT)",
        f"{measured_pair_emf_mv:+.3f} мВ",
        delta=f"При ΔT = {delta_t_val:.0f} °C ({circuit_fault_mode})"
    )

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.subheader("Зависимость Термо-ЭДС E от разности температур ΔT")
        dt_arr = np.linspace(0, 800, 81)
        e_pair_arr = (s_pair * dt_arr) / 1000.0

        fig_stand2 = go.Figure()
        fig_stand2.add_trace(go.Scatter(
            x=dt_arr, y=e_pair_arr, mode="lines",
            name=f"Линейная модель: {metal_1.split('(')[0].strip()} — {metal_2.split('(')[0].strip()}",
            line=dict(color="#80ed99", width=3.5)
        ))

        # Если выбрана стандартная пара (Хромель-Копель, Хромель-Алюмель или Железо-Константан),
        # накладываем реальную табличную кривую из PDF для сравнения с линейным приближением!
        pair_tuple = (metal_1.split("(")[0].strip(), metal_2.split("(")[0].strip())
        gost_match_key = None
        if pair_tuple == ("Хромель", "Копель"):
            gost_match_key = "ТХК (тип L, Хромель-Копель, ГОСТ Р 8.585-2001)"
        elif pair_tuple == ("Хромель", "Алюмель"):
            gost_match_key = "ТХА (тип K, Хромель-Алюмель, ГОСТ Р 8.585-2001)"
        elif pair_tuple == ("Железо", "Константан"):
            gost_match_key = "ТЖК (тип J, Железо-Константан, ГОСТ Р 8.585-2001)"

        if gost_match_key is not None:
            e_gost_dt = [calculate_nominal_emf(gost_match_key, dt) for dt in dt_arr]
            fig_stand2.add_trace(go.Scatter(
                x=dt_arr, y=e_gost_dt, mode="lines",
                name=f"Реальная НСХ по ГОСТ ({gost_match_key.split('(')[0].strip()})",
                line=dict(color="#00b4d8", width=2.5, dash="dash")
            ))

        fig_stand2.add_trace(go.Scatter(
            x=[delta_t_val], y=[measured_pair_emf_mv],
            mode="markers+text", name="Рабочая точка пары",
            text=[f"  ΔT = {delta_t_val:.0f} °C ({measured_pair_emf_mv:+.3f} мВ)"],
            textposition="top left",
            marker=dict(size=14, color="#ff4d4d", symbol="diamond", line=dict(width=2, color="white"))
        ))

        if "ai_alloy" in st.session_state:
            ai = st.session_state["ai_alloy"]
            a1, a2, a3 = ai["coeffs"]["a1"], ai["coeffs"]["a2"], ai["coeffs"]["a3"]
            e_ai_dt = a1 * dt_arr + a2 * (dt_arr ** 2) + a3 * (dt_arr ** 3)
            fig_stand2.add_trace(go.Scatter(
                x=dt_arr, y=e_ai_dt, mode="lines",
                name=f"ИИ-термоэлектрик ({ai['s_target']} мкВ/°C)",
                line=dict(color="#ff9f1c", width=2.5, dash="dot")
            ))

        fig_stand2.update_layout(
            xaxis_title="Разность температур спаев ΔT = T_hot − T_cold, °C",
            yaxis_title="Термо-ЭДС пары E, мВ",
            template="plotly_dark",
            height=430,
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified"
        )
        st.plotly_chart(fig_stand2, use_container_width=True)

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
                emf_mv=measured_pair_emf_mv,
                fault_state=circuit_fault_mode
            ),
            height=430
        )

st.markdown("---")


# =====================================================================
# 8. ИИ-МЕНТОР (ПРОФЕССОР ТЕРМОДИНАМИКИ) И СИНТЕЗАТОР ТЕРМОЭЛЕКТРИКОВ
# =====================================================================
st.subheader("👨‍🏫 ИИ-Ментор: Профессор термодинамики и Синтезатор термоэлектриков")


def build_hypothetical_thermoelectric(target_s_uv: float) -> dict:
    """
    Рассчитывает полиномиальные коэффициенты НСХ E(T) = a1*T + a2*T^2 + a3*T^3
    для гипотетического термоэлектрика по заданному коэффициенту Зеебека S (мкВ/°C).
    """
    a1 = target_s_uv / 1000.0
    sign = 1.0 if target_s_uv >= 0 else -1.0
    a2 = sign * 1.45e-5
    a3 = -sign * 4.20e-9
    t_vec = np.linspace(0, 1000, 200)
    e_vec = a1 * t_vec + a2 * (t_vec ** 2) + a3 * (t_vec ** 3)
    return {
        "name": f"ThermoAlloy-S{int(abs(target_s_uv))}",
        "s_target": round(target_s_uv, 2),
        "coeffs": {"a1": a1, "a2": a2, "a3": a3},
        "t": t_vec,
        "e": e_vec
    }


with st.expander("🔬 Интерактивный генератор гипотетического термоэлектрика (расчет полинома НСХ)", expanded=False):
    col_gen1, col_gen2 = st.columns([2, 1])
    with col_gen1:
        desired_s = st.number_input(
            "Введите желаемый коэффициент Зеебека S₀ (мкВ/°C):",
            min_value=-250.0,
            max_value=250.0,
            value=75.0,
            step=5.0
        )
    with col_gen2:
        st.write("")
        st.write("")
        if st.button("Синтезировать полином НСХ"):
            st.session_state["ai_alloy"] = build_hypothetical_thermoelectric(desired_s)
            st.rerun()

    if "ai_alloy" in st.session_state:
        ai_cur = st.session_state["ai_alloy"]
        c_a1 = ai_cur["coeffs"]["a1"]
        c_a2 = ai_cur["coeffs"]["a2"]
        c_a3 = ai_cur["coeffs"]["a3"]
        st.success(f"Активен гипотетический сплав **{ai_cur['name']}** ($S_0 = {ai_cur['s_target']}$ мкВ/°C) — кривая добавлена на графики стендов.")
        st.latex(
            rf"E(T) = a_1 T + a_2 T^2 + a_3 T^3 = "
            rf"{c_a1:.5f}\,T + ({c_a2:.2e})\,T^2 + ({c_a3:.2e})\,T^3 \text{{ [мВ]}}"
        )

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "Приветствую в физической лаборатории термоэлектрических явлений! Я — **Профессор термодинамики**.\n\n"
                "Задайте вопрос по физике эффекта Зеебека или укажите желаемый коэффициент Зеебека для расчета полинома НСХ:\n"
                "- *«Почему при равенстве температур спаев Термо-ЭДС равна нулю?»*\n"
                "- *«Как изменится ЭДС, если удлинить провода?»*\n"
                "- *«Что такое закон Вольта для последовательной цепи металлов?»*\n"
                "- *«Синтезируй термоэлектрик с коэффициентом Зеебека 85 мкВ/°C»*"
            )
        }
    ]

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input(
    "Спросите Профессора (например: 'Что такое закон Вольта?' или 'Сплав 90 мкВ/°C')..."
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
            "Если проводники термопары однородны по химическому составу, то **Термо-ЭДС не изменится** при любом удлинении проводов. "
            "Причина в том, что $E = \\int_{T_{\\text{cold}}}^{T_{\\text{hot}}} S_{AB}(T)\\,dT$ является функцией только граничных температур "
            "концов $T_{\\text{hot}}$ и $T_{\\text{cold}}$, а не градиента $\\nabla T$ по отдельности. Однако при увеличении длины $l$ возрастает "
            "внутреннее омическое сопротивление контура $R_{\\text{вн}} = \\rho \\frac{l}{S_{\\text{сеч}}}$, что увеличивает падение напряжения "
            "при протекании тока через низкоомный прибор."
        )
    elif any(k in q_low for k in ["вольт", "третьего", "третий", "последоват"]):
        reply = (
            "**Физическое объяснение (Закон Вольта / Закон третьего металла):**\n\n"
            "Согласно закону Вольта, включение в термоэлектрический контур любого третьего проводника $C$ (например, медных выводов "
            "и входной цепи вольтметра) **не изменяет результирующую Термо-ЭДС**, если оба конца этого третьего проводника находятся "
            "при одинаковой температуре $T_{\\text{cold}}$:\n"
            "$$\\int_{T_{\\text{cold}}}^{T_{\\text{cold}}} S_C(T)\\,dT = 0$$\n"
            "Дополнительные термо-ЭДС на контактах «Металл А — Медь» и «Медь — Металл B» взаимно компенсируют друг друга."
        )
    elif num_match and any(k in q_low for k in ["сплав", "зеебек", "мкв", "синтез", "коэфф", "сгенер"]):
        s_val = float(num_match.group(1).replace(",", "."))
        s_val = float(np.clip(s_val, -300.0, 300.0))
        alloy_data = build_hypothetical_thermoelectric(s_val)
        st.session_state["ai_alloy"] = alloy_data
        c1, c2, c3 = alloy_data["coeffs"]["a1"], alloy_data["coeffs"]["a2"], alloy_data["coeffs"]["a3"]

        reply = (
            f"Синтезирован гипотетический термоэлектрик **`{alloy_data['name']}`** для $S_0 = {alloy_data['s_target']}$ мкВ/°C "
            f"(кривая добавлена на графики Стенда №1 и Стенда №2):\n\n"
            f"- **Линейный коэффициент $a_1$:** `{c1:.5f}` мВ/°C\n"
            f"- **Квадратичный коэффициент нелинейности $a_2$:** `{c2:.2e}` мВ/°C²\n"
            f"- **Кубический коэффициент ангармонизма $a_3$:** `{c3:.2e}` мВ/°C³\n\n"
            f"Уравнение НСХ сплава:\n"
            f"$$E(T) = {c1:.5f}\\,T + ({c2:.2e})\\,T^2 + ({c3:.2e})\\,T^3\\text{{ [мВ]}}$$"
        )
    else:
        reply = (
            "Задайте один из фундаментальных вопросов (о равенстве температур спаев, удлинении проводов или законе Вольта) "
            "либо укажите желаемый коэффициент Зеебека в мкВ/°C (например: *«Синтезируй сплав 65 мкВ/°C»*), чтобы я рассчитал "
            "полиномиальные коэффициенты НСХ."
        )

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)