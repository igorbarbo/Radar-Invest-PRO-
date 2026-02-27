
# ARQUIVO 18: views/risk_view.py
content = '''"""Tela de análise de risco"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from core import RiskAnalyzer

def render_risk_analysis(df_precos, weights):
    """Renderiza análise de risco"""
    
    st.header("⚠️ Análise de Risco")
    
    analyzer = RiskAnalyzer(df_precos)
    
    # Métricas principais
    metrics = analyzer.calculate_all_metrics(weights)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Volatilidade", f"{metrics['volatilidade_anual']*100:.1f}%")
    with col2:
        st.metric("Max Drawdown", f"{metrics['max_drawdown']*100:.1f}%")
    with col3:
        st.metric("VaR 95%", f"{metrics['var_95']*100:.2f}%")
    with col4:
        st.metric("CVaR 95%", f"{metrics['cvar_95']*100:.2f}%")
    
    st.divider()
    
    # Monte Carlo
    st.subheader("🎲 Simulação Monte Carlo (10 anos)")
    
    with st.spinner("Simulando 10.000 cenários..."):
        mc_result = analyzer.monte_carlo_simulation(
            weights, 
            n_simulations=5000,
            n_days=2520,  # 10 anos
            initial_value=100000
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Valor Médio", f"R$ {mc_result['mean']:,.0f}")
    with col2:
        st.metric("Percentil 5%", f"R$ {mc_result['percentile_5']:,.0f}")
    with col3:
        st.metric("Percentil 95%", f"R$ {mc_result['percentile_95']:,.0f}")
    
    # Gráfico de distribuição
    fig = px.histogram(
        x=mc_result['simulations'][:, -1],
        nbins=50,
        labels={'x': 'Valor Final (R$)'},
        title='Distribuição do Valor Final'
    )
    fig.add_vline(x=mc_result['mean'], line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)
    
    # Probabilidade de lucro
    prob_lucro = mc_result['prob_profit'] * 100
    st.progress(prob_lucro/100, text=f"Probabilidade de lucro: {prob_lucro:.1f}%")
'''

with open(f"{base_path}/views/risk_view.py", "w") as f:
    f.write(content)

print("✅ views/risk_view.py")
