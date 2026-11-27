import re
import random
import sys
import base64
import html
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

THEME_MODE_OPTIONS = [
    "Светлая (дневная)",
    "Тёмная (ночная)",
]

ACCESSIBILITY_MODE_OPTIONS = [
    "Стандартный",
    "Повышенная читаемость",
    "Высокая контрастность",
]

THEME_ACCESSIBILITY_PALETTES = {
    "Светлая (дневная)": {
        "Стандартный": {
            "bg_main": "#FFFFFF",
            "bg_card": "#F8FAFC",
            "bg_nested": "#F1F5F9",
            "bg_hover": "#E2E8F0",
            "bg_active": "#CBD5E1",
            "text_primary": "#0F172A",
            "text_secondary": "#334155",
            "border": "#94A3B8",
            "border_strong": "#475569",
            "border_width": "1px",
            "accent": "#0369A1",
            "accent_hover": "#075985",
            "accent_active": "#0C4A6E",
            "accent_fg": "#FFFFFF",
            "focus": "#D97706",
            "success": "#15803D",
            "success_bg": "#DCFCE7",
            "warning": "#B45309",
            "warning_bg": "#FEF3C7",
            "error": "#B91C1C",
            "error_bg": "#FEE2E2",
            "disabled_bg": "#E2E8F0",
            "disabled_text": "#475569",
            "disabled_border": "#94A3B8",
            "font_base": "17px",
            "font_caption": "15px",
            "font_btn": "16px",
            "font_h1": "29px",
            "font_h2": "25px",
            "font_h3": "21px",
            "font_h4": "19px",
            "font_kpi": "21px",
            "line_height": "1.55",
            "touch_target": "44px",
            "slider_thumb": "24px",
            "card_pad": "1rem",
            "gap": "0.85rem",
            "caption_weight": "500",
            "alert_border_w": "1px",
            "kpi_1col_bp": "420px",
        },
        "Повышенная читаемость": {
            "bg_main": "#FFFFFF",
            "bg_card": "#F8FAFC",
            "bg_nested": "#EEF2F6",
            "bg_hover": "#E2E8F0",
            "bg_active": "#CBD5E1",
            "text_primary": "#000000",
            "text_secondary": "#1E293B",
            "border": "#64748B",
            "border_strong": "#334155",
            "border_width": "2px",
            "accent": "#0369A1",
            "accent_hover": "#075985",
            "accent_active": "#0C4A6E",
            "accent_fg": "#FFFFFF",
            "focus": "#D97706",
            "success": "#15803D",
            "success_bg": "#DCFCE7",
            "warning": "#92400E",
            "warning_bg": "#FEF3C7",
            "error": "#991B1B",
            "error_bg": "#FEE2E2",
            "disabled_bg": "#E2E8F0",
            "disabled_text": "#334155",
            "disabled_border": "#64748B",
            "font_base": "20px",
            "font_caption": "17px",
            "font_btn": "18px",
            "font_h1": "34px",
            "font_h2": "29px",
            "font_h3": "24px",
            "font_h4": "22px",
            "font_kpi": "24px",
            "line_height": "1.65",
            "touch_target": "52px",
            "slider_thumb": "28px",
            "card_pad": "1.25rem",
            "gap": "1.15rem",
            "caption_weight": "600",
            "alert_border_w": "2px",
            "kpi_1col_bp": "540px",
        },
        "Высокая контрастность": {
            "bg_main": "#FFFFFF",
            "bg_card": "#FFFFFF",
            "bg_nested": "#F8FAFC",
            "bg_hover": "#E2E8F0",
            "bg_active": "#CBD5E1",
            "text_primary": "#000000",
            "text_secondary": "#000000",
            "border": "#000000",
            "border_strong": "#000000",
            "border_width": "2px",
            "accent": "#000000",
            "accent_hover": "#1E293B",
            "accent_active": "#334155",
            "accent_fg": "#FFFFFF",
            "focus": "#D97706",
            "success": "#14532D",
            "success_bg": "#DCFCE7",
            "warning": "#78350F",
            "warning_bg": "#FEF08A",
            "error": "#7F1D1D",
            "error_bg": "#FECACA",
            "disabled_bg": "#F1F5F9",
            "disabled_text": "#334155",
            "disabled_border": "#475569",
            "font_base": "18px",
            "font_caption": "16px",
            "font_btn": "17px",
            "font_h1": "31px",
            "font_h2": "27px",
            "font_h3": "22px",
            "font_h4": "20px",
            "font_kpi": "22px",
            "line_height": "1.60",
            "touch_target": "48px",
            "slider_thumb": "26px",
            "card_pad": "1.1rem",
            "gap": "0.95rem",
            "caption_weight": "700",
            "alert_border_w": "2px",
            "kpi_1col_bp": "460px",
        },
    },
    "Тёмная (ночная)": {
        "Стандартный": {
            "bg_main": "#0E1117",
            "bg_card": "#161B24",
            "bg_nested": "#1F2633",
            "bg_hover": "#293345",
            "bg_active": "#192231",
            "text_primary": "#EEF2F6",
            "text_secondary": "#CBD5E1",
            "border": "#70829A",
            "border_strong": "#8294AD",
            "border_width": "1px",
            "accent": "#38BDF8",
            "accent_hover": "#7DD3FC",
            "accent_active": "#0EA5E9",
            "accent_fg": "#0B111A",
            "focus": "#FACC15",
            "success": "#4ADE80",
            "success_bg": "#12261E",
            "warning": "#FBBF24",
            "warning_bg": "#292011",
            "error": "#F87171",
            "error_bg": "#2B1418",
            "disabled_bg": "#1B202B",
            "disabled_text": "#94A3B8",
            "disabled_border": "#5B6B82",
            "font_base": "17px",
            "font_caption": "15px",
            "font_btn": "16px",
            "font_h1": "29px",
            "font_h2": "25px",
            "font_h3": "21px",
            "font_h4": "19px",
            "font_kpi": "21px",
            "line_height": "1.55",
            "touch_target": "44px",
            "slider_thumb": "24px",
            "card_pad": "1rem",
            "gap": "0.85rem",
            "caption_weight": "400",
            "alert_border_w": "1px",
            "kpi_1col_bp": "420px",
        },
        "Повышенная читаемость": {
            "bg_main": "#0E1117",
            "bg_card": "#161C26",
            "bg_nested": "#202837",
            "bg_hover": "#2C374C",
            "bg_active": "#1A2436",
            "text_primary": "#F5F8FC",
            "text_secondary": "#CBD6E4",
            "border": "#8DA2BD",
            "border_strong": "#A6BCD6",
            "border_width": "2px",
            "accent": "#38BDF8",
            "accent_hover": "#7DD3FC",
            "accent_active": "#0EA5E9",
            "accent_fg": "#0B111A",
            "focus": "#FACC15",
            "success": "#4ADE80",
            "success_bg": "#12281F",
            "warning": "#FBBF24",
            "warning_bg": "#2D2312",
            "error": "#F87171",
            "error_bg": "#30151A",
            "disabled_bg": "#1C222E",
            "disabled_text": "#9BA8BC",
            "disabled_border": "#6F829C",
            "font_base": "20px",
            "font_caption": "17px",
            "font_btn": "18px",
            "font_h1": "34px",
            "font_h2": "29px",
            "font_h3": "24px",
            "font_h4": "22px",
            "font_kpi": "24px",
            "line_height": "1.65",
            "touch_target": "52px",
            "slider_thumb": "28px",
            "card_pad": "1.25rem",
            "gap": "1.15rem",
            "caption_weight": "500",
            "alert_border_w": "2px",
            "kpi_1col_bp": "540px",
        },
        "Высокая контрастность": {
            "bg_main": "#000000",
            "bg_card": "#06080D",
            "bg_nested": "#0E131E",
            "bg_hover": "#1C2538",
            "bg_active": "#27334D",
            "text_primary": "#FFFFFF",
            "text_secondary": "#F8FAFC",
            "border": "#E2E8F0",
            "border_strong": "#FFFFFF",
            "border_width": "2px",
            "accent": "#FFE600",
            "accent_hover": "#FFF266",
            "accent_active": "#FFD000",
            "accent_fg": "#000000",
            "focus": "#00FFFF",
            "success": "#00FF85",
            "success_bg": "#002914",
            "warning": "#FFE600",
            "warning_bg": "#332900",
            "error": "#FF5C5C",
            "error_bg": "#380008",
            "disabled_bg": "#121722",
            "disabled_text": "#D1D9E6",
            "disabled_border": "#94A3B8",
            "font_base": "18px",
            "font_caption": "16px",
            "font_btn": "17px",
            "font_h1": "31px",
            "font_h2": "27px",
            "font_h3": "22px",
            "font_h4": "20px",
            "font_kpi": "22px",
            "line_height": "1.60",
            "touch_target": "48px",
            "slider_thumb": "26px",
            "card_pad": "1.1rem",
            "gap": "0.95rem",
            "caption_weight": "600",
            "alert_border_w": "2px",
            "kpi_1col_bp": "460px",
        },
    },
}

# Палитра по умолчанию (дневная светлая тема) для обратной совместимости
ACCESSIBILITY_PALETTES = THEME_ACCESSIBILITY_PALETTES[THEME_MODE_OPTIONS[0]]


def get_visual_system_css(
    accessibility_mode: str = "Стандартный",
    theme_mode: str = "Светлая (дневная)",
) -> str:
    """
    Формирует единую таблицу стилей KIP Simulator для выбранной цветовой темы
    («Светлая (дневная)» по умолчанию или «Тёмная (ночная)») и режима доступности
    («Стандартный», «Повышенная читаемость», «Высокая контрастность»).
    Гарантирует высокий контраст текста во всех виджетах Streamlit (включая radio, selectbox,
    slider, expander и боковую панель) без чёрного текста на тёмном фоне.
    """
    theme_key = theme_mode if theme_mode in THEME_ACCESSIBILITY_PALETTES else THEME_MODE_OPTIONS[0]
    theme_palettes = THEME_ACCESSIBILITY_PALETTES[theme_key]
    p = theme_palettes.get(accessibility_mode, theme_palettes["Стандартный"])
    is_light = (theme_key == "Светлая (дневная)")
    color_scheme = "light" if is_light else "dark"
    hc_ring = "#000000" if is_light else "#FFFFFF"

    extra_hc_rules = ""
    if accessibility_mode == "Высокая контрастность":
        extra_hc_rules = f"""
        /* Усиленное выделение активных состояний, предупреждений и подписей (Высокая контрастность) */
        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"],
        .stDownloadButton > button[kind="primary"],
        [data-testid="stBaseButton-primary"],
        [data-baseweb="tab"][aria-selected="true"] {{
            box-shadow: 0 0 0 2px {hc_ring};
            font-weight: 800;
        }}
        [data-testid="stAlert"] {{
            border-left-width: 6px !important;
        }}
        .kip-nav-status,
        .kip-stand-purpose,
        .kip-section-intro {{
            border-left-width: 6px;
        }}
        .kip-stage-step--active {{
            box-shadow: 0 0 0 2px {hc_ring};
        }}
        """
    elif accessibility_mode == "Повышенная читаемость":
        extra_hc_rules = """
        /* Дополнительные интервалы и увеличенные элементы управления (Повышенная читаемость) */
        .stMarkdown p,
        .stMarkdown li {
            margin-bottom: 0.65rem;
        }
        [data-testid="stExpander"],
        [data-testid="stAlert"],
        [data-testid="stVerticalBlockBorderWrapper"] {
            margin-bottom: 1.15rem;
        }
        """

    return f"""
    <style>
        /* =====================================================================
           ЕДИНАЯ ВИЗУАЛЬНАЯ СИСТЕМА KIP SIMULATOR (Светлая / Тёмная + Доступность)
           Активная тема: {theme_key} | Режим доступности: {accessibility_mode}
           ===================================================================== */
        :root {{
            color-scheme: {color_scheme};
            --kip-bg-main: {p["bg_main"]};
            --kip-bg-card: {p["bg_card"]};
            --kip-bg-nested: {p["bg_nested"]};
            --kip-bg-hover: {p["bg_hover"]};
            --kip-bg-active: {p["bg_active"]};
            --kip-text-primary: {p["text_primary"]};
            --kip-text-secondary: {p["text_secondary"]};
            --kip-border: {p["border"]};
            --kip-border-strong: {p["border_strong"]};
            --kip-border-width: {p["border_width"]};
            --kip-accent: {p["accent"]};
            --kip-accent-hover: {p["accent_hover"]};
            --kip-accent-active: {p["accent_active"]};
            --kip-accent-fg: {p["accent_fg"]};
            --kip-focus: {p["focus"]};
            --kip-success: {p["success"]};
            --kip-success-bg: {p["success_bg"]};
            --kip-warning: {p["warning"]};
            --kip-warning-bg: {p["warning_bg"]};
            --kip-error: {p["error"]};
            --kip-error-bg: {p["error_bg"]};
            --kip-disabled-bg: {p["disabled_bg"]};
            --kip-disabled-text: {p["disabled_text"]};
            --kip-disabled-border: {p["disabled_border"]};

            --kip-font-base: {p["font_base"]};
            --kip-font-caption: {p["font_caption"]};
            --kip-font-btn: {p["font_btn"]};
            --kip-font-h1: {p["font_h1"]};
            --kip-font-h2: {p["font_h2"]};
            --kip-font-h3: {p["font_h3"]};
            --kip-font-h4: {p["font_h4"]};
            --kip-font-kpi: {p["font_kpi"]};
            --kip-line-height: {p["line_height"]};
            --kip-caption-weight: {p["caption_weight"]};
            --kip-alert-border-w: {p["alert_border_w"]};

            --kip-radius: 10px;
            --kip-radius-sm: 8px;
            --kip-touch-target: {p["touch_target"]};
            --kip-slider-thumb: {p["slider_thumb"]};
            --kip-card-pad: {p["card_pad"]};
            --kip-gap: {p["gap"]};
        }}

        /* 1. Базовый фон, верхняя панель Streamlit, сайдбар и типографика */
        *, *::before, *::after {{
            box-sizing: border-box;
        }}

        html, body, .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            background-color: var(--kip-bg-main) !important;
            color: var(--kip-text-primary) !important;
            font-size: var(--kip-font-base);
            line-height: var(--kip-line-height);
        }}

        [data-testid="stHeader"] {{
            background-color: var(--kip-bg-main) !important;
            color: var(--kip-text-primary) !important;
            border-bottom: 1px solid var(--kip-border);
        }}

        [data-testid="stHeader"] button,
        [data-testid="stHeader"] svg {{
            color: var(--kip-text-primary) !important;
            fill: currentColor;
        }}

        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"] {{
            background-color: var(--kip-bg-card) !important;
            color: var(--kip-text-primary) !important;
        }}

        [data-testid="stSidebar"] {{
            border-right: var(--kip-border-width) solid var(--kip-border);
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] li {{
            color: var(--kip-text-primary);
        }}

        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"] {{
            background-color: var(--kip-bg-main) !important;
        }}

        .stApp h1 {{
            font-size: var(--kip-font-h1);
            line-height: 1.25;
            color: var(--kip-text-primary);
            font-weight: 700;
            margin-bottom: 0.75rem;
            overflow-wrap: break-word;
        }}

        .stApp h2 {{
            font-size: var(--kip-font-h2);
            line-height: 1.3;
            color: var(--kip-text-primary);
            font-weight: 700;
            margin-top: 1.1rem;
            margin-bottom: 0.65rem;
            overflow-wrap: break-word;
        }}

        .stApp h3 {{
            font-size: var(--kip-font-h3);
            line-height: 1.35;
            color: var(--kip-text-primary);
            font-weight: 600;
            margin-top: 0.9rem;
            margin-bottom: 0.5rem;
            overflow-wrap: break-word;
        }}

        .stApp h4 {{
            font-size: var(--kip-font-h4);
            line-height: 1.35;
            color: var(--kip-text-primary);
            font-weight: 600;
            margin-bottom: 0.45rem;
            overflow-wrap: break-word;
        }}

        .stMarkdown p,
        .stMarkdown li,
        .stMarkdown blockquote,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {{
            font-size: var(--kip-font-base);
            line-height: var(--kip-line-height);
            color: var(--kip-text-primary);
            max-width: 78ch;
            overflow-wrap: break-word;
        }}

        .stMarkdown blockquote {{
            background-color: var(--kip-bg-nested);
            border-left: 4px solid var(--kip-accent);
            padding: 0.75rem 1rem;
            border-radius: 0 var(--kip-radius-sm) var(--kip-radius-sm) 0;
            margin: 0.75rem 0;
        }}

        .stMarkdown code,
        .stApp code {{
            background-color: var(--kip-bg-nested);
            color: var(--kip-text-primary);
            border: 1px solid var(--kip-border);
            padding: 0.1rem 0.35rem;
            border-radius: 4px;
        }}

        /* Читаемые подписи без снижения прозрачности */
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
        .stCaption,
        .stApp small {{
            font-size: var(--kip-font-caption);
            font-weight: var(--kip-caption-weight);
            line-height: 1.5;
            color: var(--kip-text-secondary) !important;
            opacity: 1 !important;
            overflow-wrap: break-word;
        }}

        .stApp a {{
            color: var(--kip-accent);
            text-decoration: underline;
            text-underline-offset: 3px;
            overflow-wrap: anywhere;
        }}

        .stApp a:hover {{
            color: var(--kip-accent-hover);
        }}

        .stApp hr {{
            border-color: var(--kip-border);
            opacity: 1;
            margin: 1.25rem 0;
        }}

        /* Формулы LaTeX: горизонтальная прокрутка внутри контейнера формулы без растягивания страницы */
        .katex-display {{
            background-color: var(--kip-bg-nested);
            color: var(--kip-text-primary);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius-sm);
            padding: 0.75rem 1rem;
            margin: 0.75rem 0;
            max-width: 100%;
            overflow-x: auto;
            overflow-y: hidden;
        }}

        .katex {{
            color: var(--kip-text-primary);
            max-width: 100%;
        }}

        /* 2. Единая система карточек и контейнеров */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius);
            padding: var(--kip-card-pad);
            margin-bottom: var(--kip-gap);
            max-width: 100%;
        }}

        [data-testid="stForm"] {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius);
            padding: var(--kip-card-pad);
            margin-bottom: 1rem;
            max-width: 100%;
        }}

        [data-testid="stMetric"] {{
            background-color: var(--kip-bg-nested);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius);
            padding: 0.9rem 1rem;
            height: 100%;
        }}

        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p {{
            font-size: var(--kip-font-caption);
            line-height: 1.4;
            color: var(--kip-text-secondary);
            font-weight: 600;
            white-space: normal;
        }}

        [data-testid="stMetricValue"] {{
            font-size: var(--kip-font-kpi);
            line-height: 1.3;
            color: var(--kip-text-primary);
            font-weight: 700;
            white-space: normal;
        }}

        [data-testid="stMetricDelta"] {{
            font-size: var(--kip-font-caption);
            line-height: 1.4;
            white-space: normal;
        }}

        [data-testid="stExpander"] {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius);
            margin-bottom: 0.85rem;
            max-width: 100%;
        }}

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary svg {{
            color: var(--kip-text-primary) !important;
        }}

        [data-testid="stExpander"] summary {{
            min-height: var(--kip-touch-target);
            padding: 0.55rem 0.9rem;
            font-size: var(--kip-font-base);
            font-weight: 600;
            border-radius: var(--kip-radius);
        }}

        [data-testid="stExpander"] summary:hover {{
            background-color: var(--kip-bg-nested);
        }}

        [data-testid="stChatMessage"] {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius);
            padding: 0.95rem 1.1rem;
            margin-bottom: 0.8rem;
            max-width: 100%;
        }}

        [data-testid="stProgress"] p {{
            color: var(--kip-text-primary) !important;
        }}

        /* Статусные уведомления (инфо / успех / предупреждение / ошибка) */
        [data-testid="stAlert"],
        [data-testid="stAlert"] > div {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-radius: var(--kip-radius);
            border-width: var(--kip-alert-border-w);
            border-style: solid;
            border-color: var(--kip-border-strong) !important;
            font-size: var(--kip-font-base);
            line-height: var(--kip-line-height);
            max-width: 100%;
        }}

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] li,
        [data-testid="stAlert"] span,
        [data-testid="stAlert"] div,
        [data-testid="stAlert"] strong,
        [data-testid="stAlert"] a {{
            color: #000000 !important;
            max-width: 100%;
        }}

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] li {{
            font-size: var(--kip-font-base);
        }}

        [data-testid="stAlert"]:has([data-testid="stNotificationContentInfo"]),
        [data-testid="stAlert"]:has([data-testid="stNotificationContentSuccess"]),
        [data-testid="stAlert"]:has([data-testid="stNotificationContentWarning"]),
        [data-testid="stAlert"]:has([data-testid="stNotificationContentError"]) {{
            background-color: #FFFFFF !important;
        }}

        /* 3. Кнопки и элементы управления (с безопасным переносом текста при 320 px и зуме 200%) */
        .stButton > button,
        .stFormSubmitButton > button,
        .stDownloadButton > button,
        [data-testid="stChatInputSubmitButton"] {{
            min-height: var(--kip-touch-target);
            min-width: var(--kip-touch-target);
            height: auto;
            padding: 0.6rem 1.05rem;
            font-size: var(--kip-font-btn);
            font-weight: 600;
            line-height: 1.35;
            white-space: normal;
            word-break: break-word;
            border-radius: var(--kip-radius-sm);
            border: var(--kip-border-width) solid var(--kip-border-strong);
            background-color: var(--kip-bg-nested);
            color: var(--kip-text-primary) !important;
            transition: background-color 0.12s ease, border-color 0.12s ease, color 0.12s ease;
        }}

        .stButton > button p,
        .stFormSubmitButton > button p,
        .stDownloadButton > button p {{
            color: inherit !important;
            font-size: inherit;
            margin: 0;
        }}

        [data-testid="stChatInputSubmitButton"] {{
            padding: 0.45rem;
        }}

        .stButton > button:hover:not(:disabled),
        .stFormSubmitButton > button:hover:not(:disabled),
        .stDownloadButton > button:hover:not(:disabled),
        [data-testid="stChatInputSubmitButton"]:hover:not(:disabled) {{
            background-color: var(--kip-bg-hover);
            border-color: var(--kip-accent);
            color: var(--kip-text-primary) !important;
        }}

        .stButton > button:active:not(:disabled),
        .stFormSubmitButton > button:active:not(:disabled),
        .stDownloadButton > button:active:not(:disabled),
        [data-testid="stChatInputSubmitButton"]:active:not(:disabled) {{
            background-color: var(--kip-bg-active);
            border-color: var(--kip-accent-active);
        }}

        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"],
        .stDownloadButton > button[kind="primary"],
        [data-testid="stBaseButton-primary"] {{
            background-color: var(--kip-accent);
            border-color: var(--kip-accent);
            color: var(--kip-accent-fg) !important;
        }}

        .stButton > button[kind="primary"]:hover:not(:disabled),
        .stFormSubmitButton > button[kind="primary"]:hover:not(:disabled),
        .stDownloadButton > button[kind="primary"]:hover:not(:disabled),
        [data-testid="stBaseButton-primary"]:hover:not(:disabled) {{
            background-color: var(--kip-accent-hover);
            border-color: var(--kip-accent-hover);
            color: var(--kip-accent-fg) !important;
        }}

        .stButton > button[kind="primary"]:active:not(:disabled),
        .stFormSubmitButton > button[kind="primary"]:active:not(:disabled),
        .stDownloadButton > button[kind="primary"]:active:not(:disabled),
        [data-testid="stBaseButton-primary"]:active:not(:disabled) {{
            background-color: var(--kip-accent-active);
            border-color: var(--kip-accent-active);
            color: var(--kip-accent-fg) !important;
        }}

        .stButton > button:disabled,
        .stFormSubmitButton > button:disabled,
        .stDownloadButton > button:disabled,
        [data-testid="stChatInputSubmitButton"]:disabled {{
            background-color: var(--kip-disabled-bg);
            border-color: var(--kip-disabled-border);
            color: var(--kip-disabled-text) !important;
            cursor: not-allowed;
        }}

        .stSelectbox label,
        .stNumberInput label,
        .stTextInput label,
        .stSlider label,
        .stRadio > label,
        .stCheckbox label,
        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] p {{
            font-size: var(--kip-font-btn);
            font-weight: 600;
            line-height: 1.4;
            color: var(--kip-text-primary) !important;
            margin-bottom: 0.35rem;
        }}

        .stTextInput input,
        .stNumberInput input,
        [data-testid="stChatInput"] textarea,
        [data-baseweb="select"] > div {{
            min-height: var(--kip-touch-target);
            font-size: var(--kip-font-base);
            background-color: var(--kip-bg-nested) !important;
            color: var(--kip-text-primary) !important;
            border: var(--kip-border-width) solid var(--kip-border-strong);
            border-radius: var(--kip-radius-sm);
        }}

        [data-baseweb="select"] span,
        [data-baseweb="select"] input,
        [data-baseweb="select"] svg {{
            color: var(--kip-text-primary) !important;
        }}

        [data-baseweb="popover"],
        [data-baseweb="popover"] ul,
        [role="listbox"],
        [role="option"] {{
            background-color: var(--kip-bg-card) !important;
            color: var(--kip-text-primary) !important;
        }}

        [role="option"]:hover,
        [role="option"][aria-selected="true"] {{
            background-color: var(--kip-bg-hover) !important;
            color: var(--kip-text-primary) !important;
        }}

        [data-testid="stChatInput"] textarea::placeholder,
        .stTextInput input::placeholder {{
            color: var(--kip-text-secondary) !important;
            opacity: 0.85;
        }}

        .stTextInput input:hover:not(:disabled),
        .stNumberInput input:hover:not(:disabled),
        [data-baseweb="select"] > div:hover {{
            border-color: var(--kip-accent);
        }}

        .stTextInput input:disabled,
        .stNumberInput input:disabled {{
            background-color: var(--kip-disabled-bg) !important;
            color: var(--kip-disabled-text) !important;
            border-color: var(--kip-disabled-border);
            cursor: not-allowed;
        }}

        .stNumberInput button {{
            min-height: var(--kip-touch-target);
            min-width: var(--kip-touch-target);
            border-color: var(--kip-border-strong);
            background-color: var(--kip-bg-nested);
            color: var(--kip-text-primary);
        }}

        .stNumberInput button:hover:not(:disabled) {{
            background-color: var(--kip-bg-hover);
            border-color: var(--kip-accent);
        }}

        [data-testid="stSlider"] [data-baseweb="slider"] {{
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }}

        [data-testid="stSlider"] [role="slider"] {{
            width: var(--kip-slider-thumb);
            height: var(--kip-slider-thumb);
            border: 2px solid var(--kip-text-primary);
        }}

        [data-testid="stSlider"] [data-testid="stTickBarMin"],
        [data-testid="stSlider"] [data-testid="stTickBarMax"],
        [data-testid="stSlider"] [data-testid="stThumbValue"] {{
            color: var(--kip-text-primary) !important;
        }}

        /* Явный контрастный цвет подписей радиокнопок и чекбоксов в обеих темах */
        .stRadio [role="radiogroup"] label,
        .stRadio [role="radiogroup"] label p,
        .stRadio [role="radiogroup"] label div,
        .stRadio [role="radiogroup"] label span,
        .stCheckbox label,
        .stCheckbox label p,
        .stCheckbox label span {{
            color: var(--kip-text-primary) !important;
            opacity: 1 !important;
        }}

        .stRadio [role="radiogroup"] label,
        .stCheckbox label {{
            min-height: var(--kip-touch-target);
            padding: 0.35rem 0.5rem;
            border-radius: var(--kip-radius-sm);
            display: flex;
            align-items: center;
        }}

        .stRadio [role="radiogroup"] label:hover,
        .stCheckbox label:hover {{
            background-color: var(--kip-bg-nested);
        }}

        [data-baseweb="tab-list"] {{
            gap: 0.45rem;
            flex-wrap: wrap;
        }}

        [data-baseweb="tab"] {{
            min-height: var(--kip-touch-target);
            padding: 0.5rem 0.95rem;
            font-size: var(--kip-font-btn);
            font-weight: 600;
            color: var(--kip-text-secondary) !important;
            background-color: var(--kip-bg-nested);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius-sm) var(--kip-radius-sm) 0 0;
            white-space: normal;
        }}

        [data-baseweb="tab"] p {{
            color: inherit !important;
            margin: 0;
        }}

        [data-baseweb="tab"]:hover {{
            color: var(--kip-text-primary) !important;
            border-color: var(--kip-accent);
        }}

        [data-baseweb="tab"][aria-selected="true"] {{
            color: var(--kip-accent-fg) !important;
            background-color: var(--kip-accent);
            border-color: var(--kip-accent);
        }}

        /* Видимый фокус клавиатуры */
        button:focus-visible,
        a:focus-visible,
        input:focus-visible,
        textarea:focus-visible,
        select:focus-visible,
        summary:focus-visible,
        [role="tab"]:focus-visible,
        [role="slider"]:focus-visible,
        [tabindex]:focus-visible,
        [data-baseweb="select"] > div:focus-within,
        [data-testid="stChatInput"]:focus-within {{
            outline: 3px solid var(--kip-focus);
            outline-offset: 2px;
        }}

        /* 4. Таблицы, графики Plotly и 3D iframe без переполнения всей страницы */
        [data-testid="stDataFrame"] {{
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius-sm);
            max-width: 100%;
            overflow-x: auto;
        }}

        .stMarkdown table {{
            display: block;
            max-width: 100%;
            overflow-x: auto;
            border-collapse: collapse;
        }}

        .stPlotlyChart {{
            max-width: 100%;
            overflow-x: auto;
            overflow-y: visible;
        }}

        .stPlotlyChart .js-plotly-plot,
        .stPlotlyChart .plot-container {{
            max-width: 100%;
            overflow: visible;
        }}

        iframe {{
            max-width: 100% !important;
            width: 100% !important;
            border-radius: var(--kip-radius-sm);
        }}

        /* 5. Навигация и индикатор активного раздела */
        .kip-nav-status {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border);
            border-left: 4px solid var(--kip-accent);
            border-radius: var(--kip-radius-sm);
            padding: 0.6rem 0.95rem;
            margin-bottom: 0.65rem;
            font-size: var(--kip-font-caption);
            font-weight: var(--kip-caption-weight);
            line-height: 1.45;
            color: var(--kip-text-secondary);
            overflow-wrap: break-word;
        }}

        .kip-nav-status strong {{
            color: var(--kip-text-primary);
        }}

        .kip-sidebar-group-title {{
            font-size: var(--kip-font-btn);
            font-weight: 700;
            color: var(--kip-text-primary);
            margin-top: 0.25rem;
            margin-bottom: 0.35rem;
        }}

        /* 6. Эргономика исследовательских стендов */
        .kip-stand-purpose {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border);
            border-left: 4px solid var(--kip-accent);
            border-radius: var(--kip-radius);
            padding: 0.85rem 1.1rem;
            margin-bottom: 1rem;
            font-size: var(--kip-font-base);
            line-height: var(--kip-line-height);
            color: var(--kip-text-primary);
            max-width: 100%;
        }}

        .kip-param-group-title {{
            font-size: var(--kip-font-h4);
            font-weight: 700;
            color: var(--kip-text-primary);
            margin-top: 0;
            margin-bottom: 0.35rem;
        }}

        .kip-param-hint {{
            font-size: var(--kip-font-caption);
            font-weight: var(--kip-caption-weight);
            line-height: 1.45;
            color: var(--kip-text-secondary);
            margin-bottom: 0.65rem;
        }}

        .kip-fault-banner {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            padding: 0.6rem 0.85rem;
            border-radius: var(--kip-radius-sm);
            border: var(--kip-border-width) solid var(--kip-border);
            margin-bottom: 0.75rem;
            font-size: var(--kip-font-caption);
            font-weight: 600;
            color: var(--kip-text-primary);
        }}

        .kip-fault-banner--ok {{
            background-color: var(--kip-success-bg);
            border-color: var(--kip-success);
        }}

        .kip-fault-banner--warn {{
            background-color: var(--kip-warning-bg);
            border-color: var(--kip-warning);
        }}

        .kip-fault-banner--err {{
            background-color: var(--kip-error-bg);
            border-color: var(--kip-error);
        }}

        .kip-kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: var(--kip-gap);
            margin-top: 0.4rem;
            margin-bottom: 1.1rem;
            align-items: stretch;
        }}

        .kip-kpi-card {{
            background-color: var(--kip-bg-nested);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius);
            padding: var(--kip-card-pad);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 0.45rem;
            min-width: 0;
        }}

        .kip-kpi-card--alert {{
            border-color: var(--kip-warning);
            background-color: var(--kip-warning-bg);
        }}

        .kip-kpi-card--error {{
            border-color: var(--kip-error);
            background-color: var(--kip-error-bg);
        }}

        .kip-kpi-label {{
            font-size: var(--kip-font-caption);
            line-height: 1.35;
            font-weight: 600;
            color: var(--kip-text-secondary);
            overflow-wrap: break-word;
        }}

        .kip-kpi-value {{
            font-size: var(--kip-font-kpi);
            line-height: 1.3;
            font-weight: 700;
            color: var(--kip-text-primary);
            overflow-wrap: anywhere;
        }}

        .kip-kpi-sub {{
            font-size: var(--kip-font-caption);
            font-weight: var(--kip-caption-weight);
            line-height: 1.4;
            color: var(--kip-text-secondary);
            overflow-wrap: anywhere;
        }}

        .kip-notes-box {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius);
            padding: var(--kip-card-pad);
            margin-top: 0.5rem;
            margin-bottom: 0.85rem;
            font-size: var(--kip-font-base);
            line-height: var(--kip-line-height);
            color: var(--kip-text-primary);
        }}

        .kip-notes-box p {{
            margin: 0.35rem 0;
            font-size: var(--kip-font-base);
            line-height: var(--kip-line-height);
            color: var(--kip-text-primary);
            max-width: 100%;
        }}

        /* 7. Эргономика теории, подбора термопар и справочного помощника */
        .kip-section-intro {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border);
            border-left: 4px solid var(--kip-accent);
            border-radius: var(--kip-radius);
            padding: 0.9rem 1.15rem;
            margin-bottom: 1rem;
            font-size: var(--kip-font-base);
            line-height: var(--kip-line-height);
            color: var(--kip-text-primary);
        }}

        .kip-stage-header-card {{
            background-color: var(--kip-bg-nested);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius);
            padding: 0.85rem 1.1rem;
            margin-bottom: 0.75rem;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
        }}

        .kip-stage-badge {{
            display: inline-block;
            background-color: var(--kip-accent);
            color: var(--kip-accent-fg);
            font-size: var(--kip-font-caption);
            font-weight: 700;
            padding: 0.25rem 0.7rem;
            border-radius: var(--kip-radius-sm);
        }}

        .kip-stage-title-text {{
            font-size: var(--kip-font-h4);
            font-weight: 700;
            color: var(--kip-text-primary);
            overflow-wrap: break-word;
        }}

        .kip-stage-steps {{
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 0.4rem;
            margin-bottom: 0.75rem;
        }}

        .kip-stage-step {{
            text-align: center;
            padding: 0.45rem 0.5rem;
            line-height: 1.35;
            border-radius: var(--kip-radius-sm);
            border: var(--kip-border-width) solid var(--kip-border);
            background-color: var(--kip-bg-card);
            color: var(--kip-text-secondary);
            font-size: 14px;
            font-weight: 600;
            overflow-wrap: break-word;
        }}

        .kip-stage-step--active {{
            background-color: var(--kip-accent);
            border-color: var(--kip-accent);
            color: var(--kip-accent-fg);
            font-weight: 700;
        }}

        .kip-theory-figure {{
            text-align: center;
            margin: 1.15rem auto;
            max-width: 720px;
            width: 100%;
            background-color: var(--kip-bg-nested);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius);
            padding: 0.75rem;
        }}

        .kip-theory-figure img {{
            max-width: 100%;
            width: auto;
            height: auto;
            object-fit: contain;
            border-radius: var(--kip-radius-sm);
            display: block;
            margin: 0 auto;
        }}

        .kip-theory-figcaption {{
            font-style: italic;
            color: var(--kip-text-secondary);
            font-size: var(--kip-font-caption);
            font-weight: var(--kip-caption-weight);
            line-height: 1.45;
            margin-top: 0.55rem;
            text-align: left;
        }}

        .kip-status-banner {{
            padding: 0.8rem 1.05rem;
            border-radius: var(--kip-radius);
            border: var(--kip-alert-border-w) solid var(--kip-border);
            margin-bottom: 0.9rem;
            font-size: var(--kip-font-base);
            font-weight: 700;
            line-height: 1.45;
            color: var(--kip-text-primary);
            overflow-wrap: break-word;
        }}

        .kip-status-banner--ok {{
            background-color: var(--kip-success-bg);
            border-color: var(--kip-success);
        }}

        .kip-status-banner--conditional {{
            background-color: var(--kip-warning-bg);
            border-color: var(--kip-warning);
        }}

        .kip-status-banner--error {{
            background-color: var(--kip-error-bg);
            border-color: var(--kip-error);
        }}

        .kip-detail-card {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius);
            padding: var(--kip-card-pad);
            margin-bottom: 0.85rem;
            max-width: 82ch;
            overflow-wrap: break-word;
        }}

        .kip-detail-card--warn {{
            background-color: var(--kip-warning-bg);
            border-color: var(--kip-warning);
            max-width: 100%;
        }}

        .kip-equip-svg-wrap {{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            max-width: 100%;
        }}

        .kip-equip-svg-wrap svg {{
            max-width: 100%;
            height: auto;
        }}

        .kip-panel-badge {{
            display: inline-block;
            font-size: 13px;
            font-weight: 700;
            padding: 0.2rem 0.6rem;
            border-radius: var(--kip-radius-sm);
            border: var(--kip-border-width) solid var(--kip-border);
            background-color: var(--kip-bg-nested);
            color: var(--kip-accent);
            margin-bottom: 0.4rem;
        }}

        .kip-panel-badge--model {{
            color: var(--kip-warning);
            border-color: var(--kip-warning);
            background-color: var(--kip-warning-bg);
        }}

        /* 7.1. Интерактивная проверка знаний: Детектор мифов и Хронология открытий */
        .kip-myth-card {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border-strong);
            border-left: 5px solid var(--kip-accent);
            border-radius: var(--kip-radius);
            padding: var(--kip-card-pad);
            margin-bottom: 0.9rem;
        }}

        .kip-myth-meta {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            margin-bottom: 0.65rem;
        }}

        .kip-myth-badge {{
            display: inline-block;
            background-color: var(--kip-bg-nested);
            color: var(--kip-text-primary);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius-sm);
            padding: 0.2rem 0.65rem;
            font-size: var(--kip-font-caption);
            font-weight: 700;
        }}

        .kip-myth-statement {{
            font-size: var(--kip-font-h4);
            font-weight: 700;
            line-height: 1.45;
            color: var(--kip-text-primary);
            background-color: var(--kip-bg-nested);
            border: var(--kip-border-width) solid var(--kip-border);
            border-radius: var(--kip-radius-sm);
            padding: 0.9rem 1.05rem;
            margin: 0.35rem 0 0.5rem 0;
            overflow-wrap: break-word;
        }}

        .kip-chrono-card {{
            background-color: var(--kip-bg-card);
            border: var(--kip-border-width) solid var(--kip-border);
            border-left: 5px solid var(--kip-accent);
            border-radius: var(--kip-radius);
            padding: 0.75rem 0.95rem;
            margin-bottom: 0.45rem;
            color: var(--kip-text-primary);
        }}

        .kip-chrono-card--ok {{
            background-color: var(--kip-success-bg);
            border-color: var(--kip-success);
            border-left-color: var(--kip-success);
        }}

        .kip-chrono-card--wrong {{
            background-color: var(--kip-warning-bg);
            border-color: var(--kip-warning);
            border-left-color: var(--kip-warning);
        }}

        .kip-chrono-head {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.3rem;
        }}

        .kip-chrono-pos {{
            display: inline-block;
            background-color: var(--kip-accent);
            color: var(--kip-accent-fg);
            border-radius: var(--kip-radius-sm);
            padding: 0.15rem 0.55rem;
            font-size: var(--kip-font-caption);
            font-weight: 800;
        }}

        .kip-chrono-year {{
            display: inline-block;
            background-color: var(--kip-bg-nested);
            color: var(--kip-text-primary);
            border: var(--kip-border-width) solid var(--kip-border-strong);
            border-radius: var(--kip-radius-sm);
            padding: 0.15rem 0.55rem;
            font-size: var(--kip-font-caption);
            font-weight: 700;
        }}

        .kip-chrono-title {{
            font-size: var(--kip-font-base);
            font-weight: 700;
            color: var(--kip-text-primary);
        }}

        .kip-chrono-desc {{
            font-size: var(--kip-font-caption);
            line-height: 1.45;
            color: var(--kip-text-secondary);
            margin-top: 0.2rem;
        }}

        .kip-chrono-hint {{
            font-size: var(--kip-font-caption);
            font-weight: 700;
            color: var(--kip-text-primary);
            margin-top: 0.35rem;
        }}

        .kip-timeline-item {{
            position: relative;
            padding: 0.65rem 0.9rem 0.65rem 1.1rem;
            margin-bottom: 0.55rem;
            background-color: var(--kip-bg-nested);
            border: var(--kip-border-width) solid var(--kip-border);
            border-left: 5px solid var(--kip-success);
            border-radius: var(--kip-radius-sm);
            color: var(--kip-text-primary);
        }}

        /* 8. Адаптивные брейкпоинты (ПК, планшет, 200% масштаб браузера, 430 / 390 / 360 / 320 px) */
        .main .block-container {{
            max-width: 100%;
        }}

        [data-testid="stVerticalBlock"] {{
            min-width: 0;
        }}

        @media (max-width: 1120px) {{
            .kip-kpi-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
        }}

        /* Служебные маркеры и якоря автопрокрутки не занимают видимую высоту */
        .kip-scroll-anchor {{
            display: block;
            height: 0;
            margin: 0;
            padding: 0;
            scroll-margin-top: 72px;
        }}

        iframe[height="0"] {{
            height: 0 !important;
            min-height: 0 !important;
            border: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            display: block;
        }}

        [data-testid="stVerticalBlock"] > div:has(.kip-mobile-nav-2x2-marker),
        [data-testid="stVerticalBlock"] > div:has(.kip-top-nav-wrap-marker),
        [data-testid="stVerticalBlock"] > div:has(.kip-inline-pair-marker),
        [data-testid="stVerticalBlock"] > div:has(.kip-scroll-anchor),
        [data-testid="stVerticalBlock"] > div:has(iframe[height="0"]) {{
            margin: 0 !important;
            padding: 0 !important;
            height: 0 !important;
            min-height: 0 !important;
            overflow: hidden !important;
        }}

        @media (max-width: 767px) {{
            [data-testid="stHorizontalBlock"] {{
                flex-direction: column !important;
                gap: 0.7rem !important;
            }}
            [data-testid="column"],
            [data-testid="stColumn"] {{
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 0 !important;
            }}
            /* Исключение для компактных парных кнопок (навигация 2 × 2 и игровые кнопки Правда/Миф, Выше/Ниже) */
            [data-testid="stVerticalBlock"] > div:has(.kip-mobile-nav-2x2-marker) ~ [data-testid="stHorizontalBlock"],
            [data-testid="stVerticalBlock"] > div:has(.kip-inline-pair-marker) ~ [data-testid="stHorizontalBlock"] {{
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                gap: 0.45rem !important;
            }}
            [data-testid="stVerticalBlock"] > div:has(.kip-mobile-nav-2x2-marker) ~ [data-testid="stHorizontalBlock"] > [data-testid="column"],
            [data-testid="stVerticalBlock"] > div:has(.kip-mobile-nav-2x2-marker) ~ [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
            [data-testid="stVerticalBlock"] > div:has(.kip-inline-pair-marker) ~ [data-testid="stHorizontalBlock"] > [data-testid="column"],
            [data-testid="stVerticalBlock"] > div:has(.kip-inline-pair-marker) ~ [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
                width: calc(50% - 0.25rem) !important;
                flex: 1 1 calc(50% - 0.25rem) !important;
                min-width: 0 !important;
            }}
            /* Адаптивное перестроение 4-кнопочного верхнего меню в сетку 2 × 2 на узком экране */
            [data-testid="stVerticalBlock"] > div:has(.kip-top-nav-wrap-marker) ~ [data-testid="stHorizontalBlock"] {{
                flex-direction: row !important;
                flex-wrap: wrap !important;
                gap: 0.45rem !important;
            }}
            [data-testid="stVerticalBlock"] > div:has(.kip-top-nav-wrap-marker) ~ [data-testid="stHorizontalBlock"] > [data-testid="column"],
            [data-testid="stVerticalBlock"] > div:has(.kip-top-nav-wrap-marker) ~ [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
                width: calc(50% - 0.25rem) !important;
                flex: 1 1 calc(50% - 0.25rem) !important;
                min-width: 0 !important;
            }}
            [data-testid="stVerticalBlock"] > div:has(.kip-mobile-nav-2x2-marker) ~ [data-testid="stHorizontalBlock"] .stButton > button,
            [data-testid="stVerticalBlock"] > div:has(.kip-top-nav-wrap-marker) ~ [data-testid="stHorizontalBlock"] .stButton > button {{
                padding: 0.5rem 0.55rem;
            }}
            .block-container {{
                padding-left: 0.65rem !important;
                padding-right: 0.65rem !important;
            }}
            .stMarkdown p,
            .stMarkdown li,
            .kip-detail-card {{
                max-width: 100%;
            }}
            .kip-stage-steps {{
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }}
            .kip-equip-svg-wrap {{
                justify-content: flex-start;
                margin-top: 0.35rem;
            }}
            .stPlotlyChart {{
                margin-left: 0 !important;
                margin-right: 0 !important;
            }}
        }}

        @media (max-width: {p["kpi_1col_bp"]}) {{
            .kip-kpi-grid {{
                grid-template-columns: 1fr;
            }}
            .kip-kpi-card {{
                padding: 0.8rem 0.85rem;
            }}
        }}

        @media (max-width: 360px) {{
            .block-container {{
                padding-left: 0.45rem !important;
                padding-right: 0.45rem !important;
            }}
            .kip-stage-steps {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
            .stApp h1 {{
                font-size: 24px;
            }}
            .stApp h2 {{
                font-size: 21px;
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            .stButton > button,
            .stFormSubmitButton > button,
            .stDownloadButton > button,
            [data-testid="stChatInputSubmitButton"] {{
                transition: none;
                transform: none;
            }}
        }}
        {extra_hc_rules}
    </style>
    """


def apply_visual_system_css(
    accessibility_mode: str = "Стандартный",
    theme_mode: str = "Светлая (дневная)",
) -> None:
    """Применяет CSS активной цветовой темы и режима доступности без перезапуска приложения."""
    st.markdown(get_visual_system_css(accessibility_mode, theme_mode), unsafe_allow_html=True)


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
    display_mode: str = "Адаптивный (ПК + смартфон)",
    theme_mode: str = "Светлая (дневная)"
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

    is_light_theme = (theme_mode == "Светлая (дневная)")
    plotly_template = "plotly_white" if is_light_theme else "plotly_dark"
    chart_bg = "#FFFFFF" if is_light_theme else "#0E1117"
    chart_font_col = "#0F172A" if is_light_theme else "#EEF2F6"
    x_grid_col = "rgba(15, 23, 42, 0.16)" if is_light_theme else "rgba(255,255,255,0.14)"
    x_zero_col = "rgba(15, 23, 42, 0.40)" if is_light_theme else "rgba(255,255,255,0.32)"
    y_grid_col = "rgba(15, 23, 42, 0.12)" if is_light_theme else "rgba(255,255,255,0.10)"
    y_zero_col = "rgba(15, 23, 42, 0.35)" if is_light_theme else "rgba(255,255,255,0.28)"
    minor_grid_col = "rgba(15, 23, 42, 0.06)" if is_light_theme else "rgba(255,255,255,0.04)"

    # 3. Градуировка горизонтальной оси температуры с равномерным шагом 250 °C (от 0 в обе стороны)
    xaxis_cfg = dict(
        title=dict(text=x_title, font=dict(size=title_size, color=chart_font_col)),
        range=x_range,
        tickmode="linear",
        tick0=0,
        dtick=250,
        tickangle=0,
        ticks="outside",
        ticklen=5,
        tickfont=dict(size=x_tick_size, color=chart_font_col),
        automargin=True,
        showgrid=True,
        gridcolor=x_grid_col,
        zerolinecolor=x_zero_col
    )
    yaxis_cfg = dict(
        title=dict(text=y_title, font=dict(size=title_size, color=chart_font_col)),
        range=y_range,
        nticks=y_nticks,
        tickfont=dict(size=y_tick_size, color=chart_font_col),
        automargin=True,
        showgrid=True,
        gridcolor=y_grid_col,
        zerolinecolor=y_zero_col
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
        template=plotly_template,
        paper_bgcolor=chart_bg,
        plot_bgcolor=chart_bg,
        font=dict(color=chart_font_col),
        hovermode=hover_mode,
        xaxis=xaxis_cfg,
        yaxis=yaxis_cfg,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=legend_y,
            xanchor="center",
            x=0.5,
            font=dict(size=legend_size, color=chart_font_col),
            bgcolor="rgba(0, 0, 0, 0.0)",
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
                gridcolor=minor_grid_col
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
    t_kz_val: float | None = None,
    theme_mode: str = "Светлая (дневная)"
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
    is_light = (theme_mode == "Светлая (дневная)")
    border_col = ("#b91c1c" if is_light else "#ff2a2a") if fault_state != "Норма" else ("#0369a1" if is_light else "#00b4d8")
    scene_bg_css = "#f1f5f9" if is_light else "#0e1117"
    scene_bg_three = "0xf1f5f9" if is_light else "0x0e1117"
    hud_bg_css = "rgba(255, 255, 255, 0.94)" if is_light else "rgba(20, 24, 33, 0.92)"
    hud_fg_css = "#0f172a" if is_light else "#eef2f6"
    hud_bold_css = "#b45309" if is_light else "#ff9f1c"
    hot_badge_css = "#c2410c" if is_light else "#ff6b35"
    cold_badge_css = "#0369a1" if is_light else "#4cc9f0"
    leg_bg_css = "rgba(255, 255, 255, 0.90)" if is_light else "rgba(20, 24, 33, 0.85)"
    hint_bg_css = "rgba(255, 255, 255, 0.90)" if is_light else "rgba(14, 17, 23, 0.82)"
    hint_fg_css = "#334155" if is_light else "#cbd5e1"
    hud_border_css = "1px solid #cbd5e1" if is_light else "none"
    svg_stroke_css = "#0f172a" if is_light else "#ffffff"
    svg_mask_bg = "#f1f5f9" if is_light else "#0e1117"
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
            * {{ box-sizing: border-box; }}
            body {{ margin: 0; overflow: hidden; background-color: {scene_bg_css}; font-family: sans-serif; }}
            #hud {{
                position: absolute; top: 10px; left: 10px; color: {hud_fg_css};
                max-width: calc(100vw - 20px);
                background: {hud_bg_css}; padding: 9px 12px;
                border: {hud_border_css};
                border-radius: 8px; border-left: 4px solid {border_col}; font-size: 12px;
                pointer-events: none; z-index: 10; line-height: 1.42;
                overflow-wrap: break-word; word-break: break-word;
            }}
            #bottom-overlay {{
                position: absolute; bottom: 8px; left: 10px; right: 10px;
                display: flex; flex-direction: column; align-items: flex-start; gap: 5px;
                pointer-events: none; z-index: 10;
            }}
            #legend {{
                max-width: 100%; color: {hud_fg_css};
                background: {leg_bg_css}; padding: 5px 9px; border: {hud_border_css};
                border-radius: 6px; font-size: 11px; line-height: 1.35;
                overflow-wrap: break-word; word-break: break-word;
            }}
            #hint {{
                max-width: 100%; color: {hint_fg_css};
                background: {hint_bg_css}; padding: 5px 9px; border: {hud_border_css};
                border-radius: 6px; font-size: 11px; line-height: 1.35;
                overflow-wrap: break-word; word-break: break-word;
            }}
            #fallback2d {{
                display: none; width: 100vw; height: 100vh; padding: 10px;
                align-items: center; justify-content: center; flex-direction: column;
                background-color: {scene_bg_css}; color: {hud_fg_css};
            }}
            #fallback2d svg {{ max-width: 100%; height: auto; }}
            .hot-badge {{ color: {hot_badge_css}; font-weight: bold; }}
            .cold-badge {{ color: {cold_badge_css}; font-weight: bold; }}
            #hud b {{ color: {hud_bold_css}; }}
            @media (max-width: 480px) {{
                #hud {{ top: 8px; left: 8px; max-width: calc(100vw - 16px); padding: 7px 9px; font-size: 11px; line-height: 1.35; }}
                #bottom-overlay {{ bottom: 6px; left: 8px; right: 8px; gap: 4px; }}
                #legend, #hint {{ padding: 4px 8px; font-size: 10.5px; }}
            }}
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
        <div id="bottom-overlay">
            <div id="legend">
                🔴 Внизу: Горячий спай (T_hot) &nbsp;|&nbsp; 🔵 Вверху: Холодный спай (T_cold)
            </div>
            <div id="hint">🖱️ ЛКМ: вращать 3D | Колесо: масштаб | ПКМ: панорама</div>
        </div>

        <!-- Автономный 2D SVG-fallback при недоступности Three.js, OrbitControls или WebGL -->
        <div id="fallback2d">
            <svg width="320" height="360" viewBox="0 0 320 360">
                <defs>
                    <linearGradient id="gradWire" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" style="stop-color:{cold_css};stop-opacity:1" />
                        <stop offset="100%" style="stop-color:{hot_css};stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="85" y="45" width="150" height="36" rx="6" fill="{cold_css}" stroke="{svg_stroke_css}" stroke-width="1.5"/>
                <text x="160" y="68" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">Холодный спай ({t_cold:.0f} °C)</text>
                <line x1="115" y1="81" x2="155" y2="290" stroke="url(#gradWire)" stroke-width="8" stroke-linecap="round"/>
                <line x1="205" y1="81" x2="165" y2="290" stroke="url(#gradWire)" stroke-width="8" stroke-linecap="round"/>
                {"<rect x='115' y='165' width='35' height='22' fill='" + svg_mask_bg + "'/><circle cx='132' cy='176' r='10' fill='none' stroke='#dc2626' stroke-width='2' stroke-dasharray='3,3'/><text x='70' y='180' fill='#dc2626' font-size='11' font-weight='bold'>Обрыв I=0</text>" if is_open else ""}
                {"<line x1='128' y1='185' x2='192' y2='185' stroke='#dc2626' stroke-width='6'/><text x='235' y='189' fill='#dc2626' font-size='11' font-weight='bold'>КЗ (" + kz_label + ")</text>" if is_short else ""}
                <circle cx="160" cy="295" r="20" fill="{hot_css}" stroke="{svg_stroke_css}" stroke-width="1.5"/>
                <text x="160" y="335" fill="{hot_badge_css}" font-size="12" font-weight="bold" text-anchor="middle">Горячий спай ({t_hot:.0f} °C)</text>
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
                    scene.background = new THREE.Color({scene_bg_three});

                    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
                    camera.position.set(0.0, 0.3, 6.8);

                    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
                    if (!renderer || !renderer.domElement) {{
                        throw new Error('WebGL контекст недоступен');
                    }}
                    renderer.setSize(window.innerWidth, window.innerHeight);
                    renderer.setPixelRatio(window.devicePixelRatio || 1);
                    document.body.appendChild(renderer.domElement);

                    const updateControlHint = function() {{
                        const hintEl = document.getElementById('hint');
                        const fb = document.getElementById('fallback2d');
                        if (!hintEl || (fb && fb.style.display === 'flex')) return;
                        const isTouch = (window.matchMedia && window.matchMedia('(pointer: coarse)').matches)
                            || ('ontouchstart' in window && window.innerWidth <= 768);
                        hintEl.innerText = isTouch
                            ? '👆 1 палец: вращать 3D | 2 пальца: масштаб и панорама'
                            : '🖱️ ЛКМ: вращать 3D | Колесо: масштаб | ПКМ: панорама';
                    }};
                    updateControlHint();

                    const reducedMotionQuery = window.matchMedia
                        ? window.matchMedia('(prefers-reduced-motion: reduce)')
                        : null;
                    let prefersReducedMotion = Boolean(reducedMotionQuery && reducedMotionQuery.matches);
                    let animFrameId = null;
                    let isInteracting = false;
                    let settleFrames = 0;

                    const controls = new THREE.OrbitControls(camera, renderer.domElement);
                    controls.enableDamping = !prefersReducedMotion;
                    controls.dampingFactor = 0.06;
                    controls.autoRotate = !prefersReducedMotion;
                    controls.autoRotateSpeed = 0.8;

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

                    const prevCamPos = new THREE.Vector3();
                    const prevTarget = new THREE.Vector3();

                    function renderOnce() {{
                        renderer.render(scene, camera);
                    }}

                    function stopLoop() {{
                        if (animFrameId !== null) {{
                            cancelAnimationFrame(animFrameId);
                            animFrameId = null;
                        }}
                    }}

                    function startLoop() {{
                        if (animFrameId === null && !prefersReducedMotion) {{
                            settleFrames = 0;
                            animFrameId = requestAnimationFrame(animate);
                        }}
                    }}

                    function animate() {{
                        if (prefersReducedMotion) {{
                            animFrameId = null;
                            return;
                        }}
                        prevCamPos.copy(camera.position);
                        prevTarget.copy(controls.target);
                        controls.update();
                        renderer.render(scene, camera);

                        const moved = prevCamPos.distanceToSquared(camera.position) > 1e-10
                            || prevTarget.distanceToSquared(controls.target) > 1e-10;
                        if (isInteracting || controls.autoRotate || moved) {{
                            settleFrames = 0;
                            animFrameId = requestAnimationFrame(animate);
                        }} else if (settleFrames < 4) {{
                            settleFrames += 1;
                            animFrameId = requestAnimationFrame(animate);
                        }} else {{
                            animFrameId = null;
                        }}
                    }}

                    controls.addEventListener('start', function() {{
                        controls.autoRotate = false;
                        isInteracting = true;
                        startLoop();
                    }});

                    controls.addEventListener('end', function() {{
                        isInteracting = false;
                        if (!prefersReducedMotion) {{
                            startLoop();
                        }}
                    }});

                    controls.addEventListener('change', function() {{
                        if (prefersReducedMotion) {{
                            renderOnce();
                        }} else {{
                            startLoop();
                        }}
                    }});

                    if (reducedMotionQuery) {{
                        const handleMotionChange = function(event) {{
                            prefersReducedMotion = Boolean(event.matches);
                            controls.enableDamping = !prefersReducedMotion;
                            controls.autoRotate = !prefersReducedMotion;
                            if (prefersReducedMotion) {{
                                stopLoop();
                                renderOnce();
                            }} else {{
                                startLoop();
                            }}
                        }};
                        if (typeof reducedMotionQuery.addEventListener === 'function') {{
                            reducedMotionQuery.addEventListener('change', handleMotionChange);
                        }} else if (typeof reducedMotionQuery.addListener === 'function') {{
                            reducedMotionQuery.addListener(handleMotionChange);
                        }}
                    }}

                    if (prefersReducedMotion) {{
                        renderOnce();
                    }} else {{
                        startLoop();
                    }}

                    window.addEventListener('resize', () => {{
                        camera.aspect = window.innerWidth / window.innerHeight;
                        camera.updateProjectionMatrix();
                        renderer.setSize(window.innerWidth, window.innerHeight);
                        updateControlHint();
                        renderOnce();
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
    fault_state: str,
    theme_mode: str = "Светлая (дневная)"
) -> str:
    """
    3D-модель для Стенда №2 с раздельной проверкой THREE / THREE.OrbitControls
    и перехватом ошибок WebGLRenderer (автоматический переход на 2D SVG).
    """
    is_light = (theme_mode == "Светлая (дневная)")
    border_col = ("#b91c1c" if is_light else "#ff2a2a") if fault_state != "Норма" else ("#15803d" if is_light else "#80ed99")
    scene_bg_css = "#f1f5f9" if is_light else "#0e1117"
    scene_bg_three = "0xf1f5f9" if is_light else "0x0e1117"
    hud_bg_css = "rgba(255, 255, 255, 0.94)" if is_light else "rgba(20, 24, 33, 0.92)"
    hud_fg_css = "#0f172a" if is_light else "#eef2f6"
    hud_bold_css = "#15803d" if is_light else "#80ed99"
    hint_bg_css = "rgba(255, 255, 255, 0.90)" if is_light else "rgba(14, 17, 23, 0.82)"
    hint_fg_css = "#334155" if is_light else "#cbd5e1"
    hud_border_css = "1px solid #cbd5e1" if is_light else "none"
    svg_mask_bg = "#f1f5f9" if is_light else "#0e1117"
    svg_stroke_css = "#0f172a" if is_light else "#ffffff"
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
            * {{ box-sizing: border-box; }}
            body {{ margin: 0; overflow: hidden; background-color: {scene_bg_css}; font-family: sans-serif; }}
            #hud {{
                position: absolute; top: 10px; left: 10px; color: {hud_fg_css};
                max-width: calc(100vw - 20px);
                background: {hud_bg_css}; padding: 9px 12px;
                border: {hud_border_css};
                border-radius: 8px; border-left: 4px solid {border_col}; font-size: 12px;
                pointer-events: none; z-index: 10; line-height: 1.42;
                overflow-wrap: break-word; word-break: break-word;
            }}
            #bottom-overlay {{
                position: absolute; bottom: 8px; left: 10px; right: 10px;
                display: flex; flex-direction: column; align-items: flex-start; gap: 5px;
                pointer-events: none; z-index: 10;
            }}
            #hint {{
                max-width: 100%; color: {hint_fg_css};
                background: {hint_bg_css}; padding: 5px 9px; border: {hud_border_css};
                border-radius: 6px; font-size: 11px; line-height: 1.35;
                overflow-wrap: break-word; word-break: break-word;
            }}
            #fallback2d {{
                display: none; width: 100vw; height: 100vh; padding: 10px;
                align-items: center; justify-content: center; flex-direction: column;
                background-color: {scene_bg_css}; color: {hud_fg_css};
            }}
            #fallback2d svg {{ max-width: 100%; height: auto; }}
            #hud b {{ color: {hud_bold_css}; }}
            @media (max-width: 480px) {{
                #hud {{ top: 8px; left: 8px; max-width: calc(100vw - 16px); padding: 7px 9px; font-size: 11px; line-height: 1.35; }}
                #bottom-overlay {{ bottom: 6px; left: 8px; right: 8px; }}
                #hint {{ padding: 4px 8px; font-size: 10.5px; }}
            }}
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
        <div id="bottom-overlay">
            <div id="hint">🖱️ ЛКМ: вращать 3D | Колесо: масштаб | ПКМ: панорама</div>
        </div>

        <div id="fallback2d">
            <svg width="320" height="360" viewBox="0 0 320 360">
                <rect x="95" y="45" width="130" height="70" rx="8" fill="#1f2937" stroke="#9aa5b1" stroke-width="2"/>
                <text x="160" y="75" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">Милливольтметр</text>
                <text x="160" y="98" fill="#80ed99" font-size="11" text-anchor="middle">{u_meter_str}</text>
                <line x1="115" y1="115" x2="155" y2="290" stroke="{col1_css}" stroke-width="7" stroke-linecap="round"/>
                <line x1="205" y1="115" x2="165" y2="290" stroke="{col2_css}" stroke-width="7" stroke-linecap="round"/>
                {"<rect x='115' y='180' width='35' height='22' fill='" + svg_mask_bg + "'/><text x='65' y='195' fill='#dc2626' font-size='11' font-weight='bold'>Обрыв I=0</text>" if is_open else ""}
                {"<line x1='130' y1='200' x2='190' y2='200' stroke='#dc2626' stroke-width='6'/><text x='225' y='204' fill='#dc2626' font-size='11' font-weight='bold'>Перемычка КЗ</text>" if is_short else ""}
                <circle cx="160" cy="295" r="18" fill="#ff5400" stroke="{svg_stroke_css}" stroke-width="1.5"/>
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
                    scene.background = new THREE.Color({scene_bg_three});

                    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
                    camera.position.set(0.0, 0.5, 7.2);

                    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
                    if (!renderer || !renderer.domElement) {{
                        throw new Error('WebGL контекст недоступен');
                    }}
                    renderer.setSize(window.innerWidth, window.innerHeight);
                    renderer.setPixelRatio(window.devicePixelRatio || 1);
                    document.body.appendChild(renderer.domElement);

                    const updateControlHint = function() {{
                        const hintEl = document.getElementById('hint');
                        const fb = document.getElementById('fallback2d');
                        if (!hintEl || (fb && fb.style.display === 'flex')) return;
                        const isTouch = (window.matchMedia && window.matchMedia('(pointer: coarse)').matches)
                            || ('ontouchstart' in window && window.innerWidth <= 768);
                        hintEl.innerText = isTouch
                            ? '👆 1 палец: вращать 3D | 2 пальца: масштаб и панорама'
                            : '🖱️ ЛКМ: вращать 3D | Колесо: масштаб | ПКМ: панорама';
                    }};
                    updateControlHint();

                    const reducedMotionQuery = window.matchMedia
                        ? window.matchMedia('(prefers-reduced-motion: reduce)')
                        : null;
                    let prefersReducedMotion = Boolean(reducedMotionQuery && reducedMotionQuery.matches);
                    let animFrameId = null;
                    let isInteracting = false;
                    let settleFrames = 0;

                    const controls = new THREE.OrbitControls(camera, renderer.domElement);
                    controls.enableDamping = !prefersReducedMotion;
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

                    const prevCamPos = new THREE.Vector3();
                    const prevTarget = new THREE.Vector3();

                    function renderOnce() {{
                        renderer.render(scene, camera);
                    }}

                    function stopLoop() {{
                        if (animFrameId !== null) {{
                            cancelAnimationFrame(animFrameId);
                            animFrameId = null;
                        }}
                    }}

                    function startLoop() {{
                        if (animFrameId === null && !prefersReducedMotion) {{
                            settleFrames = 0;
                            animFrameId = requestAnimationFrame(animate);
                        }}
                    }}

                    function animate() {{
                        if (prefersReducedMotion) {{
                            animFrameId = null;
                            return;
                        }}
                        prevCamPos.copy(camera.position);
                        prevTarget.copy(controls.target);
                        controls.update();
                        renderer.render(scene, camera);

                        const moved = prevCamPos.distanceToSquared(camera.position) > 1e-10
                            || prevTarget.distanceToSquared(controls.target) > 1e-10;
                        if (isInteracting || moved) {{
                            settleFrames = 0;
                            animFrameId = requestAnimationFrame(animate);
                        }} else if (settleFrames < 4) {{
                            settleFrames += 1;
                            animFrameId = requestAnimationFrame(animate);
                        }} else {{
                            animFrameId = null;
                        }}
                    }}

                    controls.addEventListener('start', function() {{
                        isInteracting = true;
                        startLoop();
                    }});

                    controls.addEventListener('end', function() {{
                        isInteracting = false;
                        if (!prefersReducedMotion) {{
                            startLoop();
                        }}
                    }});

                    controls.addEventListener('change', function() {{
                        if (prefersReducedMotion) {{
                            renderOnce();
                        }} else {{
                            startLoop();
                        }}
                    }});

                    if (reducedMotionQuery) {{
                        const handleMotionChange = function(event) {{
                            prefersReducedMotion = Boolean(event.matches);
                            controls.enableDamping = !prefersReducedMotion;
                            if (prefersReducedMotion) {{
                                stopLoop();
                                renderOnce();
                            }}
                        }};
                        if (typeof reducedMotionQuery.addEventListener === 'function') {{
                            reducedMotionQuery.addEventListener('change', handleMotionChange);
                        }} else if (typeof reducedMotionQuery.addListener === 'function') {{
                            reducedMotionQuery.addListener(handleMotionChange);
                        }}
                    }}

                    renderOnce();

                    window.addEventListener('resize', () => {{
                        camera.aspect = window.innerWidth / window.innerHeight;
                        camera.updateProjectionMatrix();
                        renderer.setSize(window.innerWidth, window.innerHeight);
                        updateControlHint();
                        renderOnce();
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
# 5. НАВИГАЦИЯ, УПРАВЛЕНИЕ СОСТОЯНИЕМ И СТРУКТУРИРОВАННАЯ БОКОВАЯ ПАНЕЛЬ
# =====================================================================
MAIN_SECTIONS = [
    "Теоретическая часть",
    "Исследовательские стенды",
    "Подбор термопары",
    "Справочный помощник",
]

MAIN_SECTION_LABELS = {
    "Теоретическая часть": "📚 Теория",
    "Исследовательские стенды": "🔬 Стенды",
    "Подбор термопары": "🧭 Подбор термопары",
    "Справочный помощник": "📘 Помощник",
}

LAB_STAND_OPTIONS = [
    "Стенд №1: Визуализация градиента температур и генерация Термо-ЭДС",
    "Стенд №2: Исследование эффекта Зеебека в разнородных металлах (Термоэлектрические пары)",
]

LAB_STAND_SHORT_LABELS = {
    LAB_STAND_OPTIONS[0]: "Стенд №1: Градиент и НСХ",
    LAB_STAND_OPTIONS[1]: "Стенд №2: Пары металлов",
}

CHART_DISPLAY_OPTIONS = [
    "Адаптивный (ПК + смартфон)",
    "Смартфон (320–430 px)",
    "Компьютер (широкий экран)",
]

FAULT_MODE_OPTIONS = [
    "Норма",
    "Обрыв термоэлектрического контура",
    "Паразитный спай (КЗ)",
]

OPEN_METER_OPTIONS = [
    "Вторичный прибор с контролем обрыва (шунт входа)",
    "Идеальный высокоомный вольтметр на разрыве (измерение U_хх)",
]

KZ_CONTACT_OPTIONS = [
    "Непосредственное соприкосновение электродов A и B",
    "Перемычка из третьего металла C (изотермическая при T_кз)",
]

DEFAULT_STAND2_METAL_1 = "Хромель (Ni90-Cr10)"
DEFAULT_STAND2_METAL_2 = "Копель (Cu56-Ni44-Mn)"


def _resolve_metal_default(metal_names: list[str], preferred_name: str, fallback_idx: int = 0) -> str:
    """Выбирает металл по названию независимо от порядка элементов в METALS_DB."""
    if preferred_name in metal_names:
        return preferred_name
    if metal_names:
        return metal_names[min(fallback_idx, len(metal_names) - 1)]
    return preferred_name


def init_app_session_state() -> None:
    """Инициализирует устойчивые ключи st.session_state для сохранения параметров при смене разделов."""
    sensor_keys = list(THERMOCOUPLES_DB.keys())
    metal_names = list(METALS_DB.keys())

    defaults = {
        # Навигация, история переходов и автопрокрутка
        "active_section": MAIN_SECTIONS[0],
        "nav_history": [],
        "active_lab_stand": LAB_STAND_OPTIONS[0],
        "_pending_scroll_target": None,
        "_scroll_nonce": 0,
        # Настройки отображения, темы и доступности (по умолчанию дневная светлая тема)
        "theme_mode": THEME_MODE_OPTIONS[0],
        "chart_display_mode": CHART_DISPLAY_OPTIONS[0],
        "accessibility_mode": ACCESSIBILITY_MODE_OPTIONS[0],
        # Общие параметры физических неисправностей
        "fault_mode": FAULT_MODE_OPTIONS[0],
        "open_meter_mode": OPEN_METER_OPTIONS[0],
        "r_cold_branch_ohm": 8.0,
        "r_hot_loop_ohm": 5.0,
        "r_bridge_ohm": 0.0,
        # Параметры Стенда №1
        "stand1_sensor_name": sensor_keys[0],
        "stand1_t_hot": int(THERMOCOUPLES_DB[sensor_keys[0]]["default_hot"]),
        "stand1_t_cold": 20,
        "stand1_t_kz": 260,
        "stand1_kz_contact_type": KZ_CONTACT_OPTIONS[0],
        # Параметры Стенда №2
        "stand2_metal_1": _resolve_metal_default(metal_names, DEFAULT_STAND2_METAL_1, 0),
        "stand2_metal_2": _resolve_metal_default(metal_names, DEFAULT_STAND2_METAL_2, len(metal_names) - 1),
        "stand2_t_hot": 520,
        "stand2_t_cold": 20,
        "stand2_t_kz": 270,
        # Параметры теории и справочника
        "theory_stage_idx": 0,
        "glossary_search": "",
        "gen_desired_s": 75.0,
        "theory_subtab": "Изучение по этапам (1–6)",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def request_page_scroll(anchor_id: str) -> None:
    """Планирует однократную автопрокрутку к указанному якорю после обновления страницы."""
    st.session_state["_pending_scroll_target"] = anchor_id
    st.session_state["_scroll_nonce"] = int(st.session_state.get("_scroll_nonce", 0)) + 1


def build_autoscroll_html(anchor_id: str, nonce: int) -> str:
    """
    Формирует компактный JS-скрипт для мгновенной прокрутки родительского окна Streamlit
    к целевому якорю (или в самый верх страницы) после смены этапа теории или раздела.
    """
    safe_anchor = re.sub(r"[^a-zA-Z0-9_-]", "", str(anchor_id))
    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin:0;padding:0;overflow:hidden;">
    <script>
        (function() {{
            const targetId = "{safe_anchor}";
            const nonce = {int(nonce)};
            let cancelledByUser = false;
            const timers = [];

            function getParentContext() {{
                try {{
                    const pWin = window.parent;
                    const pDoc = pWin && pWin.document;
                    if (pWin && pDoc) {{
                        return {{ win: pWin, doc: pDoc }};
                    }}
                }} catch (e) {{
                    return null;
                }}
                return null;
            }}

            function getScrollContainers(doc) {{
                const list = [
                    doc.querySelector('section[data-testid="stMain"]'),
                    doc.querySelector('[data-testid="stMain"]'),
                    doc.querySelector('[data-testid="stAppViewContainer"]'),
                    doc.querySelector('section.main'),
                    doc.scrollingElement,
                    doc.documentElement,
                    doc.body
                ];
                const unique = [];
                for (const node of list) {{
                    if (node && unique.indexOf(node) === -1) {{
                        unique.push(node);
                    }}
                }}
                return unique;
            }}

            function findScrollableAncestor(el, win, doc) {{
                let node = el ? el.parentElement : null;
                while (node && node !== doc.body && node !== doc.documentElement) {{
                    const st = win.getComputedStyle(node);
                    const oy = st ? st.overflowY : "";
                    if ((oy === "auto" || oy === "scroll" || oy === "overlay") && node.scrollHeight > node.clientHeight + 2) {{
                        return node;
                    }}
                    node = node.parentElement;
                }}
                return null;
            }}

            function performScroll() {{
                if (cancelledByUser) return;
                const ctx = getParentContext();
                if (!ctx) return;
                const {{ win, doc }} = ctx;

                if (targetId === "kip-page-top-anchor") {{
                    for (const sc of getScrollContainers(doc)) {{
                        try {{
                            sc.scrollTop = 0;
                        }} catch (e) {{}}
                    }}
                    try {{ win.scrollTo(0, 0); }} catch (e) {{}}
                    return;
                }}

                const anchorEl = doc.getElementById(targetId);
                if (!anchorEl) return;

                const headerEl = doc.querySelector('[data-testid="stHeader"]');
                const headerOffset = headerEl ? Math.ceil(headerEl.getBoundingClientRect().height) + 12 : 68;
                const scrollParent = findScrollableAncestor(anchorEl, win, doc);

                if (scrollParent) {{
                    const elRect = anchorEl.getBoundingClientRect();
                    const contRect = scrollParent.getBoundingClientRect();
                    const desiredTop = Math.max(0, scrollParent.scrollTop + (elRect.top - contRect.top) - headerOffset);
                    try {{
                        scrollParent.scrollTo({{ top: desiredTop, behavior: "auto" }});
                    }} catch (e) {{
                        scrollParent.scrollTop = desiredTop;
                    }}
                }} else {{
                    const elRect = anchorEl.getBoundingClientRect();
                    const currentY = win.scrollY || doc.documentElement.scrollTop || doc.body.scrollTop || 0;
                    const desiredTop = Math.max(0, currentY + elRect.top - headerOffset);
                    try {{
                        win.scrollTo({{ top: desiredTop, behavior: "auto" }});
                    }} catch (e) {{
                        anchorEl.scrollIntoView({{ behavior: "auto", block: "start" }});
                    }}
                }}
            }}

            const ctxInit = getParentContext();
            if (!ctxInit) return;
            const cancelEvents = ["wheel", "touchstart", "pointerdown", "keydown"];
            const onUserInput = function() {{
                cancelledByUser = true;
                while (timers.length) {{
                    clearTimeout(timers.pop());
                }}
                for (const ev of cancelEvents) {{
                    ctxInit.win.removeEventListener(ev, onUserInput, true);
                }}
            }};
            for (const ev of cancelEvents) {{
                ctxInit.win.addEventListener(ev, onUserInput, {{ capture: true, passive: true }});
            }}

            performScroll();
            if (typeof ctxInit.win.requestAnimationFrame === "function") {{
                ctxInit.win.requestAnimationFrame(performScroll);
            }}
            timers.push(setTimeout(performScroll, 60));
            timers.push(setTimeout(performScroll, 180));
            timers.push(setTimeout(function() {{
                performScroll();
                for (const ev of cancelEvents) {{
                    ctxInit.win.removeEventListener(ev, onUserInput, true);
                }}
            }}, 340));
            void nonce;
        }})();
    </script>
    </body>
    </html>
    """


def render_pending_page_scroll() -> None:
    """Выполняет запланированную автопрокрутку один раз и сбрасывает флаг."""
    target_anchor = st.session_state.get("_pending_scroll_target")
    if not target_anchor:
        return
    st.session_state["_pending_scroll_target"] = None
    nonce = int(st.session_state.get("_scroll_nonce", 0))
    components.html(build_autoscroll_html(str(target_anchor), nonce), height=0)


def navigate_to_section(target_section: str) -> None:
    """Выполняет переход в выбранный основной раздел с сохранением предыдущего раздела в истории."""
    if target_section not in MAIN_SECTIONS:
        return
    current = st.session_state.get("active_section", MAIN_SECTIONS[0])
    if target_section != current:
        history = list(st.session_state.get("nav_history", []))
        history.append(current)
        st.session_state["nav_history"] = history[-20:]
        st.session_state["active_section"] = target_section
        request_page_scroll("kip-page-top-anchor")


def navigate_back() -> None:
    """Возвращает пользователя в предыдущий открытый раздел из истории переходов."""
    history = list(st.session_state.get("nav_history", []))
    if history:
        prev_section = history.pop()
        st.session_state["nav_history"] = history
        st.session_state["active_section"] = prev_section
        request_page_scroll("kip-page-top-anchor")


def _on_sidebar_nav_change() -> None:
    """Обработчик переключения основного раздела из боковой панели."""
    chosen = st.session_state.get("_sidebar_nav_radio")
    if chosen in MAIN_SECTIONS:
        navigate_to_section(chosen)


def _on_sidebar_stand_change() -> None:
    """Обработчик переключения активного стенда из боковой панели."""
    chosen_stand = st.session_state.get("_sidebar_stand_radio")
    if chosen_stand in LAB_STAND_OPTIONS:
        st.session_state["active_lab_stand"] = chosen_stand
        request_page_scroll("kip-page-top-anchor")


def _on_sidebar_fault_change() -> None:
    """Синхронизирует режим неисправности при переключении из боковой панели."""
    chosen_fault = st.session_state.get("_sidebar_fault_select")
    if chosen_fault in FAULT_MODE_OPTIONS:
        st.session_state["fault_mode"] = chosen_fault


def _on_main_fault_change(widget_key: str) -> None:
    """Синхронизирует режим неисправности при переключении на странице стенда."""
    chosen_fault = st.session_state.get(widget_key)
    if chosen_fault in FAULT_MODE_OPTIONS:
        st.session_state["fault_mode"] = chosen_fault


def _on_sidebar_a11y_change() -> None:
    """Синхронизирует режим доступности при переключении из боковой панели (без перезапуска)."""
    chosen_mode = st.session_state.get("_sidebar_a11y_radio")
    if chosen_mode in ACCESSIBILITY_MODE_OPTIONS:
        st.session_state["accessibility_mode"] = chosen_mode


def _on_top_a11y_change() -> None:
    """Синхронизирует режим доступности при переключении из верхней панели (без перезапуска)."""
    chosen_mode = st.session_state.get("_top_a11y_radio")
    if chosen_mode in ACCESSIBILITY_MODE_OPTIONS:
        st.session_state["accessibility_mode"] = chosen_mode


def _on_sidebar_theme_change() -> None:
    """Синхронизирует цветовую тему (Светлая / Тёмная) при переключении из боковой панели."""
    chosen_theme = st.session_state.get("_sidebar_theme_radio")
    if chosen_theme in THEME_MODE_OPTIONS:
        st.session_state["theme_mode"] = chosen_theme


def _on_top_theme_change() -> None:
    """Синхронизирует цветовую тему (Светлая / Тёмная) при переключении из верхней панели."""
    chosen_theme = st.session_state.get("_top_theme_radio")
    if chosen_theme in THEME_MODE_OPTIONS:
        st.session_state["theme_mode"] = chosen_theme


def _toggle_theme_mode() -> None:
    """Быстро переключает цветовую тему между светлой (дневной) и тёмной (ночной)."""
    cur_theme = st.session_state.get("theme_mode", THEME_MODE_OPTIONS[0])
    st.session_state["theme_mode"] = (
        THEME_MODE_OPTIONS[1] if cur_theme == THEME_MODE_OPTIONS[0] else THEME_MODE_OPTIONS[0]
    )


def render_sidebar_navigation_and_controls() -> dict:
    """
    Отрисовывает компактную боковую панель, разделённую на четыре логические группы:
    1. Навигация.
    2. Параметры эксперимента (выбор стенда и сводка; подробные настройки вынесены на страницу стенда).
    3. Физические неисправности (быстрый синхронизированный переключатель состояния контура).
    4. Настройки отображения (режим доступности и режим отображения графиков).
    """
    st.sidebar.title("⚛️ KIP Simulator")
    st.sidebar.caption("Тема: «Термо-ЭДС. Эффект Зеебека»")

    # -----------------------------------------------------------------
    # ГРУППА 1: НАВИГАЦИЯ
    # -----------------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧭 Навигация")
    st.session_state["_sidebar_nav_radio"] = st.session_state["active_section"]
    st.sidebar.radio(
        "Основной раздел приложения:",
        options=MAIN_SECTIONS,
        key="_sidebar_nav_radio",
        on_change=_on_sidebar_nav_change,
    )

    history = st.session_state.get("nav_history", [])
    if history:
        prev_sec = history[-1]
        if st.sidebar.button(
            f"⬅️ Назад: {prev_sec}",
            key="sidebar_nav_back_btn",
            use_container_width=True
        ):
            navigate_back()
            st.rerun()

    active_section = st.session_state["active_section"]

    # -----------------------------------------------------------------
    # ГРУППА 2: ПАРАМЕТРЫ ЭКСПЕРИМЕНТА (переключатель стенда + краткая сводка)
    # -----------------------------------------------------------------
    if active_section == "Исследовательские стенды":
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔬 Параметры эксперимента")

        st.session_state["_sidebar_stand_radio"] = st.session_state["active_lab_stand"]
        st.sidebar.radio(
            "Активный исследовательский стенд:",
            options=LAB_STAND_OPTIONS,
            key="_sidebar_stand_radio",
            on_change=_on_sidebar_stand_change,
        )
        lab_mode = st.session_state["active_lab_stand"]

        if lab_mode.startswith("Стенд №1"):
            s_code = THERMOCOUPLES_DB[st.session_state["stand1_sensor_name"]]["short_code"]
            st.sidebar.caption(
                f"Текущие настройки: **{s_code}**, "
                f"T_hot = {st.session_state['stand1_t_hot']} °C, "
                f"T_cold = {st.session_state['stand1_t_cold']} °C. "
                "Все элементы настройки вынесены на страницу стенда."
            )
        else:
            m1_short = st.session_state["stand2_metal_1"].split("(")[0].strip()
            m2_short = st.session_state["stand2_metal_2"].split("(")[0].strip()
            st.sidebar.caption(
                f"Текущая пара: **{m1_short} — {m2_short}**, "
                f"T_hot = {st.session_state['stand2_t_hot']} °C, "
                f"T_cold = {st.session_state['stand2_t_cold']} °C. "
                "Все элементы настройки вынесены на страницу стенда."
            )

        # -------------------------------------------------------------
        # ГРУППА 3: ФИЗИЧЕСКИЕ НЕИСПРАВНОСТИ (быстрый синхронизированный выбор)
        # -------------------------------------------------------------
        st.sidebar.markdown("---")
        st.sidebar.subheader("⚡ Физические неисправности")
        st.session_state["_sidebar_fault_select"] = st.session_state["fault_mode"]
        st.sidebar.selectbox(
            "Состояние термоэлектрического контура:",
            options=FAULT_MODE_OPTIONS,
            key="_sidebar_fault_select",
            on_change=_on_sidebar_fault_change,
        )
        st.sidebar.caption("Детальные параметры обрыва и КЗ настраиваются в блоке неисправностей на странице стенда.")
    else:
        st.sidebar.markdown("---")
        st.sidebar.caption(
            "Параметры экспериментов и неисправностей сохранены в текущей сессии и "
            "доступны при возврате в раздел «Исследовательские стенды»."
        )

    # -----------------------------------------------------------------
    # ГРУППА 4: НАСТРОЙКИ ОТОБРАЖЕНИЯ, ТЕМЫ И ДОСТУПНОСТИ (общие настройки)
    # -----------------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎛️ Настройки отображения")

    st.session_state["_sidebar_theme_radio"] = st.session_state["theme_mode"]
    st.sidebar.radio(
        "☀️ / 🌙 Тема оформления:",
        options=THEME_MODE_OPTIONS,
        key="_sidebar_theme_radio",
        on_change=_on_sidebar_theme_change,
        help="Светлая (дневная) тема по умолчанию: чёрный текст на белом фоне. Тёмная (ночная): светлый текст на тёмном фоне.",
    )

    st.session_state["_sidebar_a11y_radio"] = st.session_state["accessibility_mode"]
    st.sidebar.radio(
        "👁️ Режим доступности интерфейса:",
        options=ACCESSIBILITY_MODE_OPTIONS,
        key="_sidebar_a11y_radio",
        on_change=_on_sidebar_a11y_change,
        help="Переключает размер шрифта, толщину границ и контрастность выбранной темы без перезапуска приложения.",
    )

    cur_chart_mode = st.session_state["chart_display_mode"]
    chart_mode = st.sidebar.selectbox(
        "Режим отображения графиков:",
        options=CHART_DISPLAY_OPTIONS,
        index=CHART_DISPLAY_OPTIONS.index(cur_chart_mode) if cur_chart_mode in CHART_DISPLAY_OPTIONS else 0,
    )
    st.session_state["chart_display_mode"] = chart_mode

    return {
        "lab_mode": st.session_state["active_lab_stand"],
        "chart_display_mode": chart_mode,
        "circuit_fault_mode": st.session_state["fault_mode"],
        "accessibility_mode": st.session_state["accessibility_mode"],
        "theme_mode": st.session_state["theme_mode"],
    }


def render_top_navigation_bar() -> None:
    """
    Компактная верхняя панель навигации по четырём основным разделам с быстрым
    переключением режима доступности (удобно на смартфоне без открытия боковой панели).
    """
    active_section = st.session_state["active_section"]
    a11y_mode = st.session_state["accessibility_mode"]
    theme_mode = st.session_state["theme_mode"]
    is_light_now = (theme_mode == THEME_MODE_OPTIONS[0])
    theme_btn_label = "🌙 Тёмная тема" if is_light_now else "☀️ Светлая тема"
    history = st.session_state.get("nav_history", [])

    status_suffix = ""
    if active_section == "Исследовательские стенды":
        active_stand_short = LAB_STAND_SHORT_LABELS.get(
            st.session_state["active_lab_stand"],
            st.session_state["active_lab_stand"]
        )
        status_suffix = f" &nbsp;→&nbsp; <strong>{active_stand_short}</strong>"

    a11y_badge = (
        f" &nbsp;|&nbsp; Тема: <strong>{html.escape(theme_mode)}</strong>"
        f" &nbsp;|&nbsp; Режим: <strong>{html.escape(a11y_mode)}</strong>"
    )

    if history:
        prev_section = history[-1]
        bar_left, bar_mid, bar_right = st.columns([2.6, 1.2, 1.2])
        with bar_left:
            st.markdown(
                f'<div class="kip-nav-status">Открытый раздел: <strong>{active_section}</strong>{status_suffix}{a11y_badge}</div>',
                unsafe_allow_html=True,
            )
        with bar_mid:
            if st.button(
                f"⬅️ Вернуться: {MAIN_SECTION_LABELS[prev_section]}",
                key="top_nav_back_btn",
                use_container_width=True,
            ):
                navigate_back()
                st.rerun()
        with bar_right:
            st.button(
                theme_btn_label,
                key="top_quick_theme_btn",
                use_container_width=True,
                on_click=_toggle_theme_mode,
            )
    else:
        bar_left, bar_right = st.columns([3.4, 1.1])
        with bar_left:
            st.markdown(
                f'<div class="kip-nav-status">Открытый раздел: <strong>{active_section}</strong>{status_suffix}{a11y_badge}</div>',
                unsafe_allow_html=True,
            )
        with bar_right:
            st.button(
                theme_btn_label,
                key="top_quick_theme_btn",
                use_container_width=True,
                on_click=_toggle_theme_mode,
            )

    is_mobile_nav = (st.session_state.get("chart_display_mode") == "Смартфон (320–430 px)")
    if is_mobile_nav:
        with st.container():
            st.markdown('<div class="kip-mobile-nav-2x2-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
            for row_start in range(0, len(MAIN_SECTIONS), 2):
                row_secs = MAIN_SECTIONS[row_start:row_start + 2]
                nav_row = st.columns(2)
                for c_i, section_name in enumerate(row_secs):
                    idx = row_start + c_i
                    is_current = (section_name == active_section)
                    with nav_row[c_i]:
                        if st.button(
                            MAIN_SECTION_LABELS[section_name],
                            key=f"top_nav_btn_{idx}",
                            type="primary" if is_current else "secondary",
                            use_container_width=True,
                        ):
                            if not is_current:
                                navigate_to_section(section_name)
                                st.rerun()
    else:
        with st.container():
            st.markdown('<div class="kip-top-nav-wrap-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
            nav_cols = st.columns(4)
            for idx, section_name in enumerate(MAIN_SECTIONS):
                is_current = (section_name == active_section)
                with nav_cols[idx]:
                    if st.button(
                        MAIN_SECTION_LABELS[section_name],
                        key=f"top_nav_btn_{idx}",
                        type="primary" if is_current else "secondary",
                        use_container_width=True,
                    ):
                        if not is_current:
                            navigate_to_section(section_name)
                            st.rerun()

    if active_section == "Исследовательские стенды":
        stand_cols = st.columns(2)
        for s_idx, stand_full in enumerate(LAB_STAND_OPTIONS):
            is_stand_active = (st.session_state["active_lab_stand"] == stand_full)
            with stand_cols[s_idx]:
                if st.button(
                    LAB_STAND_SHORT_LABELS[stand_full],
                    key=f"top_stand_btn_{s_idx}",
                    type="primary" if is_stand_active else "secondary",
                    use_container_width=True,
                ):
                    if not is_stand_active:
                        st.session_state["active_lab_stand"] = stand_full
                        st.rerun()

    with st.expander(f"🎨 Тема: {theme_mode} • Доступность: {a11y_mode}", expanded=False):
        st.session_state["_top_theme_radio"] = st.session_state["theme_mode"]
        st.radio(
            "Цветовая тема оформления:",
            options=THEME_MODE_OPTIONS,
            key="_top_theme_radio",
            on_change=_on_top_theme_change,
            horizontal=True,
        )
        st.session_state["_top_a11y_radio"] = st.session_state["accessibility_mode"]
        st.radio(
            "Режим доступности интерфейса:",
            options=ACCESSIBILITY_MODE_OPTIONS,
            key="_top_a11y_radio",
            on_change=_on_top_a11y_change,
            horizontal=True,
        )

    st.markdown("---")


def render_kpi_cards_grid(cards: list[dict]) -> None:
    """
    Отрисовывает адаптивную сетку из 4 карточек числовых показателей одинаковой высоты:
    - широкий экран (> 1120 px): 4 колонки;
    - планшет / промежуточная ширина (<= 1120 px): 2 колонки;
    - компактный экран (<= 420 / 460 / 540 px в зависимости от режима доступности): 1 колонка.
    """
    items_html = []
    for card in cards:
        tone = card.get("tone", "normal")
        tone_cls = ""
        if tone == "warn":
            tone_cls = " kip-kpi-card--alert"
        elif tone == "error":
            tone_cls = " kip-kpi-card--error"
        lbl = html.escape(str(card["label"]))
        val = html.escape(str(card["value"]))
        sub = html.escape(str(card["sub"]))
        items_html.append(
            f'<div class="kip-kpi-card{tone_cls}">'
            f'<div class="kip-kpi-label">{lbl}</div>'
            f'<div class="kip-kpi-value">{val}</div>'
            f'<div class="kip-kpi-sub">{sub}</div>'
            f'</div>'
        )
    st.markdown(f'<div class="kip-kpi-grid">{"".join(items_html)}</div>', unsafe_allow_html=True)


def render_stand_fault_panel(stand_id: str, t_cold: float, t_hot: float) -> dict:
    """
    Единый визуально отделённый блок настройки физических неисправностей цепи на странице стенда.
    Не изменяет физические алгоритмы: только собирает и сохраняет в st.session_state те же параметры.
    """
    with st.container(border=True):
        cur_fault = st.session_state["fault_mode"]
        if cur_fault == "Норма":
            banner_cls = "kip-fault-banner--ok"
            banner_txt = "Статус цепи: Норма (замкнутый исправный контур)"
        elif cur_fault == "Обрыв термоэлектрического контура":
            banner_cls = "kip-fault-banner--err"
            banner_txt = "Неисправность: обрыв термоэлектрического контура (ток I = 0 мкА)"
        else:
            banner_cls = "kip-fault-banner--warn"
            banner_txt = "Неисправность: паразитный спай / короткое замыкание (шунтирование рабочего спая)"

        st.markdown('<div class="kip-param-group-title">⚡ Моделирование физических неисправностей цепи</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kip-fault-banner {banner_cls}"><span>{html.escape(banner_txt)}</span></div>', unsafe_allow_html=True)

        fault_widget_key = f"_{stand_id}_fault_select"
        st.session_state[fault_widget_key] = st.session_state["fault_mode"]
        circuit_fault_mode = st.selectbox(
            "Состояние термоэлектрического контура:",
            options=FAULT_MODE_OPTIONS,
            key=fault_widget_key,
            on_change=_on_main_fault_change,
            args=(fault_widget_key,),
            help="Выберите «Норма» для штатного измерения, «Обрыв» для размыкания цепи или «Паразитный спай (КЗ)» для моделирования нарушения изоляции.",
        )

        open_circuit_meter_mode = st.session_state["open_meter_mode"]
        r_cold_branch_input = float(st.session_state["r_cold_branch_ohm"])
        r_hot_loop_input = float(st.session_state["r_hot_loop_ohm"])
        r_bridge_input = float(st.session_state["r_bridge_ohm"])
        t_kz_val = None
        kz_contact_type = st.session_state["stand1_kz_contact_type"]

        if circuit_fault_mode == "Обрыв термоэлектрического контура":
            st.markdown(
                '<div class="kip-param-hint">При обрыве термоток равен нулю, но ЭДС холостого хода сохраняется. '
                'Выберите, как ведёт себя подключённый измерительный прибор:</div>',
                unsafe_allow_html=True,
            )
            cur_open = st.session_state["open_meter_mode"]
            open_circuit_meter_mode = st.radio(
                "Режим измерительного прибора при обрыве:",
                options=OPEN_METER_OPTIONS,
                index=OPEN_METER_OPTIONS.index(cur_open) if cur_open in OPEN_METER_OPTIONS else 0,
                key=f"{stand_id}_open_meter_radio",
            )
            st.session_state["open_meter_mode"] = open_circuit_meter_mode

        elif circuit_fault_mode == "Паразитный спай (КЗ)":
            st.markdown(
                '<div class="kip-param-hint">Задайте температуру в месте замыкания электродов и сопротивления участков цепи '
                'для расчёта локального тока петли КЗ и напряжения на входе прибора по теореме Тевенина:</div>',
                unsafe_allow_html=True,
            )
            kz_min = int(min(t_cold, t_hot))
            kz_max = int(max(t_cold, t_hot))
            state_kz_key = "stand1_t_kz" if stand_id == "stand1" else "stand2_t_kz"
            kz_slider_key = "stand1_t_kz_slider" if stand_id == "stand1" else "stand2_t_kz_slider"
            if kz_slider_key in st.session_state and not (kz_min <= int(st.session_state[kz_slider_key]) <= kz_max):
                del st.session_state[kz_slider_key]

            is_mob_kz = (st.session_state.get("chart_display_mode") == "Смартфон (320–430 px)")
            if stand_id == "stand1":
                cur_contact = st.session_state["stand1_kz_contact_type"]
                if is_mob_kz:
                    if kz_min == kz_max:
                        t_kz_int = kz_min
                        st.info(f"Температура перемычки T_кз зафиксирована на {kz_min} °C (T_hot = T_cold).")
                    else:
                        t_kz_init = int(np.clip(int(st.session_state[state_kz_key]), kz_min, kz_max))
                        t_kz_int = st.slider(
                            "Температура в точке перемычки (T_кз), °C:",
                            min_value=kz_min,
                            max_value=kz_max,
                            value=t_kz_init,
                            step=10,
                            key="stand1_t_kz_slider",
                            help="Температура в промежуточной зоне, где термоэлектроды замкнулись между собой.",
                        )
                    kz_contact_type = st.selectbox(
                        "Характер паразитного контакта:",
                        options=KZ_CONTACT_OPTIONS,
                        index=KZ_CONTACT_OPTIONS.index(cur_contact) if cur_contact in KZ_CONTACT_OPTIONS else 0,
                        key="stand1_kz_contact_select",
                        help="Непосредственное касание проводов A и B или изотермическая перемычка из третьего металла C.",
                    )
                else:
                    kz_c1, kz_c2 = st.columns(2)
                    with kz_c1:
                        if kz_min == kz_max:
                            t_kz_int = kz_min
                            st.info(f"Температура перемычки T_кз зафиксирована на {kz_min} °C (T_hot = T_cold).")
                        else:
                            t_kz_init = int(np.clip(int(st.session_state[state_kz_key]), kz_min, kz_max))
                            t_kz_int = st.slider(
                                "Температура в точке перемычки (T_кз), °C:",
                                min_value=kz_min,
                                max_value=kz_max,
                                value=t_kz_init,
                                step=10,
                                key="stand1_t_kz_slider",
                                help="Температура в промежуточной зоне, где термоэлектроды замкнулись между собой.",
                            )
                    with kz_c2:
                        kz_contact_type = st.selectbox(
                            "Характер паразитного контакта:",
                            options=KZ_CONTACT_OPTIONS,
                            index=KZ_CONTACT_OPTIONS.index(cur_contact) if cur_contact in KZ_CONTACT_OPTIONS else 0,
                            key="stand1_kz_contact_select",
                            help="Непосредственное касание проводов A и B или изотермическая перемычка из третьего металла C.",
                        )
                st.session_state[state_kz_key] = t_kz_int
                t_kz_val = float(t_kz_int)
                st.session_state["stand1_kz_contact_type"] = kz_contact_type
            else:
                if kz_min == kz_max:
                    t_kz_int = kz_min
                    st.info(f"Температура перемычки T_кз зафиксирована на {kz_min} °C (T_hot = T_cold).")
                else:
                    t_kz_init = int(np.clip(int(st.session_state[state_kz_key]), kz_min, kz_max))
                    t_kz_int = st.slider(
                        "Температура перемычки КЗ (T_кз), °C:",
                        min_value=kz_min,
                        max_value=kz_max,
                        value=t_kz_init,
                        step=10,
                        key="stand2_t_kz_slider",
                        help="Температура в точке короткого замыкания проводников ветвей А и B.",
                    )
                st.session_state[state_kz_key] = t_kz_int
                t_kz_val = float(t_kz_int)

            is_mob_fault = (st.session_state.get("chart_display_mode") == "Смартфон (320–430 px)")
            if is_mob_fault:
                r_cold_branch_input = float(st.number_input(
                    "R_уч1 (до КЗ), Ом:",
                    min_value=0.1,
                    max_value=500.0,
                    value=float(st.session_state["r_cold_branch_ohm"]),
                    step=0.5,
                    key=f"{stand_id}_r_cold_input",
                    help="Сопротивление проводов на холодном участке от клемм прибора (T_cold) до точки КЗ (T_кз).",
                ))
                r_hot_loop_input = float(st.number_input(
                    "R_уч2 (от КЗ до спая), Ом:",
                    min_value=0.1,
                    max_value=500.0,
                    value=float(st.session_state["r_hot_loop_ohm"]),
                    step=0.5,
                    key=f"{stand_id}_r_hot_input",
                    help="Сопротивление горячего участка проводов от точки КЗ (T_кз) до рабочего спая (T_hot).",
                ))
                r_bridge_input = float(st.number_input(
                    "Перемычка R_кз, Ом:",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(st.session_state["r_bridge_ohm"]),
                    step=0.5,
                    key=f"{stand_id}_r_bridge_input",
                    help="Переходное сопротивление в точке контакта (0 Ом — глухое металлическое замыкание).",
                ))
            else:
                rc1, rc2, rc3 = st.columns(3)
                with rc1:
                    r_cold_branch_input = float(st.number_input(
                        "R_уч1 (до КЗ), Ом:",
                        min_value=0.1,
                        max_value=500.0,
                        value=float(st.session_state["r_cold_branch_ohm"]),
                        step=0.5,
                        key=f"{stand_id}_r_cold_input",
                        help="Сопротивление проводов на холодном участке от клемм прибора (T_cold) до точки КЗ (T_кз).",
                    ))
                with rc2:
                    r_hot_loop_input = float(st.number_input(
                        "R_уч2 (от КЗ до спая), Ом:",
                        min_value=0.1,
                        max_value=500.0,
                        value=float(st.session_state["r_hot_loop_ohm"]),
                        step=0.5,
                        key=f"{stand_id}_r_hot_input",
                        help="Сопротивление горячего участка проводов от точки КЗ (T_кз) до рабочего спая (T_hot).",
                    ))
                with rc3:
                    r_bridge_input = float(st.number_input(
                        "Перемычка R_кз, Ом:",
                        min_value=0.0,
                        max_value=100.0,
                        value=float(st.session_state["r_bridge_ohm"]),
                        step=0.5,
                        key=f"{stand_id}_r_bridge_input",
                        help="Переходное сопротивление в точке контакта (0 Ом — глухое металлическое замыкание).",
                    ))
            st.session_state["r_cold_branch_ohm"] = r_cold_branch_input
            st.session_state["r_hot_loop_ohm"] = r_hot_loop_input
            st.session_state["r_bridge_ohm"] = r_bridge_input

    return {
        "circuit_fault_mode": circuit_fault_mode,
        "open_circuit_meter_mode": open_circuit_meter_mode,
        "r_cold_branch_input": r_cold_branch_input,
        "r_hot_loop_input": r_hot_loop_input,
        "r_bridge_input": r_bridge_input,
        "t_kz_val": t_kz_val,
        "kz_contact_type": kz_contact_type,
    }
# =====================================================================
# 6. СТЕНД №1: ВИЗУАЛИЗАЦИЯ ГРАДИЕНТА ТЕМПЕРАТУР И ГЕНЕРАЦИЯ ТЕРМО-ЭДС
# =====================================================================
def render_stand_1_section(params: dict) -> None:
    """Отрисовывает Стенд №1 в унифицированной 8-блочной эргономической структуре."""
    chart_display_mode = params["chart_display_mode"]
    is_mobile_view = (chart_display_mode == "Смартфон (320–430 px)")

    # 1. НАЗВАНИЕ СТЕНДА
    st.title("Стенд №1: Визуализация градиента температур и генерация Термо-ЭДС")

    # 2. КРАТКОЕ НАЗНАЧЕНИЕ
    st.markdown(
        '<div class="kip-stand-purpose">'
        '<strong>Назначение стенда:</strong> исследование формирования термо-ЭДС по табличным номинальным '
        'статическим характеристикам (НСХ) стандартных термопар, влияния температуры холодного спая '
        'и физических нарушений термоэлектрической цепи.'
        '</div>',
        unsafe_allow_html=True,
    )

    # 3. ПАРАМЕТРЫ ЭКСПЕРИМЕНТА (Основные настройки + отдельно Неисправности)
    st.subheader("Параметры эксперимента")
    with st.container(border=True):
        st.markdown('<div class="kip-param-group-title">🔧 Основные параметры термопары и температурного режима</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="kip-param-hint">Выберите градуировку термопары и задайте температуры рабочего (горячего) '
            'и свободного (холодного) спаев.</div>',
            unsafe_allow_html=True,
        )

        sensor_keys = list(THERMOCOUPLES_DB.keys())
        cur_sensor = st.session_state["stand1_sensor_name"]
        if cur_sensor not in sensor_keys:
            cur_sensor = sensor_keys[0]
        sensor_name = st.selectbox(
            "Термопара из расчётной базы симулятора:",
            options=sensor_keys,
            index=sensor_keys.index(cur_sensor),
            key="stand1_sensor_select",
            help="Градуировочная таблица НСХ, по которой рассчитывается термо-ЭДС E(T) при T₀ = 0 °C.",
        )
        st.session_state["stand1_sensor_name"] = sensor_name
        spec = THERMOCOUPLES_DB[sensor_name]

        t_hot_clamped = int(np.clip(
            int(st.session_state["stand1_t_hot"]),
            int(spec["min_t"]),
            int(spec["max_t"]),
        ))
        if "stand1_t_hot_slider" in st.session_state and not (
            int(spec["min_t"]) <= int(st.session_state["stand1_t_hot_slider"]) <= int(spec["max_t"])
        ):
            del st.session_state["stand1_t_hot_slider"]
        t_cold_clamped = int(np.clip(int(st.session_state["stand1_t_cold"]), -50, 100))
        if is_mobile_view:
            t_hot = float(st.slider(
                "Температура горячего (рабочего) спая T_hot, °C:",
                min_value=int(spec["min_t"]),
                max_value=int(spec["max_t"]),
                value=t_hot_clamped,
                step=10,
                key="stand1_t_hot_slider",
                help="Температура измеряемой среды в зоне рабочего спая термопары.",
            ))
            t_cold = float(st.slider(
                "Температура холодного спая T_cold, °C:",
                min_value=-50,
                max_value=100,
                value=t_cold_clamped,
                step=10,
                key="stand1_t_cold_slider",
                help="Температура свободных концов (клеммной колодки прибора), относительно которой формируется разность ЭДС.",
            ))
        else:
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                t_hot = float(st.slider(
                    "Температура горячего (рабочего) спая T_hot, °C:",
                    min_value=int(spec["min_t"]),
                    max_value=int(spec["max_t"]),
                    value=t_hot_clamped,
                    step=10,
                    key="stand1_t_hot_slider",
                    help="Температура измеряемой среды в зоне рабочего спая термопары.",
                ))
            with t_col2:
                t_cold = float(st.slider(
                    "Температура холодного спая T_cold, °C:",
                    min_value=-50,
                    max_value=100,
                    value=t_cold_clamped,
                    step=10,
                    key="stand1_t_cold_slider",
                    help="Температура свободных концов (клеммной колодки прибора), относительно которой формируется разность ЭДС.",
                ))
        st.session_state["stand1_t_hot"] = int(t_hot)
        st.session_state["stand1_t_cold"] = int(t_cold)

    fault_cfg = render_stand_fault_panel("stand1", t_cold=t_cold, t_hot=t_hot)
    circuit_fault_mode = fault_cfg["circuit_fault_mode"]
    open_circuit_meter_mode = fault_cfg["open_circuit_meter_mode"]
    r_cold_branch_input = fault_cfg["r_cold_branch_input"]
    r_hot_loop_input = fault_cfg["r_hot_loop_input"]
    r_bridge_input = fault_cfg["r_bridge_input"]
    t_kz_stand1 = fault_cfg["t_kz_val"]
    kz_contact_type = fault_cfg["kz_contact_type"]

    # Расчёт физических величин (существующие функции без изменений)
    e_kz_stand1 = calculate_nominal_emf(sensor_name, t_kz_stand1) if t_kz_stand1 is not None else None
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
        r_bridge_ohm=r_bridge_input,
    )

    # 4. РАСЧЁТНАЯ ФОРМУЛА
    st.subheader("Расчётная формула")
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

    # 5. ОСНОВНЫЕ ЧИСЛОВЫЕ ПОКАЗАТЕЛИ (4 адаптивные равновеликие карточки)
    st.subheader("Основные числовые показатели")
    fault_tone = (
        "error" if circuit_fault_mode == "Обрыв термоэлектрического контура"
        else ("warn" if circuit_fault_mode == "Паразитный спай (КЗ)" else "normal")
    )
    render_kpi_cards_grid([
        {
            "label": "1. Генерируемая Термо-ЭДС E_ген",
            "value": f"{phys['e_gen_mv']:+.3f} мВ",
            "sub": f"E(T_hot) = {e_hot:.3f} мВ | E(T_cold) = {e_cold:.3f} мВ",
            "tone": "normal",
        },
        {
            "label": "2. Напряжение на приборе U_приб",
            "value": phys["u_meter_str"],
            "sub": phys["circuit_state"],
            "tone": fault_tone,
        },
        {
            "label": "3. Чувствительность S(T_hot) и ток",
            "value": f"S = {seebeck_hot:.2f} мкВ/°C",
            "sub": phys["current_status"],
            "tone": "normal",
        },
        {
            "label": "4. Перепад температур ΔT",
            "value": f"{delta_t:+.1f} °C",
            "sub": f"T_hot ({t_hot:.0f} °C) − T_cold ({t_cold:.0f} °C)",
            "tone": "normal",
        },
    ])

    theme_mode_cur = params.get("theme_mode", THEME_MODE_OPTIONS[0])
    is_light_ui = (theme_mode_cur == "Светлая (дневная)")

    # 6. ГРАФИК И 7. 3D-ВИЗУАЛИЗАЦИЯ (рядом на ПК, вертикально на телефоне)
    def _draw_stand1_plot() -> None:
        st.subheader("График: формирование Термо-ЭДС на характеристике НСХ")
        t_curve = spec["temps"]
        e_curve_abs = spec["values"]
        e_curve_rel = e_curve_abs - e_cold

        light_curve_map = {"#80ed99": "#15803d", "#00b4d8": "#0369a1", "#f77f00": "#c2410c"}
        main_curve_col = light_curve_map.get(spec["color"], spec["color"]) if is_light_ui else spec["color"]
        ref_line_col = "#475569" if is_light_ui else "#adb5bd"
        ref_marker_col = "#0f172a" if is_light_ui else "#ffffff"
        marker_ring_col = "#0f172a" if is_light_ui else "white"
        cold_txt_col = "#0369a1" if is_light_ui else "#4cc9f0"
        hot_txt_col = "#b91c1c" if is_light_ui else "#ff6b6b"
        kz_col = "#b45309" if is_light_ui else "#ff9f1c"

        fig_stand1 = go.Figure()
        all_y_stand1 = [e_curve_rel, e_curve_abs, np.array([0.0, phys["e_gen_mv"]])]

        fig_stand1.add_trace(go.Scatter(
            x=t_curve, y=e_curve_rel, mode="lines",
            name=f"E(T) − E({t_cold:.0f} °C)",
            line=dict(color=main_curve_col, width=3),
            hovertemplate="T = %{x:.0f} °C<br>E_ген = %{y:+.3f} мВ<extra>Основная НСХ</extra>"
        ))

        fig_stand1.add_trace(go.Scatter(
            x=t_curve, y=e_curve_abs, mode="lines+markers",
            name="Таблица E(T) при T₀ = 0 °C",
            line=dict(color=ref_line_col, width=1.5, dash="dash"),
            marker=dict(size=3.5 if is_mobile_view else 4, color=ref_marker_col),
            hovertemplate="T = %{x:.0f} °C<br>E_табл = %{y:+.3f} мВ<extra>При T₀ = 0 °C</extra>"
        ))

        fig_stand1.add_trace(go.Scatter(
            x=[t_cold], y=[0.0],
            mode="markers+text", name="Холодный спай (T_cold)",
            text=["T_cold"] if is_mobile_view else [f"  T_cold = {t_cold:.0f} °C"],
            textposition="bottom right",
            textfont=dict(size=12 if is_mobile_view else 11, color=cold_txt_col),
            marker=dict(size=10, color="#0284c7" if is_light_ui else "#00b4d8", symbol="circle", line=dict(width=1.5, color=marker_ring_col)),
            hovertemplate=(
                f"Холодный спай T_cold = {t_cold:.0f} °C<br>"
                f"E_табл(T_cold) = {e_cold:.3f} мВ<br>E_отн = 0.000 мВ<extra></extra>"
            )
        ))

        fig_stand1.add_trace(go.Scatter(
            x=[t_hot], y=[phys["e_gen_mv"]],
            mode="markers+text", name="Рабочий спай (E_ген)",
            text=[f"T_hot ({phys['e_gen_mv']:+.1f})"] if is_mobile_view else [f"  T_hot = {t_hot:.0f} °C ({phys['e_gen_mv']:+.2f} мВ)"],
            textposition="top left",
            textfont=dict(size=12 if is_mobile_view else 11, color=hot_txt_col),
            marker=dict(size=12, color="#dc2626" if is_light_ui else "#ff4d4d", symbol="diamond", line=dict(width=1.5, color=marker_ring_col)),
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
                text=[f"T_кз ({phys['u_meter_mv']:+.1f})"] if is_mobile_view else [f"T_кз ({phys['u_meter_mv']:+.1f} мВ)"],
                textposition="bottom right",
                textfont=dict(size=12 if is_mobile_view else 11, color=kz_col),
                marker=dict(size=12, color=kz_col, symbol="x", line=dict(width=2, color=marker_ring_col)),
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
                line=dict(color=kz_col, width=2.5, dash="dot"),
                hovertemplate="T = %{x:.0f} °C<br>E_мод = %{y:+.3f} мВ<extra>Условная НСХ</extra>"
            ))

        plotly_cfg1, angle_note1 = configure_adaptive_plotly_layout(
            fig=fig_stand1,
            x_main=t_curve,
            y_main=e_curve_rel,
            all_y_arrays=all_y_stand1,
            x_title="Температура T, °C",
            y_title="Термо-ЭДС E, мВ",
            display_mode=chart_display_mode,
            theme_mode=theme_mode_cur,
        )
        st.plotly_chart(fig_stand1, use_container_width=True, config=plotly_cfg1)
        st.caption(f"📐 {angle_note1}")

    def _draw_stand1_3d() -> None:
        st.subheader("3D-визуализация теплового градиента спаев")
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
                t_kz_val=t_kz_stand1,
                theme_mode=theme_mode_cur,
            ),
            height=410 if is_mobile_view else 460,
        )

    if is_mobile_view:
        _draw_stand1_plot()
        _draw_stand1_3d()
    else:
        col_plot, col_3d = st.columns([3, 2])
        with col_plot:
            _draw_stand1_plot()
        with col_3d:
            _draw_stand1_3d()

    # 8. ДОПОЛНИТЕЛЬНЫЕ ПОЯСНЕНИЯ
    st.subheader("Дополнительные пояснения")
    extra_kz_html = ""
    if circuit_fault_mode == "Паразитный спай (КЗ)" and "третьего" in kz_contact_type:
        extra_kz_html = (
            "<p><strong>Закон промежуточных металлов (Вольта):</strong> если перемычка из третьего металла C находится "
            "при единой температуре T_кз, сумма контактных ЭДС на её краях равна нулю, и измеряемый сигнал "
            "определяется температурой T_кз и делителем сопротивлений R_уч2 и R_кз.</p>"
        )
    st.markdown(
        '<div class="kip-notes-box">'
        f'<p><strong>Электроды термопары:</strong> {html.escape(spec["electrodes"][0])} / {html.escape(spec["electrodes"][1])}</p>'
        f'<p><strong>Состояние цепи:</strong> {html.escape(phys["circuit_state"])}</p>'
        f'<p><strong>Ток в контуре:</strong> {html.escape(phys["current_status"])}</p>'
        f'<p><strong>Статус измерения:</strong> {html.escape(phys["measurement_state"])}</p>'
        f'{extra_kz_html}'
        '</div>',
        unsafe_allow_html=True,
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
            f"Генерируемая ЭДС E_ген при T_cold={t_cold:.0f} °C, мВ": [f"{(v - e_cold):+.3f}" for v in spec["values"]],
        })
        st.dataframe(df_gost, use_container_width=True, height=240)


# =====================================================================
# 7. СТЕНД №2: ИССЛЕДОВАНИЕ ЭФФЕКТА ЗЕЕБЕКА В РАЗНОРОДНЫХ МЕТАЛЛАХ
# =====================================================================
def render_stand_2_section(params: dict) -> None:
    """Отрисовывает Стенд №2 в унифицированной 8-блочной эргономической структуре."""
    chart_display_mode = params["chart_display_mode"]
    is_mobile_view = (chart_display_mode == "Смартфон (320–430 px)")

    # 1. НАЗВАНИЕ СТЕНДА
    st.title("Стенд №2: Исследование эффекта Зеебека в разнородных металлах (Термоэлектрические пары)")

    # 2. КРАТКОЕ НАЗНАЧЕНИЕ
    st.markdown(
        '<div class="kip-stand-purpose">'
        '<strong>Назначение стенда:</strong> сравнение термоэлектрических пар из различных металлов и сплавов, '
        'расчёт итогового коэффициента Зеебека пары и сопоставление линейного приближения с табличной нелинейной НСХ.'
        '</div>',
        unsafe_allow_html=True,
    )

    # 3. ПАРАМЕТРЫ ЭКСПЕРИМЕНТА (Основные настройки + отдельно Неисправности)
    st.subheader("Параметры эксперимента")
    with st.container(border=True):
        st.markdown('<div class="kip-param-group-title">🔧 Выбор термоэлектродов и температурного режима</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="kip-param-hint">Подберите материалы двух ветвей контура и установите температуры спаев. '
            'При выборе одинаковых металлов результирующая ЭДС равна нулю (закон однородной цепи).</div>',
            unsafe_allow_html=True,
        )

        metal_names = list(METALS_DB.keys())
        default_m1 = _resolve_metal_default(metal_names, DEFAULT_STAND2_METAL_1, 0)
        default_m2 = _resolve_metal_default(metal_names, DEFAULT_STAND2_METAL_2, len(metal_names) - 1)
        cur_m1 = st.session_state["stand2_metal_1"]
        cur_m2 = st.session_state["stand2_metal_2"]
        idx_m1 = metal_names.index(cur_m1) if cur_m1 in metal_names else metal_names.index(default_m1)
        idx_m2 = metal_names.index(cur_m2) if cur_m2 in metal_names else metal_names.index(default_m2)

        if is_mobile_view:
            metal_1 = st.selectbox(
                "Металл / сплав ветви А (Термоэлектрод 1):",
                options=metal_names,
                index=idx_m1,
                key="stand2_metal1_select",
                help="Материал первой ветви (положительный электрод при S₁ > S₂).",
            )
            metal_2 = st.selectbox(
                "Металл / сплав ветви B (Термоэлектрод 2):",
                options=metal_names,
                index=idx_m2,
                key="stand2_metal2_select",
                help="Материал второй ветви (отрицательный электрод при S₁ > S₂).",
            )
            t_hot_s2 = float(st.slider(
                "Температура горячего спая T_hot, °C:",
                min_value=-100,
                max_value=800,
                value=int(np.clip(int(st.session_state["stand2_t_hot"]), -100, 800)),
                step=10,
                key="stand2_t_hot_slider",
                help="Температура рабочего спая двух выбранных проводников.",
            ))
            t_cold_s2 = float(st.slider(
                "Температура холодного спая T_cold, °C:",
                min_value=-100,
                max_value=200,
                value=int(np.clip(int(st.session_state["stand2_t_cold"]), -100, 200)),
                step=10,
                key="stand2_t_cold_slider",
                help="Температура клемм подключения к измерительному вольтметру.",
            ))
        else:
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                metal_1 = st.selectbox(
                    "Металл / сплав ветви А (Термоэлектрод 1):",
                    options=metal_names,
                    index=idx_m1,
                    key="stand2_metal1_select",
                    help="Материал первой ветви (положительный электрод при S₁ > S₂).",
                )
            with m_col2:
                metal_2 = st.selectbox(
                    "Металл / сплав ветви B (Термоэлектрод 2):",
                    options=metal_names,
                    index=idx_m2,
                    key="stand2_metal2_select",
                    help="Материал второй ветви (отрицательный электрод при S₁ > S₂).",
                )
            t2_col1, t2_col2 = st.columns(2)
            with t2_col1:
                t_hot_s2 = float(st.slider(
                    "Температура горячего спая T_hot, °C:",
                    min_value=-100,
                    max_value=800,
                    value=int(np.clip(int(st.session_state["stand2_t_hot"]), -100, 800)),
                    step=10,
                    key="stand2_t_hot_slider",
                    help="Температура рабочего спая двух выбранных проводников.",
                ))
            with t2_col2:
                t_cold_s2 = float(st.slider(
                    "Температура холодного спая T_cold, °C:",
                    min_value=-100,
                    max_value=200,
                    value=int(np.clip(int(st.session_state["stand2_t_cold"]), -100, 200)),
                    step=10,
                    key="stand2_t_cold_slider",
                    help="Температура клемм подключения к измерительному вольтметру.",
                ))
        st.session_state["stand2_metal_1"] = metal_1
        st.session_state["stand2_metal_2"] = metal_2
        st.session_state["stand2_t_hot"] = int(t_hot_s2)
        st.session_state["stand2_t_cold"] = int(t_cold_s2)

    fault_cfg2 = render_stand_fault_panel("stand2", t_cold=t_cold_s2, t_hot=t_hot_s2)
    circuit_fault_mode = fault_cfg2["circuit_fault_mode"]
    open_circuit_meter_mode = fault_cfg2["open_circuit_meter_mode"]
    r_cold_branch_input = fault_cfg2["r_cold_branch_input"]
    r_hot_loop_input = fault_cfg2["r_hot_loop_input"]
    r_bridge_input = fault_cfg2["r_bridge_input"]
    t_kz_s2 = fault_cfg2["t_kz_val"]

    # Расчёт физических величин (существующие формулы и функции без изменений)
    delta_t_val = t_hot_s2 - t_cold_s2
    s_metal1 = METALS_DB[metal_1]["seebeck"]
    s_metal2 = METALS_DB[metal_2]["seebeck"]
    s_pair = s_metal1 - s_metal2  # мкВ/°C

    e_hot_lin = (s_pair * t_hot_s2) / 1000.0
    e_cold_lin = (s_pair * t_cold_s2) / 1000.0
    e_kz_lin = (s_pair * t_kz_s2) / 1000.0 if t_kz_s2 is not None else None

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
        r_bridge_ohm=r_bridge_input,
    )

    # 4. РАСЧЁТНАЯ ФОРМУЛА
    st.subheader("Расчётная формула")
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

    # 5. ОСНОВНЫЕ ЧИСЛОВЫЕ ПОКАЗАТЕЛИ (4 адаптивные равновеликие карточки)
    st.subheader("Основные числовые показатели")
    fault_tone2 = (
        "error" if circuit_fault_mode == "Обрыв термоэлектрического контура"
        else ("warn" if circuit_fault_mode == "Паразитный спай (КЗ)" else "normal")
    )
    render_kpi_cards_grid([
        {
            "label": f"1. S₁ ({metal_1.split('(')[0].strip()})",
            "value": f"{s_metal1:+.1f} мкВ/°C",
            "sub": "Приближённо при ~20 °C",
            "tone": "normal",
        },
        {
            "label": f"2. S₂ ({metal_2.split('(')[0].strip()})",
            "value": f"{s_metal2:+.1f} мкВ/°C",
            "sub": f"S_пары = {s_pair:+.1f} мкВ/°C",
            "tone": "normal",
        },
        {
            "label": "3. Генерируемая ЭДС E_ген (лин.)",
            "value": f"{phys_s2['e_gen_mv']:+.3f} мВ",
            "sub": f"ΔT = {delta_t_val:+.0f} °C ({t_hot_s2:.0f} − {t_cold_s2:.0f} °C)",
            "tone": "normal",
        },
        {
            "label": "4. Напряжение на приборе U_приб",
            "value": phys_s2["u_meter_str"],
            "sub": phys_s2["current_status"],
            "tone": fault_tone2,
        },
    ])

    # Определяем совпадение пары с табличной НСХ (исходные данные и знаки без изменений)
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
    t_grid_s2 = np.linspace(-100, 800, 91)
    e_lin_arr = (s_pair * (t_grid_s2 - t_cold_s2)) / 1000.0
    e_gost_arr = None
    if gost_match_key is not None:
        e_ref_cold = gost_sign * calculate_nominal_emf(gost_match_key, t_cold_s2)
        e_gost_arr = np.array([gost_sign * calculate_nominal_emf(gost_match_key, t_val) - e_ref_cold for t_val in t_grid_s2])
        e_gost_hot = gost_sign * calculate_nominal_emf(gost_match_key, t_hot_s2) - e_ref_cold
        comparison_caption = (
            f"📌 **Сравнение моделей при $T_{{\\text{{hot}}}} = {t_hot_s2:.0f}\\text{{ }}^\\circ\\text{{C}}$, "
            f"$T_{{\\text{{cold}}}} = {t_cold_s2:.0f}\\text{{ }}^\\circ\\text{{C}}$:** "
            f"линейное приближение даёт $E_{{\\text{{лин}}}} = {phys_s2['e_gen_mv']:+.3f}\\text{{ мВ}}$, "
            f"табличная нелинейная характеристика даёт $E_{{\\text{{табл}}}} = {e_gost_hot:+.3f}\\text{{ мВ}}$ "
            f"(расхождение из-за зависимости $S(T)$ составляет ${abs(phys_s2['e_gen_mv'] - e_gost_hot):.3f}\\text{{ мВ}}$)."
        )

    theme_mode_cur = params.get("theme_mode", THEME_MODE_OPTIONS[0])
    is_light_ui = (theme_mode_cur == "Светлая (дневная)")

    # 6. ГРАФИК И 7. 3D-ВИЗУАЛИЗАЦИЯ (рядом на ПК, вертикально на телефоне)
    def _draw_stand2_plot() -> None:
        st.subheader("График: сравнение линейного приближения и табличной НСХ")
        lin_col = "#15803d" if is_light_ui else "#80ed99"
        gost_col = "#0369a1" if is_light_ui else "#00b4d8"
        marker_ring_col = "#0f172a" if is_light_ui else "white"
        cold_txt_col = "#0369a1" if is_light_ui else "#4cc9f0"
        hot_txt_col = "#b91c1c" if is_light_ui else "#ff6b6b"
        kz_col = "#b45309" if is_light_ui else "#ff9f1c"

        fig_stand2 = go.Figure()
        all_y_stand2 = [e_lin_arr, np.array([0.0, phys_s2["e_gen_mv"]])]

        fig_stand2.add_trace(go.Scatter(
            x=t_grid_s2, y=e_lin_arr, mode="lines",
            name=f"Линейная (S = {s_pair:+.1f} мкВ/°C)",
            line=dict(color=lin_col, width=3.2),
            hovertemplate="T_hot = %{x:.0f} °C<br>E_лин = %{y:+.3f} мВ<extra>Линейное приближение</extra>"
        ))

        if gost_match_key is not None and e_gost_arr is not None:
            all_y_stand2.append(e_gost_arr)
            fig_stand2.add_trace(go.Scatter(
                x=t_grid_s2, y=e_gost_arr, mode="lines",
                name=f"Табличная НСХ ({THERMOCOUPLES_DB[gost_match_key]['short_code']})",
                line=dict(color=gost_col, width=2.5, dash="dash"),
                hovertemplate="T_hot = %{x:.0f} °C<br>E_табл = %{y:+.3f} мВ<extra>Табличная НСХ</extra>"
            ))

        fig_stand2.add_trace(go.Scatter(
            x=[t_cold_s2], y=[0.0],
            mode="markers+text", name="Холодный спай (T_cold)",
            text=["T_cold"] if is_mobile_view else [f"T_cold ({t_cold_s2:.0f}°C)"],
            textposition="bottom right",
            textfont=dict(size=12 if is_mobile_view else 11, color=cold_txt_col),
            marker=dict(size=10, color="#0284c7" if is_light_ui else "#00b4d8", symbol="circle", line=dict(width=1.5, color=marker_ring_col)),
            hovertemplate=f"Холодный спай T_cold = {t_cold_s2:.0f} °C<br>E = 0.000 мВ<extra></extra>"
        ))

        fig_stand2.add_trace(go.Scatter(
            x=[t_hot_s2], y=[phys_s2["e_gen_mv"]],
            mode="markers+text", name="Рабочая точка (E_ген)",
            text=[f"T_hot ({phys_s2['e_gen_mv']:+.1f})"] if is_mobile_view else [f"  T_hot = {t_hot_s2:.0f} °C ({phys_s2['e_gen_mv']:+.2f} мВ)"],
            textposition="top left",
            textfont=dict(size=12 if is_mobile_view else 11, color=hot_txt_col),
            marker=dict(size=12, color="#dc2626" if is_light_ui else "#ff4d4d", symbol="diamond", line=dict(width=1.5, color=marker_ring_col)),
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
                text=[f"T_кз ({phys_s2['u_meter_mv']:+.1f})"] if is_mobile_view else [f"T_кз ({phys_s2['u_meter_mv']:+.1f} мВ)"],
                textposition="bottom right",
                textfont=dict(size=12 if is_mobile_view else 11, color=kz_col),
                marker=dict(size=12, color=kz_col, symbol="x", line=dict(width=2, color=marker_ring_col)),
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
                line=dict(color=kz_col, width=2.5, dash="dot"),
                hovertemplate="T_hot = %{x:.0f} °C<br>E_мод = %{y:+.3f} мВ<extra>Условная НСХ</extra>"
            ))

        plotly_cfg2, angle_note2 = configure_adaptive_plotly_layout(
            fig=fig_stand2,
            x_main=t_grid_s2,
            y_main=e_lin_arr,
            all_y_arrays=all_y_stand2,
            x_title="Температура T_hot, °C",
            y_title=f"Термо-ЭДС (отн. {t_cold_s2:.0f} °C), мВ",
            display_mode=chart_display_mode,
            theme_mode=theme_mode_cur,
        )
        st.plotly_chart(fig_stand2, use_container_width=True, config=plotly_cfg2)
        st.caption(f"📐 {angle_note2}")

    def _draw_stand2_3d() -> None:
        st.subheader("3D-визуализация термоэлектрического контура")
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
                fault_state=circuit_fault_mode,
                theme_mode=theme_mode_cur,
            ),
            height=410 if is_mobile_view else 460,
        )

    if is_mobile_view:
        _draw_stand2_plot()
        _draw_stand2_3d()
    else:
        col_l, col_r = st.columns([3, 2])
        with col_l:
            _draw_stand2_plot()
        with col_r:
            _draw_stand2_3d()

    # 8. ДОПОЛНИТЕЛЬНЫЕ ПОЯСНЕНИЯ
    st.subheader("Дополнительные пояснения")
    if comparison_caption:
        st.markdown(comparison_caption)

    st.info(
        "ℹ️ **Об используемом приближении (п. 3.4 ТЗ):** Абсолютные коэффициенты Зеебека металлов $S_1$ и $S_2$ "
        "в данной модели являются **приближёнными справочными значениями при комнатной температуре ($\\approx 20\\text{ }^\\circ\\text{C}$)**. "
        "Расчёт по формуле $E = S_{\\text{пары}} \\cdot \\Delta T$ использует **линейное приближение с постоянным коэффициентом Зеебека**, "
        "которое физически строго справедливо только при малых перепадах температур $\\Delta T$. На широком интервале температур "
        "коэффициент Зеебека зависит от температуры $S(T)$, и точная ЭДС определяется интегралом "
        "$E = \\int_{T_{\\text{cold}}}^{T_{\\text{hot}}} [S_A(T) - S_B(T)]\\,dT$."
    )

    st.markdown(
        '<div class="kip-notes-box">'
        f'<p><strong>Состояние цепи:</strong> {html.escape(phys_s2["circuit_state"])}</p>'
        f'<p><strong>Статус измерения:</strong> {html.escape(phys_s2["measurement_state"])}</p>'
        f'<p><strong>Ветвь А ({html.escape(metal_1)}):</strong> {html.escape(METALS_DB[metal_1]["description"])}</p>'
        f'<p><strong>Ветвь B ({html.escape(metal_2)}):</strong> {html.escape(METALS_DB[metal_2]["description"])}</p>'
        '<p><strong>Примечание о единицах измерения:</strong> в интерфейсе используется обозначение мкВ/°C; '
        'для температурных приращений (ΔT) числовые значения чувствительности в мкВ/°C и мкВ/К эквивалентны.</p>'
        '</div>',
        unsafe_allow_html=True,
    )


# =====================================================================
# 8. СПРАВОЧНЫЙ ПОМОЩНИК И ГЕНЕРАТОР УСЛОВНОЙ НСХ
# =====================================================================
HYPO_SEEBECK_MIN = -250.0
HYPO_SEEBECK_MAX = 250.0
MAX_ASSISTANT_QA_PAIRS = 50


def _format_hypothetical_nsh_name(target_s_uv: float) -> str:
    """Формирует отображаемое название условной НСХ с сохранением знака S0 (S−85 / S+85 / S0)."""
    s_rounded = round(float(target_s_uv), 2)
    if s_rounded == 0.0:
        return "Условная-НСХ-S0"
    mag_str = f"{abs(s_rounded):g}"
    if s_rounded < 0.0:
        return f"Условная-НСХ-S−{mag_str}"
    return f"Условная-НСХ-S+{mag_str}"


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
        "name": _format_hypothetical_nsh_name(target_s_uv),
        "s_target": round(target_s_uv, 2),
        "coeffs": {"a1": a1, "a2": a2, "a3": a3},
        "t": t_vec,
        "e": e_vec
    }


def _trim_assistant_history(max_pairs: int = MAX_ASSISTANT_QA_PAIRS) -> None:
    """Ограничивает историю диалога помощника последними max_pairs парами «вопрос — ответ»."""
    msgs = st.session_state.get("messages", [])
    max_dialog_msgs = max_pairs * 2
    if not msgs:
        return
    if msgs[0].get("role") == "assistant":
        welcome = [msgs[0]]
        dialog = msgs[1:]
        if len(dialog) > max_dialog_msgs:
            st.session_state["messages"] = welcome + dialog[-max_dialog_msgs:]
    elif len(msgs) > max_dialog_msgs:
        st.session_state["messages"] = msgs[-max_dialog_msgs:]


def _process_reference_assistant_query(user_query: str) -> None:
    """
    Обрабатывает вопрос пользователя по локальной базе проверенных разборов и формул
    без использования внешней языковой модели. Приоритет отдаётся более специфическим намерениям.
    """
    st.session_state["messages"].append({"role": "user", "content": user_query})

    q_low = user_query.lower()
    num_match = re.search(r"([-+−]?\d+(?:[.,]\d+)?)", q_low)

    # 1. Наиболее специфическое намерение: расчёт условной полиномиальной НСХ по числу
    if num_match and any(k in q_low for k in ["модел", "нсх", "сплав", "зеебек", "мкв", "коэфф", "постро"]):
        s_raw = float(num_match.group(1).replace(",", ".").replace("−", "-"))
        s_val = float(np.clip(s_raw, HYPO_SEEBECK_MIN, HYPO_SEEBECK_MAX))
        clamp_note = ""
        if s_raw != s_val:
            clamp_note = (
                f"> *Примечание: введённое значение $S_0 = {s_raw:g}$ мкВ/°C выходит за допустимый "
                f"диапазон генератора (${HYPO_SEEBECK_MIN:g}\ldots+{HYPO_SEEBECK_MAX:g}$ мкВ/°C) "
                f"и ограничено значением ${s_val:g}$ мкВ/°C.*\n\n"
            )
        alloy_data = build_hypothetical_thermoelectric(s_val)
        st.session_state["ai_alloy"] = alloy_data
        st.session_state["gen_desired_s"] = s_val
        c1, c2, c3 = alloy_data["coeffs"]["a1"], alloy_data["coeffs"]["a2"], alloy_data["coeffs"]["a3"]

        reply = (
            f"{clamp_note}"
            f"Построена условная математическая характеристика **`{alloy_data['name']}`** для $S_0 = {alloy_data['s_target']}$ мкВ/°C "
            f"(кривая добавлена на графики Стенда №1 и Стенда №2):\n\n"
            f"- **Линейный коэффициент $a_1 = S_0 / 1000$:** `{c1:.5f}` мВ/°C\n"
            f"- **Заданный модельный коэффициент $a_2$:** `{c2:.2e}` мВ/°C²\n"
            f"- **Заданный модельный коэффициент $a_3$:** `{c3:.2e}` мВ/°C³\n\n"
            f"$$E(T) = {c1:.5f}\\,T + ({c2:.2e})\\,T^2 + ({c3:.2e})\\,T^3\\text{{ [мВ]}}$$\n\n"
            f"> *Предупреждение: полученная характеристика является математической моделью и не подтверждает "
            f"существование реального термоэлектрического материала с такими свойствами.*"
        )
    # 2. Закон Вольта / промежуточных металлов (проверяется раньше общих вопросов о проводах)
    elif any(k in q_low for k in ["вольт", "третьего", "третий", "третьем", "промежуточн", "последоват", "медн", "щуп"]):
        reply = (
            "**Физическое объяснение (Закон Вольта / Закон промежуточных металлов):**\n\n"
            "Согласно закону промежуточных металлов, включение в термоэлектрический контур любого третьего проводника $C$ (например, медных выводов "
            "и входной цепи вольтметра) **не изменяет результирующую Термо-ЭДС**, если оба конца этого третьего проводника находятся "
            "при одинаковой температуре $T_{\\text{cold}}$:\n"
            "$$\\int_{T_{\\text{cold}}}^{T_{\\text{cold}}} S_C(T)\\,dT = 0$$\n"
            "Дополнительные термо-ЭДС на контактах «Металл А — Медь» и «Медь — Металл B» взаимно компенсируют друг друга."
        )
    # 3. Влияние длины и сечения проводников (убрано слишком общее ключевое слово «провод»)
    elif any(k in q_low for k in ["удлин", "длин", "сечен"]):
        reply = (
            "**Физическое объяснение (Влияние длины и сечения проводников):**\n\n"
            "Если проводники термопары однородны по химическому составу, то **генерируемая Термо-ЭДС не изменится** при удлинении проводов. "
            "Причина в том, что $E = \\int_{T_{\\text{cold}}}^{T_{\\text{hot}}} S_{AB}(T)\\,dT$ является функцией только граничных температур "
            "концов $T_{\\text{hot}}$ и $T_{\\text{cold}}$, а не градиента $\\nabla T$ по отдельности. Однако при увеличении длины $l$ возрастает "
            "внутреннее омическое сопротивление контура $R_{\\text{тп}} = \\rho \\frac{l}{S_{\\text{сеч}}}$, что увеличивает падение напряжения "
            "при протекании тока через низкоомный прибор."
        )
    # 4. Равенство температур спаев (T_hot = T_cold)
    elif any(k in q_low for k in ["равенств", "нулю", "ноль", "одинаков"]):
        reply = (
            "**Физическое объяснение (Равенство температур спаев $T_{\\text{hot}} = T_{\\text{cold}}$):**\n\n"
            "В замкнутом контуре из двух металлов $A$ и $B$ результирующая Термо-ЭДС определяется интегралом:\n"
            "$$E = \\int_{T_{\\text{cold}}}^{T_{\\text{hot}}} \\left(S_A(T) - S_B(T)\\right) dT$$\n"
            "При $T_{\\text{hot}} = T_{\\text{cold}}$ верхний и нижний пределы интегрирования совпадают, поэтому интеграл "
            "тождественно равен нулю ($E = 0$). Термодинамически это прямое следствие **Второго начала термодинамики**: "
            "в изотермическом контуре невозможно непрерывное преобразование теплоты в электрическую работу без перепада температур."
        )
    # 5. Неподдерживаемые вопросы — штатный ответ без выдумывания новых тем
    else:
        reply = (
            "В справочной базе помощника доступны разборы тем: **равенство температур спаев**, **влияние длины проводников**, "
            "**закон промежуточных металлов (Вольта)**, а также расчёт **условной полиномиальной модели НСХ** по заданному "
            "коэффициенту Зеебека (например: *«Модель НСХ 65 мкВ/°C»*)."
        )

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    _trim_assistant_history()


def render_reference_assistant_section() -> None:
    """
    Отрисовывает раздел «Справочный помощник» с чётким визуальным разделением двух инструментов:
    1. Интерактивный справочный помощник (локальная база физических разборов + практикум).
    2. Генератор условной НСХ (самостоятельный расчётный блок учебной полиномиальной модели).
    """
    is_mobile_view = (st.session_state.get("chart_display_mode") == "Смартфон (320–430 px)")

    st.header("📘 Справочный помощник и Генератор условной НСХ")
    st.markdown(
        '<div class="kip-section-intro">'
        '<strong>Локальный справочный модуль:</strong> все ответы и расчёты формируются строго по встроенной базе '
        'проверенных физических разборов и формул (внешняя генеративная языковая модель не используется).'
        '</div>',
        unsafe_allow_html=True,
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

    # Обрабатываем ввод из нижнего поля st.chat_input() до отрисовки ленты сообщений, чтобы ответ сразу появился в карточке
    user_query = st.chat_input(
        "Введите вопрос по теме (например: 'Что такое закон Вольта?' или 'Модель НСХ 90 мкВ/°C')..."
    )
    if user_query:
        _process_reference_assistant_query(user_query)

    def _draw_assistant_panel() -> None:
        with st.container(border=True):
            st.markdown('<span class="kip-panel-badge">ИНСТРУМЕНТ 1 • ЛОКАЛЬНАЯ БАЗА РАЗБОРОВ</span>', unsafe_allow_html=True)
            st.subheader("💬 Интерактивный справочный помощник")
            st.caption(
                "Нажмите на готовую тему ниже или введите вопрос в поле внизу экрана — помощник вернёт "
                "проверенное физическое объяснение с формулами."
            )

            quick_queries = [
                ("Равенство температур спаев (T_hot = T_cold)", "Почему при равенстве температур спаев Термо-ЭДС равна нулю?"),
                ("Влияние длины проводов термопары", "Как изменится ЭДС, если удлинить провода?"),
                ("Закон Вольта (третьего металла)", "Что такое закон Вольта для последовательной цепи металлов?"),
                ("Построить модель НСХ 85 мкВ/°C", "Построй условную НСХ для 85 мкВ/°C"),
            ]
            if is_mobile_view:
                for q_idx, (btn_label, q_text) in enumerate(quick_queries):
                    if st.button(btn_label, key=f"quick_q_btn_{q_idx}", use_container_width=True):
                        _process_reference_assistant_query(q_text)
                        st.rerun()
            else:
                q_cols = st.columns(2)
                for q_idx, (btn_label, q_text) in enumerate(quick_queries):
                    with q_cols[q_idx % 2]:
                        if st.button(btn_label, key=f"quick_q_btn_{q_idx}", use_container_width=True):
                            _process_reference_assistant_query(q_text)
                            st.rerun()

            st.markdown("---")
            for msg in st.session_state["messages"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    def _draw_generator_and_practicum_panel() -> None:
        # Самостоятельный, визуально отделённый блок Генератора условной НСХ
        with st.container(border=True):
            st.markdown('<span class="kip-panel-badge kip-panel-badge--model">ИНСТРУМЕНТ 2 • УЧЕБНАЯ МАТЕМАТИЧЕСКАЯ МОДЕЛЬ</span>', unsafe_allow_html=True)
            st.subheader("📐 Генератор условной НСХ")
            st.warning(
                "⚠️ **Предупреждение:** Полученная характеристика является математической моделью "
                "и не подтверждает существование реального термоэлектрического материала с такими свойствами."
            )
            gen_default_s = float(np.clip(
                float(st.session_state.get("gen_desired_s", 75.0)),
                HYPO_SEEBECK_MIN,
                HYPO_SEEBECK_MAX,
            ))
            if "gen_desired_s_input" in st.session_state and not (
                HYPO_SEEBECK_MIN <= float(st.session_state["gen_desired_s_input"]) <= HYPO_SEEBECK_MAX
            ):
                del st.session_state["gen_desired_s_input"]
            desired_s = st.number_input(
                "Задайте начальный коэффициент Зеебека S₀ при 0 °C (мкВ/°C):",
                min_value=HYPO_SEEBECK_MIN,
                max_value=HYPO_SEEBECK_MAX,
                value=gen_default_s,
                step=5.0,
                key="gen_desired_s_input",
                help="Начальный наклон полиномиальной характеристики E(T) = a₁T + a₂T² + a₃T³. Допустимый диапазон: от −250 до +250 мкВ/°C.",
            )
            desired_s = float(np.clip(float(desired_s), HYPO_SEEBECK_MIN, HYPO_SEEBECK_MAX))
            st.session_state["gen_desired_s"] = desired_s
            if st.button("📐 Построить условную НСХ", key="build_hypo_nsh_btn", type="primary", use_container_width=True):
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
            else:
                st.caption("После нажатия кнопки расчётная кривая автоматически добавится пунктиром на графики Стенда №1 и Стенда №2.")

        # Отдельный компактный блок практикума с качественными вопросами
        with st.container(border=True):
            st.subheader("🎓 Справочный практикум")
            st.caption("Случайный качественный вопрос для быстрой проверки понимания темы:")
            if st.button("🧠 Случайный качественный вопрос", key="assistant_random_q_btn", use_container_width=True):
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
                st.info(f"**Тема: {pq['title']}**\n\n{pq['question']}")
                st.caption(f"💡 *Подсказка:* {pq['hint']}")

    if is_mobile_view:
        _draw_assistant_panel()
        _draw_generator_and_practicum_panel()
    else:
        col_assist, col_gen = st.columns([3, 2])
        with col_assist:
            _draw_assistant_panel()
        with col_gen:
            _draw_generator_and_practicum_panel()


# =====================================================================
# 9. ТЕОРЕТИЧЕСКИЙ РАЗДЕЛ: «ТЕРМО-ЭДС. ЭФФЕКТ ЗЕЕБЕКА»
# =====================================================================


def render_theory_image(rel_path: str, caption: str) -> None:
    """
    Отображает иллюстрацию из папки assets с сохранением пропорций, без растягивания
    и с корректным масштабированием на мобильных и настольных экранах.
    """
    found_path = resolve_asset_path(rel_path)
    safe_caption = html.escape(caption)
    if found_path is not None:
        img_bytes = found_path.read_bytes()
        b64_encoded = base64.b64encode(img_bytes).decode("utf-8")
        st.markdown(
            f"""
            <figure class="kip-theory-figure">
                <img src="data:image/png;base64,{b64_encoded}" alt="{safe_caption}" />
                <figcaption class="kip-theory-figcaption">{safe_caption}</figcaption>
            </figure>
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



# =====================================================================
# 9.1. ИНТЕРАКТИВНАЯ ПРОВЕРКА ЗНАНИЙ: ДЕТЕКТОР МИФОВ И ХРОНОЛОГИЯ ОТКРЫТИЙ
# =====================================================================
MYTH_DETECTOR_CASES = [
    {
        "id": 0,
        "category": "История открытия • Этап 1",
        "stage_idx": 0,
        "statement": (
            "В 1821 году Томас Зеебек в опыте с висмутом и медью сразу доказал, "
            "что магнитную стрелку отклоняет электрический ток, вызванный разностью температур."
        ),
        "is_truth": False,
        "proof_options": [
            "Сам Зеебек называл явление «термомагнетизмом» и связывал его с земным магнетизмом; верное объяснение через электрический ток дал Х. К. Эрстед в 1823 году.",
            "Зеебек вообще не использовал магнитную стрелку, а сразу измерял напряжение цифровым вольтметром.",
            "Опыт с висмутом и медью провёл Алессандро Вольта в 1800 году при создании вольтова столба.",
        ],
        "correct_proof_idx": 0,
        "explanation": (
            "По реферату (гл. 1.3): Зеебек полагал, что разность температур «намагничивает» металлы, "
            "и называл явление термомагнитным эффектом. Верное объяснение через термоток и термин "
            "«термоэлектричество» ввёл Ханс Кристиан Эрстед в 1823 году."
        ),
    },
    {
        "id": 1,
        "category": "Физика эффекта • Этап 2",
        "stage_idx": 1,
        "statement": (
            "Удача первого опыта Зеебека во многом объяснялась выбором висмута: у него коэффициент "
            "Зеебека достигает нескольких десятков мкВ/К по модулю, тогда как у меди — всего около 2 мкВ/К."
        ),
        "is_truth": True,
        "proof_options": [
            "У висмута термоэлектрический эффект выражен особенно ярко среди металлов, а ЭДС пары зависит от разности коэффициентов Зеебека двух проводников.",
            "Висмут — полупроводник с коэффициентом Зеебека более 5000 мкВ/К, поэтому стрелка отклонилась даже без нагрева.",
            "У меди коэффициент Зеебека максимален среди всех металлов, а висмут в опыте служил только магнитным экраном.",
        ],
        "correct_proof_idx": 0,
        "explanation": (
            "По реферату (гл. 2.1): у меди коэффициент Зеебека составляет около 2 мкВ/К, а у висмута — "
            "несколько десятков мкВ/К по модулю, благодаря чему пара висмут–медь дала заметное отклонение стрелки."
        ),
    },
    {
        "id": 2,
        "category": "Эффект Пельтье и опыт Ленца • Этап 3",
        "stage_idx": 2,
        "statement": (
            "Если пропустить постоянный электрический ток через спай висмута и сурьмы, каплю воды "
            "на спае можно заморозить, а при изменении направления тока — растопить."
        ),
        "is_truth": True,
        "proof_options": [
            "Это опыт Э. Х. Ленца (1838 г.), подтвердивший обратимость эффекта Пельтье: тепловая мощность Q̇ = Π·I меняет знак при смене направления тока.",
            "Это следствие закона Джоуля–Ленца Q̇ = I²R, который вызывает охлаждение контакта при любом направлении тока.",
            "Вода замерзает исключительно из-за эффекта Томсона в однородном проводнике без контакта разнородных металлов.",
        ],
        "correct_proof_idx": 0,
        "explanation": (
            "По реферату (гл. 1.4 и 2.2): в 1838 году российский физик Э. Х. Ленц поместил каплю воды на спай "
            "висмута и сурьмы — при одном направлении тока капля замерзала, при обратном оттаивала."
        ),
    },
    {
        "id": 3,
        "category": "Законы термоцепей • Этап 4",
        "stage_idx": 3,
        "statement": (
            "Если сильно нагреть горелкой середину замкнутого кольца из одного однородного медного провода, "
            "в цепи возникнет устойчивый термоток."
        ),
        "is_truth": False,
        "proof_options": [
            "По закону однородной цепи (и опытам Г. Магнуса 1851 г.) в цепи из одного однородного проводника нагревом нельзя создать термоток.",
            "Термоток возникнет, только если предварительно скрутить медный провод в спираль.",
            "Закон промежуточных температур запрещает нагревать медный провод выше 100 °C.",
        ],
        "correct_proof_idx": 0,
        "explanation": (
            "По реферату (гл. 3.2): для возникновения эффекта Зеебека необходимы два разнородных проводника "
            "и разность температур их спаев; в однородном проводнике нагревом создать термоток невозможно."
        ),
    },
    {
        "id": 4,
        "category": "Законы термоцепей • Этап 4",
        "stage_idx": 3,
        "statement": (
            "Подключение вольтметра с медными проводами к термопаре всегда искажает её термо-ЭДС, "
            "даже если обе клеммы подключения имеют одинаковую температуру."
        ),
        "is_truth": False,
        "proof_options": [
            "По закону промежуточных металлов включение третьего проводника не меняет ЭДС, если оба его конца находятся при одинаковой температуре.",
            "Медь вообще не даёт контактной разности потенциалов ни с одним сплавом при любых температурах.",
            "Искажение исчезает только тогда, когда клеммы вольтметра нагреты до температуры горячего спая.",
        ],
        "correct_proof_idx": 0,
        "explanation": (
            "По реферату (гл. 3.2): закон промежуточных металлов позволяет подключать к термопаре "
            "измерительный прибор и паять/сваривать спай без искажения ЭДС, если концы третьего металла изотермичны."
        ),
    },
    {
        "id": 5,
        "category": "Компенсация холодного спая • Этап 4",
        "stage_idx": 3,
        "statement": (
            "Термопара реагирует на разность температур рабочего и холодного спаев, поэтому без учёта "
            "температуры свободных концов (компенсации холодного спая) измерение будет неточным."
        ),
        "is_truth": True,
        "proof_options": [
            "Показания зависят от разности температур спаев: раньше свободные концы держали в тающем льду (0 °C), а современные приборы вводят поправку автоматически.",
            "Компенсация холодного спая нужна только для охлаждения усилителя внутри вторичного прибора.",
            "Температура свободных концов влияет на показания лишь при обрыве термопары.",
        ],
        "correct_proof_idx": 0,
        "explanation": (
            "По реферату (гл. 3.1): термо-ЭДС зависит от разности температур рабочего спая и свободных концов, "
            "поэтому современные приборы измеряют температуру клемм термистором или термометром сопротивления и вводят поправку."
        ),
    },
    {
        "id": 6,
        "category": "Стандартные термопары • Этап 5",
        "stage_idx": 4,
        "statement": (
            "Платинородиевая термопара типа B (ТПР) — самая дорогая и точная, поэтому она лучше всего "
            "подходит для измерения комнатной температуры от 0 до 40 °C."
        ),
        "is_truth": False,
        "proof_options": [
            "При температурах ниже +50 °C тип B практически не даёт полезного сигнала (ЭДС при 0 и 42 °C почти одинакова); он предназначен для высоких температур.",
            "Платина мгновенно разрушается на воздухе при комнатной температуре.",
            "У типа B слишком высокая чувствительность (более 200 мкВ/°C), из-за чего прибор зашкаливает при 20 °C.",
        ],
        "correct_proof_idx": 0,
        "explanation": (
            "По реферату (гл. 3.3 и 4.2): тип B работает при очень высоких температурах (до 1700–1800 °C), "
            "а ниже 50 °C практически не даёт сигнала, поэтому для комнатных температур он не подходит."
        ),
    },
    {
        "id": 7,
        "category": "Материалы термопар • Этап 5",
        "stage_idx": 4,
        "statement": (
            "Термопара типа N (нихросил–нисил) создана как улучшенная замена типа K (хромель–алюмель): "
            "она лучше сопротивляется окислению и меньше дрейфует при высоких температурах."
        ),
        "is_truth": True,
        "proof_options": [
            "Благодаря добавкам кремния сплавы нихросил и нисил устойчивее к окислению и меньше меняют градуировку, хотя их чувствительность чуть ниже (~39 против ~41 мкВ/°C).",
            "Тип N изготовлен из вольфрама и платины и работает на открытом воздухе до 2500 °C.",
            "Тип N обладает самой высокой чувствительностью среди всех стандартных пар — около 68 мкВ/°C.",
        ],
        "correct_proof_idx": 0,
        "explanation": (
            "По реферату (гл. 4.3): пара нихросил–нисил (тип N) разработана как более стабильная замена типа K "
            "с лучшей стойкостью к окислению и меньшим дрейфом (наибольшая чувствительность ~68 мкВ/°C у типа E)."
        ),
    },
    {
        "id": 8,
        "category": "Высокотемпературные пары • Этап 5",
        "stage_idx": 4,
        "statement": (
            "Вольфрам-рениевые термопары рассчитаны на 2200–2500 °C, поэтому их можно свободно применять "
            "в обычной открытой воздушной печи."
        ),
        "is_truth": False,
        "proof_options": [
            "На воздухе вольфрам быстро окисляется, поэтому вольфрам-рениевые термопары допускаются только в вакууме, инертной или восстановительной среде.",
            "Вольфрам-рениевые пары работают только в криогенной области при температурах жидкого гелия.",
            "В воздушной печи их нельзя применять только потому, что они перестают давать сигнал выше 800 °C.",
        ],
        "correct_proof_idx": 0,
        "explanation": (
            "По реферату (гл. 4.5): вольфрам-рениевые термопары измеряют 2200–2500 °C только в вакууме, "
            "инертной или восстановительной среде, так как на воздухе вольфрам быстро окисляется."
        ),
    },
    {
        "id": 9,
        "category": "Полупроводники и добротность ZT • Этапы 5–6",
        "stage_idx": 4,
        "statement": (
            "Для эффективного термоэлектрического генератора или модуля Пельтье нужен материал "
            "с максимально высокой теплопроводностью, чтобы тепло быстрее проходило через элемент."
        ),
        "is_truth": False,
        "proof_options": [
            "По формуле добротности ZT = α²σT/κ хороший термоэлектрик должен сочетать высокие α и σ с низкой теплопроводностью κ — поэтому используют полупроводники (Bi₂Te₃ и др.).",
            "Добротность ZT не зависит от теплопроводности и определяется только температурой плавления металла.",
            "Лучшим материалом для генераторов является чистая медь с КПД выше 50 %.",
        ],
        "correct_proof_idx": 0,
        "explanation": (
            "По реферату (гл. 4.6): добротность ZT = α²σT/κ обратно пропорциональна теплопроводности κ. "
            "Если теплопроводность велика, разность температур быстро выравнивается, поэтому применяют полупроводники."
        ),
    },
]

CHRONOLOGY_EVENTS = [
    {
        "id": 0,
        "year": "1800 г.",
        "title": "Алессандро Вольта — «вольтов столб»",
        "desc": "Создан первый источник постоянного тока, открывший эпоху систематических опытов с электричеством.",
    },
    {
        "id": 1,
        "year": "1820 г.",
        "title": "Ханс Кристиан Эрстед — магнитное действие тока",
        "desc": "Обнаружено, что проводник с электрическим током отклоняет магнитную стрелку компаса.",
    },
    {
        "id": 2,
        "year": "1821 г.",
        "title": "Томас Иоганн Зеебек — открытие термо-ЭДС",
        "desc": "В опыте с кольцом из висмута и меди при нагревании одного спая зафиксировано отклонение стрелки.",
    },
    {
        "id": 3,
        "year": "1834 г.",
        "title": "Жан Шарль Пельтье — обратный эффект",
        "desc": "Открыто выделение или поглощение дополнительной теплоты в спае разнородных проводников при пропускании тока.",
    },
    {
        "id": 4,
        "year": "1838 г.",
        "title": "Э. Х. Ленц — опыт с замерзающей каплей воды",
        "desc": "Наглядно доказано тепловое действие эффекта Пельтье: капля воды на спае висмута и сурьмы замерзала и оттаивала.",
    },
    {
        "id": 5,
        "year": "1851–1857 гг.",
        "title": "Уильям Томсон (лорд Кельвин) — единая теория",
        "desc": "Выведены термодинамические соотношения между эффектами Зеебека и Пельтье и предсказан эффект Томсона.",
    },
    {
        "id": 6,
        "year": "1886 г.",
        "title": "Анри Луи Ле Шателье — платинородиевая термопара",
        "desc": "Предложена термопара платина–платинородий, ставшая основой высокотемпературной и эталонной термометрии.",
    },
    {
        "id": 7,
        "year": "1930-е – 1956 г.",
        "title": "Школа А. Ф. Иоффе — полупроводники, ТГ-1 и «Морозко»",
        "desc": "Показана перспективность полупроводников; созданы генератор ТГ-1 («партизанский котелок») и серийный холодильник «Морозко» (1956).",
    },
]


def _make_shuffled_chrono_order(seed_val: int | None = None) -> list[int]:
    """Создаёт перемешанный порядок событий хронологии (гарантированно не совпадающий с верным)."""
    ids = [ev["id"] for ev in CHRONOLOGY_EVENTS]
    rng = random.Random(seed_val)
    order = list(ids)
    for _ in range(15):
        rng.shuffle(order)
        exact = sum(1 for pos, eid in enumerate(order) if pos == eid)
        if exact <= 2 and order != ids:
            return order
    return list(reversed(ids))


def _make_myth_proof_orders(seed_val: int | None = None) -> dict[int, list[int]]:
    """Генерирует перемешанный порядок 3 вариантов доказательства для каждого дела Детектора мифов."""
    rng = random.Random(seed_val)
    orders: dict[int, list[int]] = {}
    for case in MYTH_DETECTOR_CASES:
        perm = [0, 1, 2]
        rng.shuffle(perm)
        orders[case["id"]] = perm
    return orders


def _init_knowledge_check_state() -> None:
    """Инициализирует состояние интерактивных игр «Детектор мифов» и «Хронология открытий»."""
    if "check_game_mode" not in st.session_state:
        st.session_state["check_game_mode"] = "myth"
    if "myth_order" not in st.session_state:
        st.session_state["myth_order"] = [c["id"] for c in MYTH_DETECTOR_CASES]
    if "myth_idx" not in st.session_state:
        st.session_state["myth_idx"] = 0
    if "myth_answers" not in st.session_state:
        st.session_state["myth_answers"] = {}
    if "myth_streak" not in st.session_state:
        st.session_state["myth_streak"] = 0
    if "myth_best_streak" not in st.session_state:
        st.session_state["myth_best_streak"] = 0
    if "myth_proof_orders" not in st.session_state:
        st.session_state["myth_proof_orders"] = _make_myth_proof_orders(seed_val=1821)

    if "chrono_order" not in st.session_state:
        st.session_state["chrono_order"] = _make_shuffled_chrono_order(seed_val=1838)
    if "chrono_checked" not in st.session_state:
        st.session_state["chrono_checked"] = False
    if "chrono_attempts" not in st.session_state:
        st.session_state["chrono_attempts"] = 0
    if "chrono_revealed_ids" not in st.session_state:
        st.session_state["chrono_revealed_ids"] = []
    if "chrono_solved" not in st.session_state:
        st.session_state["chrono_solved"] = False
    if "chrono_best_correct" not in st.session_state:
        st.session_state["chrono_best_correct"] = 0


def _compute_knowledge_rank(myth_points: int, myth_max: int, chrono_points: int, chrono_max: int) -> tuple[str, int, int]:
    """Вычисляет итоговый балл и инженерный ранг по результатам обеих игр."""
    total_pts = myth_points + chrono_points
    max_pts = max(myth_max + chrono_max, 1)
    pct = (total_pts / max_pts) * 100.0
    if pct >= 99.9:
        rank = "Хранитель законов Кельвина"
    elif pct >= 80.0:
        rank = "Эксперт термоэлектричества"
    elif pct >= 55.0:
        rank = "Инженер-термометрист"
    elif pct >= 25.0:
        rank = "Ассистент лаборатории"
    else:
        rank = "Наблюдатель опыта 1821 г."
    return rank, total_pts, max_pts


def _submit_myth_verdict(case_id: int, chosen_truth: bool) -> None:
    """Фиксирует выбор «Правда / Миф» для текущего дела и обновляет серию побед."""
    answers = dict(st.session_state.get("myth_answers", {}))
    if case_id in answers:
        return
    case = MYTH_DETECTOR_CASES[case_id]
    is_ok = (chosen_truth == case["is_truth"])
    answers[case_id] = {
        "verdict_choice": chosen_truth,
        "verdict_ok": is_ok,
        "proof_choice": None,
        "proof_ok": None,
    }
    st.session_state["myth_answers"] = answers
    if is_ok:
        new_streak = int(st.session_state.get("myth_streak", 0)) + 1
        st.session_state["myth_streak"] = new_streak
        st.session_state["myth_best_streak"] = max(int(st.session_state.get("myth_best_streak", 0)), new_streak)
    else:
        st.session_state["myth_streak"] = 0


def _submit_myth_proof(case_id: int, radio_key: str, perm: list[int]) -> None:
    """Фиксирует выбранное физическое или историческое доказательство (+1 бонусный балл)."""
    answers = dict(st.session_state.get("myth_answers", {}))
    if case_id not in answers or answers[case_id]["proof_choice"] is not None:
        return
    case = MYTH_DETECTOR_CASES[case_id]
    chosen_text = st.session_state.get(radio_key)
    displayed_opts = [case["proof_options"][i] for i in perm]
    if chosen_text not in displayed_opts:
        return
    orig_idx = perm[displayed_opts.index(chosen_text)]
    answers[case_id]["proof_choice"] = orig_idx
    answers[case_id]["proof_ok"] = (orig_idx == case["correct_proof_idx"])
    st.session_state["myth_answers"] = answers


def _reset_myth_detector(shuffle_cases: bool = False) -> None:
    """Сбрасывает прогресс Детектора мифов (опционально перемешивая порядок дел)."""
    order = [c["id"] for c in MYTH_DETECTOR_CASES]
    if shuffle_cases:
        random.shuffle(order)
    st.session_state["myth_order"] = order
    st.session_state["myth_idx"] = 0
    st.session_state["myth_answers"] = {}
    st.session_state["myth_streak"] = 0
    st.session_state["myth_best_streak"] = 0
    st.session_state["myth_proof_orders"] = _make_myth_proof_orders()
    request_page_scroll("kip-theory-content-anchor")


def _jump_to_theory_stage(stage_idx: int, stage_titles: list[str]) -> None:
    """Переносит пользователя из игры сразу на нужный этап теории для повторения."""
    clamped = int(np.clip(stage_idx, 0, len(stage_titles) - 1))
    st.session_state["theory_stage_idx"] = clamped
    st.session_state["theory_stage_selectbox"] = stage_titles[clamped]
    st.session_state["theory_subtab"] = "Изучение по этапам (1–6)"
    request_page_scroll("kip-theory-stage-anchor")


def _move_chrono_item(pos: int, delta: int) -> None:
    """Перемещает событие хронологии на одну позицию вверх или вниз."""
    order = list(st.session_state.get("chrono_order", []))
    new_pos = pos + delta
    if 0 <= pos < len(order) and 0 <= new_pos < len(order):
        order[pos], order[new_pos] = order[new_pos], order[pos]
        st.session_state["chrono_order"] = order
        st.session_state["chrono_checked"] = False
        st.session_state["chrono_solved"] = False


def _check_chronology() -> None:
    """Проверяет текущую последовательность хронологии и обновляет статистику."""
    order = list(st.session_state.get("chrono_order", []))
    correct_cnt = sum(1 for pos, eid in enumerate(order) if pos == eid)
    st.session_state["chrono_checked"] = True
    st.session_state["chrono_attempts"] = int(st.session_state.get("chrono_attempts", 0)) + 1
    st.session_state["chrono_best_correct"] = max(
        int(st.session_state.get("chrono_best_correct", 0)),
        correct_cnt,
    )
    st.session_state["chrono_solved"] = (correct_cnt == len(CHRONOLOGY_EVENTS))


def _reveal_one_chrono_hint() -> None:
    """Открывает год одного ещё не открытого события, стоящего не на своём месте."""
    order = list(st.session_state.get("chrono_order", []))
    revealed = list(st.session_state.get("chrono_revealed_ids", []))
    candidates = [eid for pos, eid in enumerate(order) if pos != eid and eid not in revealed]
    if not candidates:
        candidates = [eid for eid in order if eid not in revealed]
    if candidates:
        revealed.append(candidates[0])
        st.session_state["chrono_revealed_ids"] = revealed


def _show_solved_chronology() -> None:
    """Устанавливает правильный порядок всех событий хронологии для разбора."""
    st.session_state["chrono_order"] = [ev["id"] for ev in CHRONOLOGY_EVENTS]
    st.session_state["chrono_checked"] = True
    st.session_state["chrono_revealed_ids"] = [ev["id"] for ev in CHRONOLOGY_EVENTS]


def _reset_chronology() -> None:
    """Перемешивает события хронологии заново для новой попытки."""
    st.session_state["chrono_order"] = _make_shuffled_chrono_order()
    st.session_state["chrono_checked"] = False
    st.session_state["chrono_attempts"] = 0
    st.session_state["chrono_revealed_ids"] = []
    st.session_state["chrono_solved"] = False
    st.session_state["chrono_best_correct"] = 0
    request_page_scroll("kip-theory-content-anchor")


def render_myth_detector_game(stage_titles: list[str]) -> None:
    """Отрисовывает интерактивную игру «Детектор мифов» (вердикт Правда/Миф + доказательство)."""
    myth_order = list(st.session_state["myth_order"])
    total_cases = len(myth_order)
    curr_pos = int(np.clip(int(st.session_state["myth_idx"]), 0, total_cases - 1))
    st.session_state["myth_idx"] = curr_pos
    answers = st.session_state["myth_answers"]
    answered_cnt = len(answers)

    st.progress(
        answered_cnt / total_cases,
        text=f"Разобрано дел: {answered_cnt} из {total_cases} • Текущее дело: №{curr_pos + 1}",
    )

    case_id = myth_order[curr_pos]
    case = MYTH_DETECTOR_CASES[case_id]
    ans = answers.get(case_id)

    verdict_badge = "⏳ Ожидает вердикта"
    if ans is not None:
        verdict_badge = "✅ Вердикт верен" if ans["verdict_ok"] else "❌ Ошибка в вердикте"

    st.markdown(
        f'<div class="kip-myth-card">'
        f'<div class="kip-myth-meta">'
        f'<span class="kip-myth-badge">🕵️ Дело №{curr_pos + 1} из {total_cases} • {html.escape(case["category"])}</span>'
        f'<span class="kip-myth-badge">{html.escape(verdict_badge)}</span>'
        f'</div>'
        f'<div class="kip-myth-statement">«{html.escape(case["statement"])}»</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if ans is None:
        st.caption("Шаг 1 из 2: оцените утверждение — это научный факт из реферата или распространённый миф?")
        with st.container():
            st.markdown('<div class="kip-inline-pair-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
            v_col1, v_col2 = st.columns(2)
        st.caption("Шаг 1 из 2: нажмите кнопку ниже — это научный факт из реферата или миф?")
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            if st.button(
                "✅ ПРАВДА",
                key=f"myth_btn_true_{case_id}",
                type="primary",
                use_container_width=True,
            ):
                _submit_myth_verdict(case_id, True)
                st.rerun()
        with v_col2:
            if st.button(
                "❌ МИФ",
                key=f"myth_btn_false_{case_id}",
                type="secondary",
                use_container_width=True,
            ):
                _submit_myth_verdict(case_id, False)
                st.rerun()
    else:
        truth_word = "ПРАВДА" if case["is_truth"] else "МИФ"
        if ans["verdict_ok"]:
            st.success(f"🎯 Точно! Это действительно **{truth_word}** (+1 балл за вердикт).")
        else:
            st.error(f"💥 Промах! На самом деле это **{truth_word}**.")

        perm = st.session_state["myth_proof_orders"].get(case_id, [0, 1, 2])
        displayed_proofs = [case["proof_options"][i] for i in perm]
        radio_key = f"myth_proof_radio_{case_id}"

        if ans["proof_choice"] is None:
            with st.container(border=True):
                st.markdown("**Шаг 2 из 2 • Бонус-доказательство (+1 балл):** выберите закон или факт из реферата, который это доказывает:")
                st.radio(
                    "Аргумент защиты / опровержения:",
                    options=displayed_proofs,
                    key=radio_key,
                )
                st.button(
                    "⚖️ Предъявить доказательство",
                    key=f"myth_proof_submit_{case_id}",
                    type="primary",
                    use_container_width=True,
                    on_click=_submit_myth_proof,
                    args=(case_id, radio_key, perm),
                )
        else:
            if ans["proof_ok"]:
                st.success("🏅 Доказательство принято! Вы указали верный физический/исторический аргумент (+1 бонусный балл).")
            else:
                st.warning(
                    f"⚠️ Доказательство неточное. Верный аргумент: **{case['proof_options'][case['correct_proof_idx']]}**"
                )
            st.info(f"📖 **Разбор по реферату:** {case['explanation']}")
            st.button(
                f"📖 Повторить {stage_titles[case['stage_idx']].split('.')[0]} в теории",
                key=f"myth_jump_stage_{case_id}",
                on_click=_jump_to_theory_stage,
                args=(case["stage_idx"], stage_titles),
            )

    st.markdown("---")
    m_nav1, m_nav2, m_nav3 = st.columns([1, 1, 1])
    with m_nav1:
        if st.button("⬅️ Предыдущее дело", key="myth_prev_case_btn", disabled=(curr_pos == 0), use_container_width=True):
            st.session_state["myth_idx"] = curr_pos - 1
            request_page_scroll("kip-theory-content-anchor")
            st.rerun()
    with m_nav2:
        st.button(
            "🔀 Начать заново",
            key="myth_restart_btn",
            use_container_width=True,
            on_click=_reset_myth_detector,
            args=(True,),
        )
    with m_nav3:
        if st.button(
            "Следующее дело ➡️",
            key="myth_next_case_btn",
            disabled=(curr_pos >= total_cases - 1),
            type="primary" if (ans is not None and curr_pos < total_cases - 1) else "secondary",
            use_container_width=True,
        ):
            st.session_state["myth_idx"] = curr_pos + 1
            request_page_scroll("kip-theory-content-anchor")
            st.rerun()

    if answered_cnt == total_cases:
        v_ok = sum(1 for a in answers.values() if a["verdict_ok"])
        p_ok = sum(1 for a in answers.values() if a["proof_ok"] is True)
        st.markdown("---")
        with st.container(border=True):
            st.subheader("🏆 Итоговый протокол «Детектора мифов»")
            st.markdown(
                f"- **Верных вердиктов («Правда / Миф»):** `{v_ok} / {total_cases}`\n"
                f"- **Бонусов за точное доказательство:** `{p_ok} / {total_cases}`\n"
                f"- **Лучшая серия побед подряд:** `{st.session_state['myth_best_streak']}`"
            )
            summary_rows = []
            for idx_r, cid in enumerate(myth_order, start=1):
                c_item = MYTH_DETECTOR_CASES[cid]
                a_item = answers[cid]
                summary_rows.append({
                    "№": idx_r,
                    "Тема": c_item["category"],
                    "Истина": "Правда" if c_item["is_truth"] else "Миф",
                    "Вердикт": "✅ Верно" if a_item["verdict_ok"] else "❌ Ошибка",
                    "Доказательство": (
                        "✅ +1" if a_item["proof_ok"] is True
                        else ("❌ 0" if a_item["proof_ok"] is False else "— Не выбрано")
                    ),
                })
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)


def render_chronology_game() -> None:
    """Отрисовывает интерактивную игру «Хронология открытий термоэлектричества (1800–1956)»."""
    order = list(st.session_state["chrono_order"])
    checked = bool(st.session_state["chrono_checked"])
    solved = bool(st.session_state["chrono_solved"])
    revealed_ids = set(st.session_state.get("chrono_revealed_ids", []))
    is_mobile_view = (st.session_state.get("chart_display_mode") == "Смартфон (320–430 px)")
    n_events = len(CHRONOLOGY_EVENTS)

    st.markdown(
        "**Задание:** расставьте 8 ключевых вех развития термоэлектричества из реферата "
        "в правильном хронологическом порядке — от **самого раннего события (№1)** сверху "
        "до **самого позднего (№8)** снизу. Переставляйте карточки кнопками **⬆️** и **⬇️**, затем нажмите **«Проверить хронологию»**."
    )

    if solved:
        st.success(
            f"🎉 Безупречно! Вся хронология открытий (1800–1956) собрана верно "
            f"(попыток проверки: {st.session_state['chrono_attempts']})."
        )
        with st.container(border=True):
            st.subheader("📜 Полная лента времени термоэлектричества (1800–1956)")
            for ev in CHRONOLOGY_EVENTS:
                st.markdown(
                    f'<div class="kip-timeline-item">'
                    f'<strong>{html.escape(ev["year"])} — {html.escape(ev["title"])}</strong><br/>'
                    f'<span style="font-size: var(--kip-font-caption); color: var(--kip-text-secondary);">{html.escape(ev["desc"])}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.button(
            "🔀 Перемешать и собрать заново",
            key="chrono_solved_reset_btn",
            type="primary",
            use_container_width=True,
            on_click=_reset_chronology,
        )
        return

    if checked:
        exact_now = sum(1 for pos, eid in enumerate(order) if pos == eid)
        if exact_now == n_events:
            st.success("🎉 Все 8 событий стоят на своих местах!")
        else:
            st.warning(
                f"🔍 Точно на своём месте сейчас: **{exact_now} из {n_events}**. "
                f"Обратите внимание на подсказки направления («раньше» / «позже») в жёлтых карточках и переставьте их."
            )

    for pos, eid in enumerate(order):
        ev = CHRONOLOGY_EVENTS[eid]
        is_exact = (pos == eid)

        card_cls = "kip-chrono-card"
        hint_html = ""
        year_badge = ""

        if checked and is_exact:
            card_cls = "kip-chrono-card kip-chrono-card--ok"
            year_badge = f'<span class="kip-chrono-year">✅ {html.escape(ev["year"])}</span>'
            hint_html = '<div class="kip-chrono-hint">✅ На своём месте</div>'
        elif checked and not is_exact:
            card_cls = "kip-chrono-card kip-chrono-card--wrong"
            if eid in revealed_ids:
                year_badge = f'<span class="kip-chrono-year">💡 {html.escape(ev["year"])}</span>'
            if eid < pos:
                hint_html = '<div class="kip-chrono-hint">⬆️ Это событие произошло РАНЬШЕ — поднимите карточку выше</div>'
            else:
                hint_html = '<div class="kip-chrono-hint">⬇️ Это событие произошло ПОЗЖЕ — опустите карточку ниже</div>'
        elif eid in revealed_ids:
            year_badge = f'<span class="kip-chrono-year">💡 {html.escape(ev["year"])}</span>'

        card_html = (
            f'<div class="{card_cls}">'
            f'<div class="kip-chrono-head">'
            f'<span class="kip-chrono-pos">#{pos + 1}</span>'
            f'{year_badge}'
            f'<span class="kip-chrono-title">{html.escape(ev["title"])}</span>'
            f'</div>'
            f'<div class="kip-chrono-desc">{html.escape(ev["desc"])}</div>'
            f'{hint_html}'
            f'</div>'
        )

        if is_mobile_view:
            st.markdown(card_html, unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="kip-inline-pair-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
                mc1, mc2 = st.columns(2)
                with mc1:
                    st.button(
                        "⬆️ Выше",
                        key=f"chrono_up_{pos}_{eid}",
                        disabled=(pos == 0),
                        use_container_width=True,
                        on_click=_move_chrono_item,
                        args=(pos, -1),
                    )
                with mc2:
                    st.button(
                        "⬇️ Ниже",
                        key=f"chrono_down_{pos}_{eid}",
                        disabled=(pos == n_events - 1),
                        use_container_width=True,
                        on_click=_move_chrono_item,
                        args=(pos, 1),
                    )
        else:
            c_card, c_up, c_dn = st.columns([5.6, 0.85, 0.85])
            with c_card:
                st.markdown(card_html, unsafe_allow_html=True)
            with c_up:
                st.button(
                    "⬆️",
                    key=f"chrono_up_{pos}_{eid}",
                    disabled=(pos == 0),
                    use_container_width=True,
                    help="Переместить событие выше (раньше по времени)",
                    on_click=_move_chrono_item,
                    args=(pos, -1),
                )
            with c_dn:
                st.button(
                    "⬇️",
                    key=f"chrono_down_{pos}_{eid}",
                    disabled=(pos == n_events - 1),
                    use_container_width=True,
                    help="Переместить событие ниже (позже по времени)",
                    on_click=_move_chrono_item,
                    args=(pos, 1),
                )

    st.markdown("---")
    act1, act2, act3, act4 = st.columns(4)
    with act1:
        st.button(
            "🔍 Проверить хронологию",
            key="chrono_check_btn",
            type="primary",
            use_container_width=True,
            on_click=_check_chronology,
        )
    with act2:
        st.button(
            "💡 Открыть 1 дату",
            key="chrono_hint_btn",
            disabled=(len(revealed_ids) >= n_events),
            use_container_width=True,
            on_click=_reveal_one_chrono_hint,
        )
    with act3:
        st.button(
            "🔀 Перемешать",
            key="chrono_shuffle_btn",
            use_container_width=True,
            on_click=_reset_chronology,
        )
    with act4:
        st.button(
            "📜 Показать ответ",
            key="chrono_solve_btn",
            use_container_width=True,
            on_click=_show_solved_chronology,
        )


def render_knowledge_check_hub(stage_titles: list[str]) -> None:
    """
    Интерактивный центр проверки знаний в разделе «Теория»:
    объединяет «Детектор мифов» (10 дел) и «Хронологию открытий» (8 вех 1800–1956),
    ведёт общий рейтинг и сохраняет классический чек-лист из 10 вопросов в свёрнутом блоке.
    """
    _init_knowledge_check_state()

    answers = st.session_state["myth_answers"]
    v_ok = sum(1 for a in answers.values() if a["verdict_ok"])
    p_ok = sum(1 for a in answers.values() if a["proof_ok"] is True)
    myth_pts = v_ok + p_ok
    myth_max = len(MYTH_DETECTOR_CASES) * 2

    chrono_best = int(st.session_state["chrono_best_correct"])
    chrono_max = len(CHRONOLOGY_EVENTS)
    chrono_status = (
        "✅ Собрано (8 / 8)" if st.session_state["chrono_solved"]
        else f"Лучший: {chrono_best} / {chrono_max}"
    )

    rank_title, total_pts, max_pts = _compute_knowledge_rank(myth_pts, myth_max, chrono_best, chrono_max)

    st.subheader("🎯 Интерактивная проверка знаний: Детектор мифов и Хронология")
    st.caption(
        "Вместо обычного списка вопросов из методички проверьте понимание реферата в двух игровых режимах: "
        "разоблачайте физические мифы с доказательствами и соберите ленту открытий 1800–1956 годов."
    )

    render_kpi_cards_grid([
        {
            "label": "1. Детектор мифов",
            "value": f"{v_ok} / {len(MYTH_DETECTOR_CASES)}",
            "sub": f"Бонус за доказательства: +{p_ok} (всего {myth_pts}/{myth_max})",
            "tone": "normal",
        },
        {
            "label": "2. Хронология (1800–1956)",
            "value": chrono_status,
            "sub": f"Попыток проверки: {st.session_state['chrono_attempts']}",
            "tone": "normal",
        },
        {
            "label": "3. Серия побед (комбо)",
            "value": f"🔥 {st.session_state['myth_streak']}",
            "sub": f"Рекорд серии: {st.session_state['myth_best_streak']} подряд",
            "tone": "normal",
        },
        {
            "label": "4. Текущий ранг",
            "value": rank_title,
            "sub": f"Общий счёт: {total_pts} из {max_pts} баллов",
            "tone": "normal",
        },
    ])

    st.markdown("---")
    st.markdown("### 🕵️ Блок 1. Детектор мифов (10 дел)")
    render_myth_detector_game(stage_titles)

    st.markdown("---")
    st.markdown("### ⏳ Блок 2. Хронология открытий (1800–1956)")
    render_chronology_game()


def _on_theory_stage_select_change(stage_titles: list[str]) -> None:
    """Синхронизирует theory_stage_idx при выборе этапа и прокручивает экран к началу текста этапа."""
    chosen_title = st.session_state.get("theory_stage_selectbox")
    if chosen_title in stage_titles:
        st.session_state["theory_stage_idx"] = stage_titles.index(chosen_title)
        request_page_scroll("kip-theory-stage-anchor")


def _step_theory_stage(delta: int, stage_titles: list[str]) -> None:
    """Обновляет оба ключа этапа и планирует автопрокрутку к началу текста выбранного этапа."""
    curr = int(st.session_state.get("theory_stage_idx", 0))
    new_idx = int(np.clip(curr + delta, 0, len(stage_titles) - 1))
    st.session_state["theory_stage_idx"] = new_idx
    st.session_state["theory_stage_selectbox"] = stage_titles[new_idx]
    request_page_scroll("kip-theory-stage-anchor")


def render_theory_section() -> None:
    """
    Главный учебный модуль «Теория: Термо-ЭДС. Эффект Зеебека».
    Разделён на три компактных подраздела (Этапы 1–6 последовательно, Самопроверка, Словарь терминов),
    чтобы не выводить весь материал одной длинной страницей.
    """
    st.header("📚 Теория: Термо-ЭДС. Эффект Зеебека")
    st.markdown(
        '<div class="kip-section-intro">'
        '<strong>Теоретический материал для KIP Simulator</strong><br/>'
        '<strong>Основа:</strong> загруженный реферат «Термо-ЭДС. Эффект Зеебека» (17 страниц).<br/>'
        '<strong>Принцип подготовки:</strong> текст сокращён и структурирован для изучения внутри приложения. '
        'Физические положения, формулы, исторические сведения и числовые данные взяты из реферата. '
        'Внешние сведения не добавлялись.'
        '</div>',
        unsafe_allow_html=True,
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

    theory_subtabs = [
        ("Изучение по этапам (1–6)", "📖 Этапы теории (1–6)"),
        ("Самопроверка", "🎯 Проверка: Мифы и Хронология"),
        ("Словарь терминов", "🗂️ Словарь терминов (12)"),
    ]
    cur_subtab = st.session_state.get("theory_subtab", theory_subtabs[0][0])
    valid_keys = [k for k, _ in theory_subtabs]
    if cur_subtab not in valid_keys:
        cur_subtab = valid_keys[0]
        st.session_state["theory_subtab"] = cur_subtab

    st.markdown('<div id="kip-theory-content-anchor" class="kip-scroll-anchor" aria-hidden="true"></div>', unsafe_allow_html=True)
    sub_cols = st.columns(3)
    for s_idx, (sub_key, sub_label) in enumerate(theory_subtabs):
        is_sub_active = (cur_subtab == sub_key)
        with sub_cols[s_idx]:
            if st.button(
                sub_label,
                key=f"theory_subtab_btn_{s_idx}",
                type="primary" if is_sub_active else "secondary",
                use_container_width=True,
            ):
                if not is_sub_active:
                    st.session_state["theory_subtab"] = sub_key
                    st.rerun()

    st.markdown("---")

    # -----------------------------------------------------------------
    # ПОДРАЗДЕЛ 1: ПОСЛЕДОВАТЕЛЬНОЕ ИЗУЧЕНИЕ (ЭТАПЫ 1–6)
    # -----------------------------------------------------------------
    if cur_subtab == "Изучение по этапам (1–6)":
        stage_titles = [s[0] for s in stages_list]
        curr_idx = int(np.clip(int(st.session_state["theory_stage_idx"]), 0, len(stages_list) - 1))
        st.session_state["theory_stage_idx"] = curr_idx
        if st.session_state.get("theory_stage_selectbox") != stage_titles[curr_idx]:
            st.session_state["theory_stage_selectbox"] = stage_titles[curr_idx]

        # Быстрый выбор этапа + наглядный индикатор прогресса (синхронизация через on_change)
        st.selectbox(
            "Переход к этапу изучения:",
            options=stage_titles,
            key="theory_stage_selectbox",
            on_change=_on_theory_stage_select_change,
            args=(stage_titles,),
        )

        st.markdown('<div id="kip-theory-stage-anchor" class="kip-scroll-anchor" aria-hidden="true"></div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="kip-stage-header-card">'
            f'<span class="kip-stage-badge">Текущий этап: {curr_idx + 1} из {len(stages_list)}</span>'
            f'<span class="kip-stage-title-text">{html.escape(stage_titles[curr_idx])}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        def _select_theory_stage(target_idx: int) -> None:
            clamped_idx = int(np.clip(target_idx, 0, len(stages_list) - 1))
            st.session_state["theory_stage_idx"] = clamped_idx
            st.session_state["theory_stage_selectbox"] = stage_titles[clamped_idx]
            request_page_scroll("kip-theory-stage-anchor")

        step_cols = st.columns(len(stages_list))
        for idx_s in range(len(stages_list)):
            is_cur_step = (idx_s == curr_idx)
            btn_label = f"● Этап {idx_s + 1}" if is_cur_step else f"Этап {idx_s + 1}"
            with step_cols[idx_s]:
                st.button(
                    btn_label,
                    key=f"theory_step_pill_btn_{idx_s}",
                    type="primary" if is_cur_step else "secondary",
                    use_container_width=True,
                    on_click=_select_theory_stage,
                    args=(idx_s,),
                )
        st.progress(
            (curr_idx + 1) / len(stages_list),
            text=f"Текущий этап: {curr_idx + 1} из {len(stages_list)}"
        )

        # Разумная ширина текстового блока на широком экране (центрированная читаемая колонка)
        is_mobile_view = (st.session_state.get("chart_display_mode") == "Смартфон (320–430 px)")
        if is_mobile_view:
            with st.container(border=True):
                stages_list[curr_idx][1]()
        else:
            _, read_col, _ = st.columns([0.06, 0.88, 0.06])
            with read_col:
                with st.container(border=True):
                    stages_list[curr_idx][1]()

        # Кнопки перехода назад / вперёд (синхронизация через on_click до отрисовки виджетов)
        nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
        with nav_col1:
            st.button(
                "⬅️ Предыдущий этап",
                key="theory_prev_btn",
                disabled=(curr_idx == 0),
                use_container_width=True,
                on_click=_step_theory_stage,
                args=(-1, stage_titles),
            )
        with nav_col2:
            if st.button("🎯 Проверить знания (Мифы и Хронология)", key="theory_goto_qa_btn", use_container_width=True):
                st.session_state["theory_subtab"] = "Самопроверка"
                request_page_scroll("kip-theory-content-anchor")
                st.rerun()
        with nav_col3:
            st.button(
                "Следующий этап ➡️",
                key="theory_next_btn",
                disabled=(curr_idx == len(stages_list) - 1),
                use_container_width=True,
                on_click=_step_theory_stage,
                args=(1, stage_titles),
            )

    # -----------------------------------------------------------------
    # ПОДРАЗДЕЛ 2: ИНТЕРАКТИВНАЯ ПРОВЕРКА ЗНАНИЙ (ДЕТЕКТОР МИФОВ + ХРОНОЛОГИЯ)
    # -----------------------------------------------------------------
    elif cur_subtab == "Самопроверка":
        stage_titles = [s[0] for s in stages_list]
        render_knowledge_check_hub(stage_titles)

        st.markdown("---")
        with st.expander("📋 Классические контрольные вопросы по реферату (10)", expanded=False):
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
                st.markdown(f"**{q_text}**  \n{a_text}")

        qa_nav1, qa_nav2 = st.columns(2)
        with qa_nav1:
            if st.button("⬅️ Вернуться к этапам теории", key="qa_back_stages_btn", use_container_width=True):
                st.session_state["theory_subtab"] = "Изучение по этапам (1–6)"
                request_page_scroll("kip-theory-content-anchor")
                st.rerun()
        with qa_nav2:
            if st.button("Открыть словарь терминов ➡️", key="qa_goto_glossary_btn", use_container_width=True):
                st.session_state["theory_subtab"] = "Словарь терминов"
                request_page_scroll("kip-theory-content-anchor")
                st.rerun()

    # -----------------------------------------------------------------
    # ПОДРАЗДЕЛ 3: СЛОВАРЬ ТЕРМИНОВ
    # -----------------------------------------------------------------
    else:
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

        search_term = st.text_input("🔍 Поиск по словарю терминов:", value=st.session_state.get("glossary_search", ""), key="glossary_search_input")
        st.session_state["glossary_search"] = search_term
        query_clean = search_term.strip().casefold()
        if not query_clean:
            st.dataframe(
                pd.DataFrame(glossary_data),
                use_container_width=True,
                hide_index=True
            )
        else:
            filtered_glossary = [
                row for row in glossary_data
                if query_clean in row["Термин"].casefold()
                or query_clean in row["Значение по материалу реферата"].casefold()
            ]
            if filtered_glossary:
                st.dataframe(
                    pd.DataFrame(filtered_glossary),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("По вашему запросу ничего не найдено.")

        if st.button("⬅️ Вернуться к этапам теории", key="glossary_back_stages_btn"):
            st.session_state["theory_subtab"] = "Изучение по этапам (1–6)"
            request_page_scroll("kip-theory-content-anchor")
            st.rerun()

    # -----------------------------------------------------------------
    # БЛОК В КОНЦЕ ТЕОРИИ: ИСПОЛЬЗОВАННАЯ ЛИТЕРАТУРА И СКАЧИВАНИЕ DOCX
    # -----------------------------------------------------------------
    st.markdown("---")
    with st.expander("📚 Использованная литература", expanded=False):
        lit_md = "\n".join(
            f"{idx}. {item}" for idx, item in enumerate(THEORY_LITERATURE_LIST, start=1)
        )
        st.markdown(lit_md)

    st.download_button(
        label="📄 Скачать полный реферат (DOCX)",
        data=_get_referat_docx_bytes(),
        file_name="Реферат_Термо-ЭДС_Эффект_Зеебека.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        key="theory_download_referat_docx_btn",
        use_container_width=True,
    )

THEORY_LITERATURE_LIST = [
    "Иоффе А. Ф. Полупроводниковые термоэлементы. — М.; Л.: Изд-во АН СССР, 1960.",
    "Льоцци М. История физики. — М.: Мир, 1970.",
    "Анатычук Л. И. Термоэлементы и термоэлектрические устройства: справочник. — Киев: Наукова думка, 1979.",
    "Бурштейн А. И. Физические основы расчёта полупроводниковых термоэлектрических устройств. — М.: Физматгиз, 1962.",
    "Сгибнев И. В., Копылов А. П. Термоэлектричество // Энергия: экономика, техника, экология. — 2017. — № 12. — С. 31–36.",
    "Преображенский В. П. Теплотехнические измерения и приборы. — М.: Энергия, 1978.",
    "ГОСТ Р 8.585-2001. ГСИ. Термопары. Номинальные статические характеристики преобразования.",
    "ГОСТ 6616-94. Преобразователи термоэлектрические. Общие технические условия.",
]

EMBEDDED_REFERAT_DOCX_B64 = (
    "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"
    "NWsvzB8ayxYnxquVainAlABTAkzZwTDlaqfducZO9Y3uO+xSz6WsobWDTa385m/cn9nGUmsls3bwxDNxKtLawcXa0nG681pt8dBY"
    "fWn/bw9rqxECz/e39fz+3TMayW53Pkd13EV5rHfuds91bmS6b6FA2ly6jvI4xWd/Ga2CHrnDnd/bD+cyLxdf2Zd5OVd4JTVyFL48"
    "qEJKhWx+slQoBxUSVEhQITtYhXwFymx3bpqEcJJBGU74ilTg8j2Ji5Q8CHpFsNrpGlOwz66WTemVb2R1WM7+d7rnhmoVZ6vEiORn"
    "ypdzg2dud89HSkdFXONIgHeZYjcygzMtw4S7hvXzrlRYpnum861uwyTSBF3XeQHdi1AzdhCpf/oOeuy02pbpvg8UutG5ZV+VqAcl"
    "uC9jaXxQczz6tlQejfcFdv9AgehD7vtOt0kbevuqe+5AhsNRWAVc3eA6D+6TJbbR+T7zCx1d0MZM48GbnevYY2fVyvhWOnuxe0HN"
    "pAmZCrk77ren4qd/GVZTQGk2M3K5bJYTL3L5bGqGMEEPa4qmd6EGsbs7xa5ESK7sZggy6apJoKqTNm3JOmTYu4int8QWSTCZWG13"
    "LyF/7HSVbySslM3MSyhJsaF8kh7eMIHrJBZ81I3ON1Tf+brzUefL6HFo8Y1MMS+ZlpB5iElJbCSi0INq1OGt6532XiTw90jf96n2"
    "XudO94yk4m0yqHGTLz4p8nWVn0zym5BVMUZ+cfEtxPM79PdiBol7jz6pNolvtZJfZchcZJAuZzpfmMDX6TIMyqBkpjFqobSLhsNE"
    "f88QYpT/1vkks4efJO9/hew+yy1qyA1pMxatdQ9KTl/3mkKRNuBL923ubHfu7OfPDRqHnhOfp15d7VzufMFwMEz0SuMhbSStya3d"
    "d7vnbaQ636FS9PbsYVp4IKUwhptj+dJUKVsubuF4zLtUHK/W68sv1l9vRaazT1aiy79aWKqLITCT2l9frh2vV5v12qvV+rFGs973"
    "69rCfGNtCmKh2Vg0M2hldXm5WV9ZUVEvrp48Wm/2F/gq59A2Xl21u9cazfnfNWvL9qXxWr15bLGx9pvVpbmWXWk1rEl2oa/i2mqr"
    "cXi5NlefnrFbe99DuNVjDbey0T46tWJ/F/reysJU/9teeTO6hfPY7ZmVN3s3uWsRyNTE9lzVU0DUj7FjshY6H0oCSx5migioT4Uz"
    "TezI0rotSOqEYr8wGmHpF/IFlv7sFnuZCmHpr660Xlo4fqL1wtK8m4ZLteUjjZ83F/xXZMmC8YlHTc5NIl9W3DW8JWNM4tqxVr15"
    "aCxf7H0bvGkRsXdorFC2e/TlpdVFLkg6uVewsDRPWccWmistichDY5Vs2f3y+7lopRxttE64ay3k9OTiwvGlk/WlWGD3CnvCzO5j"
    "XCHP9NIvHsix4q8aHMD0lQyQZhcCupUAHwPGq8iYOxlnkvZEhaDFCEIhX64Wp6cqgZ4NeOCx4oFIaHm4CDLou/IsYYS+rj3uzhpu"
    "+GSoBNhKbiBhnMVzAzvi37oXETiYW8ZHYW5c7Fzn4X5h1PnuoJFVzldklolj4ETWmVXznkyryM6RqUUR9zBublK8s/nEnWGYxdbU"
    "fmc2OvMvIsvkbvpWJpvVhGlm3ktKgYR2EhGcJPvxBmaQJ+Zi6o8fHI+HWYYVJQN3iCnbPQfx6Hxe13jCyEdXnwwsx2LC2SGB1YN1"
    "ao4sRANhXFeh/jGIQW5znCWXf5ah9SIKXfvhDc2SozaVTTmy605ZwTepG/Kcf2xY1KC+29d7RWPAq6a3eJK3ZvX0YkCiYXVmsJpD"
    "dRYDInvRwUrxnqZUaKHLA6IKxQz4saZ9e2jRzSHTqWduY5hiqtP3MyJoXafcizbjlp9udc/wQqESeClu8GV3o9JolnvAmeGd7/bS"
    "EqaEGekY2UlqtkdY3JP9rUgXq0Ut1mx1fXGjoJEeOtnsDdArq56RtVfOzNe0MCLglBWnd5L6rgFSY6nkjlXl5617QfEM655HaX+l"
    "MaVFYo3hHuJJYaSInmNKWFnGr8ASnOHlaU7RBX5j0LTiWHp/oDZ7aJ1yqDgzuARZmVzWDMDtYqMsJoQLZ/S06x3lU65bUQlCxT/T"
    "m6cADLEHbtqe8t2PTQyrQYQ8zAPtTfl61HoaZ4OTCjjS7KYpb9n7XOchpuv7TAeRLswXGwsjZzobo/AVlfx0tcAesc3dx8Fo+X0w"
    "Wh46pi8YLc6U/ClEjHBH8UAe+XeF1S4h5w7BkH670b0kievVjvkBpcUcAkCwjWCalCez07liiF2eDqZJME128s7QpHQA6MRCwHk7"
    "PDZKxpd5f4r8m/syL+3LVNMRzMHDCQ+2+wJLUCdwWslQxdhsc24zgCe2k0wZfR9Av9gd4FiH6eWfi4Mv7BKG50jB9Ga9AX3lpnRG"
    "C6abg8gyci0ARIVT28XuWRF66MJTXI+8hvg1TStG6jKlCcPU3pVTOzUjeiLyOzzLb/WfKIYTWRNW5r/82t8Cum4zeTO58fEytIWk"
    "K75z712+230Hm+smSwf2QqYYBnv3ki0QIpk+YHr+Rf/K6fyfzkw121X8hTnVZaXeplALwnJln8N0th/N1DSDVsZ0FEtsIVK9pSTv"
    "9WAQgSNs9JNfGlo2IpvwwtOey1rIONRpFgEuxjS4nlphxrgY550iCwQtcbwLdcrOZFxcYIOHoKlV5/Bo31FtCAwzaV3FIaiGlbjb"
    "Y+S1+kiOy2pgHmt6avtEahIauyEiKg4mDPI8zBtjRUUUGledUveGCBQsVJWkcvRwOyIzARdiXq+DRYgVTYksbk0hZ0UDxfY1gm89"
    "s8eSImB8pzMf+KAjBCZ8MWVIYci1iMCVmf4HDHVH3jOJUQM90S2Zb3O9b0thCPPWEt/tolHaNpOruMDUcR92mJJ9DNKQ/UDZEqm7"
    "K3l3+lfYkR52pIcd6TtzR/pnZoJ4BYaecO7RBBGMTnJBqz2YbxsIU0IiGLy70+DtwYyE1zvhVDWaxbmF7YZ3MenwiTLP8CkaKkn7"
    "6/cAgRQBjkksgxm+5Vbn8nOEnu8FcH1i0Akb0wgi2chGDqV8FsLw36gIt4UI9z+O1psiicw0ZTuR4Jjc15BQ8nCYyWoUkMxw7R+6"
    "xY+ydeULlu9WntC3DeLpv0Jvd3D9vkvrtWOJSHG8wF3iJRwUGxJwYN7ddEw8D7e11Dw2o9Qes4RlLltZDfsDLb0ggIejWx54v4HJ"
    "8WS3uMF3A6DqdwSoQH05i/V8bhTPbKk8Mz1dndgikjx4ZoNn9uF1W/DMPqhntoDo+wxRwXpHLka7S3pWY/fcwb79KggxBa9ckAwR"
    "Ech3EdlnJbx4DqbRX7HPKUU+HO2XJmYnpyv5LYSED/cP201CzPnJ2pIi6E9MLq0sHBrm8JxbGbzsxMMTjrjUZH96W1CecGctvPRz"
    "lr9Ye4gpUIYDM6D790ywKHhRvL9wmUckho74rG11PJrguaIQ0969Bqu0tcXIL6GnhMQa4LkQal8ipXw0HjhGAs0JKONoiWmTh4N/"
    "AI4pERVsjV1pawxuyUzpuHj35i9lKvzNTe1Y/W3mfBrk/feFuRZYUckiUSCyuyyswKyxU5KPmQnlLOaTF28uSt75IA1gSaQxAz/o"
    "A2Cje57CDES+7XZePjkDe5TIRKl/7uHaNIf5NU1WFG7Maoji+IavhA502gmDQLGdthlNkfLc45kOpvEe0Q7Gl1xXQZl85r/u039E"
    "gOSUhVuB+woEWAcenPYkjkJkWBWSuVepzW/r8AyLlokCHBxrQmtohyVXUQHGchiNQksSm0CgVC5ov7/jaJTwQGBEmWAUTMCGBBoi"
    "+mVLIokiaGzEJBVz4nk8k6Tu0K62dt3jRdOSpvxoy4dncVj3epxa1TS1QXaUbgYf0bTTlCcwZBlm4FwGpITzq6QTfoxCx1Ry2Ymp"
    "iXJu80D5YGkFOubh6ZgnbHzsPkvrK5lRikFqZ36ZQYQhvtyeMRMpiBsjcU2qOfFI9CFC9LMYV5wX64zoQziJDG4jzSW5JYruAnYR"
    "g04yJonjZJU+jJGHLIxRQipZigt2pDHa6hXvpnImoYStEq6wWcjktOSvVUcJqV1CKrQnZgulorLEKAMMle8XY21ktJh6UdibC3WV"
    "o3ZA1Fv/Peutpl/jMqIXE9WC17hEa+D4kf/a5nhKMtlGURFnV6yltHtQaPNLJONVmdqtvYiYnRq0TME84D7vzvBtg+3M/b9TK8CQ"
    "V+dDL+7fTvZVP0YaVAGsPn4UhSWTlmcVXcROPotbU0E0iYJo+OVBpdI2k9m9NNVoIXF6JxoAdiXaUJl/ItJTbh6R9rOPDjRNy4Pr"
    "/lFNoPt/Z7Cl1GRjm1Kz6aWBu387mEABgGoJs0K0a1Zwp4d/LKVTDxy5OS7Exp0mqJLLXxCMpyMAiBgY4h9jwtrKb1u8VaIuQU5N"
    "2w1Dsg50XhwFReXHZ2dmcuXAV4c9R2HP0TAKfgeQ88ZXf4WGUqz7e6ZLvaZSggB5ttzXBOYxXQ4rKIGSMEFTni/lchOOMtdXTBq+"
    "KAMW7JX0kQUtGLQg0yQmAh00lSIk7QW0Sz8xmCuKJInVoHiG3D5dS/MsqMd4/oUpFqbYT5lixSHzSfOMGZW0lAzPQ7uB32RgiAaD"
    "tepZf8qZecmsD9sLJKpNNHaSDgTQaWucef38CpBrL5bGgmZ9aTycRxAZTFGD+FCtNKFtthwm2HXwIllQ2OEE4dczM5OR67KABAf7"
    "rU5MIyKwsFAxp1iLP8IFEqTlltxZN06K7HIpRLUQMaVuQH0mrNgJNTQRdnaVm77PzKArorVtYDhKCkqaUhrZhmi1/ypO3zpqFKd4"
    "xo2eDeu4zSjtiwbXPQTK1TuwsxrotFNeP9qxID2C9EhM3PJ4YuKGuRHmRqQYeoJfwvQuAEQ0VSJBs09WFAMahcumZLLkpHJ2gY83"
    "lcjSQybNiI7FXoenQtzCeSFf4Zsc3vYHA+B1F/wW4wRaH8WgL+cLlampmeLmbpEQpRrcIg/vFglRqg8apao0x5+gjfrgELJA8BOv"
    "AdhRgagSB4pi5agZQ67ChNe751P6St6iwSOoytXyRGlqZmJzGRBco0EGPLwMCK7R5IkAjzahqw9CHb4JHw9XMm1klAnCgrBkH/Hv"
    "2cwv9mWOSHDMCEP0MkSYlOmTPSmZAhx8Cmnmn9BcCscjulMs0icM2GQz/SKLf79Z+4mQZEU6x/QefIIIjdi7qq1WIk16vEBRZ/cU"
    "BwKwIpAd+6nNxqegmH0R/QAEZ/7G8VjDdaUiudxBLn2MgfC6yqB95va+QLvkUQaPpxNZWOgUIJ+fuNtn5DU1K8SvLWuOK1JhoHK3"
    "KS696kZN1ur5T1EqbXPqsTGFs0ss6wuOQJgNQXwCC2xlMpKyLggQUxu4dCMjjz6XbIB9YVGrnO2BOaGfrxtJQtnUpIxQybeWAhcp"
    "FqdoxGuCsoWXwenvvAJUTghZgs2h8HQqwyAtdmeMebx23EzR0u07G0jRLT2ntja1ai0qbgLvtUUPMl+52NsZK/L1xzhK4hX7wy8r"
    "kjfj6T2wKY02HCUXJnOV6WpAySHd5jNx8DOT3ELBNdl311atKw7ypizmTXwOsRv7Fynvw48JHSSXKWdtti+VhAm81wMRB2BK1Sxd"
    "rKAz6WHzbBCuh5AzJ5IFUZte5ibLZ08BuOAlAnHcZyplO+/QKXkeNnwiRsAH0almMITwGT/KOQN1KLigva5C/UqnLlVuySC5osxH"
    "AgYX7RduJuW7PGA6WE73C2IILVmoUl8cpCLDh8UgbfxM6CBNiyqn0hBSFGzXO+WTdrswPmGTOxpSa4P4DX0l6tF8PLTLvgsVKkQw"
    "yhzfto5Z7GL0vj0j8mPv+kjIphoJBwH93Xr8u2wWIDggXynHIv+siHp+8Ocubk3eC3nYomLi8ddWPpAm88N7l3VSqUyZzL9w5pjF"
    "9nJuiJ+fbsmlV66a4Sc88zw6jEPbPlSqeWxZBwgFZIfqZCMq/7owY8kFViDCiNv7VqK1TzWLX5SbVU5bPsq7YCVrm4YkDwJEUdYW"
    "eRyXZwDNVWRrUNaUaqMBlNjPOXTPjOKQ4DyDmUpxYnpzMjI4JAIZ+fBkZHBIPKhDonRAp7CdQT/L/eB0tMu440gQJxRluw0GmEiX"
    "QxLEMoIC4G/6MiYOt78qZQ48yE+Pby4YgpciCIaHFwxPiFmOINbus78+cujJmw9gBbNBHN9jW3sENHosz2ahEcMsiEHB4uGbQIo2"
    "O/kzpQ3WZahYG6h6XDU3yayQSebtIiyNPe64aYNOGY6f/Zz0Glc5FzszfqA0XtoPksvBccsy+p5Avsn9fJvcn9d/Clg+BphklVyj"
    "yG+pINCh0czfxcZFPF2m9mWm92V+riD5zwHcOBHA0EwaN199rFC8UrDLhcI1ywHYqQ2DiiEVtldWPr/LnJmJqZsvudyzkalw2q0E"
    "8RMyoo0qYO83MxTzg5u4ZMcGuqhJbsbDgL2hptEoeR+ovi3jgO9u12RvA/cerreTRo8K5E4sHTNK3CHz3+2VKaM1hlcIu8esLN12"
    "U24YjBlMEH1NLFhSMMN5ULWKyfCb35rXyz7ICA5LY2iN9eikZxgpIyEXzVVBz7/XF/XePDlIhOh8Nowg78pJmkijmDHZCU6Onaxs"
    "cS5bQCsBrQS0cmThZH0lPQzbJouZubkvI1cldExkSypJQEt+ROQsHxP7nVOOpODsRNfvvoOYnAIcqqaxduEP0bHabu88+NKepowt"
    "goIvqFWnXsNc8j6qXYwUgVgKpTEwpONsLYJDABCZJNbW8yfezJFvBNkk0CM7RrNMbhFDUnDDwnKJ+Bl3oRc3Ks+SUCSMjEiawUgO"
    "0qHGO35G8IE5qNi9BGrz6aGT+DRXEu8sx1jnEwvQcdyzY6TVQ35NQVy3dnQ8hwCu32j0DfcpROCi2WC6qDQN/N7Gd6XW9rrPqrIW"
    "4RwTghSgtKPQfOh9ckD1u6HSuDUURy1nt1jUPi+FjFdx9/Bio+DEfD5bLU7OzG7OagW6O+DENEB6kD3mge5+ULq7jGV5BXmgkNie"
    "BSlLVuF2yviaprRTbq9e0B/2pQkGL7t1WDjJZ1IqXlTgYHR+bqpSmJ7aSkIESzJIiIeXEIH3fszR+Vc3AW2KDhCldlvQzfg3sBfQ"
    "x3nW7IoDFIqheVu5y3yw7zqABtrPYR0BRYqx411NMsFuvS8ACK7R+ZQbSfDmEIoejcpUwDMiihJPZzp/5oOAIxVZEi3H2HvJ1e/Z"
    "T4g42TYCZK7WtjUH09n1iarOWp8smIC7FFggcnEIwKX3mwncDYAesE4tV2/xHVLrP64ZsLURiHMaaRSdF/JuD2mKJgRI4mfwWBA2"
    "kdH1fTOpbPCQ4XAuANCii5rWcNxkMNvQlHFAR4yo+UF1QYuqXDwNFzL/z5HMIVp2f/2fZ448949bUKFu8+Y/z6SkfiAJdiVJkIIJ"
    "2HGaQJ4rjyfRvsw/boW5EkgASSdTCJvOkyNhmoRpgmq6Jp2HYXHBdJE2UdjcGWBSUIN/k/bkX+X/ZB9FTCmlBBMmjqOMboudId0A"
    "NxteEc3Ro1aMWRoFTPA8JJNceTRTbscL6U1Sm05waVbxWRZc5J77sUURlkRYEgYBBfYEsKNI9xg7MgcVjAaIVNS4zTAPPF3CTAtE"
    "yXCX81vfkVtaZ8dF2PHGKAxfIV8dn54d3yKgNdjvwX4P9vu29wR/hgjxKcdQhbB50kUSCLK7ZYmbqsWKRz2d4sfrEheybtktI/mT"
    "qS78cPr0kfoPp7FfUYM++oxjH3CRnCL0xXhEbbNRgbiaZdzKDXP4aPwc+dS8Ff0tQslZqGpJ2u7GlJfmT5n/aoz81Go0tyMDUeT4"
    "OFzbN/FsYLOav8iAQsK67Y81oiVY9RKw3Xe659jJOTAUDIP5NbWvOvObo0fqbK2KYoBMLrtH+oAKZalzPJxIlZfMpucSRsI50EKR"
    "JFYUQXuHF35ODT2kQeNc2DF3pZxK3XP0UQqB10TrjRfgu7G1A1QGzQE4XaY2O2bVmmwVR3sdgEZiUBhbHGkaaeIL+dqm7xr5mEvg"
    "JxvCzUnlzNJ+9Xx5P48TWagTPmgi+soNNJFgbIW1zShoLH4RmaJXpSoEjHxMFs39guodbwFe4zcoHQ/duI1BGcIpicfpJ0UompEi"
    "PFK9u0OkFLVbtUJlGnhHfEiV+mTs3OBsWv3K+lBuQXcXbbwUOQUj5WphZoxKYteXmqGUtNq8/67rvratyTGomU+VAq5v20CLi2ei"
    "0PXUC1FTTkXvlV8ZnlF0doUz2GfGZ7eINc87d0I4ljEcy/gQxzIGr9yDeeUIw3bseDuj3ShXtMa9VIh04taiQNJCOu+iSWb3zHcp"
    "g3G4M640PVGuZEshrDPkvw/573dy/vtLgAdhJsCzTH7lTFYcp3EAfBC2EgoXRYbvbCRgwTPiCnhWJSGfVAJADRRjYURJAeWJOUrf"
    "2p2G5aBC1Lj4KCGFfbnduc5r4LgK4T7HV7ycf2Vf5uWy/lN5Ben4ZwCUjJTzNIwuGX0ncamv/tBawTMNhZCc2uoAq4nF7kjnguQK"
    "OQTjzFQyjOnxYqOl1ZMubcXC4muLfb5rfnthPrpm8VNI8/iBldXl5WZ9ZeVXC0v1F1dPHq03V6J7sx7VLSytNF5dNe281mjO/65Z"
    "W7YvjdfqzWOLjbXfrC7NtexKq7GscuxCXym11Vbj8HJtrj49Y7f2vj9C4XloLKszoY/WjzWa9UlqXKHGhaXj/nrtWKvePDSWL9pd"
    "9m3wpkU6cGisULZ79OWl1UUuqL1uPBaWNJqL9WOtQ2OVvN12bKG50lLPuZItu9t+PxeNwNFG64S71qq/3ppcXDi+dLK+1Ip+7pXs"
    "T6NszjaWWnoLJ0JulcEjvDUu2//Mb4uW/xiDTQJGVtpWZj1i6Wpkqsm6FdWRgl/BK747veJvoXvuoIww7I0J8yrOKUGIBHd0ud0A"
    "ho+yVij5nVSYxTdLEcJOKP5XTMgA4SMWw2tBC7oxus5CZOBYepyZSB6xCtoWdlb6MqIRrF7RFVASVoPa0dsD51qsTuBaE8QwpsJu"
    "JXbFVCthJhZuoyBjI0ZEs4keI4+hlagD+IAN4AkxdJzTE93mgISIHI3OWZaR3zbImatKCSTGi0p0m0UC2bfk1jlbmW0qgpyhYPyE"
    "Vgd1uZVLhVuvXIdyGBFjmhjzmNQi+FrVMlDxq1A8DauboulqWN/BHycECt/KPNlgSjiC1a2AYWvV2GdbG0xVrPXTchyzNN6FJqQI"
    "mEGuixVlQbNW5FdmDYxC8GWLhWx+djIf8OqikGIfPg14NeDVf42F1TMKzjfBq6YILduXU4TYv0msysFPSCrbIdWROjdNa54XRcgo"
    "VFT5jTGltUvphsJbei4JoQWxDkrgZV6Yz/hq2bwkvfj/p1TpooDBzsAOoWhpaod+ehrbZKVl9EL7WuyNnEAqnGgdE4R2yDCSEmGr"
    "jBb8qsox612LN4BR8v6pHbGvKtVpK+d7oQRuMMrAPq0HJR6vi92bGo9QaObUAPw2yBobgD43BFPYRZcxi/o8r5mXC6+MoqxzpcrE"
    "RDUo6+T+BFEogVwK5JIdvfDsnr8ACeIpwtbzPcYoHaKKdezE0WZBGyjwK1i7F5FAiQy4qF6zIWSbYsOaNvQxIhZsYpozdWxGghzY"
    "ULZb2xESme7fYoqg+kl+r73OtMnof5N+0uDmZRBJkNjDDdMBgnCbQrCZLeemNvSIhceedyS/Kf/zpo5R36bkFfhgZy2634wEcPsR"
    "73CfCy0RBSd7CKvJaf7bqkmmvX4RhoFCELD5cH8us4dD6x0JJ8pDIRfslEa+20ENiHnuFjABXty/reAemVzk6rFB87Y+wEJUBd0W"
    "55HJTRSz+6UP3DmYhjH8LcZmUABa4T3TIbq/8wG9+Cv/fkxttsdJ42pZVgVCBF1AK4p5sQBNmuM7Z1YgDY0Azl0jVr4jq5A/e03+"
    "lT/wsAtPOZ8CQ6qA5hIPo2HpS8fAnMDgBEAZ56JtQ1c6H+Ez8W2+l8lzAq00WIaEYHSQYY0jU6BF6NPAeOvlKhWS3ogje4x/8SUL"
    "w/XSN42TuymXdVX8jNeqwbSWCI3xfnxuqOGD1DdTbB7Qxmvdf+NZkWW0l6mniRaXqenABQCrTRAdM2HJKnS2htaIbtRKsWxOnXXN"
    "OpsIsEvi3W5pIOnZWwEhJmTWLk2erBnETBfHI3nibJPvjRd0IpYbtnB8brZ49nS+QEBc7Xzd+VCnRSBQnHDSupGok6DV5BZfSsUC"
    "qHfMAENqaJkzX7WLmxQSrGs3yyX3iNRMNLhtC0TBep6aTfaABfAzlchNVLDZGvciy7GrauKQ4EJWnuq2VsBrWXdireHFFbYckvky"
    "BSipGxsw1M/7I53rWJqZKOWnxlPnOgaHbMDMB4NDthkwcy/Q2QDxkJhy1PtnkpjJ6GDE3RXwAygWjHBe0k+STWjU8LPQjd+oDvRh"
    "L5pJN4E3YUTkvkgpoUgpBucvk4w26oubhEulEwyuiuo3oOkkOsBKpQ+0U0g7BdFpjZfaJvyRsPKxCS8Z5jEYLfxEEwwoRjiXvjgg"
    "dI1KELJ0/7Jwnf75QnpDrQMOW1dAO6BPHpDzAcbN0RpCRpZOtteVZNOSQ263DR+NtiT+p2oExelk4Hv3bxsuc9Ca0dERSODrUtmD"
    "a+2GRxMq0lzPwDpaiDojbaOrr39RUDYDPSLfkh+fLcwUyyndsXy49cZiPQrgCNHPYcfSw+9YMq/T0akV+/toj8NU9O7TO9XoMXbM"
    "vBZ/NvypXb5QHwZ1b6SsLvV+MJFQfqIwnSuUK0mfZ3pZh42IYVk//LKOlIR3K7PA+648S0u9r2uPu7O2/L/uZQHqy9WDFSlbm/gK"
    "7GEglIgZwMJ4PheDBW4xJqf7Hgwj0EIoxgKHeTAjKxncJiQB+WV/Be+EV/hDfnsuyoymVNnafmcjVjalGqyyxDeCdAKCyYPHYPsA"
    "dpQrIlHYjJZBham9HkJ6+MhtoheFppzfCNioNgg4WpAW0OwKn3Gggo/USkOk3AONJyxpAFI9MLrQs4BmgtN827Emidm9SD4kCzZL"
    "DaHAnOpS42EygaA625VmiiojqLt7gVa3QYOnwWmqm3oArXF3XdAYMZD3eVbNUW7K9xR6/TXvRNAW7OkqUWbxXgXJ0RGis9donY4y"
    "kKeAbg9N+uQNDAgVatRuQvOJ47B2JmLp+MHTCvaSrCl9LrlRnHHFyanpHP8PWsRp+YX5fnFWmw9aJGiRbb+d/WokvOLTrJ30cMyp"
    "k3GYkDf3S8xKWG9I7SBa2D8uyWbChIsmgBFrCHTJY+fB4AHTJ2aVKmKPG0yLSPTLR8MNSYeCrxRCN0kTSO6zeR7Bxu03dGjkuqQ9"
    "lSq+1yS+80vIoJcauCjJjCjVtnCnQkzmip4gfNe0khfaPtNbCjbD2z+7ntRwkv2mJ9kzJz3PlciCqKmXggaWCfEy8whPoSYRUyxN"
    "j/k51keRMeuu2jQWqvFTljRKsfeZBSU0wfQVLYYXWJ5lolu5joMAKOAn7BbuEjl5UxtZjTlb5xoLkjodI2awSrBCC5cwWf6Cgty6"
    "+MRWT5R6fqQt8qVqeSo3WQ47YR/hZq7BrVmPcv9W2LI1lvcMx8qbPaPUXYsCTZ4ucfQ0rMnLyAhtJ0WDm1jwVLh3g0pzIzmktmOO"
    "XJaekeoILMRg0kXQDgo1eP97GgsVJkQod8rH0lJ9oExqUCgwhm/ymBt8k0Hti/FIzRRVr+SUNexDUgj6wURnOvd8Ic7zZEob5oIf"
    "ybkuLOty+lKcixUwr5OsdL+nS7Z+5KOKfzMHERDUaAQREJZBQvC3z4ymdKW6cZhWeNWilbR+DIKqt+jg/UNuYIAsUkGVhJUUVpKJ"
    "WUWMnWKliP2yObTZ0SvmZY2WnGa5xc9pJXlOjZl7lkkILBSK1brTHP2OuSrTT35dfz7m/vjHaOomZ6bjr37kkMLUwj6vCZ9aOlIc"
    "Q5aOBcLINrT2bHXgAl1ISQjnH/bcp2xEGZie2nQ7QenTFiBaaH8gYA+RwWWEwibO2s4dJJvYSJGheIJlsEo+IOro3LAKTZPirnXG"
    "rzJ22b4R2QASfLwKantfgknmNPaCTN3u6R4RmeI3ud3doqFoyzUcs7T0lSH4M+84zuTO3WSvlBmN9jZr3Vpz16xzyhmF/ivkJ7LT"
    "+UoqM9bjjSt6deckYwj4PXmUn+NHnzCkjfB75AJdqc+1nCP4WKNBLoyX6sfqzfrSXD3TPLgwf2is+cJ8QQk0Wm8sk8pivn6strrY"
    "cvshl48ffpNf1g6N5XIT5Ljg8wk+l8cL3opYPv7rWlPPNpZ1D5f50lw4foI0GbnxrEvM0Wi1Gid7P7skGtHNJ+q1eeXniJJqWBPj"
    "r8dXW5a9wzvSlo+TreQI7aSWYyepY74+t3CytqhaV1q1pmp1LZ9rLMrnplQgys/hMnaQ/yS+Yb4x9/PmgiX1UPKShdYcPfMJQOZO"
    "1Jq2s8RvDGUko0Hk49HG/BvPC5pQxKpyejz//wNQSwMECgAAAAAAh07iQAAAAAAAAAAAAAAAAAoAAABjdXN0b21YbWwvUEsDBBQA"
    "AAAIAIdO4kAU1AOQwQAAAFQBAAATAAAAY3VzdG9tWG1sL2l0ZW0xLnhtbJ2QwWqDQBCG74W+wzL3umohBHHNobbQW2jSc1jWNQpx"
    "ZnHGat6+giS1h146x5n/+5iZfDd1F/Xle24JDSRRDMqjo6rFs4HP49vTFhSLxcpeCL2Bq2fYFY8POWduYKGutGLVLEE20IiETOtx"
    "HKMxcORQU123zpfkhs6j6DROnvU8ermjsLDZP+kiX7Y4eCf7ngL/bugi138FmvA6yU++Ce9Yk+LQVgZOUzzXiZM43YASP8kHiZX5"
    "/gRWzptCr59RfANQSwMEFAAAAAgAh07iQGNDe0XlAAAARwEAABgAAABjdXN0b21YbWwvaXRlbVByb3BzMS54bWxlj1FrgzAUhd8H"
    "+w9y3zVG69RiLLRO6OvYYK8hXtuAScTE2jH23xc3GHR9upx7uN85t9pd1RBccLLSaAY0iiFALUwn9YnB22sbFhBYx3XHB6ORwQda"
    "2NWPD1Vntx133Doz4dGhCvxC+nlsGHzuaZnnbd6ESZztw01c0LCk6SFMi2ZDn/Msa8vkCwKfrT3GMjg7N24JseKMitvIjKi92ZtJ"
    "cefldCKm76XAxohZoXYkieMnImYfr97VAPXa5/f6BXt7K9dq8yT/UpZliZbRRkLfU2lKvHX4ATf+PyB1Rf6xV33ze/0NUEsDBBQA"
    "AAAIAIdO4kAMpHVCqAQAAOoqAAASAAAAd29yZC9udW1iZXJpbmcueG1s7VrdbuI4FL5fad8BReKyhAAFBg0dtXS66mo0Wu10tNcm"
    "mGJNbEe2Q6ZzOS+zj7CPNa+wx3ZiEqDsEGhFtNw0tc+Pjz//5Hw5vH33lUaNJRaScDb2glbba2AW8hlhj2Pv88PdxdBrSIXYDEWc"
    "4bH3hKX37urXX96mI5bQKRag2AAfTI7SOBx7C6Xike/LcIEpki1KQsEln6tWyKnP53MSYj/lYuZ32kHb/BcLHmIpwc8EsSWSXuaO"
    "bnrjMWYw1pwLipRscfHoUyS+JPEFeI+RIlMSEfUEvtv93A0fe4lgoyygCxeQNhnZgLJHbiE2ZrFlXGt5y8OEYqbMiL7AEcTAmVyQ"
    "eDWNqt5gios8pOWuSSxplOulcdDbGM9N+WfW4FagFJZi5XDD3RYwZtaIRhYHvb6rVV33GLR3TSZbEe3CxfAzIZTHzCOhiDDnpho0"
    "RXDhSByyv38TPIldODE5zNs9++J86ZO5R2Ttvjl5xanJvRxsHN1PCxRjF04sJ4lUnN4ihZzfNE1baSxbIcvugcLhCbo+iFZGXoOG"
    "o/tHxgWaRjC3NOg19N72ruDeQVOpBArVx4Q2Sq372dhrGxUmyQxkSxSNvev37+9urnu3nq+NaRIp8gEvcfTwFONcx/RGutdqKRpH"
    "uaxsHy21gMBDjwX/Kjj+cOqXEKUdG25LoXLjwPqDq/KOus5pEkVYWQk4esBfnejH939c/+9h7iXC80w9/kPoWSjAIHuWdKARc1jK"
    "Qaet3fgrTcI0INqRlUJjgdijuea7/Vw7cy/sKOKOMyVBE8mQwG799ESnHO4aML0GhIsdIQyaiQ3M8htoGfhdJMYpRAQz1qEXgQyO"
    "DyQ/BoxBr5cjkyNexNGIqwA54YkgWDQ+4rSA5lqvhrTYVQHXzvFx/fH972Mg2wncntuGrBFXQfYv2NA6d4HXr9ulpT6N6qqjAqbd"
    "08V0ONy1WztavBemC8LgtpjhOYJLU5tm98AKv5cCuXeyIMNduQtkI64JyJcnC3Kv694a224HI64JyMBDjp8jHOUKvmzvfLkZcU1A"
    "HpwuyIOd77lLLa4JyPAh4ER3cr+388VnxCcLMmTEBUKjM+NCE6IutDS/CTb4TX8SDG9uupX5Tdm+mJb/b/jNc4nOmfAA1S0Qx/0J"
    "z3PIFomNPpqWT671nhnQPiT9OahfPls/U6ICpVzt5hLwB/POMyV6BZDPlOgVQD5TolcA+UyJXgHkMyV6EZD3pESdTUp0Nxn2O8HA"
    "fqnev+TTL9kfgxLNcEgoyqpLMpnPIU0w5REZoxC7L+rFUlAzaLn+HaWgYn5uCJuu8UwWSMCHbtOeEyHVB6JLhOW2U7KVomdqP+W0"
    "0qq+QCmnGkDNzglipEm7LZg9EIqlrvI0/uQUQSXaMZ0tEp0hrnev1yeGdkfIbxNdlrP1NdMHR2bHolStA1VelGb3BNflP/duVR5z"
    "CEzNXh2RqkpGDkSqeVlHsKqSisPBavbriFdVfnAUvJqDOkJWNds/FmTNYR1Rq5q+HxG15pt6ALeZksNPmiAFgb+rqkSpVOHyE52y"
    "gDlo6uJGycxm7lvN8iL7NrOuSfi3mpnfW+Wj2af9jerVv1BLAwQUAAAACACHTuJAA98jffUCAAAUDAAAEgAAAHdvcmQvZm9udFRh"
    "YmxlLnhtbNWW326bMBTG7yftHZDvWwwhDY1KqzZrpN30Yu20a4eYxBq2kU2a5Rl2Ne099gLT3ma72Fvs2AbyD6amajeVKBEc7A/7"
    "x/nOydnFJ55791RpJkWCgmOMPCpSOWVilqD3d+OjGHm6JGJKciloglZUo4vz16/OlsNMilJ7MF/oIU8TNC/LYuj7Op1TTvSxLKiA"
    "m5lUnJRwqWY+J+rjojhKJS9IySYsZ+XKDzE+QZWMeoiKzDKW0jcyXXAqSjvfVzQHRSn0nBW6Vls+RG0p1bRQMqVaw5557vQ4YaKR"
    "CaI9Ic5SJbXMymPYjO9W5BspmB5ge8Zz5PF0+HYmpCKTHNgtgwidV+C85VAQDsE7xqn2bujSeyc5EXZAQYTUNIAx9yRPEA7hc4J7"
    "uI8j+IZwFiHfKKVzojQt64GjkQtnhLN8VUeV1bXjC1am8zo+pRlZ5KWbotkM4gs9wQm6xhiH1+MxcpEgQSOIDOL+VRUJYU3uOK0i"
    "vSYCCQTrsjqRGRM4HYiAzhgOEzTP9F0G7QH59e3zzx9fLQeSlzcAqV7wLeO3C+HWu48oAEQY0AT1xw3cQRSfuPA2IrIoZaW7Seie"
    "KGZenbu1ichsAo7eGhGOseFmtw8YG0RBHWlFBBMMpaCCBoiMhjnMM7sQVSAMun/CoTNT7EohH9cYwjh2b9jlToPBeNzm1xNiuIS3"
    "k3cY5gqyIbLGMeYJOwzjMEMibhlGL5nWLenQieH/GmYkF4pRZWpIB4wB2OLUYjDVIzoIBpdTqmrTbZrjYBpRnSbrpHiG8vH7+5dH"
    "l49TSJrHlI/DGcXGOeHVRontxaPxYDS+rGzSMAqewTgfoNOZDq9b86VvXb3148ywU0px6MLb5ukopZ3ZUj9nXUJ2Ig2Jpra2lhBL"
    "FKYaHddsGp2/VNIRydlEsVYOIR7bbmvLBzjouYsINIL9rhtGgwO7Lvyf2um6DwFxu+IT2V5M+0AhgN0HeAD+COFq0J4PtmftFtOX"
    "lQ9P5IyXSKL6s6HP/wBQSwMECgAAAAAAh07iQAAAAAAAAAAAAAAAAAYAAABfcmVscy9QSwMEFAAAAAgAh07iQAEiIh/9AAAA4QIA"
    "AAsAAABfcmVscy8ucmVsc62S3UoDMRCF7wXfIcx9N9sqItJsb0TonUh9gCGZ3Q3d/JBMtX17g3+4sK698HIyZ858c8h6c3SDeKGU"
    "bfAKllUNgrwOxvpOwfPuYXELIjN6g0PwpOBEGTbN5cX6iQbkMpR7G7MoLj4r6JnjnZRZ9+QwVyGSL502JIdcytTJiHqPHclVXd/I"
    "9NMDmpGn2BoFaWuuQexOsWz+2zu0rdV0H/TBkeeJFXKsKM6YOmIFryEZaT4Hq4IMcppmdT7N75dKR4wGGaUOiRYxlZwS25LsN1Bh"
    "eSzP+V0xB7Q8H2h8/FQ8dGTyhsw8EsY4R3T1n0T6kDm4eZ4PzReSHH3M5g1QSwMECgAAAAAAh07iQAAAAAAAAAAAAAAAABAAAABj"
    "dXN0b21YbWwvX3JlbHMvUEsDBBQAAAAIAIdO4kB0Pzl6vAAAACgBAAAeAAAAY3VzdG9tWG1sL19yZWxzL2l0ZW0xLnhtbC5yZWxz"
    "hc/BigIxDAbgu+A7lNydzngQkel4WRa8ibjgtXQyM8VpU5oo+vYWTyss7DEJ+f6k3T/CrO6Y2VM00FQ1KIyOeh9HAz/n79UWFIuN"
    "vZ0pooEnMuy75aI94WylLPHkE6uiRDYwiaSd1uwmDJYrShjLZKAcrJQyjzpZd7Uj6nVdb3T+bUD3YapDbyAf+gbU+ZlK8v82DYN3"
    "+EXuFjDKHxHa3VgoXMJ8zJS4yDaPKAa8YHi3mqrcC7pr9cd/3QtQSwMECgAAAAAAh07iQAAAAAAAAAAAAAAAAAsAAAB3b3JkL19y"
    "ZWxzL1BLAwQUAAAACACHTuJAEr2FzxkBAAA7BAAAHAAAAHdvcmQvX3JlbHMvZG9jdW1lbnQueG1sLnJlbHOtk01LxDAQhu+C/yHk"
    "btOuuopsuhcR9ioVvGbT6Qc2SUmmYv+9Q2XbXVjqJZfATMj7PpmP3f7HdOwbfGidlTxLUs7Aale2tpb8o3i7e+YsoLKl6pwFyUcI"
    "fJ/f3uzeoVNIj0LT9oGRig2SN4j9ixBBN2BUSFwPlm4q541CCn0teqW/VA1ik6Zb4c81eH6hyQ6l5P5QPnFWjD05/6/tqqrV8Or0"
    "YMDiFQtROYuFOnZAosrXgJLPqYRIubgOsY0JYQdzBE8FXiDm1BrEY0wIPQR05pO+PFciScScFS2CydZoHmLSIM3LWU+mUEznKsN9"
    "TIbKOQS/lOMvXvXfxPQPgEhDERaCU2atDVlUBBw72u95IsIUn+zFxcrnv1BLAwQUAAAACACHTuJASou1PYQBAACdBgAAEwAAAFtD"
    "b250ZW50X1R5cGVzXS54bWy1lTtPwzAUhXck/kPkFSVuGRBCTTvwGKFDkViNc9Na+CX7prT/npu0zdBGfRBYIiXOOefT8XUymqyM"
    "TpYQonI2Z8NswBKw0hXKznP2PntJ71kSUdhCaGchZ2uIbDK+vhrN1h5iQmobc7ZA9A+cR7kAI2LmPFhaKV0wAuk2zLkX8kvMgd8O"
    "BndcOotgMcXag41HT1CKSmPyvKLHGxKSs+Rx814dlTPhvVZSIIHyepV36gLoeES4tMUeXboly0jZmMeF8vFmm/BG1QRVQDIVAV+F"
    "IQ4uq4jOfBjNFYKZBufjMDvO2xHrylJJKJysDFWRtaa1HwRUcJSBdE0wp1Z6Z0NdewFF6i/Lli7A5eG7vmv1xYlN9ZdndpZ9Zvi3"
    "CwVv96nvPtduVLOEGOmIGZ21zkYoe2zsGo6STsRMfOpf9L7XwQFIa30GhEMI/We+A6E2PplvK/MJgerrPQgHBK31SYgIiIQQ/55h"
    "53waAdca/gOg8T0Zj/SxB95c+89CY7OL5M3PZfwDUEsBAhQAFAAAAAgAh07iQEqLtT2EAQAAnQYAABMAAAAAAAAAAQAgAAAAg5gA"
    "AFtDb250ZW50X1R5cGVzXS54bWxQSwECFAAKAAAAAACHTuJAAAAAAAAAAAAAAAAABgAAAAAAAAAAABAAAACXlAAAX3JlbHMvUEsB"
    "AhQAFAAAAAgAh07iQAEiIh/9AAAA4QIAAAsAAAAAAAAAAQAgAAAAu5QAAF9yZWxzLy5yZWxzUEsBAhQACgAAAAAAh07iQAAAAAAA"
    "AAAAAAAAAAoAAAAAAAAAAAAQAAAAZYoAAGN1c3RvbVhtbC9QSwECFAAKAAAAAACHTuJAAAAAAAAAAAAAAAAAEAAAAAAAAAAAABAA"
    "AADhlQAAY3VzdG9tWG1sL19yZWxzL1BLAQIUABQAAAAIAIdO4kB0Pzl6vAAAACgBAAAeAAAAAAAAAAEAIAAAAA+WAABjdXN0b21Y"
    "bWwvX3JlbHMvaXRlbTEueG1sLnJlbHNQSwECFAAUAAAACACHTuJAFNQDkMEAAABUAQAAEwAAAAAAAAABACAAAACNigAAY3VzdG9t"
    "WG1sL2l0ZW0xLnhtbFBLAQIUABQAAAAIAIdO4kBjQ3tF5QAAAEcBAAAYAAAAAAAAAAEAIAAAAH+LAABjdXN0b21YbWwvaXRlbVBy"
    "b3BzMS54bWxQSwECFAAKAAAAAACHTuJAAAAAAAAAAAAAAAAACQAAAAAAAAAAABAAAAAAAAAAZG9jUHJvcHMvUEsBAhQAFAAAAAgA"
    "h07iQDISfzZeAQAAcgIAABAAAAAAAAAAAQAgAAAAJwAAAGRvY1Byb3BzL2FwcC54bWxQSwECFAAUAAAACACHTuJAuc7ja10BAABu"
    "AgAAEQAAAAAAAAABACAAAACzAQAAZG9jUHJvcHMvY29yZS54bWxQSwECFAAUAAAACACHTuJApuqX4ZUBAADyAgAAEwAAAAAAAAAB"
    "ACAAAAA/AwAAZG9jUHJvcHMvY3VzdG9tLnhtbFBLAQIUAAoAAAAAAIdO4kAAAAAAAAAAAAAAAAAFAAAAAAAAAAAAEAAAAAUFAAB3"
    "b3JkL1BLAQIUAAoAAAAAAIdO4kAAAAAAAAAAAAAAAAALAAAAAAAAAAAAEAAAAAeXAAB3b3JkL19yZWxzL1BLAQIUABQAAAAIAIdO"
    "4kASvYXPGQEAADsEAAAcAAAAAAAAAAEAIAAAADCXAAB3b3JkL19yZWxzL2RvY3VtZW50LnhtbC5yZWxzUEsBAhQAFAAAAAgAh07i"
    "QMZb7T3uYwAAXIcDABEAAAAAAAAAAQAgAAAASCYAAHdvcmQvZG9jdW1lbnQueG1sUEsBAhQAFAAAAAgAh07iQAPfI331AgAAFAwA"
    "ABIAAAAAAAAAAQAgAAAAcpEAAHdvcmQvZm9udFRhYmxlLnhtbFBLAQIUABQAAAAIAIdO4kCAX01ynw0AADsbAAAQAAAAAAAAAAEA"
    "IAAAABwSAAB3b3JkL2Zvb3RlcjEueG1sUEsBAhQAFAAAAAgAh07iQAykdUKoBAAA6ioAABIAAAAAAAAAAQAgAAAAmowAAHdvcmQv"
    "bnVtYmVyaW5nLnhtbFBLAQIUABQAAAAIAIdO4kApHSknWQQAAJQKAAARAAAAAAAAAAEAIAAAAJQNAAB3b3JkL3NldHRpbmdzLnht"
    "bFBLAQIUABQAAAAIAIdO4kAA2vG2PwgAABpFAAAPAAAAAAAAAAEAIAAAACgFAAB3b3JkL3N0eWxlcy54bWxQSwECFAAKAAAAAACH"
    "TuJAAAAAAAAAAAAAAAAACwAAAAAAAAAAABAAAADpHwAAd29yZC90aGVtZS9QSwECFAAUAAAACACHTuJA4XVZ7QMGAAC5GAAAFQAA"
    "AAAAAAABACAAAAASIAAAd29yZC90aGVtZS90aGVtZTEueG1sUEsFBgAAAAAXABcAlwUAADiaAAAAAA=="
)


def _get_referat_docx_bytes() -> bytes:
    """Возвращает байты DOCX-файла реферата (сначала ищет файл на диске, иначе использует встроенную копию)."""
    for candidate_rel in (
        "assets/Реферат_Термо-ЭДС_Эффект_Зеебека.docx",
        "assets/Документ DOCX (5) 2.docx",
        "Документ DOCX (5) 2.docx",
    ):
        found = resolve_asset_path(candidate_rel)
        if found is not None:
            return found.read_bytes()
    return base64.b64decode(EMBEDDED_REFERAT_DOCX_B64)


# =====================================================================
# 10. МОДУЛЬ ПОДБОРА ТЕРМОПАРЫ ПО УСЛОВИЯМ ЭКСПЛУАТАЦИИ
# =====================================================================

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


CHANNEL_PURPOSE_OPTIONS = [
    "Универсальный технологический контроль (погружной в защитной гильзе)",
    "Погружной контроль потока технологической среды (нефть / фракции / газ)",
    "Контактное измерение наружной поверхности труб змеевика (tube-skin)",
    "Многоточечный температурный профиль аппарата (колонна / слои катализатора реактора)",
    "Контроль дымовых / уходящих газов в газоходе и конвективной зоне",
]


def evaluate_thermocouple_selection(
    t_min: float,
    t_max: float,
    environment: str,
    priority: str,
    channel_purpose: str = CHANNEL_PURPOSE_OPTIONS[0],
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

        # Учёт назначения измерительного канала (п. 7 требований нефтепереработки)
        if channel_purpose == "Контактное измерение наружной поверхности труб змеевика (tube-skin)":
            if code == "N":
                score += 14.0
                reasons.append(
                    "назначение канала tube-skin (наружная поверхность труб змеевика печи): сплав нихросил–нисил (тип N) "
                    "устойчив к длительному высокотемпературному окислению и дрейфу в топке/радиантной зоне"
                )
            elif code == "K":
                score += 10.0
                reasons.append(
                    "назначение канала tube-skin: широко применяется в специализированных поверхностных сборках "
                    "(типа WIKA TC59 / ABB SensyTemp с приварной пластиной или защитным экраном от прямого факела)"
                )
            elif code in ("S", "R", "B"):
                score -= 22.0
        elif channel_purpose == "Многоточечный температурный профиль аппарата (колонна / слои катализатора реактора)":
            if code in ("N", "K"):
                score += 11.0
                reasons.append(
                    "назначение канала — многоточечный профиль по высоте аппарата: допускает компактное кабельное "
                    "исполнение с минеральной изоляцией (MI-кабель, многозонные сборки типа WIKA TC95 / Endress+Hauser iTHERM MultiSens)"
                )
            elif code == "E":
                score += 5.0
            elif code in ("S", "R", "B"):
                score -= 18.0
        elif channel_purpose == "Погружной контроль потока технологической среды (нефть / фракции / газ)":
            if code in ("K", "N"):
                score += 8.0
                reasons.append(
                    "назначение канала — погружной контроль потока в защитной гильзе (термокармане): "
                    "обеспечивает механическую прочность и стабильность показаний в технологическом трубопроводе"
                )
        elif channel_purpose == "Контроль дымовых / уходящих газов в газоходе и конвективной зоне":
            if code in ("K", "N"):
                score += 9.0
                reasons.append(
                    "назначение канала — контроль дымовых газов в газоходе: жаростойкая пара в защитном чехле, "
                    "устойчивая к продуктам сгорания топлива"
                )

    scored.sort(key=lambda item: item[0], reverse=True)
    _, best_code, best_reasons = scored[0]
    primary_spec = SELECTOR_TC_SPECS[best_code]

    # Дополнительные инженерные предупреждения по назначению измерительного канала
    if channel_purpose == "Контактное измерение наружной поверхности труб змеевика (tube-skin)":
        status_code = "conditional"
        warnings_list.append(
            "НАЗНАЧЕНИЕ КАНАЛА — ПОВЕРХНОСТЬ ТРУБ ЗМЕЕВИКА (TUBE-SKIN): запрещено переносить диапазон нагрева "
            "продукта (350–400 °C) на стенку трубы — температура металла змеевика значительно выше температуры нефти "
            "и зависит от теплового потока и коксования. Требуется специализированная поверхностная термопара "
            "с приварной/прижимной контактной площадкой и тепловым экраном от излучения факела (например, WIKA TC59 / ABB SensyTemp)."
        )
    elif channel_purpose == "Многоточечный температурный профиль аппарата (колонна / слои катализатора реактора)":
        if environment in ("восстановительная", "среда с пониженным содержанием кислорода") or t_max >= 350.0:
            status_code = "conditional"
        warnings_list.append(
            "НАЗНАЧЕНИЕ КАНАЛА — МНОГОТОЧЕЧНЫЙ ПРОФИЛЬ АППАРАТА: один датчик не отражает распределение температур "
            "по высоте колонны или слоям катализатора. Необходимо многозонное измерение (многоточечные сборки "
            "в защитной гильзе / термокармане) с проверкой герметичности, давления, состава среды (H₂, H₂S) "
            "и резервированием критических каналов."
        )

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


# ---------------------------------------------------------------------
# 10.1. БАЗА ПРОИЗВОДСТВЕННЫХ ПРИМЕНЕНИЙ И УСЛОВНЫЕ SVG-СХЕМЫ ОБОРУДОВАНИЯ
# ---------------------------------------------------------------------
def get_equipment_svg(icon_key: str) -> str:
    """Возвращает компактную векторную схему промышленного оборудования (SVG, без внешних зависимостей)."""
    svgs = {
        "heat_furnace": (
            '<svg viewBox="0 0 120 72" width="120" height="72" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="10" y="14" width="84" height="48" rx="4" fill="#1b2230" stroke="#9aa5b1" stroke-width="2"/>'
            '<rect x="20" y="24" width="64" height="28" rx="2" fill="#2b1d1a" stroke="#ff6b35" stroke-width="1.5"/>'
            '<rect x="34" y="34" width="36" height="12" rx="2" fill="#ff9f1c" opacity="0.85"/>'
            '<line x1="108" y1="30" x2="74" y2="30" stroke="#00b4d8" stroke-width="3"/>'
            '<circle cx="74" cy="30" r="3.5" fill="#ff4d4d"/>'
            '<rect x="103" y="25" width="10" height="10" rx="2" fill="#4cc9f0"/>'
            '</svg>'
        ),
        "rotary_kiln": (
            '<svg viewBox="0 0 120 72" width="120" height="72" xmlns="http://www.w3.org/2000/svg">'
            '<g transform="rotate(-7 60 36)">'
            '<rect x="14" y="24" width="90" height="22" rx="3" fill="#232c3d" stroke="#adb5bd" stroke-width="2"/>'
            '<rect x="64" y="26" width="38" height="18" fill="#ff6b35" opacity="0.45"/>'
            '<line x1="36" y1="22" x2="36" y2="48" stroke="#e0e6ed" stroke-width="2.5"/>'
            '<line x1="82" y1="22" x2="82" y2="48" stroke="#e0e6ed" stroke-width="2.5"/>'
            '</g>'
            '<line x1="84" y1="8" x2="84" y2="28" stroke="#00b4d8" stroke-width="2.5"/>'
            '<circle cx="84" cy="28" r="3.5" fill="#ff4d4d"/>'
            '<polygon points="30,58 42,58 36,48" fill="#6c757d"/>'
            '<polygon points="78,52 90,52 84,42" fill="#6c757d"/>'
            '</svg>'
        ),
        "extruder": (
            '<svg viewBox="0 0 120 72" width="120" height="72" xmlns="http://www.w3.org/2000/svg">'
            '<polygon points="18,12 38,12 32,30 24,30" fill="#2b3a4a" stroke="#adb5bd" stroke-width="1.5"/>'
            '<rect x="16" y="30" width="76" height="18" rx="2" fill="#1f2937" stroke="#adb5bd" stroke-width="2"/>'
            '<path d="M22,39 Q28,32 34,39 T46,39 T58,39 T70,39 T82,39" fill="none" stroke="#ff9f1c" stroke-width="2"/>'
            '<polygon points="92,32 108,36 108,42 92,46" fill="#4cc9f0" opacity="0.8"/>'
            '<line x1="56" y1="14" x2="56" y2="33" stroke="#00b4d8" stroke-width="2.5"/>'
            '<circle cx="56" cy="33" r="3" fill="#ff4d4d"/>'
            '<line x1="78" y1="14" x2="78" y2="33" stroke="#00b4d8" stroke-width="2.5"/>'
            '<circle cx="78" cy="33" r="3" fill="#ff4d4d"/>'
            '</svg>'
        ),
        "freezer": (
            '<svg viewBox="0 0 120 72" width="120" height="72" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="16" y="12" width="80" height="48" rx="4" fill="#132232" stroke="#4cc9f0" stroke-width="2"/>'
            '<rect x="24" y="19" width="64" height="10" rx="2" fill="#1d3557" stroke="#90e0ef" stroke-width="1"/>'
            '<line x1="36" y1="42" x2="50" y2="42" stroke="#90e0ef" stroke-width="1.5"/>'
            '<line x1="43" y1="35" x2="43" y2="49" stroke="#90e0ef" stroke-width="1.5"/>'
            '<line x1="108" y1="38" x2="78" y2="38" stroke="#f77f00" stroke-width="2.5"/>'
            '<circle cx="78" cy="38" r="3.5" fill="#4cc9f0"/>'
            '<rect x="103" y="33" width="9" height="10" rx="2" fill="#80ed99"/>'
            '</svg>'
        ),
        "glass_furnace": (
            '<svg viewBox="0 0 120 72" width="120" height="72" xmlns="http://www.w3.org/2000/svg">'
            '<path d="M16,32 Q60,6 104,32 L104,60 L16,60 Z" fill="#1b2230" stroke="#adb5bd" stroke-width="2"/>'
            '<rect x="22" y="42" width="76" height="14" fill="#ff6b35" opacity="0.78"/>'
            '<line x1="60" y1="6" x2="60" y2="39" stroke="#e0e6ed" stroke-width="4"/>'
            '<circle cx="60" cy="39" r="3.5" fill="#ffd166"/>'
            '<rect x="54" y="3" width="12" height="7" rx="1.5" fill="#00b4d8"/>'
            '</svg>'
        ),
        "boiler_flue": (
            '<svg viewBox="0 0 120 72" width="120" height="72" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="10" y="22" width="100" height="28" fill="#1b2230" stroke="#9aa5b1" stroke-width="2"/>'
            '<path d="M22,36 L44,36 M40,32 L45,36 L40,40" fill="none" stroke="#ff9f1c" stroke-width="1.8"/>'
            '<path d="M74,36 L96,36 M92,32 L97,36 L92,40" fill="none" stroke="#ff9f1c" stroke-width="1.8"/>'
            '<line x1="60" y1="8" x2="60" y2="37" stroke="#00b4d8" stroke-width="3"/>'
            '<circle cx="60" cy="37" r="3.5" fill="#ff4d4d"/>'
            '<rect x="53" y="4" width="14" height="8" rx="2" fill="#4cc9f0"/>'
            '</svg>'
        ),
        "lab_furnace": (
            '<svg viewBox="0 0 120 72" width="120" height="72" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="24" y="16" width="72" height="40" rx="5" fill="#1b2230" stroke="#adb5bd" stroke-width="2"/>'
            '<line x1="10" y1="36" x2="110" y2="36" stroke="#e0e6ed" stroke-width="7" opacity="0.35"/>'
            '<rect x="44" y="28" width="32" height="16" rx="2" fill="#ff5400" opacity="0.65"/>'
            '<line x1="106" y1="36" x2="64" y2="36" stroke="#00b4d8" stroke-width="2.5"/>'
            '<circle cx="64" cy="36" r="3.5" fill="#ffd166"/>'
            '</svg>'
        ),
        "tube_furnace_avt": (
            '<svg viewBox="0 0 120 72" width="120" height="72" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="14" y="14" width="78" height="48" rx="4" fill="#1b2230" stroke="#9aa5b1" stroke-width="2"/>'
            '<path d="M22,24 H76 V34 H28 V44 H76 V54 H104" fill="none" stroke="#ff9f1c" stroke-width="3.5" stroke-linejoin="round"/>'
            '<circle cx="52" cy="34" r="3.5" fill="#ff4d4d"/>'
            '<line x1="52" y1="34" x2="52" y2="8" stroke="#f77f00" stroke-width="2"/>'
            '<circle cx="100" cy="54" r="3.5" fill="#00b4d8"/>'
            '<line x1="100" y1="54" x2="100" y2="38" stroke="#00b4d8" stroke-width="2"/>'
            '</svg>'
        ),
        "distillation_column": (
            '<svg viewBox="0 0 120 72" width="120" height="72" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="42" y="6" width="30" height="60" rx="12" fill="#1b2230" stroke="#9aa5b1" stroke-width="2"/>'
            '<line x1="44" y1="20" x2="70" y2="20" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,2"/>'
            '<line x1="44" y1="34" x2="70" y2="34" stroke="#ff9f1c" stroke-width="2"/>'
            '<line x1="44" y1="48" x2="70" y2="48" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,2"/>'
            '<line x1="88" y1="16" x2="64" y2="16" stroke="#00b4d8" stroke-width="2"/><circle cx="64" cy="16" r="2.8" fill="#4cc9f0"/>'
            '<line x1="88" y1="34" x2="64" y2="34" stroke="#ff9f1c" stroke-width="2"/><circle cx="64" cy="34" r="2.8" fill="#ff9f1c"/>'
            '<line x1="88" y1="52" x2="64" y2="52" stroke="#ff4d4d" stroke-width="2"/><circle cx="64" cy="52" r="2.8" fill="#ff4d4d"/>'
            '</svg>'
        ),
        "hydrotreating_reactor": (
            '<svg viewBox="0 0 120 72" width="120" height="72" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="38" y="8" width="36" height="56" rx="14" fill="#1b2230" stroke="#adb5bd" stroke-width="2.2"/>'
            '<rect x="42" y="20" width="28" height="14" rx="2" fill="#2b3a4a" stroke="#80ed99" stroke-width="1"/>'
            '<rect x="42" y="40" width="28" height="14" rx="2" fill="#2b3a4a" stroke="#ff9f1c" stroke-width="1"/>'
            '<line x1="56" y1="4" x2="56" y2="56" stroke="#00b4d8" stroke-width="2.5"/>'
            '<circle cx="56" cy="24" r="2.8" fill="#80ed99"/>'
            '<circle cx="56" cy="37" r="2.8" fill="#ffd166"/>'
            '<circle cx="56" cy="49" r="2.8" fill="#ff4d4d"/>'
            '</svg>'
        ),
    }
    return svgs.get(icon_key, svgs["heat_furnace"])


# База типовых производственных применений по типам термопар (с привязкой к диапазонам и ограничениям)
INDUSTRIAL_APPLICATIONS_DB = {
    "K": [
        # Высокотемпературные применения типа K (сценарий 700–1000 °C)
        {
            "industry": "Металлургия и машиностроение",
            "equipment": "Камеры промышленных печей",
            "install_point": "Свод или боковая стена рабочей камеры (в жаростойком защитном чехле / гильзе)",
            "controlled_temp": "700…1000 °C (типовой режим нагрева)",
            "t_low": 500.0,
            "t_high": 1150.0,
            "explanation": (
                "Контроль температурного поля внутри рабочей камеры печи для поддержания заданного "
                "технологического профиля нагрева и регулирования подачи топлива/мощности."
            ),
            "limitations": (
                "В окислительной атмосфере требуется жаростойкий чехол (сплавы Inconel/хромоникелевые стали или керамика); "
                "при низком содержании кислорода возможен дрейф НСХ («зелёная гниль» хрома)."
            ),
            "icon": "heat_furnace"
        },
        {
            "industry": "Металлообработка и термические цеха",
            "equipment": "Печи термической обработки металлов",
            "install_point": "Рабочее пространство зоны отжига, нормализации или закалки вблизи садки",
            "controlled_temp": "700…1000 °C (режимы закалки, отжига, нормализации сталей)",
            "t_low": 500.0,
            "t_high": 1150.0,
            "explanation": (
                "Контроль температуры садки и печной атмосферы для получения заданной микроструктуры "
                "и механических свойств металлических изделий."
            ),
            "limitations": (
                "При работе в защитных/восстановительных газовых средах (эндогаз, диссоциированный аммиак) "
                "необходима герметичная защитная гильза либо переход на тип N; требуется периодическая поверка из-за дрейфа."
            ),
            "icon": "heat_furnace"
        },
        {
            "industry": "Прокатное и кузнечно-прессовое производство",
            "equipment": "Зоны нагрева металлических заготовок",
            "install_point": "Стенки и своды методических / камерных нагревательных печей по зонам (подогрев, нагрев, томление)",
            "controlled_temp": "700…1050 °C (нагрев заготовок перед пластической деформацией)",
            "t_low": 550.0,
            "t_high": 1150.0,
            "explanation": (
                "Зональное регулирование температуры заготовок перед прокаткой или ковкой для исключения "
                "недогрева или пережога металла."
            ),
            "limitations": (
                "Высокие тепловые удары, окалина и вибрация требуют усиленных защитных гильз, "
                "минералоизолированного (КМС/MI) кабельного исполнения и корректного выбора глубины погружения."
            ),
            "icon": "heat_furnace"
        },
        {
            "industry": "Энергетика, металлургия и котельные установки",
            "equipment": "Контроль горячих газов в газоходах",
            "install_point": "Прямой участок газохода или дымохода перпендикулярно потоку газа в защитной гильзе",
            "controlled_temp": "600…1000 °C (высокотемпературные газоходы печей и энергетических агрегатов)",
            "t_low": 450.0,
            "t_high": 1100.0,
            "explanation": (
                "Измерение температуры отходящих и дымовых газов для контроля полноты сгорания топлива, "
                "теплового КПД и защиты рекуператоров от перегрева."
            ),
            "limitations": (
                "Абразивный износ золой, сернистая коррозия и вибрация потока требуют расчёта прочности гильзы "
                "и подбора коррозионностойкого материала оболочки."
            ),
            "icon": "boiler_flue"
        },
        # Умеренно-температурные применения типа K (сценарий 20–300 °C и −50…+100 °C)
        {
            "industry": "Переработка полимеров и химическая промышленность",
            "equipment": "Экструдеры и литьевые машины",
            "install_point": "Зоны нагрева материального цилиндра и формующей головки (посадочные гнёзда в металле)",
            "controlled_temp": "120…320 °C (температура расплава и цилиндра по зонам)",
            "t_low": 20.0,
            "t_high": 450.0,
            "explanation": (
                "Поддержание точного температурного профиля по зонам экструдера для стабильной вязкости "
                "расплава полимера и предотвращения термической деструкции."
            ),
            "limitations": (
                "Механическая вибрация и высокое давление расплава требуют вибростойкого кабельного исполнения "
                "с байонетным или резьбовым креплением."
            ),
            "icon": "extruder"
        },
        {
            "industry": "Теплоэнергетика и ЖКХ",
            "equipment": "Газоход котельной установки и теплообменники",
            "install_point": "Выходной газоход за котлом, коллекторы перегретого пара или теплоносителя",
            "controlled_temp": "80…350 °C (уходящие дымовые газы и теплоносители)",
            "t_low": -50.0,
            "t_high": 450.0,
            "explanation": (
                "Контроль температуры уходящих газов и теплоносителя для оценки эффективности теплообмена "
                "и предотвращения конденсации кислот в дымовом тракте."
            ),
            "limitations": (
                "Необходимо учитывать давление среды, коррозионность конденсата и температурный предел "
                "компенсационного кабеля и клеммной головки."
            ),
            "icon": "boiler_flue"
        },
        {
            "industry": "Машиностроение и лакокрасочное производство",
            "equipment": "Промышленные сушильные и термокамеры",
            "install_point": "Внутренний объём камеры в зоне циркуляции воздуха (вдали от прямого излучения ТЭНов)",
            "controlled_temp": "20…300 °C (сушка покрытий, низкий отпуск, полимеризация)",
            "t_low": -50.0,
            "t_high": 400.0,
            "explanation": (
                "Контроль равномерности прогрева изделий и поддержание заданного режима сушки или низкого отпуска."
            ),
            "limitations": (
                "В диапазоне до 300 °C типовой пример требует сопоставления с термометрами сопротивления (Pt100), "
                "если требуется повышенная точность; при наличии паров растворителей требуется взрывозащищённое исполнение."
            ),
            "icon": "heat_furnace"
        },
        {
            "industry": "Нефтеперерабатывающая промышленность (НПЗ, установки АВТ)",
            "equipment": "Трубчатая печь нагрева нефти и атмосферная ректификационная колонна",
            "install_point": (
                "Выходной трансферный трубопровод нефти в защитной гильзе (350–400 °C), наружная поверхность труб змеевика "
                "(поверхностная сборка tube-skin типа WIKA TC59 / ABB SensyTemp) и многоточечный профиль колонны"
            ),
            "controlled_temp": "100…400 °C (нефть на выходе печи и профиль колонны; стенка труб змеевика — отдельный канал)",
            "t_low": 80.0,
            "t_high": 950.0,
            "explanation": (
                "Контроль нагрева нефти перед подачей в атмосферную колонну, диагностика локального перегрева "
                "и коксообразования на трубах змеевика (tube-skin), а также многоточечный контроль температурного профиля колонны."
            ),
            "limitations": (
                "Нельзя переносить диапазон нефти (350–400 °C) на стенку труб змеевика или дымовые газы; "
                "требуются термокарманы по расчёту на прочность (ASME PTC 19.3 TW) и взрывозащита Ex i / Ex d."
            ),
            "icon": "tube_furnace_avt"
        },
    ],
    "N": [
        {
            "industry": "Металлургия и термическая обработка",
            "equipment": "Высокотемпературные печи термообработки и отжига",
            "install_point": "Рабочая камера печи в зоне длительной выдержки (жаростойкий чехол / MI-кабель)",
            "controlled_temp": "700…1150 °C (длительная эксплуатация в окислительной атмосфере)",
            "t_low": 500.0,
            "t_high": 1250.0,
            "explanation": (
                "Применяется как более стабильная альтернатива типу K при длительном нагреве: нихросил–нисил "
                "меньше подвержен окислению и температурному дрейфу градуировки."
            ),
            "limitations": (
                "Точный верхний рабочий предел конкретного датчика зависит от диаметра электродов и материала "
                "защитной оболочки (например, сплав Nicrobell / Inconel 600) — обязательна сверка с паспортом."
            ),
            "icon": "heat_furnace"
        },
        {
            "industry": "Производство строительных материалов",
            "equipment": "Цементная вращающаяся печь (зоны подогрева и газоходы)",
            "install_point": "Циклонные теплообменники, газоход отходящих газов и зона входа сырья",
            "controlled_temp": "700…1100 °C (высокопылевые горячие газовые потоки)",
            "t_low": 500.0,
            "t_high": 1200.0,
            "explanation": (
                "Контроль теплового режима циклонных теплообменников и газоходов цементной печи "
                "в условиях непрерывной круглосуточной работы."
            ),
            "limitations": (
                "Сильный абразивный износ цементной пылью, щёлочная коррозия и вибрация требуют массивных "
                "износостойких защитных гильз; пример типовой и требует подбора исполнения арматуры."
            ),
            "icon": "rotary_kiln"
        },
        {
            "industry": "Химическая и нефтехимическая промышленность",
            "equipment": "Реакторы, трубчатые печи и технологические установки",
            "install_point": "Защитные гильзы на трубопроводах, кожухах реакторов и в камерах подогрева",
            "controlled_temp": "20…900 °C (стабильный непрерывный контроль)",
            "t_low": -100.0,
            "t_high": 950.0,
            "explanation": (
                "Контроль температурных профилей технологических потоков и стенок аппаратов при длительном "
                "межповерочном интервале."
            ),
            "limitations": (
                "Необходимо учитывать давление, агрессивность химической среды и взрывозащиту; "
                "в восстановительной атмосфере требуется герметичный чехол."
            ),
            "icon": "boiler_flue"
        },
        {
            "industry": "Нефтеперерабатывающая промышленность (установки АВТ и гидроочистки)",
            "equipment": "Трубчатые печи (tube-skin), ректификационные колонны и реакторы гидроочистки",
            "install_point": (
                "Поверхность труб змеевика (с приварной площадкой и тепловым экраном), многоточечные сборки "
                "по высоте атмосферной колонны и в слоях катализатора реактора гидроочистки (типа WIKA TC95 / Endress+Hauser iTHERM MultiSens)"
            ),
            "controlled_temp": "100…900 °C (в зависимости от точки: продукт, профиль колонны/реактора, стенка змеевика)",
            "t_low": 80.0,
            "t_high": 950.0,
            "explanation": (
                "Сплав нихросил–нисил (тип N) обладает повышенной стабильностью градуировки и стойкостью к высокотемпературному "
                "окислению (на трубах печи) и меньше подвержен дрейфу при длительном межремонтном пробеге установок НПЗ."
            ),
            "limitations": (
                "В водородсодержащей и сероводородной среде (гидроочистка) обязательна герметичная защитная гильза "
                "из коррозионностойкой стали/сплава (AISI 321 / 316Ti / Incoloy 825), MI-кабель с герметичным уплотнением "
                "и резервирование каналов (2oo3 / дублирование)."
            ),
            "icon": "hydrotreating_reactor"
        },
    ],
    "T": [
        # Низкотемпературные применения типа T (сценарий −50…+100 °C)
        {
            "industry": "Пищевая промышленность и холодильная логистика",
            "equipment": "Морозильные камеры",
            "install_point": "Внутренний объём камеры хранения и зона воздухоохладителя (влагозащищённый корпус)",
            "controlled_temp": "−50…0 °C (глубокая заморозка и хранение)",
            "t_low": -200.0,
            "t_high": 120.0,
            "explanation": (
                "Контроль температуры воздуха и продукта в камерах шоковой заморозки и низкотемпературного хранения; "
                "тип T сохраняет стабильность и воспроизводимость при отрицательных температурах."
            ),
            "limitations": (
                "Конденсация влаги и обледенение требуют герметичной защиты кабельного ввода и коррозионностойкого "
                "чехла (нержавеющая сталь); не применять выше +350 °C."
            ),
            "icon": "freezer"
        },
        {
            "industry": "Промышленная холодильная техника",
            "equipment": "Холодильное оборудование",
            "install_point": "Трубопроводы испарителей, конденсаторов и камеры охлаждения агрегатов",
            "controlled_temp": "−50…+100 °C (циклы охлаждения и оттайки)",
            "t_low": -200.0,
            "t_high": 350.0,
            "explanation": (
                "Контроль температуры хладагента, теплообменных поверхностей и режимов автоматической оттайки "
                "промышленных холодильных машин."
            ),
            "limitations": (
                "Высокая теплопроводность меди может вызывать теплоотвод по электроду — требуется достаточная "
                "глубина погружения и вибростойкое крепление на компрессорных узлах."
            ),
            "icon": "freezer"
        },
        {
            "industry": "Пищевая переработка",
            "equipment": "Системы охлаждения пищевых продуктов",
            "install_point": "Туннельные охладители, танки охлаждения, теплообменники и линии пастеризации/охлаждения",
            "controlled_temp": "−40…+100 °C (охлаждение и санитарная обработка)",
            "t_low": -100.0,
            "t_high": 150.0,
            "explanation": (
                "Контроль соблюдения холодовой цепи и температурных переходов от мойки/нагрева к охлаждению "
                "для обеспечения микробиологической безопасности продукции."
            ),
            "limitations": (
                "Обязательно гигиеническое исполнение арматуры (нержавеющая сталь AISI 316L), устойчивость "
                "к агрессивным моющим растворам (CIP-мойка) и герметичность IP67/IP68."
            ),
            "icon": "freezer"
        },
        {
            "industry": "Фармацевтика и медицина",
            "equipment": "Фармацевтические холодильные установки",
            "install_point": "Контрольные точки холодильных камер, климатических шкафов и установок лиофилизации",
            "controlled_temp": "−50…+40 °C (хранение субстанций, вакцин и реагентов)",
            "t_low": -200.0,
            "t_high": 120.0,
            "explanation": (
                "Мониторинг и температурное картирование зон хранения термолабильных препаратов, "
                "где важна повторяемость показаний при отрицательных и околонулевых температурах."
            ),
            "limitations": (
                "Требуется калибровка по регламенту GMP и проверка класса допуска датчика; "
                "для предельно высокой точности часто сопоставляется с Pt100."
            ),
            "icon": "freezer"
        },
    ],
    "J": [
        {
            "industry": "Переработка пластмасс и резины",
            "equipment": "Экструдеры и термопластавтоматы",
            "install_point": "Зоны нагрева цилиндра, сопла и пресс-форм",
            "controlled_temp": "50…350 °C (переработка полимеров и эластомеров)",
            "t_low": 0.0,
            "t_high": 450.0,
            "explanation": (
                "Классическое применение пары железо–константан благодаря высокой чувствительности (около 55 мкВ/°C) "
                "и малой инерционности."
            ),
            "limitations": (
                "Железный термоэлектрод подвержен ржавлению во влажной среде (нежелательна работа с конденсацией влаги); "
                "на воздухе рабочий предел ограничен +750 °C."
            ),
            "icon": "extruder"
        },
        {
            "industry": "Общее машиностроение и энергетика",
            "equipment": "Печи низко- и среднетемпературного нагрева, сушильные камеры",
            "install_point": "Рабочая камера печи отпуска, сушки или газоход в защитном чехле",
            "controlled_temp": "100…700 °C (отпуск, сушка, термообработка цветных металлов)",
            "t_low": 20.0,
            "t_high": 750.0,
            "explanation": (
                "Контроль температурных режимов печей, работающих ниже предела интенсивного окисления железа."
            ),
            "limitations": (
                "На воздухе нельзя превышать практический предел 750 °C из-за быстрого окисления железа; "
                "требуется защита от влаги и сернистых газов."
            ),
            "icon": "heat_furnace"
        },
    ],
    "E": [
        {
            "industry": "Химическая промышленность и криогенная техника",
            "equipment": "Реакторы, теплообменники и криогенные установки",
            "install_point": "Узлы контроля малых перепадов температур и охлаждаемые трубопроводы",
            "controlled_temp": "−200…+350 °C (регистрация малых изменений температуры)",
            "t_low": -250.0,
            "t_high": 450.0,
            "explanation": (
                "Максимальная среди стандартных термопар чувствительность (около 68 мкВ/°C) повышает "
                "помехоустойчивость сигнала и разрешение при измерении небольших перепадов температур."
            ),
            "limitations": (
                "Типовой пример: в реферате не выделен отдельный численный верхний рабочий предел "
                "(указана таблица до 1000 °C), а реальный ресурс зависит от атмосферы и защитной гильзы."
            ),
            "icon": "lab_furnace"
        },
        {
            "industry": "Энергетика и промышленные печи",
            "equipment": "Газоходы и камеры нагрева с повышенными требованиями к чувствительности",
            "install_point": "Зоны контроля температуры газов и стенок аппаратов в защитном чехле",
            "controlled_temp": "300…850 °C (окислительная или инертная атмосфера)",
            "t_low": 250.0,
            "t_high": 1000.0,
            "explanation": (
                "Высокий уровень выходного сигнала упрощает измерение в условиях промышленных электромагнитных помех."
            ),
            "limitations": (
                "При приближении к границе стандартной таблицы (+1000 °C) необходимо сверяться с паспортом датчика; "
                "не рекомендуется в восстановительных средах без герметичного чехла."
            ),
            "icon": "boiler_flue"
        },
    ],
    "S": [
        # Высокотемпературные применения типа S (сценарий 1200–1500 °C)
        {
            "industry": "Металлургия и тяжёлое машиностроение",
            "equipment": "Высокотемпературные печи",
            "install_point": "Свод и рабочее пространство печи в газоплотном керамическом защитном чехле (корунд Al₂O₃)",
            "controlled_temp": "1100…1550 °C (нагрев, спекание, высокотемпературные процессы)",
            "t_low": 900.0,
            "t_high": 1600.0,
            "explanation": (
                "Непрерывный стабильный контроль температуры выше предела работы неблагородных сплавов (типов K и N), "
                "где критична воспроизводимость показаний."
            ),
            "limitations": (
                "Обязательна защита от загрязнения парами металлов, кремния и восстановительных газов газоплотным "
                "керамическим чехлом; чувствительность около 10 мкВ/°C требует малошумящего измерительного канала."
            ),
            "icon": "heat_furnace"
        },
        {
            "industry": "Термическое производство и порошковая металлургия",
            "equipment": "Установки термообработки",
            "install_point": "Рабочая зона высокотемпературного отжига, спекания или пайки",
            "controlled_temp": "1000…1550 °C (высокотемпературная термообработка сплавов)",
            "t_low": 800.0,
            "t_high": 1600.0,
            "explanation": (
                "Точное выдерживание температурного графика в печах термообработки специальных сталей, "
                "жаропрочных сплавов и порошковых заготовок."
            ),
            "limitations": (
                "Высокая стоимость платинородиевых электродов; хрупкость керамической арматуры при механических ударах "
                "и резких термоциклах."
            ),
            "icon": "heat_furnace"
        },
        {
            "industry": "Научные исследования и метрология",
            "equipment": "Лабораторные высокотемпературные печи",
            "install_point": "Трубчатая или камерная электропечь, эталонные и поверочные установки",
            "controlled_temp": "800…1600 °C (исследовательские и поверочные измерения)",
            "t_low": 0.0,
            "t_high": 1600.0,
            "explanation": (
                "Высокая стабильность градуировки делает платина–платинородий основным выбором для лабораторных "
                "печей и эталонных/калибровочных измерений."
            ),
            "limitations": (
                "Необходима чистая окислительная или инертная атмосфера и защита керамическим чехлом; "
                "недопустим контакт платины с металлическими защитными гильзами при высокой температуре."
            ),
            "icon": "lab_furnace"
        },
        {
            "industry": "Стекольная промышленность",
            "equipment": "Соответствующие участки стекольного производства (стекловаренные печи, питатели)",
            "install_point": "Свод печи, распределительные каналы (фидеры) и зоны выработки стекломассы",
            "controlled_temp": "1100…1550 °C (варка, осветление и выработка стекла)",
            "t_low": 1000.0,
            "t_high": 1600.0,
            "explanation": (
                "Поддержание стабильной вязкости стекломассы на участках варки и в питателях, "
                "где отклонение температуры напрямую влияет на качество формования."
            ),
            "limitations": (
                "Агрессивное воздействие паров щелочей и расплава стекла требует специальных защитных чехлов "
                "(керамика, платинированные колпачки); исполнение подбирается строго под конкретную зону печи."
            ),
            "icon": "glass_furnace"
        },
    ],
    "R": [
        {
            "industry": "Металлургия и тяжёлое машиностроение",
            "equipment": "Высокотемпературные печи",
            "install_point": "Рабочее пространство и свод печи в газоплотном керамическом чехле",
            "controlled_temp": "1100…1550 °C (промышленные высокотемпературные процессы)",
            "t_low": 900.0,
            "t_high": 1600.0,
            "explanation": (
                "Аналогично типу S обеспечивает высокую стабильность при температуре до 1600 °C "
                "(повышенное до 13 % содержание родия даёт немного больший выходной сигнал при близкой стабильности)."
            ),
            "limitations": (
                "Обязательна защита керамическими чехлами от загрязнения; высокая стоимость; "
                "малая чувствительность (около 10 мкВ/°C)."
            ),
            "icon": "heat_furnace"
        },
        {
            "industry": "Термическое производство",
            "equipment": "Установки термообработки",
            "install_point": "Высокотемпературные зоны спекания, гомогенизации и отжига",
            "controlled_temp": "1000…1550 °C (контроль садки и рабочей камеры)",
            "t_low": 800.0,
            "t_high": 1600.0,
            "explanation": (
                "Стабильное поддержание режима высокотемпературной термообработки с минимальным дрейфом характеристики."
            ),
            "limitations": (
                "Требуется защита от термоударов и восстановительных газов; сверка конструкции с паспортом датчика."
            ),
            "icon": "heat_furnace"
        },
        {
            "industry": "Научные исследования и метрология",
            "equipment": "Лабораторные высокотемпературные печи",
            "install_point": "Камеры лабораторных муфельных и трубчатых печей",
            "controlled_temp": "800…1600 °C (испытания материалов и калибровка)",
            "t_low": 0.0,
            "t_high": 1600.0,
            "explanation": (
                "Применяется в высокоточных лабораторных измерениях и калибровочных установках "
                "наряду с типом S."
            ),
            "limitations": (
                "Необходим газоплотный керамический чехол и прецизионный измерительный прибор "
                "с компенсацией холодного спая."
            ),
            "icon": "lab_furnace"
        },
        {
            "industry": "Стекольная промышленность",
            "equipment": "Соответствующие участки стекольного производства (стекловаренные печи, фидеры)",
            "install_point": "Сводовая зона, каналы питателей и зоны кондиционирования стекломассы",
            "controlled_temp": "1100…1550 °C (технологический контроль варки и выработки)",
            "t_low": 1000.0,
            "t_high": 1600.0,
            "explanation": (
                "Обеспечивает длительный точный контроль температуры стекломассы и газового пространства печи."
            ),
            "limitations": (
                "Химическая агрессивность среды требует подбора защитного чехла и исполнения погружной части."
            ),
            "icon": "glass_furnace"
        },
    ],
    "B": [
        # Условные высокотемпературные применения типа B (сценарий 1700–1800 °C и 1200–1600 °C)
        {
            "industry": "Стекольная промышленность",
            "equipment": "Высокотемпературные печи стекольного производства (стекловаренная печь)",
            "install_point": "Свод варочного бассейна и высокотемпературные зоны (в газоплотном корундовом чехле)",
            "controlled_temp": "1400…1750+ °C (условно в пределах таблицы до +1820 °C)",
            "t_low": 1100.0,
            "t_high": 1820.0,
            "explanation": (
                "Контроль наиболее горячих зон стекловаренных печей, где температура превышает рабочий предел "
                "термопар типов S и R (+1600 °C)."
            ),
            "limitations": (
                "ОБЯЗАТЕЛЬНА ПРОВЕРКА КОНСТРУКЦИИ И РЕАЛЬНОГО РАБОЧЕГО ДИАПАЗОНА: при 1700–1800 °C датчик "
                "работает у верхней границы стандартной таблицы (+1820 °C); срок службы критически зависит от "
                "диаметра проволоки, стойкости керамического чехла, вертикальной установки и состава печной атмосферы. "
                "Ниже +50 °C тип B практически не даёт сигнала."
            ),
            "icon": "glass_furnace"
        },
        {
            "industry": "Производство технической керамики и огнеупоров",
            "equipment": "Высокотемпературные печи керамического производства",
            "install_point": "Зона высокотемпературного обжига и спекания в газоплотном керамическом чехле",
            "controlled_temp": "1400…1750+ °C (обжиг огнеупоров и технической керамики)",
            "t_low": 1100.0,
            "t_high": 1820.0,
            "explanation": (
                "Контроль пиковых температур спекания оксидной керамики и огнеупорных материалов."
            ),
            "limitations": (
                "ОБЯЗАТЕЛЬНА ПРОВЕРКА КОНСТРУКЦИИ И РЕАЛЬНОГО РАБОЧЕГО ДИАПАЗОНА: табличный предел +1820 °C "
                "не является гарантией длительной непрерывной работы конкретной модели датчика и защитного чехла; "
                "необходима сверка с паспортом производителя и оценка провисания/ползучести керамической трубки."
            ),
            "icon": "heat_furnace"
        },
    ],
    "W-Re": [
        # Экстремальные температуры 2200–2500 °C (только вакуум / инертная / восстановительная среда)
        {
            "industry": "Металлургия тугоплавких металлов и аэрокосмическая отрасль",
            "equipment": "Вакуумные высокотемпературные печи",
            "install_point": "Рабочая камера вакуумного спекания, плавки или термообработки",
            "controlled_temp": "2200…2500 °C (только в вакууме)",
            "t_low": 2000.0,
            "t_high": 2500.0,
            "allowed_envs": ("вакуум",),
            "explanation": (
                "Контроль экстремальных температур спекания тугоплавких металлов, карбидов и композитов "
                "в глубоком вакууме, где платинородиевые пары уже расплавляются."
            ),
            "limitations": (
                "Условный типовой пример: требуется сверка конкретной марки (например, ВР-5/20 и др.), "
                "подбор высокотемпературной изоляции (BeO / HfO₂ / ThO₂) и строгий контроль вакуума — "
                "при попадании кислорода вольфрам мгновенно окисляется."
            ),
            "icon": "lab_furnace"
        },
        {
            "industry": "Специальное материаловедение и производство полупроводников",
            "equipment": "Высокотемпературные печи с инертной или восстановительной средой",
            "install_point": "Зона нагрева установок выращивания кристаллов и графитации (в защитной среде Ar / H₂)",
            "controlled_temp": "2200…2500 °C (только в инертной или восстановительной среде)",
            "t_low": 2000.0,
            "t_high": 2500.0,
            "allowed_envs": ("инертная", "восстановительная"),
            "explanation": (
                "Измерение сверхвысоких температур при синтезе и термообработке материалов в защитной атмосфере "
                "(аргон, водород) при полном отсутствии кислорода."
            ),
            "limitations": (
                "Условный типовой пример: категорически недопустима разгерметизация печи с подсосом воздуха; "
                "необходим подбор конкретной градуировки, защитного чехла и проверка совместимости изоляции со средой."
            ),
            "icon": "lab_furnace"
        },
    ]
}


def filter_industrial_examples(
    tc_code: str,
    t_min: float,
    t_max: float,
    environment: str
) -> list[dict]:
    """
    Отбирает типовые производственные примеры для выбранного типа термопары,
    согласованные с введённым диапазоном температур [t_min, t_max] и рабочей средой.
    """
    examples = INDUSTRIAL_APPLICATIONS_DB.get(tc_code, [])
    matched = []
    for ex in examples:
        allowed_envs = ex.get("allowed_envs")
        if allowed_envs is not None and environment not in allowed_envs:
            continue
        # Проверяем пересечение температурного диапазона примера с заданным интервалом [t_min, t_max]
        overlap_low = max(t_min, ex["t_low"])
        overlap_high = min(t_max, ex["t_high"])
        if overlap_high >= overlap_low:
            # Оцениваем релевантность по доле покрытия целевого интервала
            span = max(t_max - t_min, 1.0)
            coverage = (overlap_high - overlap_low) / span
            # Бонус, если верхняя рабочая температура задачи попадает прямо в окно примера
            max_bonus = 0.5 if (ex["t_low"] <= t_max <= ex["t_high"]) else 0.0
            matched.append((coverage + max_bonus, ex))

    # Сортируем по релевантности (при равенстве сохраняем исходный порядок)
    matched.sort(key=lambda pair: pair[0], reverse=True)
    return [item[1] for item in matched[:4]]


def render_single_tc_examples_grid(
    tc_code: str,
    tc_title: str,
    t_min: float,
    t_max: float,
    environment: str,
    is_conditional: bool
) -> None:
    """
    Отрисовывает карточки производственного применения для одного типа термопары:
    на компьютере — в две колонки, на телефоне — в одну колонку.
    """
    examples = filter_industrial_examples(tc_code, t_min, t_max, environment)
    is_mobile_view = (st.session_state.get("chart_display_mode") == "Смартфон (320–430 px)")

    if is_conditional:
        if tc_code == "B":
            st.warning(
                "⚠️ **Условный характер примеров для типа B (ТПР):** при температуре "
                f"**{t_min:.0f}…{t_max:.0f} °C** измерение ведётся вблизи верхней границы стандартной таблицы (+1820 °C). "
                "Приведённые ниже печи стекольного и керамического производства являются типовыми ориентирами — "
                "**обязательно проверьте конкретную конструкцию датчика (диаметр проволоки, тип керамического чехла) "
                "и его реальный рабочий диапазон по паспорту производителя**."
            )
        else:
            st.warning(
                f"⚠️ **Условный статус рекомендации для {tc_title}:** поскольку для заданной температуры или среды "
                f"(«{environment}») требуется уточнение паспортных ограничений, приведённые ниже примеры носят "
                "типовой справочный характер и не заменяют проверку конкретного исполнения датчика."
            )

    if not examples:
        st.info(
            f"Для **{tc_title}** в заданном диапазоне **{t_min:.0f}…{t_max:.0f} °C** (среда: *{environment}*) "
            "нет подтверждённых типовых производственных примеров в базе приложения — подбор узла измерения "
            "требует индивидуальной проработки по каталогам производителей и паспорту оборудования."
        )
        return

    def _draw_example_card(ex: dict) -> None:
        with st.container(border=True):
            svg_markup = get_equipment_svg(ex["icon"])
            if is_mobile_view:
                st.markdown(f"#### {ex['equipment']}")
                st.caption(f"🏭 **Отрасль:** {ex['industry']}")
                st.markdown(f'<div class="kip-equip-svg-wrap">{svg_markup}</div>', unsafe_allow_html=True)
            else:
                top_l, top_r = st.columns([3, 1])
                with top_l:
                    st.markdown(f"#### {ex['equipment']}")
                    st.caption(f"🏭 **Отрасль:** {ex['industry']}")
                with top_r:
                    st.markdown(f'<div class="kip-equip-svg-wrap">{svg_markup}</div>', unsafe_allow_html=True)

            st.markdown(f"- **Место установки:** {ex['install_point']}")
            st.markdown(f"- **Контролируемая температура:** {ex['controlled_temp']}")
            st.markdown(f"- **Что контролируют и почему подходит:** {ex['explanation']}")
            st.caption(f"⚠️ *Инженерные ограничения:* {ex['limitations']}")
            st.caption("ℹ️ *Типовой производственный пример; требует подбора конкретного исполнения датчика и защитной гильзы.*")

    if is_mobile_view:
        for ex in examples:
            _draw_example_card(ex)
    else:
        for row_start in range(0, len(examples), 2):
            row_items = examples[row_start:row_start + 2]
            cols = st.columns(len(row_items))
            for col, ex in zip(cols, row_items):
                with col:
                    _draw_example_card(ex)


def render_industrial_applications_block(
    result: dict,
    t_min: float,
    t_max: float,
    environment: str
) -> None:
    """
    Отображает блок «Производственное применение» для рекомендованного типа термопары
    и подходящих альтернатив. При отказе подбора (status == 'error') не выводится.
    """
    if result.get("status") == "error" or result.get("primary") is None:
        return

    st.subheader("🏭 Производственное применение и типовое оборудование")
    st.markdown(
        f"Ниже показаны типовые технологические процессы и промышленное оборудование, "
        f"соответствующие подобранным типам термопар для заданного диапазона **{t_min:.0f}…{t_max:.0f} °C** "
        f"и рабочей среды **«{environment}»**."
    )

    is_cond = result["status"] in ("warning", "conditional")
    primary_sp = result["primary"]

    tab_entries = [
        (f"Основной: {primary_sp['code']} ({primary_sp['gost'].split(' ')[0]})", primary_sp, is_cond)
    ]
    for alt_item in result.get("alternatives", []):
        alt_sp = alt_item["spec"]
        alt_cond = is_cond or (alt_sp.get("confirmed_work_max") is None)
        tab_entries.append(
            (f"Альтернатива: {alt_sp['code']} ({alt_sp['gost'].split(' ')[0]})", alt_sp, alt_cond)
        )

    if len(tab_entries) == 1:
        _, sp_item, cond_flag = tab_entries[0]
        render_single_tc_examples_grid(sp_item["code"], sp_item["title"], t_min, t_max, environment, cond_flag)
    else:
        tabs = st.tabs([entry[0] for entry in tab_entries])
        for tab, (_, sp_item, cond_flag) in zip(tabs, tab_entries):
            with tab:
                render_single_tc_examples_grid(sp_item["code"], sp_item["title"], t_min, t_max, environment, cond_flag)

    with st.expander("🛡️ Инженерная памятка: три уровня применимости и источники сведений", expanded=False):
        st.markdown(
            "**Разграничивайте три уровня при проектировании узла измерения температуры:**\n"
            "1. **Возможность измерения заданной температуры термоэлектродами** — определяется градуировкой (НСХ) и свойствами сплавов.\n"
            "2. **Допустимость эксплуатации конкретного исполнения термопары** — зависит от диаметра электродов, минеральной изоляции, "
            "материала защитной оболочки (гильзы), конструкции спая и длительности работы.\n"
            "3. **Пригодность датчика для конкретной промышленной точки измерения** — определяется атмосферой, химическим составом среды, "
            "давлением, вибрацией, коррозионным и абразивным воздействием, а также требуемой точностью.\n\n"
            "> **Важно:** рабочий диапазон самих термоэлектродов нельзя автоматически переносить на весь измерительный узел "
            "вместе с защитной гильзой, клеммной головкой и компенсационным кабелем.\n\n"
            "**Технические ориентиры и источники (включая нефтепереработку):**\n"
            "- [WIKA — Tubeskin Thermocouple Model TC59 & Multipoint Model TC95](https://www.wika.com/)\n"
            "- [ABB — SensyTemp TSP / TSH Process & Tubeskin Thermocouples](https://new.abb.com/products/measurement-products/temperature)\n"
            "- [Endress+Hauser — iTHERM MultiSens Multipoint Temperature Assemblies](https://www.endress.com/)\n"
            "- [BIPM — Guide to Secondary Thermometry: Thermocouple Thermometry (Part 1)](https://www.bipm.org/documents/20126/41773843/Thermocouple_Thermometry_Part1.pdf)"
        )


INDUSTRIAL_SCENARIOS_CAT_A = [
    {
        "id": "ind_extrusion",
        "num": 1,
        "title": "Производство полимерных изделий (экструзия)",
        "object_short": "Цилиндр экструдера, зоны нагрева и формующая головка",
        "object_type": "Поверхность цилиндра / расплав полимера (погружной или поверхностный монтаж)",
        "measured_qty": "Температура металла цилиндра по зонам нагрева или расплава полимера в формующей головке",
        "t_min": 160.0,
        "t_max": 300.0,
        "env": "воздушная / окислительная",
        "prio": "повышенная чувствительность",
        "special_conditions": (
            "Многозонный обогрев цилиндра (4–6 зон), вибрация привода шнека, необходимость малой тепловой инерции. "
            "При поверхностном монтаже в резьбовое гнездо цилиндра применяют байонетные или винтовые термопары; "
            "при погружении в поток расплава — усиленную защитную арматуру (чехол из нержавеющей стали)."
        ),
        "automation_task": (
            "Поддержание заданного температурного профиля по отдельным зонам цилиндра и формующей головки, "
            "управление электронагревателями и охлаждением зон, предотвращение термической деструкции полимера "
            "или нерасплава (брака профиля/плёнки)."
        ),
        "kip_task": (
            "Выбрать термопару с высокой чувствительностью и малой инерционностью (например, тип J / ТЖК или тип K / ТХА "
            "в зависимости от влажности и конструкции узла), определить способ установки (в глухое отверстие стенки "
            "цилиндра с термопастой или погружной монтаж в головку), проложить компенсационный кабель вдали от силовых линий "
            "нагревателей и настроить сигнализацию перегрева зоны."
        ),
        "engineering_check_note": (
            "Диапазон 160–300 °C полностью перекрывается рабочими пределами типов J (до 750 °C на воздухе, ~55 мкВ/°C) "
            "и K (до 1100–1200 °C на воздухе, ~41 мкВ/°C). При отсутствии конденсации влаги тип J обеспечивает более "
            "высокий выходной сигнал; при повышенной влажности предпочтителен тип K (железо в J подвержено коррозии)."
        ),
    },
    {
        "id": "ind_dryer",
        "num": 2,
        "title": "Промышленная сушильная установка",
        "object_short": "Сушильная камера и циркуляционный воздушный поток",
        "object_type": "Газовый поток (нагретый воздух / сушильный агент) в камере и воздуховоде",
        "measured_qty": "Температура циркуляционного воздуха на входе, в рабочей зоне и на выходе камеры",
        "t_min": 60.0,
        "t_max": 250.0,
        "env": "воздушная / окислительная",
        "prio": "универсальность",
        "special_conditions": (
            "Конвективный поток воздуха с возможным содержанием водяных паров и летучих веществ из высушиваемого сырья. "
            "Требуется защитная гильза (трубка из коррозионностойкой стали) и установка в представительной точке "
            "потока без прямого излучения от ТЭНов или калорифера."
        ),
        "automation_task": (
            "Регулирование температуры сушильного агента, управление мощностью калорифера (или подачей теплоносителя) "
            "и рециркуляцией вентиляции, предотвращение перегрева и возгорания высушиваемого материала."
        ),
        "kip_task": (
            "Подобрать коррозионностойкую термопару (тип K / ТХА или тип T / ТМК до 350 °C; для типа J учесть риск "
            "ржавления железного электрода во влажном воздухе), выбрать погружную длину гильзы для исключения теплоотвода "
            "по арматуре и предусмотреть блокировку нагрева при превышении предельной температуры."
        ),
        "engineering_check_note": (
            "Интервал 60–250 °C входит в подтверждённый рабочий диапазон типов K (−200…+1200 °C), T (−200…+350 °C) "
            "и J (−210…+750 °C). Из-за влажности сушильного агента тип K или T предпочтительнее типа J."
        ),
    },
    {
        "id": "ind_reactor",
        "num": 3,
        "title": "Химический реактор",
        "object_short": "Технологическая среда внутри реактора",
        "object_type": "Жидкая или газофазная реакционная масса (погружение в защитной гильзе)",
        "measured_qty": "Температура реакционной среды в объёме аппарата (при необходимости — дополнительно в рубашке)",
        "t_min": 20.0,
        "t_max": 300.0,
        "env": "воздушная / окислительная",
        "prio": "стабильность и точность",
        "special_conditions": (
            "Агрессивная химическая среда, перемешивание мешалкой, избыточное давление. Прямой контакт термоэлектродов "
            "со средой недопустим: обязательна герметичная защитная гильза из химически стойкого сплава или с фторопластовым/"
            "эмалевым покрытием (по паспорту), что увеличивает тепловую инерционность узла."
        ),
        "automation_task": (
            "Контроль хода экзо- или эндотермической реакции, каскадное управление подачей теплоносителя и хладагента "
            "в рубашку реактора, формирование предупредительной и аварийной сигнализации/блокировки при разгоне реакции."
        ),
        "kip_task": (
            "Выбрать стабильную термопару (тип N / ТНН или тип K / ТХА), подобрать материал и толщину стенки защитной гильзы "
            "под химический состав и давление среды, обеспечить плотный тепловой контакт спая с дном гильзы "
            "и выполнить требования взрывозащиты (искробезопасная цепь Ex i при наличии горючих паров)."
        ),
        "engineering_check_note": (
            "В диапазоне 20–300 °C термоэлектроды типов N и K работают с большим запасом по температуре, "
            "однако реальная допустимость эксплуатации определяется стойкостью материала защитной гильзы к конкретному реагенту."
        ),
    },
    {
        "id": "ind_boiler",
        "num": 4,
        "title": "Промышленная котельная установка",
        "object_short": "Дымовые газы и газоход котла",
        "object_type": "Поток дымовых (уходящих) газов в газоходе котлоагрегата",
        "measured_qty": "Температура продуктов сгорания за топкой, в конвективных поверхностях и газоходе",
        "t_min": 200.0,
        "t_max": 1000.0,
        "env": "воздушная / окислительная",
        "prio": "универсальность",
        "special_conditions": (
            "Окислительная атмосфера дымовых газов с возможным содержанием сернистых соединений, золы и сажи. "
            "Требуется жаростойкий защитный чехол, устойчивый к газовой коррозии и абразивному износу, "
            "и герметизация фланцевого/резьбового ввода в обмуровку газохода."
        ),
        "automation_task": (
            "Контроль температурного режима котлоагрегата, диагностика загрязнения поверхностей нагрева "
            "(по росту температуры уходящих газов) и контроль полноты/режима горения топлива."
        ),
        "kip_task": (
            "Назначить жаростойкую термопару (тип K / ТХА или тип N / ТНН — тип J неприменим, так как 1000 °C превышает "
            "его рабочий предел 750 °C на воздухе), выбрать длину погружения на 1/3…1/2 диаметра газохода и жаропрочный чехол, "
            "обеспечить компенсацию температуры холодного спая на клеммах."
        ),
        "engineering_check_note": (
            "Интервал 200–1000 °C перекрывается типом K (рабочий предел на воздухе 1100–1200 °C) и типом N "
            "(таблица до 1300 °C, повышенная стойкость к окислению). Тип J отбраковывается (предел 750 °C)."
        ),
    },
    {
        "id": "ind_heattreat",
        "num": 5,
        "title": "Термическая обработка металлов",
        "object_short": "Рабочая камера печи и нагреваемые изделия",
        "object_type": "Рабочее пространство камерной/шахтной печи и садка металлических заготовок",
        "measured_qty": "Температура в зонах нагрева печи при закалке, отжиге, нормализации и отпуске",
        "t_min": 700.0,
        "t_max": 1100.0,
        "env": "воздушная / окислительная",
        "prio": "стабильность и точность",
        "special_conditions": (
            "Длительная выдержка при высоких температурах, циклические нагревы и охлаждения, окалинообразование "
            "на защитной арматуре. В диапазоне 700–1100 °C у типа K при длительной работе проявляется дрейф градуировки, "
            "поэтому тип N (нихросил–нисил) обеспечивает лучшую стабильность."
        ),
        "automation_task": (
            "Точное поддержание графика термообработки (скорость нагрева, температура и время выдержки), "
            "независимое регулирование нескольких зон нагрева печи и предотвращение пережога или недогрева металла (брака)."
        ),
        "kip_task": (
            "Выбрать термопару типа N (ТНН) или типа K (ТХА) в жаростойком защитном чехле, исключить провисание "
            "горизонтально установленной арматуры при 1100 °C, предусмотреть периодическую поверку/контроль дрейфа "
            "и независимый канал защиты от перегрева печи."
        ),
        "engineering_check_note": (
            "Верхняя граница 1100 °C находится на границе подтверждённого рабочего диапазона типа K (1100–1200 °C). "
            "Согласно п. 5.3 реферата, тип N разработан как более стабильная замена типа K при высоких температурах."
        ),
    },
    {
        "id": "ind_glass",
        "num": 6,
        "title": "Производство стекла и керамики",
        "object_short": "Рабочая зона стекловаренной или керамической печи",
        "object_type": "Свод, рабочее пространство печи обжига/варки и зона питателя стекломассы",
        "measured_qty": "Высокая температура газового пространства печи и зоны плавления/обжига",
        "t_min": 1200.0,
        "t_max": 1450.0,
        "env": "воздушная / окислительная",
        "prio": "стабильность и точность",
        "special_conditions": (
            "Температура 1200–1450 °C превышает рабочий предел неблагородных термопар (для K на воздухе предел 1100–1200 °C). "
            "Необходимы платинородиевые термопары типов S или R в газоплотных керамических чехлах (корунд/муллитокремнезём) "
            "для защиты платины от паров щелочей, кремния и восстановительных газов."
        ),
        "automation_task": (
            "Поддержание температурного режима плавления стекломассы или высокотемпературного спекания/обжига керамики, "
            "управление подачей топлива и воздуха на горелки, предотвращение расстройства режима варки и деформации изделий."
        ),
        "kip_task": (
            "Применить термопару благородных металлов типа S или R (рабочий предел до +1600 °C, чувствительность ~10 мкВ/°C), "
            "обязательно установить двойной/газоплотный керамический чехол, использовать специальные компенсационные "
            "провода (медь–сплав) для платинородиевых пар и высокоточный входной преобразователь (низкий уровень мВ)."
        ),
        "engineering_check_note": (
            "Интервал 1200–1450 °C строго соответствует подтверждённому в п. 5.2 реферата рабочему диапазону "
            "термопар типов S и R (до +1600 °C на воздухе) при обязательной защите керамическим чехлом."
        ),
    },
    {
        "id": "ind_vacuum",
        "num": 7,
        "title": "Вакуумная термическая обработка",
        "object_short": "Рабочая камера вакуумной печи",
        "object_type": "Вакуумированная рабочая камера высокотемпературной печи (вакуум)",
        "measured_qty": "Сверхвысокая температура в зоне нагревателя и садки в условиях вакуума",
        "t_min": 2200.0,
        "t_max": 2450.0,
        "env": "вакуум",
        "prio": "универсальность",
        "special_conditions": (
            "Глубокий вакуум (или чистая инертная/восстановительная среда). Стандартные термопары из неблагородных и "
            "платиновых сплавов здесь неприменимы (предел таблицы типа B заканчивается на +1820 °C). "
            "Вольфрам-рениевые термопары (2200–2500 °C по п. 5.3 реферата) допустимы ТОЛЬКО при отсутствии кислорода: "
            "при попадании воздуха вольфрам мгновенно окисляется и разрушается."
        ),
        "automation_task": (
            "Контроль сверхвысокотемпературного процесса спекания/отжига тугоплавких материалов, "
            "управление мощностью нагревателей вакуумной печи и защита тепловых экранов и изделий от перегрева."
        ),
        "kip_task": (
            "Выбрать вольфрам-рениевую термопару (условная рекомендация по п. 5.3 с обязательной проверкой конкретной "
            "градуировки и паспорта), обеспечить герметичный вакуумный ввод термоэлектродов, заблокировать подачу "
            "высокой мощности при нарушении вакуума (натекании воздуха) и учесть хрупкость термоэлектродов после отжига."
        ),
        "engineering_check_note": (
            "В реферате (п. 5.3) вольфрам-рениевые термопары подтверждены для диапазона 2200–2500 °C в вакууме, "
            "инертной или восстановительной среде (в диапазоне 1820–2200 °C подтверждённых данных в реферате нет)."
        ),
    },
    {
        "id": "ind_kiln",
        "num": 8,
        "title": "Высокотемпературное промышленное обжиговое производство",
        "object_short": "Рабочая камера обжиговой печи и температурные зоны",
        "object_type": "Зоны подогрева, обжига и охлаждения туннельной или вращающейся обжиговой печи",
        "measured_qty": "Температурный профиль по длине обжиговой печи и в зоне спекания/обжига",
        "t_min": 900.0,
        "t_max": 1300.0,
        "env": "воздушная / окислительная",
        "prio": "стабильность и точность",
        "special_conditions": (
            "Верхняя граница 1300 °C превышает подтверждённый практический предел типа K на воздухе (1100–1200 °C) "
            "и достигает самой верхней границы таблицы типа N (+1300 °C, где в реферате не подтверждён гарантированный "
            "практический предел). Поэтому надёжным решением для 900–1300 °C являются платинородиевые пары S или R "
            "(рабочий предел до +1600 °C) в керамическом чехле, а тип N допустим лишь как условная альтернатива по паспорту."
        ),
        "automation_task": (
            "Контроль продольного температурного профиля обжиговой печи, регулирование подачи топлива по зонам, "
            "предотвращение недожога или оплавления продукции при нарушении технологического режима."
        ),
        "kip_task": (
            "Разделить зоны печи по температурным уровням: в зоне 900–1300 °C установить термопары типа S или R "
            "в жаростойких газоплотных керамических чехлах (в более холодных зонах до 1100 °C — тип N или K), "
            "обеспечить защиту от пыли и механических воздействий шихты/газового потока."
        ),
        "engineering_check_note": (
            "Техническая проверка: при T_max = 1300 °C тип K отбраковывается (практический предел на воздухе 1100–1200 °C), "
            "тип S / R имеет подтверждённый рабочий предел до +1600 °C, а тип N (таблица до 1300 °C) уступает по запасу."
        ),
    },
    {
        "id": "ind_refinery_avt_furnace",
        "num": 9,
        "industry_group": "Нефтеперерабатывающая промышленность (НПЗ • АТПП УГНТУ)",
        "badge_label": "Нефтепереработка • АВТ (основной процесс)",
        "title": "Атмосферно-вакуумная установка (АВТ): нагрев нефти в трубчатой печи",
        "object_short": "Поток нефти на выходе печи (350–400 °C), наружная поверхность труб змеевика и дымовые газы",
        "object_type": "Разделённые каналы: погружной в поток нефти (350–400 °C) / контактный tube-skin на трубах / газоход",
        "channel_purpose": "Контактное измерение наружной поверхности труб змеевика (tube-skin)",
        "measured_qty": (
            "1) Температура нагреваемой нефти на выходе из печи (погружное измерение в трансферном трубопроводе); "
            "2) Температура наружной поверхности труб змеевика (контактное измерение tube-skin); "
            "3) Температура дымовых газов на перевале и в конвективной камере"
        ),
        "measurement_objects_list": [
            "Температура нефти на выходе из печи (погружное измерение в защитной гильзе в потоке среды, ориентировочно 350–400 °C)",
            "Температура наружной поверхности труб змеевика (контактное измерение tube-skin — отдельный канал с более высокой температурой стенки)",
            "Температура дымовых газов в камере радиации / на перевале и в конвекционной секции (отдельный высокотемпературный канал)"
        ],
        "t_min": 350.0,
        "t_max": 400.0,
        "env": "воздушная / окислительная",
        "prio": "стабильность и точность",
        "special_conditions": (
            "Строго разделять три измерительных контура и НЕ переносить диапазон нефти (350–400 °C) на поверхность труб или дымовые газы: "
            "(а) температура нефти на выходе печи измеряется погружной термопарой в защитной гильзе (термокармане); "
            "(б) температура наружной поверхности труб змеевика (tube-skin) выше температуры нефти и зависит от теплового потока "
            "и отложения кокса внутри трубы — для неё требуется специальная поверхностная термопара с приварной/прижимной "
            "контактной площадкой и тепловым экраном от прямого излучения факела (например, WIKA TC59 / ABB SensyTemp); "
            "(в) дымовые газы контролируются отдельными жаростойкими датчиками. Взрывоопасная зона НПЗ (Ex i / Ex d)."
        ),
        "automation_task": (
            "• Поддержание заданной температуры нагрева сырой нефти на выходе из трубчатой печи перед подачей в атмосферную колонну "
            "(каскадное регулирование подачи топливного газа на горелки);\n"
            "• Непрерывный контроль локального перегрева наружной поверхности труб радиантного змеевика;\n"
            "• Раннее обнаружение образования коксовых отложений внутри труб по росту разности температур между стенкой трубы (tube-skin) и потоком нефти;\n"
            "• Формирование предупредительной и аварийной сигнализации (ПАЗ) при приближении температуры стенки к пределу жаропрочности стали трубы;\n"
            "• Передача достоверных измерительных данных и диагностического статуса каналов на АРМ оператора технологической установки."
        ),
        "kip_task": (
            "1) Разделить измерительные узлы на погружные (поток нефти 350–400 °C в термокармане с расчётом на вибропрочность от срыва вихрей) "
            "и контактные (tube-skin на поверхности змеевика с приваркой/прижимом контактной пластины и защитой спая от факела);\n"
            "2) Подобрать термопары с кабельной минеральной изоляцией (MI-кабель, типы N / ТНН или K / ТХА в жаростойкой оболочке Inconel 600 / Alloy 800H "
            "по паспорту производителя WIKA / ABB) и компенсационные кабели соответствующей градуировки;\n"
            "3) Обеспечить температурную компенсацию теплового удлинения змеевика при прокладке MI-кабеля внутри печи;\n"
            "4) Выполнить взрывозащиту цепей (искробезопасные барьеры Ex i или взрывонепроницаемые оболочки Ex d) и настроить уставки сигнализации."
        ),
        "engineering_check_note": (
            "Ориентировочный диапазон 350–400 °C относится ТОЛЬКО к нагреву нефти на выходе из печи. "
            "Для поверхности труб змеевика (tube-skin) и дымовых газов рабочая температура существенно выше и определяется "
            "тепловым расчётом печи и маркой стали змеевика — при выборе датчика обязательна проверка паспорта сборки (WIKA TC59 / ABB SensyTemp)."
        ),
        "technical_sources": [
            "WIKA — Tubeskin thermocouples for fired heaters & furnaces (Model TC59)",
            "ABB — SensyTemp TSP / TSH high-temperature & tubeskin thermocouple assemblies",
            "ГОСТ Р 8.585-2001 — Номинальные статические характеристики термопар (ТНН / ТХА)"
        ],
    },
    {
        "id": "ind_refinery_distillation_column",
        "num": 10,
        "industry_group": "Нефтеперерабатывающая промышленность (НПЗ • АТПП УГНТУ)",
        "badge_label": "Нефтепереработка • АВТ (основной процесс)",
        "title": "Атмосферная ректификационная колонна нефтепереработки",
        "object_short": "Многоточечный профиль: верх колонны, промежуточные тарелки, зона питания и куб (низ) колонны",
        "object_type": "Многоточечное погружное измерение температурного профиля по высоте колонны в защитных гильзах",
        "channel_purpose": "Многоточечный температурный профиль аппарата (колонна / слои катализатора реактора)",
        "measured_qty": (
            "Многоточечный температурный профиль по высоте ректификационной колонны: "
            "верхняя часть (пары бензиновой фракции), промежуточные тарелки и отборы боковых погонов "
            "(керосин, дизельное топливо), зона питания (ввод отбензиненной/нагретой нефти) и нижняя кубовая часть (мазут)"
        ),
        "measurement_objects_list": [
            "Верхняя часть колонны (температура уходящих паров верхнего продукта и орошения)",
            "Промежуточные уровни / контрольные тарелки и узлы боковых отборов фракций (керосиновая, дизельная фракции)",
            "Зона питания колонны (ввод нагретого сырья из трубчатой печи АВТ)",
            "Нижняя (кубовая) часть колонны (температура остатка — мазута и подачи отпарного водяного пара)"
        ],
        "t_min": 100.0,
        "t_max": 380.0,
        "env": "воздушная / окислительная",
        "prio": "стабильность и точность",
        "special_conditions": (
            "Обязательно МНОГОТОЧЕЧНОЕ измерение по высоте колонны (один датчик не позволяет судить о режиме ректификации). "
            "Условия по высоте аппарата неоднородны: от ~100–130 °C наверху до ~350–380 °C в зоне питания и кубе; "
            "присутствуют пары углеводородов, водяной пар и сернистые соединения (сероводородная коррозия и нафтеновые кислоты). "
            "Выбор конструкции термопары и защитной гильзы (термокармана из коррозионностойкой стали AISI 316Ti / 321 / дуплексных или "
            "никелевых сплавов) зависит от конкретной точки установки, давления, температуры и химического состава фракции."
        ),
        "automation_task": (
            "• Непрерывный контроль температурного профиля по высоте атмосферной колонны (верх, контрольные тарелки, зона питания, куб);\n"
            "• Оперативное выявление нарушений режима фракционирования (захлёбывание тарелок, проскок тяжёлых фракций вверх или лёгких вниз, "
            "изменение фракционного состава целевых нефтепродуктов);\n"
            "• Передача показаний в систему управления (РСУ / АСУ ТП) для стабилизации температуры верха (орошением) и отборов боковых погонов;\n"
            "• Обеспечение технологической стабильности и воспроизводимости качества дистиллятов."
        ),
        "kip_task": (
            "1) Спроектировать распределённую многоточечную систему измерения температуры по ярусам колонны (вместо одиночной точки) "
            "с учётом условий каждой отметки (температура, давление, агрессивность фракции);\n"
            "2) Подобрать термопары (например, тип K / ТХА или тип N / ТНН в кабельном MI-исполнении с изолированным рабочим спаем "
            "в цельноточеных защитных гильзах — сборки типа Endress+Hauser iTHERM / WIKA TC10 / ABB SensyTemp);\n"
            "3) Рассчитать длину погружения и прочность термокарманов в штуцерах колонны, обеспечить плотный контакт чувствительного элемента с дном гильзы;\n"
            "4) Организовать прокладку компенсационных кабелей, искробезопасное подключение (Ex i) и контроль достоверности профиля."
        ),
        "engineering_check_note": (
            "Температурный профиль колонны формируется совокупностью точек от верха (~100–130 °C) до зоны питания и куба (~350–380 °C). "
            "По температурному диапазону подходят типы K и N, однако решающее значение для ресурса имеет выбор материала и конструкции "
            "защитной гильзы под сернистую среду, давление и точку врезки на конкретной тарелке."
        ),
        "technical_sources": [
            "Endress+Hauser — iTHERM ModuLine TM131 / Multipoint temperature assemblies for distillation columns",
            "WIKA — Industrial thermocouples with barstock thermowells for refineries (Model TC10 / TW10)",
            "ABB — SensyTemp TSP111 / TSP121 modular process thermocouples"
        ],
    },
    {
        "id": "ind_refinery_hydrotreating",
        "num": 11,
        "industry_group": "Нефтеперерабатывающая промышленность (НПЗ • АТПП УГНТУ)",
        "badge_label": "Нефтепереработка • Дополнительное сложное направление",
        "title": "Каталитический реактор гидроочистки (многозонный профиль)",
        "object_short": "Входная зона и слои стационарного катализатора по высоте реактора (водородсодержащая среда)",
        "object_type": "Многоточечная зондовая сборка (multipoint) по высоте слоёв катализатора с резервированием каналов",
        "channel_purpose": "Многоточечный температурный профиль аппарата (колонна / слои катализатора реактора)",
        "measured_qty": (
            "Продольный и радиальный температурный профиль реактора гидроочистки: "
            "температура газосырьевой смеси на входе в реактор, распределение температур по высоте каждого слоя "
            "катализатора, зоны подачи охлаждающего водородсодержащего газа (квенча) и температура на выходе"
        ),
        "measurement_objects_list": [
            "Входная зона газосырьевой смеси в реактор (контроль температуры инициации реакций гидрообессеривания)",
            "Слои стационарного катализатора по высоте реактора (многоточечный контроль перепада температур ΔT по слоям)",
            "Межслоевые зоны подачи холодного водородсодержащего газа (квенч-зоны для съёма экзотермического тепла)",
            "Выходной коллектор реактора (оценка суммарного теплового эффекта и активности катализатора)"
        ],
        "t_min": 280.0,
        "t_max": 430.0,
        "env": "восстановительная",
        "prio": "стабильность и точность",
        "special_conditions": (
            "СЛОЖНЫЙ РЕЖИМ ЭКСПЛУАТАЦИИ: высокое парциальное давление водорода (восстановительная среда), наличие сероводорода (H₂S), "
            "высокое рабочее давление в корпусе реактора и экзотермический характер реакций гидроочистки. "
            "Требуется многоточечное измерение по высоте слоёв катализатора (многозонные термометрические подвески/зонды, "
            "например WIKA TC95 / Endress+Hauser iTHERM MultiSens) в толстостенной герметичной защитной гильзе высокого давления "
            "и обязательное резервирование критических измерительных каналов (дублирование / голосование 2oo3 для ПАЗ). "
            "Не допускается назначать параметры датчика без проверки паспорта производителя на стойкость к водородной деградации."
        ),
        "automation_task": (
            "• Непрерывный контроль температурного профиля по высоте реактора и в каждом слое катализатора;\n"
            "• Раннее обнаружение локальных перегревов («горячих точек» / hot spots) и неравномерности распределения потока в слое;\n"
            "• Контроль экзотермического характера процесса (оценка ΔT по слоям и управление подачей холодного водородсодержащего газа — квенча);\n"
            "• Формирование предупредительной и аварийной сигнализации/блокировки при отклонении температуры от регламентного окна;\n"
            "• Повышение отказоустойчивости за счёт резервирования измерительных каналов."
        ),
        "kip_task": (
            "1) Применить многоточечную термопару в единой защитной арматуре высокого давления (типа WIKA TC95 или "
            "Endress+Hauser iTHERM MultiSens Flex/Linear) для одновременного измерения профиля по всем слоям катализатора;\n"
            "2) Учесть восстановительную водородсодержащую атмосферу с H₂S: выбрать термопару типа N (ТНН) или K (ТХА) "
            "в герметичной минеральной изоляции с коррозионностойкой оболочкой (AISI 321 / 316Ti / Incoloy 825 / Hastelloy — строго по паспорту "
            "производителя, так как диффузия водорода вызывает дрейф стандартных термоэлектродов без герметичной защиты);\n"
            "3) Предусмотреть резервирование каналов (дублирование датчиков на критических отметках слоёв и диагностику обрыва/КЗ);\n"
            "4) Обеспечить герметичность штуцера высокого давления, взрывозащиту Ex i / Ex d и передачу профиля на мнемосхему оператора."
        ),
        "engineering_check_note": (
            "Условная рекомендация для восстановительной (водородсодержащей) среды: по температурному диапазону (~280–430 °C) "
            "и стойкости к дрейфу предпочтителен тип N (нихросил–нисил) или тип K в герметичном MI-исполнении, но конкретная "
            "марка оболочки, класс давления гильзы и схема резервирования подбираются строго по подтверждённым каталогам (WIKA TC95 / Endress+Hauser MultiSens)."
        ),
        "technical_sources": [
            "WIKA — Multipoint thermocouple assemblies for hydrotreating & catalytic reactors (Model TC95)",
            "Endress+Hauser — iTHERM MultiSens TMS01 / TMS02 multipoint temperature profiling in reactors",
            "ABB — SensyTemp multipoint thermocouple assemblies for petrochemical reactors"
        ],
    },
]

DIAGNOSTIC_CASES_CAT_B = [
    {
        "num": 1,
        "title": "Обрыв термопары (разрыв термоэлектрического контура)",
        "cause": "Механическое разрушение, перегорание рабочего спая, обрыв компенсационного провода или ослабление клеммы.",
        "channel_effect": (
            "Сопротивление измерительной цепи возрастает до бесконечности ($R_{\\text{контура}} \\to \\infty$), "
            "термоток прекращается ($I = 0\\text{ мкА}$). Вторичный прибор с функцией контроля обрыва фиксирует "
            "выход входного сигнала за верхний или нижний предел шкалы (индикация «ОБРЫВ» / «BURN-OUT»)."
        ),
        "reliability": "Недостоверно (отказ канала измерения; регулирование переводится в безопасный ручной режим / аварийный останов).",
        "stand_hint": "Можно смоделировать на Стенде №1 и Стенде №2, выбрав состояние цепи «Обрыв термоэлектрического контура».",
    },
    {
        "num": 2,
        "title": "Короткое замыкание термоэлектродов (паразитный спай)",
        "cause": "Повреждение изоляции термоэлектродов или компенсационного кабеля в промежуточной зоне при температуре $T_{\\text{кз}}$, попадание влаги или токопроводящей пыли.",
        "channel_effect": (
            "Образуется паразитный спай в точке замыкания, шунтирующий рабочий горячий спай. "
            "На вход прибора поступает искажённая термо-ЭДС, соответствующая температуре в точке КЗ $T_{\\text{кз}}$ "
            "(с учётом делителя сопротивлений участков цепи), а не реальной температуре объекта $T_{\\text{hot}}$."
        ),
        "reliability": "Недостоверно (опасное скрытое занижение показаний: прибор показывает температуру кабельной трассы вместо перегрева печи).",
        "stand_hint": "Можно смоделировать на Стенде №1 и Стенде №2, выбрав состояние цепи «Паразитный спай (КЗ)» и задав T_кз.",
    },
    {
        "num": 3,
        "title": "Переполюсовка термоэлектродов или компенсационных проводов",
        "cause": "Ошибочное подключение положительного (+) и отрицательного (−) проводников на клеммах головки термопары, промежуточной коробки или входа контроллера.",
        "channel_effect": (
            "Термо-ЭДС поступает на вход прибора с обратным знаком ($-E$). При температуре выше температуры холодного спая "
            "прибор индицирует отрицательную (заниженную) температуру и с ростом реального нагрева показывает дальнейшее "
            "«охлаждение» объекта."
        ),
        "reliability": "Недостоверно (инверсия знака сигнала приводит к неправильной работе регулятора нагрева и разгону температуры).",
        "stand_hint": "Можно проверить на Стенде №2, поменяв местами материалы ветвей A и B (знак S_пары и E_ген инвертируется).",
    },
    {
        "num": 4,
        "title": "Неправильная температура холодного спая (ошибка компенсации)",
        "cause": "Неисправность датчика температуры клеммной колодки (термистора/ТС), отключение программной компенсации холодного спая (КХС) или удлинение обычным медным проводом вместо компенсационного в зоне перепада температур.",
        "channel_effect": (
            "Термопара генерирует ЭДС, пропорциональную разности $(T_{\\text{hot}} - T_{\\text{cold}})$. "
            "Если фактическая температура свободных концов $T_{\\text{cold}}$ отличается от значения, принятого прибором "
            "(например, 0 °C или 20 °C), возникает систематическая аддитивная погрешность измерения температуры."
        ),
        "reliability": "Частично недостоверно (систематическое смещение показаний на величину ошибки определения T_cold).",
        "stand_hint": "Наглядно проверяется на Стенде №1 изменением ползунка «Температура холодного спая T_cold».",
    },
    {
        "num": 5,
        "title": "Выход измеряемой температуры за рабочий диапазон датчика",
        "cause": "Превышение допустимого верхнего предела эксплуатации (например, нагрев типа J выше 750 °C или типа K выше 1200 °C на воздухе) либо работа типа B ниже +50 °C.",
        "channel_effect": (
            "При перегреве происходит ускоренное окисление, рекристаллизация и необратимый дрейф НСХ вплоть до перегорания "
            "термоэлектродов. Для типа B ниже +50 °C термо-ЭДС близка к нулю и неоднозначна (кривая имеет минимум)."
        ),
        "reliability": "Недостоверно (необратимая деградация градуировки или зона нечувствительности ниже +50 °C для типа B).",
        "stand_hint": "Проверяется алгоритмом подбора по полному интервалу [T_min, T_max] и паспорту ограничений.",
    },
    {
        "num": 6,
        "title": "Несоответствие защитной конструкции рабочей среде",
        "cause": "Установка термопары без защитной гильзы или выбор материала чехла, нестойкого к химической агрессии, абразивному потоку, давлению или вибрации (например, железный чехол во влажной кислой среде или металлический чехол при 1450 °C).",
        "channel_effect": (
            "Быстрая коррозия, растворение или оплавление защитной арматуры, последующее загрязнение термоэлектродов "
            "(особенно критично для платинородиевых пар S, R, B без газоплотного керамического чехла) и потеря герметичности узла."
        ),
        "reliability": "Недостоверно (прогрессирующий уход градуировки и разрушение датчика).",
        "stand_hint": "Учитывается при выборе типа термопары и защитной арматуры в производственных сценариях Категории А.",
    },
    {
        "num": 7,
        "title": "Неизвестная или неподходящая рабочая атмосфера",
        "cause": "Применение датчика без достоверных сведений о составе газовой среды либо эксплуатация в восстановительной/малокислородной атмосфере без учёта стойкости сплавов (или попадание воздуха в вакуумную печь с вольфрам-рениевой термопарой).",
        "channel_effect": (
            "У никель-хромовых термопар (особенно типа K) при дефиците кислорода развивается селективное окисление хрома "
            "(«зелёная гниль») с резким занижением ЭДС. Вольфрам-рениевые пары в окислительной среде мгновенно сгорают."
        ),
        "reliability": "Недостоверно (условный выбор невозможен без уточнения состава атмосферы; для W-Re — аварийный отказ).",
        "stand_hint": "Проверяется в алгоритме подбора при выборе сред «неизвестная», «восстановительная» или «среда с пониженным содержанием кислорода».",
    },
]

ALGORITHM_TESTS_CAT_C = [
    {
        "num": 1,
        "title": "Тест 1. Температура ниже табличного диапазона НСХ",
        "desc": "Ввод T_min = −250 °C (ниже нижней границы таблиц типов J и S/R) и T_max = +1700 °C в воздушной среде.",
        "t_min": -250.0,
        "t_max": 1700.0,
        "env": "воздушная / окислительная",
        "prio": "универсальность",
        "expected": "Отказ (error): ни одна термопара не перекрывает полный интервал от −250 до +1700 °C.",
    },
    {
        "num": 2,
        "title": "Тест 2. Температура выше табличного диапазона НСХ",
        "desc": "Ввод T_min = 1800 °C, T_max = 2000 °C в вакууме — зона между табличным пределом типа B (+1820 °C) и подтверждённым интервалом W-Re (2200–2500 °C).",
        "t_min": 1800.0,
        "t_max": 2000.0,
        "env": "вакуум",
        "prio": "универсальность",
        "expected": "Отказ (error): в теоретической базе реферата нет подтверждённой термопары для 1800–2000 °C.",
    },
    {
        "num": 3,
        "title": "Тест 3. Неизвестная рабочая среда",
        "desc": "Диапазон 2200…2500 °C при выборе рабочей среды «неизвестная» (проверка защиты от небезопасной рекомендации W-Re).",
        "t_min": 2200.0,
        "t_max": 2500.0,
        "env": "неизвестная",
        "prio": "универсальность",
        "expected": "Отказ (error): при неизвестной среде вольфрам-рениевые термопары не рекомендуются из-за риска окисления.",
    },
    {
        "num": 4,
        "title": "Тест 4. Некорректный ввод: T_min больше T_max",
        "desc": "Проверка валидации границ интервала: T_min = 400 °C > T_max = 100 °C.",
        "t_min": 400.0,
        "t_max": 100.0,
        "env": "воздушная / окислительная",
        "prio": "универсальность",
        "expected": "Отказ (error): сообщение об ошибке ввода температурного интервала (T_min < T_max).",
    },
    {
        "num": 5,
        "title": "Тест 5. Верхняя граница на пределе подтверждённого рабочего диапазона",
        "desc": "Проверка режима 1700…1800 °C в инертной среде (тип B: нижний предел > 50 °C соблюдён, верхний рабочий предел в реферате не выделен).",
        "t_min": 1700.0,
        "t_max": 1800.0,
        "env": "инертная",
        "prio": "стабильность и точность",
        "expected": "Условная рекомендация (conditional): Тип B (ТПР) с предупреждением о сверке с паспортом.",
    },
    {
        "num": 6,
        "title": "Тест 6. Отсутствие подходящей термопары (проверка нижнего порога типа B)",
        "desc": "Ввод T_min = 20 °C, T_max = 1500 °C на воздухе: неблагородные пары не выдерживают 1500 °C, а тип B не работает ниже +50 °C (типы S/R перекрывают −50…+1600 °C).",
        "t_min": 20.0,
        "t_max": 1500.0,
        "env": "воздушная / окислительная",
        "prio": "стабильность и точность",
        "expected": "Подбор типов S / R (до +1600 °C) и отклонение типа B из-за T_min = 20 °C < 50 °C.",
    },
    {
        "num": 7,
        "title": "Тест 7. Проверка совпадения выбранного датчика с заданными условиями",
        "desc": "Низкотемпературный режим −50…+100 °C в воздушной среде с приоритетом «универсальность».",
        "t_min": -50.0,
        "t_max": 100.0,
        "env": "воздушная / окислительная",
        "prio": "универсальность",
        "expected": "Рекомендация (ok): Тип T (ТМК — Медь / Константан, −200…+350 °C).",
    },
]


def _apply_industrial_scenario_to_state(sc: dict) -> None:
    """Заполняет поля формы подбора и сохраняет контекст выбранного производственного сценария."""
    ch_purpose = sc.get("channel_purpose", CHANNEL_PURPOSE_OPTIONS[0])
    st.session_state["sel_t_min"] = float(sc["t_min"])
    st.session_state["sel_t_max"] = float(sc["t_max"])
    st.session_state["sel_env"] = sc["env"]
    st.session_state["sel_prio"] = sc["prio"]
    st.session_state["sel_channel_purpose"] = ch_purpose
    st.session_state["sel_object_type"] = sc["object_type"]
    st.session_state["sel_special_conditions"] = sc["special_conditions"]
    st.session_state["sel_active_industrial_id"] = sc["id"]
    st.session_state["sel_active_mode_label"] = f"Производственный сценарий №{sc['num']}: {sc['title']}"
    st.session_state["selector_committed"] = {
        "t_min": float(sc["t_min"]),
        "t_max": float(sc["t_max"]),
        "env": sc["env"],
        "prio": sc["prio"],
        "channel_purpose": ch_purpose,
        "object_type": sc["object_type"],
        "special_conditions": sc["special_conditions"],
        "industrial_scenario": sc,
        "test_case": None,
    }


def _apply_algorithm_test_to_state(tc_item: dict) -> None:
    """Загружает контрольный тест алгоритма (Категория В) без смешивания с производственными сценариями."""
    st.session_state["sel_t_min"] = float(tc_item["t_min"])
    st.session_state["sel_t_max"] = float(tc_item["t_max"])
    st.session_state["sel_env"] = tc_item["env"]
    st.session_state["sel_prio"] = tc_item["prio"]
    st.session_state["sel_channel_purpose"] = CHANNEL_PURPOSE_OPTIONS[0]
    st.session_state["sel_object_type"] = "Контрольный тест алгоритма (не производственный объект)"
    st.session_state["sel_special_conditions"] = tc_item["desc"]
    st.session_state["sel_active_industrial_id"] = None
    st.session_state["sel_active_mode_label"] = tc_item["title"]
    st.session_state["selector_committed"] = {
        "t_min": float(tc_item["t_min"]),
        "t_max": float(tc_item["t_max"]),
        "env": tc_item["env"],
        "prio": tc_item["prio"],
        "channel_purpose": CHANNEL_PURPOSE_OPTIONS[0],
        "object_type": "Контрольный тест алгоритма (не производственный объект)",
        "special_conditions": tc_item["desc"],
        "industrial_scenario": None,
        "test_case": tc_item,
    }


def render_thermocouple_selector() -> None:
    """
    Интерактивный учебный инженерный модуль «Подбор термопары по условиям эксплуатации»
    для специальности «Автоматизация технологических процессов и производств» (АТПП, УГНТУ).
    Разделён на три самостоятельные категории:
    - Категория А. Производственные сценарии (11 технологических процессов, включая нефтепереработку).
    - Категория Б. Диагностика измерительной цепи (7 характерных неисправностей).
    - Категория В. Контрольные испытания алгоритма (7 проверочных тестов).
    """
    is_mobile_view = (st.session_state.get("chart_display_mode") == "Смартфон (320–430 px)")

    st.header("🧭 Подбор термопары по условиям эксплуатации")
    st.markdown(
        '<div class="kip-section-intro">'
        'Учебный инженерный модуль для специальности <strong>«Автоматизация технологических процессов и производств» (УГНТУ)</strong>. '
        'Выбор термопары выполняется не только по температуре <strong>[T_min, T_max]</strong> и <strong>рабочей среде</strong>, '
        'но и с учётом <strong>назначения измерительного канала</strong> (погружное измерение потока, контактное измерение поверхности труб tube-skin, '
        'многоточечный профиль колонны или реактора), конструкции защитной гильзы и задачи автоматизации.'
        '</div>',
        unsafe_allow_html=True,
    )

    if "sel_t_min" not in st.session_state:
        st.session_state["sel_t_min"] = 160.0
    if "sel_t_max" not in st.session_state:
        st.session_state["sel_t_max"] = 300.0
    if "sel_env" not in st.session_state:
        st.session_state["sel_env"] = "воздушная / окислительная"
    if "sel_prio" not in st.session_state:
        st.session_state["sel_prio"] = "повышенная чувствительность"
    if "sel_channel_purpose" not in st.session_state:
        st.session_state["sel_channel_purpose"] = CHANNEL_PURPOSE_OPTIONS[0]
    if "sel_object_type" not in st.session_state:
        st.session_state["sel_object_type"] = INDUSTRIAL_SCENARIOS_CAT_A[0]["object_type"]
    if "sel_special_conditions" not in st.session_state:
        st.session_state["sel_special_conditions"] = INDUSTRIAL_SCENARIOS_CAT_A[0]["special_conditions"]
    if "sel_active_industrial_id" not in st.session_state:
        st.session_state["sel_active_industrial_id"] = None
    if "sel_active_mode_label" not in st.session_state:
        st.session_state["sel_active_mode_label"] = "Ручной ввод параметров"
    if "selector_committed" not in st.session_state:
        st.session_state["selector_committed"] = None

    # =================================================================
    # ТРИ САМОСТОЯТЕЛЬНЫЕ КАТЕГОРИИ СЦЕНАРИЕВ
    # =================================================================
    cat_tabs = st.tabs([
        f"🏭 Категория А. Производственные сценарии ({len(INDUSTRIAL_SCENARIOS_CAT_A)})",
        f"🩺 Категория Б. Диагностика измерительной цепи ({len(DIAGNOSTIC_CASES_CAT_B)})",
        f"🧪 Категория В. Контрольные испытания алгоритма ({len(ALGORITHM_TESTS_CAT_C)})",
    ])

    # -----------------------------------------------------------------
    # КАТЕГОРИЯ А. ПРОИЗВОДСТВЕННЫЕ СЦЕНАРИИ
    # -----------------------------------------------------------------
    with cat_tabs[0]:
        st.subheader("🏭 Категория А. Производственные сценарии (АТПП • УГНТУ)")
        st.caption(
            "Выберите технологический процесс (включая установки нефтепереработки — АВТ и реактор гидроочистки): "
            "приложение автоматически заполнит параметры формы подбора, объекты измерения, условия эксплуатации, "
            "задачу автоматизации и раздел «Роль специалиста КИПиА»."
        )

        active_ind_id = st.session_state.get("sel_active_industrial_id")

        def _render_industrial_scenario_card(sc: dict) -> None:
            is_selected = (active_ind_id == sc["id"])
            badge_txt = sc.get("badge_label", "Общепромышленный процесс")
            with st.container(border=True):
                st.caption(f"🏷️ {badge_txt}")
                st.markdown(f"**{sc['num']}. {sc['title']}**")
                st.caption(
                    f"Объекты: {sc['object_short']} • Диапазон: {sc['t_min']:.0f}…{sc['t_max']:.0f} °C • "
                    f"Среда: {sc['env']}"
                )
                btn_text = (
                    f"✅ Выбран: {sc['title']}"
                    if is_selected
                    else f"Выбрать процесс: {sc['title']}"
                )
                if st.button(
                    btn_text,
                    key=f"ind_scen_btn_{sc['id']}",
                    type="primary" if is_selected else "secondary",
                    use_container_width=True,
                ):
                    _apply_industrial_scenario_to_state(sc)
                    st.rerun()

        if is_mobile_view:
            for sc in INDUSTRIAL_SCENARIOS_CAT_A:
                _render_industrial_scenario_card(sc)
        else:
            for row_start in range(0, len(INDUSTRIAL_SCENARIOS_CAT_A), 2):
                row_items = INDUSTRIAL_SCENARIOS_CAT_A[row_start:row_start + 2]
                cols = st.columns(2)
                for col, sc in zip(cols, row_items):
                    with col:
                        _render_industrial_scenario_card(sc)

        # Отдельная детальная карточка выбранного производственного сценария
        selected_sc = next(
            (item for item in INDUSTRIAL_SCENARIOS_CAT_A if item["id"] == active_ind_id),
            None,
        )
        if selected_sc is not None:
            st.markdown("---")
            with st.container(border=True):
                st.markdown(
                    f'<div class="kip-status-banner kip-status-banner--ok">'
                    f'🏭 Установка / процесс №{selected_sc["num"]}: {html.escape(selected_sc["title"])}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                if selected_sc.get("industry_group"):
                    st.caption(f"Отраслевой профиль: **{selected_sc['industry_group']}**")

                objs_list = selected_sc.get("measurement_objects_list")
                if objs_list:
                    objs_md = "\n".join(f"  - {item}" for item in objs_list)
                    st.markdown(f"**Объекты измерения:**\n{objs_md}")
                else:
                    st.markdown(f"- **Объект измерения:** {selected_sc['object_short']}")

                st.markdown(
                    f"- **Измеряемая величина:** {selected_sc['measured_qty']}\n"
                    f"- **Назначение измерительного канала:** `{selected_sc.get('channel_purpose', CHANNEL_PURPOSE_OPTIONS[0])}`\n"
                    f"- **Условия эксплуатации (диапазон и среда):** `{selected_sc['t_min']:.0f}…{selected_sc['t_max']:.0f} °C` "
                    f"(среда: *{selected_sc['env']}*, приоритет: *{selected_sc['prio']}*)\n"
                    f"- **Особенности монтажа и защитной арматуры:** {selected_sc['special_conditions']}"
                )

                if is_mobile_view:
                    with st.container(border=True):
                        st.markdown("#### ⚙️ Задача автоматизации")
                        st.markdown(selected_sc["automation_task"])
                    with st.container(border=True):
                        st.markdown("#### 🛠️ Роль специалиста КИПиА")
                        st.markdown(selected_sc["kip_task"])
                else:
                    t_col1, t_col2 = st.columns(2)
                    with t_col1:
                        with st.container(border=True):
                            st.markdown("#### ⚙️ Задача автоматизации")
                            st.markdown(selected_sc["automation_task"])
                    with t_col2:
                        with st.container(border=True):
                            st.markdown("#### 🛠️ Роль специалиста КИПиА")
                            st.markdown(selected_sc["kip_task"])

                st.caption(f"📐 **Техническая проверка применимости:** {selected_sc['engineering_check_note']}")
                if selected_sc.get("technical_sources"):
                    src_lines = " | ".join(selected_sc["technical_sources"])
                    st.caption(f"📚 **Подтверждённые технические источники:** {src_lines}")
        else:
            st.info(
                f"👆 Нажмите на любой из {len(INDUSTRIAL_SCENARIOS_CAT_A)} производственных сценариев выше "
                "(включая процессы нефтепереработки №9–11), чтобы открыть карточку установки и загрузить параметры в форму подбора."
            )

    # -----------------------------------------------------------------
    # КАТЕГОРИЯ Б. ДИАГНОСТИКА ИЗМЕРИТЕЛЬНОЙ ЦЕПИ
    # -----------------------------------------------------------------
    with cat_tabs[1]:
        st.subheader("🩺 Категория Б. Диагностика измерительной цепи")
        st.caption(
            "Типовые отказы и методические нарушения в канале измерения температуры с термопарой: "
            "причины возникновения, поведение измерительного канала и оценка достоверности показаний."
        )

        diag_titles = [f"{d['num']}. {d['title']}" for d in DIAGNOSTIC_CASES_CAT_B]
        selected_diag_title = st.selectbox(
            "Выберите диагностический случай для разбора:",
            options=diag_titles,
            key="diag_case_selectbox",
        )
        diag_item = DIAGNOSTIC_CASES_CAT_B[diag_titles.index(selected_diag_title)]

        with st.container(border=True):
            st.markdown(f"#### Случай №{diag_item['num']}: {diag_item['title']}")
            st.markdown(f"- **Причина возникновения:** {diag_item['cause']}")
            st.markdown(f"- **Что происходит с измерительным каналом:** {diag_item['channel_effect']}")
            st.markdown(f"- **Достоверность показаний:** {diag_item['reliability']}")
            st.caption(f"🔬 *Проверка в симуляторе:* {diag_item['stand_hint']}")

        with st.expander("📋 Сводная таблица всех 7 диагностических случаев", expanded=False):
            diag_df = pd.DataFrame([
                {
                    "№": d["num"],
                    "Неисправность / нарушение": d["title"],
                    "Реакция измерительного канала": d["channel_effect"],
                    "Достоверность показаний": d["reliability"],
                }
                for d in DIAGNOSTIC_CASES_CAT_B
            ])
            st.dataframe(diag_df, use_container_width=True, hide_index=True)

    # -----------------------------------------------------------------
    # КАТЕГОРИЯ В. КОНТРОЛЬНЫЕ ИСПЫТАНИЯ АЛГОРИТМА
    # -----------------------------------------------------------------
    with cat_tabs[2]:
        st.subheader("🧪 Категория В. Контрольные испытания алгоритма")
        st.caption(
            "Проверочные граничные тесты для верификации логики подбора термопары "
            "(не являются производственными процессами и выделены отдельно от Категории А)."
        )

        if is_mobile_view:
            for tc_item in ALGORITHM_TESTS_CAT_C:
                with st.container(border=True):
                    st.markdown(f"**{tc_item['title']}**")
                    st.caption(tc_item["desc"])
                    st.caption(f"Ожидаемый результат: {tc_item['expected']}")
                    if st.button(
                        f"Запустить: {tc_item['title']}",
                        key=f"alg_test_btn_{tc_item['num']}",
                        use_container_width=True,
                    ):
                        _apply_algorithm_test_to_state(tc_item)
                        st.rerun()
        else:
            for row_start in range(0, len(ALGORITHM_TESTS_CAT_C), 2):
                row_items = ALGORITHM_TESTS_CAT_C[row_start:row_start + 2]
                cols = st.columns(2)
                for col, tc_item in zip(cols, row_items):
                    with col:
                        with st.container(border=True):
                            st.markdown(f"**{tc_item['title']}**")
                            st.caption(tc_item["desc"])
                            st.caption(f"Ожидаемый результат: {tc_item['expected']}")
                            if st.button(
                                f"Загрузить тест №{tc_item['num']}",
                                key=f"alg_test_btn_{tc_item['num']}",
                                use_container_width=True,
                            ):
                                _apply_algorithm_test_to_state(tc_item)
                                st.rerun()

        if st.button("🧪 Выполнить все 7 контрольных тестов и показать протокол", key="run_all_cat_c_tests_btn", use_container_width=True):
            protocol_rows = []
            for tc_item in ALGORITHM_TESTS_CAT_C:
                res = evaluate_thermocouple_selection(
                    tc_item["t_min"],
                    tc_item["t_max"],
                    tc_item["env"],
                    tc_item["prio"],
                )
                prim_title = res["primary"]["title"] if res["primary"] else "Отказ (не найден)"
                alt_titles = ", ".join(a["spec"]["code"] for a in res["alternatives"]) if res["alternatives"] else "—"
                ex_count = (
                    len(filter_industrial_examples(res["primary"]["code"], tc_item["t_min"], tc_item["t_max"], tc_item["env"]))
                    if res["primary"] and res["status"] != "error" else 0
                )
                protocol_rows.append({
                    "Контрольный тест": tc_item["title"],
                    "Вход [T_min, T_max], среда": f"{tc_item['t_min']:.0f}…{tc_item['t_max']:.0f} °C ({tc_item['env']})",
                    "Статус": res["status"],
                    "Фактический результат": prim_title,
                    "Альтернативы": alt_titles,
                    "Примеры оборудования": f"{ex_count} шт." if ex_count > 0 else "Не выводятся (отказ)",
                })
            st.dataframe(pd.DataFrame(protocol_rows), use_container_width=True, hide_index=True)

    # =================================================================
    # ФОРМА ПАРАМЕТРОВ УСЛОВИЙ ЭКСПЛУАТАЦИИ (АВТОЗАПОЛНЯЕТСЯ ИЗ КАТЕГОРИИ А/В ИЛИ ВРУЧНУЮ)
    # =================================================================
    st.markdown("---")
    with st.form("thermocouple_selector_form"):
        st.markdown('<div class="kip-param-group-title">🔧 Параметры условий эксплуатации</div>', unsafe_allow_html=True)
        st.caption(f"Источник текущих параметров формы: **{st.session_state.get('sel_active_mode_label', 'Ручной ввод параметров')}**")

        env_options = [
            "воздушная / окислительная",
            "инертная",
            "восстановительная",
            "среда с пониженным содержанием кислорода",
            "вакуум",
            "неизвестная"
        ]
        current_env = st.session_state["sel_env"] if st.session_state["sel_env"] in env_options else env_options[0]
        prio_options = [
            "универсальность",
            "стабильность и точность",
            "повышенная чувствительность"
        ]
        current_prio = st.session_state["sel_prio"] if st.session_state["sel_prio"] in prio_options else prio_options[0]
        cur_purpose = (
            st.session_state["sel_channel_purpose"]
            if st.session_state.get("sel_channel_purpose") in CHANNEL_PURPOSE_OPTIONS
            else CHANNEL_PURPOSE_OPTIONS[0]
        )

        purpose_in = st.selectbox(
            "Назначение измерительного канала:",
            options=CHANNEL_PURPOSE_OPTIONS,
            index=CHANNEL_PURPOSE_OPTIONS.index(cur_purpose),
            help="Разделяет погружное измерение потока среды, контактное измерение поверхности труб (tube-skin), многоточечный профиль колонны/реактора и контроль дымовых газов.",
        )

        if is_mobile_view:
            t_min_in = st.number_input(
                "Минимальная температура, °C:",
                min_value=-270.0,
                max_value=3000.0,
                value=float(st.session_state["sel_t_min"]),
                step=10.0
            )
            t_max_in = st.number_input(
                "Максимальная температура, °C:",
                min_value=-270.0,
                max_value=3000.0,
                value=float(st.session_state["sel_t_max"]),
                step=10.0
            )
            env_in = st.selectbox(
                "Рабочая среда:",
                options=env_options,
                index=env_options.index(current_env)
            )
            prio_in = st.selectbox(
                "Приоритет выбора:",
                options=prio_options,
                index=prio_options.index(current_prio)
            )
            obj_type_in = st.text_input(
                "Тип измеряемого объекта:",
                value=str(st.session_state.get("sel_object_type", "")),
            )
            spec_cond_in = st.text_input(
                "Особые условия эксплуатации и монтаж:",
                value=str(st.session_state.get("sel_special_conditions", "")),
            )
        else:
            col_in1, col_in2 = st.columns(2)
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
            col_in3, col_in4 = st.columns(2)
            with col_in3:
                env_in = st.selectbox(
                    "Рабочая среда:",
                    options=env_options,
                    index=env_options.index(current_env)
                )
            with col_in4:
                prio_in = st.selectbox(
                    "Приоритет выбора:",
                    options=prio_options,
                    index=prio_options.index(current_prio)
                )
            col_in5, col_in6 = st.columns(2)
            with col_in5:
                obj_type_in = st.text_input(
                    "Тип измеряемого объекта:",
                    value=str(st.session_state.get("sel_object_type", "")),
                )
            with col_in6:
                spec_cond_in = st.text_input(
                    "Особые условия эксплуатации и монтаж:",
                    value=str(st.session_state.get("sel_special_conditions", "")),
                )

        run_selection = st.form_submit_button(
            "🔍 Подобрать термопару",
            type="primary",
            use_container_width=True
        )

    if run_selection:
        prev_comm = st.session_state.get("selector_committed") or {}
        same_as_scenario = (
            prev_comm.get("industrial_scenario") is not None
            and float(t_min_in) == float(prev_comm.get("t_min", -9999))
            and float(t_max_in) == float(prev_comm.get("t_max", -9999))
            and env_in == prev_comm.get("env")
            and prio_in == prev_comm.get("prio")
            and purpose_in == prev_comm.get("channel_purpose", CHANNEL_PURPOSE_OPTIONS[0])
        )
        kept_ind = prev_comm.get("industrial_scenario") if same_as_scenario else None
        if not same_as_scenario:
            st.session_state["sel_active_industrial_id"] = None
            st.session_state["sel_active_mode_label"] = "Ручной ввод параметров"

        st.session_state["sel_t_min"] = t_min_in
        st.session_state["sel_t_max"] = t_max_in
        st.session_state["sel_env"] = env_in
        st.session_state["sel_prio"] = prio_in
        st.session_state["sel_channel_purpose"] = purpose_in
        st.session_state["sel_object_type"] = obj_type_in
        st.session_state["sel_special_conditions"] = spec_cond_in
        st.session_state["selector_committed"] = {
            "t_min": t_min_in,
            "t_max": t_max_in,
            "env": env_in,
            "prio": prio_in,
            "channel_purpose": purpose_in,
            "object_type": obj_type_in,
            "special_conditions": spec_cond_in,
            "industrial_scenario": kept_ind,
            "test_case": None,
        }

    if st.session_state["selector_committed"] is None:
        st.info("👆 Выберите производственный сценарий в **Категории А** или задайте параметры вручную и нажмите **«🔍 Подобрать термопару»**.")
        return

    committed = st.session_state["selector_committed"]
    result = evaluate_thermocouple_selection(
        committed["t_min"],
        committed["t_max"],
        committed["env"],
        committed["prio"],
        committed.get("channel_purpose", CHANNEL_PURPOSE_OPTIONS[0]),
    )

    if result["status"] == "error":
        st.markdown(
            '<div class="kip-status-banner kip-status-banner--error">'
            '🚫 Статус подбора: ОТКАЗ В РЕКОМЕНДАЦИИ (подходящий тип термопары не найден)'
            '</div>',
            unsafe_allow_html=True,
        )
        st.error(f"🚫 **Подходящий тип термопары не найден (отказ в рекомендации):**\n\n{result['message']}")
        for w in result["warnings"]:
            st.warning(f"⚠️ {w}")
    else:
        p = result["primary"]
        is_cond = result["status"] in ("warning", "conditional")

        # 1. ЗАМЕТНЫЙ СТАТУС РЕКОМЕНДАЦИИ (условный статус никогда не скрывается)
        if is_cond:
            st.markdown(
                f'<div class="kip-status-banner kip-status-banner--conditional">'
                f'⚠️ УСЛОВНАЯ РЕКОМЕНДАЦИЯ: {html.escape(p["title"])} — требуется обязательная проверка паспорта датчика и условий среды'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="kip-status-banner kip-status-banner--ok">'
                f'🏆 РЕКОМЕНДУЕМЫЙ ТИП ТЕРМОПАРЫ: {html.escape(p["title"])}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # 2. ПЕРВЫЙ БЛОК: Рекомендуемый тип, Температурный диапазон, Материалы электродов, Чувствительность
        st.subheader("1. Ключевые характеристики рекомендуемой термопары")
        render_kpi_cards_grid([
            {
                "label": "Рекомендуемый тип",
                "value": p["title"],
                "sub": f"Обозначение ГОСТ Р 8.585-2001: {p['gost']}",
                "tone": "warn" if is_cond else "normal",
            },
            {
                "label": "Температурный диапазон",
                "value": p["table_range_str"].split("(")[0].strip(),
                "sub": p["work_range_str"],
                "tone": "normal",
            },
            {
                "label": "Материалы электродов",
                "value": p["electrodes"],
                "sub": p["sim_nsh_str"],
                "tone": "normal",
            },
            {
                "label": "Чувствительность",
                "value": p["sensitivity_str"],
                "sub": f"Заданный режим: {committed['t_min']:.0f}…{committed['t_max']:.0f} °C ({committed['env']})",
                "tone": "normal",
            },
        ])

        # 3. ОБОСНОВАНИЕ ВЫБОРА И УЧЁТ УСЛОВИЙ ЭКСПЛУАТАЦИИ
        st.subheader("2. Обоснование выбора и условия эксплуатации")
        with st.container(border=True):
            st.markdown(result["justification"])
            if committed.get("channel_purpose"):
                st.markdown(f"- **Назначение измерительного канала:** {committed['channel_purpose']}")
            if committed.get("object_type"):
                st.markdown(f"- **Тип измеряемого объекта:** {committed['object_type']}")
            if committed.get("special_conditions"):
                st.markdown(f"- **Особые условия эксплуатации и монтаж:** {committed['special_conditions']}")
            st.caption(
                f"**Табличный диапазон НСХ:** {p['table_range_str']}  |  "
                f"**Статус в расчётной базе (Стенд №1):** {p['sim_nsh_str']}"
            )

        ind_sc = committed.get("industrial_scenario")
        if ind_sc is not None:
            if is_mobile_view:
                with st.container(border=True):
                    st.markdown(f"#### ⚙️ Задача автоматизации ({ind_sc['title']})")
                    st.markdown(ind_sc["automation_task"])
                with st.container(border=True):
                    st.markdown("#### 🛠️ Роль специалиста КИПиА")
                    st.markdown(ind_sc["kip_task"])
            else:
                r_col1, r_col2 = st.columns(2)
                with r_col1:
                    with st.container(border=True):
                        st.markdown(f"#### ⚙️ Задача автоматизации ({ind_sc['title']})")
                        st.markdown(ind_sc["automation_task"])
                with r_col2:
                    with st.container(border=True):
                        st.markdown("#### 🛠️ Роль специалиста КИПиА")
                        st.markdown(ind_sc["kip_task"])

        # 4. ОГРАНИЧЕНИЯ ЭКСПЛУАТАЦИИ И ВАЖНЫЕ ПРЕДУПРЕЖДЕНИЯ
        st.subheader("3. Ограничения эксплуатации и предупреждения")
        st.markdown(
            f'<div class="kip-detail-card kip-detail-card--warn">'
            f'<strong>Ограничения применения ({html.escape(p["title"])}):</strong><br/>'
            f'{html.escape(p["limitations"])}'
            f'</div>',
            unsafe_allow_html=True,
        )
        for w in result["warnings"]:
            st.warning(f"⚠️ **Важное предупреждение:** {w}")
        if not committed.get("special_conditions"):
            st.warning(
                "⚠️ **Недостаточно сведений о конструкции узла:** не указаны особые условия монтажа и защитной арматуры. "
                "Перед применением необходимо уточнить конструкцию спая, материал защитной гильзы и документацию производителя."
            )

        # 5. ПРОИЗВОДСТВЕННОЕ ПРИМЕНЕНИЕ И ТИПОВОЕ ОБОРУДОВАНИЕ
        st.markdown("---")
        render_industrial_applications_block(
            result=result,
            t_min=committed["t_min"],
            t_max=committed["t_max"],
            environment=committed["env"]
        )

        # 6. АЛЬТЕРНАТИВНЫЕ ВАРИАНТЫ
        if result["alternatives"]:
            st.markdown("---")
            st.subheader("🔄 Возможные альтернативные варианты")

            def _draw_alt_card(alt_item: dict) -> None:
                alt_sp = alt_item["spec"]
                with st.container(border=True):
                    st.markdown(f"#### {alt_sp['title']}")
                    st.markdown(f"- **Обозначение ГОСТ:** `{alt_sp['gost']}`")
                    st.markdown(f"- **Материалы электродов:** {alt_sp['electrodes']}")
                    st.markdown(f"- **Рабочий диапазон:** {alt_sp['work_range_str']}")
                    st.markdown(f"- **Табличный диапазон:** {alt_sp['table_range_str']}")
                    st.markdown(f"- **Статус в симуляторе:** {alt_sp['sim_nsh_str']}")
                    st.markdown(f"- **Чувствительность:** {alt_sp['sensitivity_str']}")
                    st.markdown(f"- **Пояснение:** {alt_item['note']}")
                    st.caption(f"⚠️ *Ограничения:* {alt_sp['limitations']}")

            if is_mobile_view:
                for alt_item in result["alternatives"]:
                    _draw_alt_card(alt_item)
            else:
                alt_cols = st.columns(len(result["alternatives"]))
                for idx, alt_item in enumerate(result["alternatives"]):
                    with alt_cols[idx]:
                        _draw_alt_card(alt_item)

    if result.get("rejected_reasons"):
        st.markdown("---")
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
        "📌 **Примечание о достоверности:** Выбор выполнен по учебно-справочным данным реферата и отраслевым "
        "каталогам промышленных средств измерений (WIKA, ABB, Endress+Hauser). При реальном промышленном внедрении "
        "необходимо свериться с паспортом конкретного датчика, требованиями ГОСТ Р 8.585-2001, диаметром термоэлектродов, "
        "конструкцией защитной арматуры (чехла) и характеристиками вторичного измерительного прибора."
    )


# =====================================================================
# 11. НИЖНЯЯ НАВИГАЦИЯ МЕЖДУ РЕЖИМАМИ И ГЛАВНЫЙ МАРШРУТИЗАТОР ПРИЛОЖЕНИЯ
# =====================================================================
def _bottom_nav_to_section(target_section: str) -> None:
    """Переходит в указанный основной раздел из нижней панели навигации."""
    navigate_to_section(target_section)


def _bottom_nav_to_stand(target_stand: str) -> None:
    """Переключает активный исследовательский стенд из нижней панели навигации и прокручивает вверх."""
    if target_stand in LAB_STAND_OPTIONS:
        st.session_state["active_lab_stand"] = target_stand
    navigate_to_section("Исследовательские стенды")
    request_page_scroll("kip-page-top-anchor")


def render_bottom_section_navigation() -> None:
    """
    Отрисовывает в самом низу каждой секции понятный блок перехода к следующему режиму
    (без необходимости прокручивать страницу обратно вверх).
    """
    active_section = st.session_state["active_section"]
    active_stand = st.session_state["active_lab_stand"]
    is_mobile_view = (st.session_state.get("chart_display_mode") == "Смартфон (320–430 px)")

    if active_section == "Теоретическая часть":
        actions = [
            ("🔬 Далее: Исследовательские стенды (Стенд №1) ➡️", "stand", LAB_STAND_OPTIONS[0], "primary"),
            ("🧭 Перейти к подбору термопары", "section", "Подбор термопары", "secondary"),
            ("📘 Перейти к справочному помощнику", "section", "Справочный помощник", "secondary"),
        ]
    elif active_section == "Исследовательские стенды":
        if active_stand.startswith("Стенд №1"):
            actions = [
                ("🔬 Далее: Стенд №2 (Пары металлов) ➡️", "stand", LAB_STAND_OPTIONS[1], "primary"),
                ("🧭 Перейти к подбору термопары", "section", "Подбор термопары", "secondary"),
                ("📚 Вернуться к теории", "section", "Теоретическая часть", "secondary"),
            ]
        else:
            actions = [
                ("🧭 Далее: Подбор термопары ➡️", "section", "Подбор термопары", "primary"),
                ("📘 Перейти к справочному помощнику", "section", "Справочный помощник", "secondary"),
                ("🔬 Вернуться к Стенду №1 (Градиент и НСХ)", "stand", LAB_STAND_OPTIONS[0], "secondary"),
            ]
    elif active_section == "Подбор термопары":
        actions = [
            ("📘 Далее: Справочный помощник и генератор НСХ ➡️", "section", "Справочный помощник", "primary"),
            ("🔬 Вернуться к исследовательским стендам", "section", "Исследовательские стенды", "secondary"),
            ("📚 Вернуться к теории", "section", "Теоретическая часть", "secondary"),
        ]
    else:
        actions = [
            ("📚 Сначала: Теоретическая часть ➡️", "section", "Теоретическая часть", "primary"),
            ("🔬 Перейти к исследовательским стендам", "section", "Исследовательские стенды", "secondary"),
            ("🧭 Перейти к подбору термопары", "section", "Подбор термопары", "secondary"),
        ]

    st.markdown("---")
    with st.container(border=True):
        st.markdown('<div class="kip-param-group-title">➡️ Переход к следующему режиму</div>', unsafe_allow_html=True)
        st.caption("Выберите следующий раздел для продолжения работы с KIP Simulator:")

        if is_mobile_view:
            for idx, (label, kind, target, btn_type) in enumerate(actions):
                cb = _bottom_nav_to_stand if kind == "stand" else _bottom_nav_to_section
                st.button(
                    label,
                    key=f"bottom_nav_btn_{active_section}_{idx}",
                    type=btn_type,
                    use_container_width=True,
                    on_click=cb,
                    args=(target,),
                )
        else:
            nav_cols = st.columns(len(actions))
            for idx, (label, kind, target, btn_type) in enumerate(actions):
                cb = _bottom_nav_to_stand if kind == "stand" else _bottom_nav_to_section
                with nav_cols[idx]:
                    st.button(
                        label,
                        key=f"bottom_nav_btn_{active_section}_{idx}",
                        type=btn_type,
                        use_container_width=True,
                        on_click=cb,
                        args=(target,),
                    )


def run_kip_simulator() -> None:
    """Условный маршрутизатор: применяет режим доступности и отображает только активный раздел."""
    init_app_session_state()
    stand_params = render_sidebar_navigation_and_controls()
    apply_visual_system_css(st.session_state["accessibility_mode"], st.session_state["theme_mode"])
    st.markdown('<div id="kip-page-top-anchor" class="kip-scroll-anchor" aria-hidden="true"></div>', unsafe_allow_html=True)
    render_top_navigation_bar()

    active_section = st.session_state["active_section"]
    if active_section == "Исследовательские стенды":
        if st.session_state["active_lab_stand"].startswith("Стенд №1"):
            render_stand_1_section(stand_params)
        else:
            render_stand_2_section(stand_params)
    elif active_section == "Теоретическая часть":
        render_theory_section()
    elif active_section == "Подбор термопары":
        render_thermocouple_selector()
    elif active_section == "Справочный помощник":
        render_reference_assistant_section()

    render_bottom_section_navigation()
    render_pending_page_scroll()


run_kip_simulator()
