import os
 
# --- AUTOCONFIGURACIÓN DE TEMA (para no depender de un config.toml aparte) ---
# Streamlit solo lee el color primario (theme.primaryColor) de .streamlit/config.toml
# al ARRANCAR el proceso. Por eso, si ese archivo no existe (o está desactualizado),
# lo generamos aquí mismo y pedimos un único reinicio. A partir de ese momento,
# todos los sliders, radios, checkboxes, etc. salen en azul de forma NATIVA,
# sin necesidad de parches CSS frágiles.
_STREAMLIT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit")
_CONFIG_PATH = os.path.join(_STREAMLIT_DIR, "config.toml")
_THEME_TOML = """[theme]
primaryColor = "#5956E9"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8FAFC"
textColor = "#111827"
font = "sans serif"
"""
 
def _ensure_theme_config() -> bool:
    """Crea/actualiza .streamlit/config.toml si hace falta. Devuelve True si acaba de crearse/cambiarse."""
    try:
        os.makedirs(_STREAMLIT_DIR, exist_ok=True)
        necesita_escribir = True
        if os.path.exists(_CONFIG_PATH):
            with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
                contenido_actual = f.read()
            necesita_escribir = "5956E9" not in contenido_actual
        if necesita_escribir:
            with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
                f.write(_THEME_TOML)
            return True
    except Exception:
        pass
    return False
 
_TEMA_RECIEN_CREADO = _ensure_theme_config()
 
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import datetime as _dt
 
# --- CONFIGURACIÓN DE PÁGINA (debe ser el primer comando de Streamlit) ---
st.set_page_config(
    page_title="Alan Health Spain - Reporting Actuarial & Business",
    page_icon="💜",
    layout="wide"
)
 
# ============================================================================
# --- DICCIONARIO DE TRADUCCIONES (Español / English) ---
# ============================================================================
TRANSLATIONS = {
    "es": {
        "lang_label": "🌐 Idioma / Language",
        "restart_warning": (
            "⚙️ **Configuración de color aplicada.** Se ha creado/actualizado "
            "`.streamlit/config.toml` con el azul de Alan (#5956E9). "
            "Detén la app (Ctrl+C en la terminal) y vuelve a ejecutar "
            "`streamlit run app_alan_health.py` **una sola vez** para que los "
            "sliders, radios y demás controles se pinten en azul de forma nativa."
        ),
        "main_title": "Reporting Mensual de Rentabilidad y Drivers Actuariales",
        "brand_title_header": "EXPERTO EN SEGUROS (ESPAÑA)",
        "sub_description": (
            "Framework de reporting interno mensual diseñado bajo los principios de "
            "<b>transparencia radical</b> de Alan. Permite monitorizar la cuenta de "
            "resultados técnica, la estrategia de <i>Pricing & Re-pricing</i> y la "
            "rentabilidad del portfolio."
        ),
        "sidebar_role": "Experto en Seguros • Mercado Español",
        "sidebar_focus_title": "Enfoque técnico & negocio:",
        "sidebar_focus_items": [
            "Estrategia de Pricing & Re-pricing",
            "Monitoreo de Márgenes y P&L de Cartera",
            "Dirección de Riesgo y Herramientas para Cuentas Clave",
        ],
        "sidebar_status_pill": "🇪🇸 Seguro de Salud y Cuantitativo Actuarial",
        "period_header": "📅 Periodo de Reporting",
        "month_label": "Mes",
        "year_label": "Año",
        "months": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
        "segment_header": "🏢 Segmento de Cliente y Oferta",
        "client_type_label": "Tipo de Cliente",
        "client_type_options": ["Empresas (B2B)", "Individuales / TNS (B2C)"],
        "b2b_offer_label": "Oferta B2B (Elegible Colectivos)",
        "b2b_members_label": "Número de Asegurados en Colectivo",
        "b2b_age_label": "Edad Media de la Plantilla (Ajuste Demográfico)",
        "b2c_offer_label": "Oferta B2C (Trabajadores No Salariados / TNS)",
        "b2c_members_label": "Número de Asegurados Individuales",
        "claims_header": "📊 Drivers de Siniestralidad y Reservas",
        "frequency_label": "Frecuencia (Reclamos / Miembro / Mes)",
        "avg_cost_label": "Costo Medio por Reclamo (€)",
        "rsp_label": "Reserva de Siniestros Pendientes (RSP / RBNS) (%)",
        "ibnr_label": "Reserva IBNR (% Siniestros No Reportados)",
        "prevention_label": "Adopción Salud Digital / Prevención (%)",
        "expenses_header": "💸 Cargas de Gastos y Operación (% Prima)",
        "commissions_label": "Comisiones / Adquisición (CAC) (%)",
        "admin_label": "Gastos Admin & Operaciones Ops (%)",
        "reinsurance_label": "Costo de Reaseguro / Capital (%)",
        "period_badge": "📅 Periodo de Reporting: {mes} {anio}",
        "kpi_premiums": "Primas Devengadas Mes",
        "kpi_loss_ratio": "Loss Ratio Incurrido (S/P)",
        "kpi_loss_ratio_target": "Objetivo <78%",
        "kpi_combined_ratio": "Combined Ratio Total",
        "kpi_surplus": "Superávit",
        "kpi_deficit": "Déficit",
        "kpi_net_result": "Resultado Técnico Neto Mes",
        "pnl_subheader": "📊 Desglose de la Cuenta de Resultados (P&L Actuarial)",
        "pnl_concepts": ["Primas Devengadas", "Siniestros Pagados", "Reserva Siniestros Pendientes (RSP)",
                          "Reserva IBNR", "Gastos Operativos & CAC", "Resultado Neto"],
        "pnl_concept_col": "Concepto",
        "pnl_amount_col": "Monto (€)",
        "sens_subheader": "📈 Sensibilidad Combined Ratio vs Adopción Preventiva",
        "sens_x_col": "Adopción Salud Digital (%)",
        "sens_y_col": "Combined Ratio (%)",
        "sens_breakeven": "Breakeven (100%)",
        "sens_target": "Objetivo Alan (90%)",
        "ratios_subheader": "📑 Resumen de Ratios Actuariales y Financieros",
        "ratios_col_ratio": "Ratio Actuarial",
        "ratios_col_value": "Valor Calculado",
        "ratios_col_benchmark": "Benchmark / Target Alan",
        "ratios_col_status": "Estado",
        "ratios_names": [
            "Loss Ratio Incurrido (Siniestralidad Total / Primas)",
            "Expense Ratio (Gastos Admin + Comisiones / Primas)",
            "Combined Ratio (LR + ER)",
            "Tasa de Automatización de Siniestros (Auto-claims)",
        ],
        "ratios_benchmarks": ["< 78.0%", "< 12.0%", "< 90.0%", "> 90.0%"],
        "status_ok_range": "✅ En Rango",
        "status_review_rate": "⚠️ Revisar Tarifa",
        "status_efficient": "✅ Eficiente",
        "status_high_ga": "⚠️ Alto G&A",
        "status_profitable": "🟢 Rentable",
        "status_loss": "🔴 En Pérdida",
        "status_target_met": "🟢 Objetivo Cumplido",
        "status_improve_adoption": "🟡 Mejorar Adopción",
        "footer_name_role": "Pablo Guidi — Experto en Seguros (Mercado Español)",
        "footer_sub": "Estrategia de Pricing & Re-pricing • Rentabilidad de Cartera y Gestión de Márgenes • Liderazgo Técnico",
        "footer_badge": "💜 Framework de Seguro de Salud Alan",
    },
    "en": {
        "lang_label": "🌐 Language / Idioma",
        "restart_warning": (
            "⚙️ **Color theme applied.** `.streamlit/config.toml` has been "
            "created/updated with Alan's blue (#5956E9). "
            "Stop the app (Ctrl+C in the terminal) and run "
            "`streamlit run app_alan_health.py` again **once** so sliders, "
            "radio buttons and other controls render in blue natively."
        ),
        "main_title": "Monthly Profitability & Actuarial Drivers Report",
        "brand_title_header": "INSURANCE EXPERT (SPAIN)",
        "sub_description": (
            "Internal monthly reporting framework designed under Alan's "
            "<b>radical transparency</b> principles. It allows monitoring the "
            "technical income statement, the <i>Pricing & Re-pricing</i> "
            "strategy, and portfolio profitability."
        ),
        "sidebar_role": "Insurance Expert • Spanish Market",
        "sidebar_focus_title": "Technical & Business Focus:",
        "sidebar_focus_items": [
            "Pricing & Re-pricing Strategy",
            "Margin Monitoring & Portfolio P&L",
            "Risk Steering & Key Account Tools",
        ],
        "sidebar_status_pill": "🇪🇸 Health Insurance & Actuarial Quantitative",
        "period_header": "📅 Reporting Period",
        "month_label": "Month",
        "year_label": "Year",
        "months": ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"],
        "segment_header": "🏢 Client Segment & Offer",
        "client_type_label": "Client Type",
        "client_type_options": ["Companies (B2B)", "Individuals / Self-employed (B2C)"],
        "b2b_offer_label": "B2B Offer (Group Eligible)",
        "b2b_members_label": "Number of Insured in Group",
        "b2b_age_label": "Average Workforce Age (Demographic Adjustment)",
        "b2c_offer_label": "B2C Offer (Self-employed Workers)",
        "b2c_members_label": "Number of Individual Insured",
        "claims_header": "📊 Claims & Reserves Drivers",
        "frequency_label": "Frequency (Claims / Member / Month)",
        "avg_cost_label": "Average Cost per Claim (€)",
        "rsp_label": "Reported But Not Settled Reserve (RBNS) (%)",
        "ibnr_label": "IBNR Reserve (% Unreported Claims)",
        "prevention_label": "Digital Health / Prevention Adoption (%)",
        "expenses_header": "💸 Expense & Operating Loadings (% Premium)",
        "commissions_label": "Commissions / Acquisition (CAC) (%)",
        "admin_label": "Admin & Operations Expenses (%)",
        "reinsurance_label": "Reinsurance / Capital Cost (%)",
        "period_badge": "📅 Reporting Period: {mes} {anio}",
        "kpi_premiums": "Premiums Earned (Month)",
        "kpi_loss_ratio": "Incurred Loss Ratio (Claims/Premium)",
        "kpi_loss_ratio_target": "Target <78%",
        "kpi_combined_ratio": "Total Combined Ratio",
        "kpi_surplus": "Surplus",
        "kpi_deficit": "Deficit",
        "kpi_net_result": "Net Technical Result (Month)",
        "pnl_subheader": "📊 P&L Breakdown (Actuarial Income Statement)",
        "pnl_concepts": ["Earned Premiums", "Paid Claims", "Outstanding Claims Reserve (RBNS)",
                          "IBNR Reserve", "Operating & CAC Expenses", "Net Result"],
        "pnl_concept_col": "Concept",
        "pnl_amount_col": "Amount (€)",
        "sens_subheader": "📈 Combined Ratio Sensitivity vs Preventive Adoption",
        "sens_x_col": "Digital Health Adoption (%)",
        "sens_y_col": "Combined Ratio (%)",
        "sens_breakeven": "Breakeven (100%)",
        "sens_target": "Alan Target (90%)",
        "ratios_subheader": "📑 Actuarial & Financial Ratios Summary",
        "ratios_col_ratio": "Actuarial Ratio",
        "ratios_col_value": "Calculated Value",
        "ratios_col_benchmark": "Benchmark / Alan Target",
        "ratios_col_status": "Status",
        "ratios_names": [
            "Incurred Loss Ratio (Total Claims / Premiums)",
            "Expense Ratio (Admin + Commissions / Premiums)",
            "Combined Ratio (LR + ER)",
            "Claims Automation Rate (Auto-claims)",
        ],
        "ratios_benchmarks": ["< 78.0%", "< 12.0%", "< 90.0%", "> 90.0%"],
        "status_ok_range": "✅ On Target",
        "status_review_rate": "⚠️ Review Pricing",
        "status_efficient": "✅ Efficient",
        "status_high_ga": "⚠️ High G&A",
        "status_profitable": "🟢 Profitable",
        "status_loss": "🔴 Loss-making",
        "status_target_met": "🟢 Target Met",
        "status_improve_adoption": "🟡 Improve Adoption",
        "footer_name_role": "Pablo Guidi — Insurance Expert (Spanish Market)",
        "footer_sub": "Pricing & Re-pricing Strategy • Portfolio Profitability & Margin Steering • Technical Leadership",
        "footer_badge": "💜 Alan Health Insurance Framework",
    },
}
 
# --- SELECTOR DE IDIOMA (primer widget que se crea, arriba del todo en el sidebar) ---
with st.sidebar:
    _idioma_sel = st.selectbox("🌐 Idioma / Language", ["Español", "English"], index=0)
lang = "es" if _idioma_sel == "Español" else "en"
T = TRANSLATIONS[lang]
 
# --- AVISO DE REINICIO ÚNICO (solo la primera vez que se crea/actualiza el tema) ---
if _TEMA_RECIEN_CREADO:
    st.warning(T["restart_warning"])
    st.stop()
 
# --- FUNCIÓN HELPER PARA CARGAR IMÁGENES LOCALES EN HTML ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None
 
logo_b64 = get_base64_image("logo_alan.png")
mascot_b64 = get_base64_image("mascot_alan.png")
 
# --- ESTILOS CSS PERSONALIZADOS CON SOBRESCRITURA TOTAL DE SLIDERS ---
st.markdown("""
<style>
    /* 1. REDEFINICIÓN DE VARIABLES PRIMARIAS DE STREAMLIT A AZUL/PÚRPURA (#5956E9) */
    :root, [data-testid="stAppViewContainer"], [data-testid="stApp"], [data-testid="stSidebar"] {
        --primary-color: #5956E9 !important;
        --primary: #5956E9 !important;
    }
 
    .stApp {
        background-color: #FFFFFF;
        color: #111827;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
 
    /* ============================================================ */
    /* === COLOR ÚNICO PARA TODOS LOS CAMPOS INTERACTIVOS (AZUL) === */
    /* ============================================================ */
 
    /* --- SLIDERS: número de valor mostrado encima del "thumb" --- */
    div[data-baseweb="slider"] div[data-testid="stThumbValue"],
    div[data-baseweb="slider"] div[role="slider"] div,
    div[data-testid="stSliderThumbValue"],
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #5956E9 !important;
    }
 
    /* --- SLIDERS: barra de fondo completa (riel) --- */
    div[data-baseweb="slider"] > div > div:first-child {
        background: #E2E8F0 !important;
    }
 
    /* --- SLIDERS: tramo ACTIVO/rellenado de la barra (el que sale en rojo) --- */
    div[data-baseweb="slider"] > div > div:nth-child(2),
    div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        background: #5956E9 !important;
        background-color: #5956E9 !important;
    }
 
    /* --- SLIDERS: círculo/tirador (thumb) --- */
    div[data-baseweb="slider"] [role="slider"] {
        background-color: #5956E9 !important;
        border-color: #5956E9 !important;
        box-shadow: 0 0 0 3px rgba(89, 86, 233, 0.25) !important;
    }
 
    div[data-baseweb="slider"] [role="slider"]:hover,
    div[data-baseweb="slider"] [role="slider"]:focus,
    div[data-baseweb="slider"] [role="slider"]:active {
        background-color: #5956E9 !important;
        border-color: #5956E9 !important;
        box-shadow: 0 0 0 6px rgba(89, 86, 233, 0.35) !important;
    }
 
    /* --- CHECKBOX (por si se usan) --- */
    div[data-testid="stCheckbox"] label span[data-testid="stMarkdownContainer"] {
        color: inherit;
    }
    div[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] {
        background-color: #5956E9 !important;
        border-color: #5956E9 !important;
    }
 
    /* --- SELECTBOX: borde al hacer foco --- */
    div[data-baseweb="select"] > div {
        border-color: #E2E8F0 !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: #5956E9 !important;
        box-shadow: 0 0 0 1px #5956E9 !important;
    }
 
    /* --- RED DE SEGURIDAD: pisa el rojo inline (#FF4B4B / rgb(255,75,75)) --- */
    /* Streamlit inyecta este color directamente vía style="" tomado del theme.        */
    /* Si config.toml no se aplica, esto lo corrige igualmente.                        */
    div[data-baseweb="slider"] [style*="rgb(255, 75, 75)"],
    div[data-baseweb="slider"] [style*="rgb(255,75,75)"],
    div[data-baseweb="slider"] [style*="#FF4B4B"],
    div[data-baseweb="slider"] [style*="#ff4b4b"] {
        background-color: #5956E9 !important;
        background: #5956E9 !important;
        border-color: #5956E9 !important;
        color: #5956E9 !important;
    }
    div[data-testid="stSlider"] [style*="rgb(255, 75, 75)"],
    div[data-testid="stSlider"] [style*="rgb(255,75,75)"] {
        color: #5956E9 !important;
        background-color: #5956E9 !important;
    }
    div[data-testid="stRadio"] [style*="rgb(255, 75, 75)"],
    div[data-testid="stRadio"] [style*="#FF4B4B"] {
        background-color: #5956E9 !important;
        border-color: #5956E9 !important;
        fill: #5956E9 !important;
    }
    /* Cubre el caso en que el color se aplique vía SVG fill en vez de background */
    div[data-baseweb="slider"] svg [fill="rgb(255, 75, 75)"],
    div[data-baseweb="slider"] svg [fill="#FF4B4B"] {
        fill: #5956E9 !important;
    }
 
    /* CONTENEDOR HEADER UNIFICADO */
    .custom-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        margin-bottom: 4px;
        width: 100%;
    }
 
    .header-left {
        display: flex;
        align-items: center;
        gap: 14px;
        flex: 1;
        min-width: 0;
    }
 
    .header-logo {
        height: 34px;
        width: auto;
        object-fit: contain;
        border-radius: 6px;
        flex-shrink: 0;
    }
 
    .main-title-text {
        color: #111827;
        font-size: 1.35rem;
        font-weight: 800;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.25;
        letter-spacing: -0.01em;
    }
 
    /* Oculta el icono de anclaje (🔗) que Streamlit añade automáticamente a los <h1>-<h6> */
    .main-title-text a,
    [data-testid="stHeaderActionElements"],
    .main-title-text .anchor-link {
        display: none !important;
    }
 
    /* BANNER MARCA PERSONAL */
    .personal-brand-header-badge {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border: 1.5px solid #6366F1;
        border-radius: 10px;
        padding: 6px 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        white-space: nowrap;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.12);
    }
 
    .brand-avatar {
        width: 32px;
        height: 32px;
        background-color: #5956E9;
        color: white;
        font-weight: 800;
        font-size: 0.9rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(89, 86, 233, 0.3);
    }
 
    .brand-info-text {
        display: flex;
        flex-direction: column;
        line-height: 1.15;
    }
 
    .brand-title {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #4F46E5;
        font-weight: 700;
    }
 
    .brand-name {
        font-size: 0.92rem;
        font-weight: 800;
        color: #1E1B4B;
        margin-top: -1px;
    }
 
    .sub-description {
        color: #6B7280;
        font-size: 0.92rem;
        margin-top: 6px;
        margin-bottom: 14px;
        line-height: 1.5;
    }
 
    /* Tarjetas de Métricas (KPIs) */
    div[data-testid="stMetricValue"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    div[data-testid="stMetricLabel"] p {
        color: #6B7280;
        font-size: 0.88em;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        color: #5956E9 !important;
        font-size: 1.95em !important;
        font-weight: 800 !important;
    }
 
    /* SIDEBAR MARCA PERSONAL */
    .sidebar-brand-card {
        background: linear-gradient(180deg, #FFFFFF 0%, #F5F3FF 100%);
        border: 1px solid #DDD6FE;
        border-radius: 14px;
        padding: 16px;
        margin-top: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(99, 102, 241, 0.08);
    }
 
    .sidebar-brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }
 
    .sidebar-avatar {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #5956E9 0%, #8B5CF6 100%);
        color: white;
        font-size: 1.15rem;
        font-weight: 800;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
 
    .sidebar-brand-name {
        font-weight: 800;
        font-size: 1.05rem;
        color: #1E1B4B;
        line-height: 1.2;
    }
 
    .sidebar-brand-role {
        font-size: 0.80rem;
        color: #5956E9;
        font-weight: 700;
    }
 
    .brand-status-pill {
        display: inline-block;
        background-color: #EEF2FF;
        color: #4F46E5;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        margin-top: 10px;
        border: 1px solid #C7D2FE;
    }
 
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
 
    /* FOOTER */
    .footer-brand-box {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        color: #FFFFFF;
        border-radius: 14px;
        padding: 22px 28px;
        margin-top: 35px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
        box-shadow: 0 8px 20px rgba(30, 27, 75, 0.15);
    }
 
    .footer-brand-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
 
    .footer-brand-sub {
        font-size: 0.88rem;
        color: #C7D2FE;
    }
 
    .footer-badge {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #FFFFFF;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)
 
# --- HEADER UNIFICADO ---
if logo_b64:
    logo_img_tag = f'<img src="data:image/png;base64,{logo_b64}" class="header-logo" alt="Alan Logo">'
else:
    logo_img_tag = '<span style="font-size: 1.8rem; font-weight: 800; color: #5956E9;">💜 alan</span>'
 
st.markdown(f"""
<div class="custom-header">
    <div class="header-left">
        {logo_img_tag}
        <h1 class="main-title-text">{T["main_title"]}</h1>
    </div>
    <div class="personal-brand-header-badge">
        <div class="brand-avatar">PG</div>
        <div class="brand-info-text">
            <span class="brand-title">{T["brand_title_header"]}</span>
            <span class="brand-name">Pablo Guidi</span>
        </div>
    </div>
</div>
<p class="sub-description">
{T["sub_description"]}
</p>
""", unsafe_allow_html=True)
 
st.divider()
 
# --- SIDEBAR CON MARCA PERSONAL ALINEADA A ALAN ---
with st.sidebar:
    if mascot_b64:
        st.markdown(f'<img src="data:image/png;base64,{mascot_b64}" style="width: 160px; display: block; margin: 0 auto;">', unsafe_allow_html=True)
 
    _focus_items_html = "".join(f"• {item}<br>" for item in T["sidebar_focus_items"])
    st.markdown(f"""
    <div class="sidebar-brand-card">
        <div class="sidebar-brand-header">
            <div class="sidebar-avatar">PG</div>
            <div>
                <div class="sidebar-brand-name">Pablo Guidi</div>
                <div class="sidebar-brand-role">{T["sidebar_role"]}</div>
            </div>
        </div>
        <div style="font-size:0.81rem; color:#4B5563; line-height:1.45;">
            <b>{T["sidebar_focus_title"]}</b><br>
            {_focus_items_html}
        </div>
        <div class="brand-status-pill">{T["sidebar_status_pill"]}</div>
    </div>
    """, unsafe_allow_html=True)
 
    st.header(T["period_header"])
    _hoy = _dt.date.today()
    col_mes, col_anio = st.columns(2)
    with col_mes:
        mes_seleccionado = st.selectbox(T["month_label"], T["months"], index=_hoy.month - 1)
    with col_anio:
        anio_seleccionado = st.selectbox(
            T["year_label"],
            list(range(_hoy.year - 2, _hoy.year + 2)),
            index=2  # año actual por defecto
        )
 
    st.header(T["segment_header"])
    segmento = st.radio(T["client_type_label"], T["client_type_options"])
 
    if segmento == T["client_type_options"][0]:  # B2B
        plan = st.selectbox(T["b2b_offer_label"], ["Essentiel", "Balanced", "Optimal"])
        num_miembros = st.slider(T["b2b_members_label"], min_value=50, max_value=10000, value=1000, step=50)
        edad_media = st.slider(T["b2b_age_label"], min_value=20, max_value=65, value=36)
 
        prima_base = {"Essentiel": 38.0, "Balanced": 52.0, "Optimal": 75.0}[plan]
        factor_demog = 1.0 + max(0, (edad_media - 30) * 0.015)
        prima_mes = prima_base * factor_demog
    else:  # B2C
        plan = st.selectbox(T["b2c_offer_label"], ["Alan Rubis", "Alan Emeraude", "Alan Saphir"])
        num_miembros = st.slider(T["b2c_members_label"], min_value=50, max_value=3000, value=500, step=25)
        prima_mes = {"Alan Rubis": 42.0, "Alan Emeraude": 65.0, "Alan Saphir": 95.0}[plan]
        factor_demog = 1.0
 
    st.header(T["claims_header"])
    frecuencia_reclamos = st.slider(T["frequency_label"], min_value=0.2, max_value=2.0, value=0.65, step=0.05)
    costo_medio_reclamo = st.number_input(T["avg_cost_label"], min_value=20.0, max_value=300.0, value=58.0, step=2.0)
 
    rsp_pct = st.slider(T["rsp_label"], min_value=1.0, max_value=8.0, value=3.0, step=0.5) / 100.0
    ibnr_pct = st.slider(T["ibnr_label"], min_value=1.0, max_value=10.0, value=4.5, step=0.5) / 100.0
    adopcion_prevencion = st.slider(T["prevention_label"], min_value=10, max_value=100, value=55, step=5) / 100.0
 
    st.header(T["expenses_header"])
    comisiones_pct = st.slider(T["commissions_label"], min_value=0.0, max_value=15.0, value=4.5, step=0.5) / 100.0
    operaciones_admin_pct = st.slider(T["admin_label"], min_value=5.0, max_value=20.0, value=9.5, step=0.5) / 100.0
    reaseguro_pct = st.slider(T["reinsurance_label"], min_value=0.5, max_value=5.0, value=1.5, step=0.1) / 100.0
 
# --- CÁLCULOS ACTUARIALES ---
ingresos_primas_mes = num_miembros * prima_mes
 
siniestros_pagados_base = num_miembros * frecuencia_reclamos * costo_medio_reclamo
reduccion_prevencion = adopcion_prevencion * 0.07
siniestros_pagados = siniestros_pagados_base * (1.0 - reduccion_prevencion)
 
rsp_monto = siniestros_pagados * rsp_pct
ibnr_monto = (siniestros_pagados + rsp_monto) * ibnr_pct
siniestros_totales_incurridos = siniestros_pagados + rsp_monto + ibnr_monto
 
comisiones_monto = ingresos_primas_mes * comisiones_pct
gastos_admin_monto = ingresos_primas_mes * operaciones_admin_pct
reaseguro_monto = ingresos_primas_mes * reaseguro_pct
gastos_totales_monto = comisiones_monto + gastos_admin_monto + reaseguro_monto
 
margen_tecnico_bruto = ingresos_primas_mes - siniestros_totales_incurridos
resultado_tecnico_neto = margen_tecnico_bruto - gastos_totales_monto
 
loss_ratio = (siniestros_totales_incurridos / ingresos_primas_mes) if ingresos_primas_mes > 0 else 0
expense_ratio = (gastos_totales_monto / ingresos_primas_mes) if ingresos_primas_mes > 0 else 0
combined_ratio = loss_ratio + expense_ratio
auto_claims_rate = min(0.96, 0.82 + (adopcion_prevencion * 0.12))
 
# --- TARJETAS DE MÉTRICAS CLAVE (KPIs) ---
st.markdown(f"""
<div style="display:inline-flex; align-items:center; gap:8px; background:#EEF2FF;
            border:1px solid #C7D2FE; border-radius:20px; padding:5px 14px;
            margin-bottom:14px; font-size:0.85rem; font-weight:700; color:#4F46E5;">
    {T["period_badge"].format(mes=mes_seleccionado, anio=anio_seleccionado)}
</div>
""", unsafe_allow_html=True)
 
col1, col2, col3, col4 = st.columns(4)
 
col1.metric(T["kpi_premiums"], f"{ingresos_primas_mes:,.0f} €")
col2.metric(T["kpi_loss_ratio"], f"{loss_ratio:.1%}", delta=T["kpi_loss_ratio_target"], delta_color="inverse")
col3.metric(T["kpi_combined_ratio"], f"{combined_ratio:.1%}",
            delta=(T["kpi_surplus"] if combined_ratio < 1 else T["kpi_deficit"]), delta_color="inverse")
col4.metric(T["kpi_net_result"], f"{resultado_tecnico_neto:,.0f} €")
 
st.divider()
 
# --- DASHBOARD VISUAL ---
col_left, col_right = st.columns(2)
 
with col_left:
    st.subheader(T["pnl_subheader"])
    conceptos = T["pnl_concepts"]
    valores = [
        ingresos_primas_mes,
        -siniestros_pagados,
        -rsp_monto,
        -ibnr_monto,
        -gastos_totales_monto,
        resultado_tecnico_neto
    ]
    df_pnl = pd.DataFrame({T["pnl_concept_col"]: conceptos, T["pnl_amount_col"]: valores})
 
    colors_pnl = ['#5956E9', '#EF4444', '#F87171', '#FCA5A5', '#F87171', '#10B981' if resultado_tecnico_neto >= 0 else '#EF4444']
 
    fig_pnl = px.bar(
        df_pnl,
        x=T["pnl_concept_col"],
        y=T["pnl_amount_col"],
        color=T["pnl_concept_col"],
        color_discrete_sequence=colors_pnl,
        text_auto=".0f"
    )
    fig_pnl.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="",
        yaxis_title=""
    )
    st.plotly_chart(fig_pnl, use_container_width=True)
 
with col_right:
    st.subheader(T["sens_subheader"])
    adop_range = np.linspace(0.1, 1.0, 10)
    lr_range = [((siniestros_pagados_base * (1 - (a * 0.07))) * (1 + rsp_pct) * (1 + ibnr_pct)) / ingresos_primas_mes for a in adop_range]
    cr_range = [lr + expense_ratio for lr in lr_range]
 
    df_cr = pd.DataFrame({T["sens_x_col"]: adop_range * 100, T["sens_y_col"]: np.array(cr_range) * 100})
    fig_cr = px.line(df_cr, x=T["sens_x_col"], y=T["sens_y_col"], markers=True, color_discrete_sequence=["#5956E9"])
 
    fig_cr.add_hline(y=100, line_dash="dash", line_color="#EF4444", annotation_text=T["sens_breakeven"])
    fig_cr.add_hline(y=90, line_dash="dash", line_color="#10B981", annotation_text=T["sens_target"])
 
    fig_cr.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_cr, use_container_width=True)
 
# --- TABLA DE RATIOS ACTUARIALES ---
st.subheader(T["ratios_subheader"])
ratios_df = pd.DataFrame({
    T["ratios_col_ratio"]: T["ratios_names"],
    T["ratios_col_value"]: [f"{loss_ratio:.2%}", f"{expense_ratio:.2%}", f"{combined_ratio:.2%}", f"{auto_claims_rate:.1%}"],
    T["ratios_col_benchmark"]: T["ratios_benchmarks"],
    T["ratios_col_status"]: [
        T["status_ok_range"] if loss_ratio <= 0.78 else T["status_review_rate"],
        T["status_efficient"] if expense_ratio <= 0.15 else T["status_high_ga"],
        T["status_profitable"] if combined_ratio <= 1.0 else T["status_loss"],
        T["status_target_met"] if auto_claims_rate >= 0.9 else T["status_improve_adoption"],
    ]
})
 
st.dataframe(ratios_df, use_container_width=True, hide_index=True)
 
# --- BANNER DE CIERRE ---
st.markdown(f"""
<div class="footer-brand-box">
    <div>
        <div class="footer-brand-title">{T["footer_name_role"]}</div>
        <div class="footer-brand-sub">{T["footer_sub"]}</div>
    </div>
    <div class="footer-badge">
        {T["footer_badge"]}
    </div>
</div>
""", unsafe_allow_html=True)
 
