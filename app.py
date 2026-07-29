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
 
# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Alan Health Spain - Reporting Actuarial & Business",
    page_icon="💜",
    layout="wide"
)
 
# --- AVISO DE REINICIO ÚNICO (solo la primera vez que se crea/actualiza el tema) ---
if _TEMA_RECIEN_CREADO:
    st.warning(
        "⚙️ **Configuración de color aplicada.** Se ha creado/actualizado "
        "`.streamlit/config.toml` con el azul de Alan (#5956E9). "
        "Detén la app (Ctrl+C en la terminal) y vuelve a ejecutar "
        "`streamlit run app_alan_health.py` **una sola vez** para que los "
        "sliders, radios y demás controles se pinten en azul de forma nativa."
    )
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
 
    /* --- RADIO BUTTONS: círculo exterior e interior seleccionado --- */
    div[data-testid="stRadio"] label div:first-child {
        border-color: #5956E9 !important;
    }
    div[data-testid="stRadio"] label div:first-child > div {
        background-color: #5956E9 !important;
    }
    div[data-testid="stRadio"] input:checked + div {
        border-color: #5956E9 !important;
        background-color: #5956E9 !important;
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
        margin-bottom: 8px;
        width: 100%;
    }
 
    .header-left {
        display: flex;
        align-items: center;
        gap: 16px;
        flex: 1;
    }
 
    .header-logo {
        height: 48px;
        width: auto;
        object-fit: contain;
    }
 
    .main-title-text {
        color: #111827;
        font-size: 1.75rem;
        font-weight: 800;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.2;
    }
 
    /* BANNER MARCA PERSONAL */
    .personal-brand-header-badge {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border: 1.5px solid #6366F1;
        border-radius: 12px;
        padding: 8px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        white-space: nowrap;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.12);
    }
 
    .brand-avatar {
        width: 38px;
        height: 38px;
        background-color: #5956E9;
        color: white;
        font-weight: 800;
        font-size: 1.05rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(89, 86, 233, 0.3);
    }
 
    .brand-info-text {
        display: flex;
        flex-direction: column;
    }
 
    .brand-title {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #4F46E5;
        font-weight: 700;
    }
 
    .brand-name {
        font-size: 1.05rem;
        font-weight: 800;
        color: #1E1B4B;
        margin-top: -2px;
    }
 
    .sub-description {
        color: #6B7280;
        font-size: 1.05rem;
        margin-top: 8px;
        margin-bottom: 20px;
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
        <h1 class="main-title-text">Reporting Mensual de Rentabilidad y Drivers Actuariales</h1>
    </div>
    <div class="personal-brand-header-badge">
        <div class="brand-avatar">PG</div>
        <div class="brand-info-text">
            <span class="brand-title">INSURANCE EXPERT (SPAIN)</span>
            <span class="brand-name">Pablo Guidi</span>
        </div>
    </div>
</div>
<p class="sub-description">
Framework de reporting interno mensual diseñado bajo los principios de <b>transparencia radical</b> de Alan. 
Permite monitorizar la cuenta de resultados técnica, la estrategia de <i>Pricing & Re-pricing</i> y la rentabilidad del portfolio.
</p>
""", unsafe_allow_html=True)
 
st.divider()
 
# --- SIDEBAR CON MARCA PERSONAL ALINEADA A ALAN ---
with st.sidebar:
    if mascot_b64:
        st.markdown(f'<img src="data:image/png;base64,{mascot_b64}" style="width: 160px; display: block; margin: 0 auto;">', unsafe_allow_html=True)
 
    st.markdown("""
    <div class="sidebar-brand-card">
        <div class="sidebar-brand-header">
            <div class="sidebar-avatar">PG</div>
            <div>
                <div class="sidebar-brand-name">Pablo Guidi</div>
                <div class="sidebar-brand-role">Insurance Expert • Spanish Market</div>
            </div>
        </div>
        <div style="font-size:0.81rem; color:#4B5563; line-height:1.45;">
            <b>Enfoque técnico & negocio:</b><br>
            • Pricing & Re-pricing Strategy<br>
            • Margin Monitoring & Portfolio P&L<br>
            • Risk Steering & Key Account Tools
        </div>
        <div class="brand-status-pill">🇪🇸 Health Insurance & Actuarial Quantitative</div>
    </div>
    """, unsafe_allow_html=True)
 
    st.header("🏢 Segmento de Cliente y Oferta")
    segmento = st.radio("Tipo de Cliente", ["Empresas (B2B)", "Individuales / TNS (B2C)"])
 
    if segmento == "Empresas (B2B)":
        plan = st.selectbox("Oferta B2B (Elegible Colectivos)", ["Essentiel", "Balanced", "Optimal"])
        num_miembros = st.slider("Número de Asegurados en Colectivo", min_value=50, max_value=10000, value=1000, step=50)
        edad_media = st.slider("Edad Media de la Plantilla (Ajuste Demográfico)", min_value=20, max_value=65, value=36)
        
        prima_base = {"Essentiel": 38.0, "Balanced": 52.0, "Optimal": 75.0}[plan]
        factor_demog = 1.0 + max(0, (edad_media - 30) * 0.015)
        prima_mes = prima_base * factor_demog
    else:
        plan = st.selectbox("Oferta B2C (Trabajadores No Salariados / TNS)", ["Alan Rubis", "Alan Emeraude", "Alan Saphir"])
        num_miembros = st.slider("Número de Asegurados Individuales", min_value=50, max_value=3000, value=500, step=25)
        prima_mes = {"Alan Rubis": 42.0, "Alan Emeraude": 65.0, "Alan Saphir": 95.0}[plan]
        factor_demog = 1.0
 
    st.header("📊 Drivers de Siniestralidad y Reservas")
    frecuencia_reclamos = st.slider("Frecuencia (Reclamos / Miembro / Mes)", min_value=0.2, max_value=2.0, value=0.65, step=0.05)
    costo_medio_reclamo = st.number_input("Costo Medio por Reclamo (€)", min_value=20.0, max_value=300.0, value=58.0, step=2.0)
 
    rsp_pct = st.slider("Reserva de Siniestros Pendientes (RSP / RBNS) (%)", min_value=1.0, max_value=8.0, value=3.0, step=0.5) / 100.0
    ibnr_pct = st.slider("Reserva IBNR (% Siniestros No Reportados)", min_value=1.0, max_value=10.0, value=4.5, step=0.5) / 100.0
    adopcion_prevencion = st.slider("Adopción Salud Digital / Prevención (%)", min_value=10, max_value=100, value=55, step=5) / 100.0
 
    st.header("💸 Cargas de Gastos y Operación (% Prima)")
    comisiones_pct = st.slider("Comisiones / Adquisición (CAC) (%)", min_value=0.0, max_value=15.0, value=4.5, step=0.5) / 100.0
    operaciones_admin_pct = st.slider("Gastos Admin & Operaciones Ops (%)", min_value=5.0, max_value=20.0, value=9.5, step=0.5) / 100.0
    reaseguro_pct = st.slider("Costo de Reaseguro / Capital (%)", min_value=0.5, max_value=5.0, value=1.5, step=0.1) / 100.0
 
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
col1, col2, col3, col4 = st.columns(4)
 
col1.metric("Primas Devengadas Mes", f"{ingresos_primas_mes:,.0f} €")
col2.metric("Loss Ratio Incurrido (S/P)", f"{loss_ratio:.1%}", delta="Target <78%", delta_color="inverse")
col3.metric("Combined Ratio Total", f"{combined_ratio:.1%}", delta=f"{'Superávit' if combined_ratio < 1 else 'Déficit'}", delta_color="inverse")
col4.metric("Resultado Técnico Neto Mes", f"{resultado_tecnico_neto:,.0f} €")
 
st.divider()
 
# --- DASHBOARD VISUAL ---
col_left, col_right = st.columns(2)
 
with col_left:
    st.subheader("📊 Desglose de la Cuenta de Resultados (P&L Actuarial)")
    conceptos = ["Primas Devengadas", "Siniestros Pagados", "Reserva Siniestros Pendientes (RSP)", "Reserva IBNR", "Gastos Operativos & CAC", "Resultado Neto"]
    valores = [
        ingresos_primas_mes, 
        -siniestros_pagados, 
        -rsp_monto, 
        -ibnr_monto, 
        -gastos_totales_monto, 
        resultado_tecnico_neto
    ]
    df_pnl = pd.DataFrame({"Concepto": conceptos, "Monto (€)": valores})
    
    colors_pnl = ['#5956E9', '#EF4444', '#F87171', '#FCA5A5', '#F87171', '#10B981' if resultado_tecnico_neto >= 0 else '#EF4444']
    
    fig_pnl = px.bar(
        df_pnl, 
        x="Concepto", 
        y="Monto (€)", 
        color="Concepto",
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
    st.subheader("📈 Sensibilidad Combined Ratio vs Adopción Preventiva")
    adop_range = np.linspace(0.1, 1.0, 10)
    lr_range = [((siniestros_pagados_base * (1 - (a * 0.07))) * (1 + rsp_pct) * (1 + ibnr_pct)) / ingresos_primas_mes for a in adop_range]
    cr_range = [lr + expense_ratio for lr in lr_range]
    
    df_cr = pd.DataFrame({"Adopción Salud Digital (%)": adop_range * 100, "Combined Ratio (%)": np.array(cr_range) * 100})
    fig_cr = px.line(df_cr, x="Adopción Salud Digital (%)", y="Combined Ratio (%)", markers=True, color_discrete_sequence=["#5956E9"])
    
    fig_cr.add_hline(y=100, line_dash="dash", line_color="#EF4444", annotation_text="Breakeven (100%)")
    fig_cr.add_hline(y=90, line_dash="dash", line_color="#10B981", annotation_text="Target Alan (90%)")
    
    fig_cr.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_cr, use_container_width=True)
 
# --- TABLA DE RATIOS ACTUARIALES ---
st.subheader("📑 Resumen de Ratios Actuariales y Financieros")
ratios_df = pd.DataFrame({
    "Ratio Actuarial": ["Loss Ratio Incurrido (Siniestralidad Total / Primas)", "Expense Ratio (Gastos Admin + Comisiones / Primas)", "Combined Ratio (LR + ER)", "Tasa de Automatización de Siniestros (Auto-claims)"],
    "Valor Calculado": [f"{loss_ratio:.2%}", f"{expense_ratio:.2%}", f"{combined_ratio:.2%}", f"{auto_claims_rate:.1%}"],
    "Benchmark / Target Alan": ["< 78.0%", "< 12.0%", "< 90.0%", "> 90.0%"],
    "Estado": ["✅ En Rango" if loss_ratio <= 0.78 else "⚠️ Revisar Tarifa", 
               "✅ Eficiente" if expense_ratio <= 0.15 else "⚠️ Alto G&A",
               "🟢 Rentable" if combined_ratio <= 1.0 else "🔴 En Pérdida",
               "🟢 Objetivo Cumplido" if auto_claims_rate >= 0.9 else "🟡 Mejorar Adopción"]
})
 
st.dataframe(ratios_df, use_container_width=True, hide_index=True)
 
# --- BANNER DE CIERRE ---
st.markdown("""
<div class="footer-brand-box">
    <div>
        <div class="footer-brand-title">Pablo Guidi — Insurance Expert (Spanish Market)</div>
        <div class="footer-brand-sub">Pricing & Re-pricing Strategy • Portfolio Profitability & Margin Steering • Technical Leadership</div>
    </div>
    <div class="footer-badge">
        💜 Alan Health Insurance Framework
    </div>
</div>
""", unsafe_allow_html=True)
