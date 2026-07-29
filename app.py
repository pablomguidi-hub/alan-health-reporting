import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Alan Health Spain - Reporting Actuarial & Business",
    page_icon="💜",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
        color: #111827;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Header Container */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 20px;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 25px;
        flex-wrap: wrap;
        gap: 15px;
    }

    .logo-title-box {
        display: flex;
        align-items: center;
        gap: 18px;
    }

    .main-title-text {
        color: #111827;
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }

    /* BANNER MARCA PERSONAL (Pablo Guidi) */
    .personal-brand-header-badge {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border: 1.5px solid #6366F1;
        border-radius: 12px;
        padding: 10px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.12);
    }

    .brand-avatar {
        width: 42px;
        height: 42px;
        background-color: #4F46E5;
        color: white;
        font-weight: 800;
        font-size: 1.1rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(79, 70, 229, 0.3);
    }

    .brand-info-text {
        display: flex;
        flex-direction: column;
    }

    .brand-title {
        font-size: 0.70rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #4F46E5;
        font-weight: 700;
    }

    .brand-name {
        font-size: 1.10rem;
        font-weight: 800;
        color: #1E1B4B;
        margin-top: -2px;
    }

    .sub-description {
        color: #6B7280;
        font-size: 1.05rem;
        margin-top: -10px;
        margin-bottom: 25px;
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
        color: #6366F1 !important;
        font-size: 1.95em !important;
        font-weight: 800 !important;
    }

    /* SIDEBAR MARCA PERSONAL */
    .sidebar-brand-card {
        background: linear-gradient(180deg, #FFFFFF 0%, #F5F3FF 100%);
        border: 1px solid #DDD6FE;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(99, 102, 241, 0.08);
    }

    .sidebar-brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 10px;
    }

    .sidebar-avatar {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 800;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .sidebar-brand-name {
        font-weight: 800;
        font-size: 1.1rem;
        color: #1E1B4B;
        line-height: 1.2;
    }

    .sidebar-brand-role {
        font-size: 0.82rem;
        color: #6366F1;
        font-weight: 600;
    }

    .brand-status-pill {
        display: inline-block;
        background-color: #DEF7EC;
        color: #03543F;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        margin-top: 10px;
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

# --- HEADER SUPERIOR CON LOGO OFICIAL SVG (NATIVO) Y MARCA PERSONAL ---
st.markdown("""
<div class="header-container">
    <div class="logo-title-box">
        <!-- Logo Alan Oficial SVG -->
        <svg height="46" viewBox="0 0 150 46" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 6C12 6 6 12 6 20C6 28 12 34 20 34C28 34 34 28 34 20C34 12 28 6 20 6Z" fill="#6366F1"/>
            <circle cx="8" cy="11" r="5.5" fill="#6366F1"/>
            <circle cx="8" cy="11" r="2.5" fill="#EEF2FF"/>
            <circle cx="32" cy="11" r="5.5" fill="#6366F1"/>
            <circle cx="32" cy="11" r="2.5" fill="#EEF2FF"/>
            <ellipse cx="15.5" cy="18" rx="1.8" ry="2.8" fill="#FFFFFF"/>
            <ellipse cx="24.5" cy="18" rx="1.8" ry="2.8" fill="#FFFFFF"/>
            <circle cx="15.5" cy="19" r="0.9" fill="#1E1B4B"/>
            <circle cx="24.5" cy="19" r="0.9" fill="#1E1B4B"/>
            <path d="M18.5 22.5C18.5 21 21.5 21 21.5 22.5C21.5 24.8 18.5 24.8 18.5 22.5Z" fill="#1E1B4B"/>
            <path d="M17.5 27.5C19.2 29.2 20.8 29.2 22.5 27.5" stroke="#FFFFFF" stroke-width="1.4" stroke-linecap="round"/>
            <text x="44" y="31" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="29" fill="#1E1B4B" letter-spacing="-1">alan</text>
        </svg>
        <h1 class="main-title-text">Reporting Mensual de Rentabilidad y Drivers Actuariales</h1>
    </div>
    <div class="personal-brand-header-badge">
        <div class="brand-avatar">PG</div>
        <div class="brand-info-text">
            <span class="brand-title">DESARROLLADO POR</span>
            <span class="brand-name">Pablo Guidi</span>
        </div>
    </div>
</div>
<p class="sub-description">
Framework de reporting interno mensual diseñado bajo los principios de <b>transparencia radical</b> de Alan. 
Permite monitorizar la cuenta de resultados técnica, los <i>Key Actuarial Drivers</i> y la rentabilidad por segmento y producto.
</p>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div class="sidebar-brand-header">
            <div class="sidebar-avatar">PG</div>
            <div>
                <div class="sidebar-brand-name">Pablo Guidi</div>
                <div class="sidebar-brand-role">Consultoría & Analytics Actuarial</div>
            </div>
        </div>
        <div style="font-size:0.83rem; color:#4B5563; line-height:1.4;">
            Especialista en Tarificación Salud, Reservas IBNR/RBNS y Modelización P&L.
        </div>
        <div class="brand-status-pill">🟢 Creado por Pablo Guidi</div>
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

    rbns_pct = st.slider("Reserva RBNS (% Siniestros Pendientes Notificados)", min_value=1.0, max_value=8.0, value=3.0, step=0.5) / 100.0
    ibnr_pct = st.slider("Reserva IBNR (% Siniestros Incurridos No Reportados)", min_value=1.0, max_value=10.0, value=4.5, step=0.5) / 100.0
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

rbns_monto = siniestros_pagados * rbns_pct
ibnr_monto = (siniestros_pagados + rbns_monto) * ibnr_pct
siniestros_totales_incurridos = siniestros_pagados + rbns_monto + ibnr_monto

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
    conceptos = ["Primas Devengadas", "Siniestros Pagados", "Reserva RBNS", "Reserva IBNR", "Gastos Operativos & CAC", "Resultado Neto"]
    valores = [
        ingresos_primas_mes, 
        -siniestros_pagados, 
        -rbns_monto, 
        -ibnr_monto, 
        -gastos_totales_monto, 
        resultado_tecnico_neto
    ]
    df_pnl = pd.DataFrame({"Concepto": conceptos, "Monto (€)": valores})
    
    colors_pnl = ['#6366F1', '#EF4444', '#F87171', '#FCA5A5', '#F87171', '#10B981' if resultado_tecnico_neto >= 0 else '#EF4444']
    
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
    lr_range = [((siniestros_pagados_base * (1 - (a * 0.07))) * (1 + rbns_pct) * (1 + ibnr_pct)) / ingresos_primas_mes for a in adop_range]
    cr_range = [lr + expense_ratio for lr in lr_range]
    
    df_cr = pd.DataFrame({"Adopción Salud Digital (%)": adop_range * 100, "Combined Ratio (%)": np.array(cr_range) * 100})
    fig_cr = px.line(df_cr, x="Adopción Salud Digital (%)", y="Combined Ratio (%)", markers=True, color_discrete_sequence=["#6366F1"])
    
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

# --- BANNER DE CIERRE MARCA PERSONAL ---
st.markdown("""
<div class="footer-brand-box">
    <div>
        <div class="footer-brand-title">Creado por Pablo Guidi</div>
        <div class="footer-brand-sub">Modelización Actuarial Avanzada • Analytics de Salud • Optimización P&L de Seguros</div>
    </div>
    <div class="footer-badge">
        💜 Alan Health Insurance Framework
    </div>
</div>
""", unsafe_allow_html=True)
