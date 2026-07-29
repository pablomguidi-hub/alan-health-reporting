import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Alan Health - Monthly Actuarial & Business Reporting",
    page_icon="💚",
    layout="wide"
)

st.title("💚 Alan Health: Reporting Mensual de Rentabilidad y Drivers Actuariales")
st.markdown("""
Dashboard interno alineado con el principio de **transparencia radical** de Alan. 
Permite monitorizar los *key actuarial drivers* y la rentabilidad por segmento de cliente y oferta.
""")

st.sidebar.header("🏢 Filtros del Segmento de Cliente")

segmento = st.sidebar.radio("Tipo de Cliente",)

if segmento == "Empresas (B2B)":
    plan = st.sidebar.selectbox("Oferta B2B",)
    num_miembros = st.sidebar.slider("Número de Miembros Asegurados", min_value=50, max_value=5000, value=500, step=50)
    edad_media = st.sidebar.slider("Edad Media de la Plantilla (Ajuste Demográfico)", min_value=22, max_value=60, value=35)
    prima_base = {"Essentiel": 38.0, "Balanced": 52.0, "Optimal": 75.0}[plan]
    # Factor demográfico B2B: +1.5% por cada año por encima de los 30 años
    factor_demog = 1.0 + max(0, (edad_media - 30) * 0.015)
    prima_mes = prima_base * factor_demog
else:
    plan = st.sidebar.selectbox("Oferta B2C (TNS)",)
    num_miembros = st.sidebar.slider("Número de Asegurados Individuales", min_value=50, max_value=2000, value=300, step=25)
    edad = st.sidebar.slider("Edad del Asegurado", min_value=18, max_value=75, value=40)
    
    # Lógica de precios de Alan: base a los 40 años +1€/año hasta los 60, +2€/año desde los 60
    base_precios = {"Alan Rubis": 49.0, "Alan Emeraude": 64.0, "Alan Saphir": 91.0}
    prima_base = base_precios[plan]
    
    if edad <= 60:
        prima_mes = prima_base + (edad - 40) * 1.0
    else:
        prima_mes = prima_base + (60 - 40) * 1.0 + (edad - 60) * 2.0
    
    factor_demog = 1.0

st.sidebar.header("📊 Drivers Actuariales Mensuales")
frecuencia_reclamos = st.sidebar.slider("Frecuencia (Reclamos / Miembro / Mes)", min_value=0.2, max_value=2.0, value=0.6, step=0.05)
costo_medio_reclamo = st.sidebar.number_input("Costo Medio por Reclamo (€)", min_value=20.0, max_value=300.0, value=55.0, step=5.0)
adopcion_prevencion = st.sidebar.slider("Adopción Salud Digital / Prevención (%)", min_value=10, max_value=100, value=50, step=5) / 100.0

# Cálculos Mensuales
ingresos_primas_mes = num_miembros * prima_mes
siniestros_incurridos_mes = num_miembros * frecuencia_reclamos * costo_medio_reclamo

# Reducción de siniestralidad por prevención activa
reduccion_prevencion = adopcion_prevencion * 0.07
siniestros_ajustados = siniestros_incurridos_mes * (1.0 - reduccion_prevencion)

loss_ratio = (siniestros_ajustados / ingresos_primas_mes) if ingresos_primas_mes > 0 else 0
auto_claims_rate = min(0.96, 0.82 + (adopcion_prevencion * 0.12))
margen_tecnico_mes = ingresos_primas_mes - siniestros_ajustados

col1, col2, col3, col4 = st.columns(4)
col1.metric("Primas Mensuales", f"{ingresos_primas_mes:,.0f} €")
col2.metric("Loss Ratio (S/P)", f"{loss_ratio:.1%}", delta=f"Target 78%", delta_color="inverse")
col3.metric("Auto-Claims Processing", f"{auto_claims_rate:.1%}")
col4.metric("Margen Técnico Mensual", f"{margen_tecnico_mes:,.0f} €")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Comparativa de Loss Ratio Proyectado")
    if segmento == "Empresas (B2B)":
        planes =
        primas_plan = [38 * factor_demog, 52 * factor_demog, 75 * factor_demog]
    else:
        planes =
        primas_plan =
        for p_name in planes:
            p_base = {"Alan Rubis": 49.0, "Alan Emeraude": 64.0, "Alan Saphir": 91.0}[p_name]
            if edad <= 60:
                primas_plan.append(p_base + (edad - 40) * 1.0)
            else:
                primas_plan.append(p_base + (60 - 40) * 1.0 + (edad - 60) * 2.0)
                
    lr_planes = [(frecuencia_reclamos * costo_medio_reclamo * (1.0 - reduccion_prevencion)) / p for p in primas_plan]
    
    df_lr = pd.DataFrame({"Plan": planes, "Loss Ratio (%)": [lr * 100 for lr in lr_planes]})
    fig_lr = px.bar(df_lr, x="Plan", y="Loss Ratio (%)", text_auto=".1f", color_discrete_sequence=)
    fig_lr.add_hline(y=78.0, line_dash="dash", line_color="red", annotation_text="Objetivo Target (78%)")
    st.plotly_chart(fig_lr, use_container_width=True)

with col_right:
    st.subheader("🩺 Distribución Estimada del Gasto Sanitario")
    categorias =
    pesos = [0.25, 0.35, 0.25, 0.15]
    gastos = [siniestros_ajustados * p for p in pesos]
    df_cat = pd.DataFrame({"Categoría": categorias, "Gasto Mensual (€)": gastos})
    fig_pie = px.pie(df_cat, names="Categoría", values="Gasto Mensual (€)", color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_pie, use_container_width=True)

st.caption("Caso técnico Alan España - Framework de Reporting Actuarial y de Producto.")
