import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA (Estilo Alan) ---
st.set_page_config(
    page_title="Alan Health Spain - Monthly Actuarial & Business Reporting",
    page_icon="💜",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS (Alineado con Brand & UI de Alan) ---
st.markdown("""
<style>
    /* Fondo principal y tipografía general */
    .stApp {
        background-color: #FFFFFF;
        color: #111827;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header & Branding Alan */
    .alan-brand-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 8px;
    }
    .alan-logo-badge {
        background-color: #6366F1;
        color: white;
        font-weight: 800;
        font-size: 24px;
        padding: 8px 18px;
        border-radius: 20px;
        letter-spacing: -0.5px;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
    }
    .main-title {
        color: #111827;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }
    .sub-description {
        color: #6B7280;
        font-size: 1.05rem;
        margin-top: 8px;
        margin-bottom: 24px;
    }

    /* Estilo para las Tarjetas de Métricas (KPIs) */
    div[data-testid="stMetricValue"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    div[data-testid="stMetricLabel"] p {
        color: #6B7280;
        font-size: 0.88em;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        color: #6366F1 !important; /* Violeta Alan */
        font-size: 1.9em !important;
        font-weight: 700 !important;
    }

    /* Sidebar - Estilo Alan */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #6366F1 !important;
    }

    /* Separadores */
    hr {
        border: 0;
        border-top: 1px solid #E2E8F0;
        margin: 24px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER / MARCA PERSONAL ---
st.markdown("""
<div class="alan-brand-header">
    <span class="alan-logo-badge">alan</span>
    <h1 class="main-title">Alan Health Spain: Reporting Mensual de Rentabilidad y Drivers Actuariales</h1>
</div>
<p class="sub-description">
Framework de reporting interno mensual diseñado bajo los principios de <b>transparencia radical</b> de Alan. 
Permite monitorizar la cuenta de resultados técnica, los <i>Key Actuarial Drivers</i> y la rentabilidad por segmento y producto.
</p>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONTEXTO Y OFERTAS OFICIALES DE ALAN ---
st.sidebar.header("🏢 Segmento de Cliente y Oferta")
segmento = st.sidebar.radio("Tipo de Cliente", ["Empresas (B2B)", "Individuales / TNS (B2C)"])

if segmento == "Empresas (B2B)":
    plan = st.sidebar.selectbox("Oferta B2B (Elegible Colectivos)", ["Essentiel", "Balanced", "Optimal"])
    num_miembros = st.sidebar.slider("Número de Asegurados en Colectivo", min_value=50, max_value=10000, value=1000, step=50)
    edad_media = st.sidebar.slider("Edad Media de la Plantilla (Ajuste Demográfico)", min_value=20, max_value=65, value=36)
    
    # Primas base estimadas B2B
    prima_base = {"Essentiel": 38.0, "Balanced": 52.0, "Optimal": 75.0}[plan]
    # Factor demográfico actuarial B2B (+1.5% por año sobre 30 años base)
    factor_demog = 1.0 + max(0, (edad_media - 30) * 0.015)
    prima_mes = prima_base * factor_demog
else:
    plan = st.sidebar.selectbox("Oferta B2C (Trabajadores No Salariados / TNS)", ["Alan Rubis", "Alan Emeraude", "Alan Saphir"])
    num_miembros = st.sidebar.slider("Número de Asegurados Individuales", min_value=50, max_value=3000, value=500, step=25)
    prima_mes = {"Alan Rubis": 42.0, "Alan Emeraude": 65.0, "Alan Saphir": 95.0}[plan]
    factor_demog = 1.0

st.sidebar.header("📊 Drivers de Siniestralidad y Reservas")
frecuencia_reclamos = st.sidebar.slider("Frecuencia (Reclamos / Miembro / Mes)", min_value=0.2, max_value=2.0, value=0.65, step=0.05)
costo_medio_reclamo = st.sidebar.number_input("Costo Medio por Reclamo (€)", min_value=20.0, max_value=300.0, value=58.0, step=2.0)

# Reservas Actuariales
rbns_pct = st.sidebar.slider("Reserva RBNS (% Siniestros Pendientes Notificados)", min_value=1.0, max_value=8.0, value=3.0, step=0.5) / 100.0
ibnr_pct = st.sidebar.slider("Reserva IBNR (% Siniestros Incurridos No Reportados)", min_value=1.0, max_value=10.0, value=4.5, step=0.5) / 100.0
adopcion_prevencion = st.sidebar.slider("Adopción Salud Digital / Prevención (%)", min_value=10, max_value=100, value=55, step=5) / 100.0

st.sidebar.header("💸 Cargas de Gastos y Operación (% Prima)")
comisiones_pct = st.sidebar.slider("Comisiones / Adquisición (CAC) (%)", min_value=0.0, max_value=15.0, value=4.5, step=0.5) / 100.0
operaciones_admin_pct = st.sidebar.slider("Gastos Admin & Operaciones Ops (%)", min_value=5.0, max_value=20.0, value=9.5, step=0.5) / 100.0
reaseguro_pct = st.sidebar.slider("Costo de Reaseguro / Capital (%)", min_value=0.5, max_value=5.0, value=1.5, step=0.1) / 100.0

# --- CÁLCULOS ACTUARIALES ---
ingresos_primas_mes = num_miembros * prima_mes

# Siniestralidad
siniestros_pagados_base = num_miembros * frecuencia_reclamos * costo_medio_reclamo
reduccion_prevencion = adopcion_prevencion * 0.07 # Reducción por prevención activa
siniestros_pagados = siniestros_pagados_base * (1.0 - reduccion_prevencion)

rbns_monto = siniestros_pagados * rbns_pct
ibnr_monto = (siniestros_pagados + rbns_monto) * ibnr_pct
siniestros_totales_incurridos = siniestros_pagados + rbns_monto + ibnr_monto

# Gastos Operativos y Adquisición
comisiones_monto = ingresos_primas_mes * comisiones_pct
gastos_admin_monto = ingresos_primas_mes * operaciones_admin_pct
reaseguro_monto = ingresos_primas_mes * reaseguro_pct
gastos_totales_monto = comisiones_monto + gastos_admin_monto + reaseguro_monto

# Márgenes y Ratios Actuariales
margen_tecnico_bruto = ingresos_primas_mes - siniestros_totales_incurridos
resultado_tecnico_neto = margen_tecnico_bruto - gastos_totales_monto

loss_ratio = (siniestros_totales_incurridos / ingresos_primas_mes) if ingresos_primas_mes > 0 else 0
expense_ratio = (gastos_totales_monto / ingresos_primas_mes) if ingresos_primas_mes > 0 else 0
combined_ratio = loss_ratio + expense_ratio
auto_claims_rate = min(0.96, 0.82 + (adopcion_prevencion * 0.12))

# --- TARJETAS DE MÉTRICAS CLAVE (KPIs) ---
st.divider()
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
    
    # Paleta con identidad visual Alan
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

st.caption("Alan Health Insurance - Framework de Reporting Actuarial y de Producto v3.0.")
