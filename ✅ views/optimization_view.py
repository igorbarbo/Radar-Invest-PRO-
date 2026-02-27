
# ARQUIVO 17: views/optimization_view.py
content = '''"""Tela de otimização"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from core import PortfolioOptimizer, data_fetcher
from config import ESTRATEGIAS

def render_optimization(df_precos):
    """Renderiza tela de otimização"""
    
    st.header("🎯 Otimização de Carteira")
    
    # Sidebar - parâmetros
    with st.sidebar:
        st.subheader("Parâmetros")
        
        estrategia = st.selectbox(
            "Estratégia",
            ["max_sharpe", "min_variance", "target_return", "risk_parity"],
            format_func=lambda x: {
                "max_sharpe": "Máximo Sharpe",
                "min_variance": "Mínima Variância",
                "target_return": "Target de Retorno",
                "risk_parity": "Risk Parity"
            }[x]
        )
        
        if estrategia == "target_return":
            target = st.slider("Retorno Alvo (%)", 5.0, 20.0, 10.0) / 100
        
        taxa_livre_risco = st.slider("Taxa Livre de Risco (%)", 0.0, 15.0, 10.0) / 100
    
    # Otimização
    optimizer = PortfolioOptimizer(df_precos)
    
    if estrategia == "max_sharpe":
        resultado = optimizer.optimize_max_sharpe(taxa_livre_risco)
    elif estrategia == "min_variance":
        resultado = optimizer.optimize_min_variance()
    elif estrategia == "target_return":
        resultado = optimizer.optimize_target_return(target)
    else:
        resultado = optimizer.optimize_risk_parity()
    
    # Resultados
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Retorno Esperado", f"{resultado['retorno_esperado']*100:.1f}%")
    with col2:
        st.metric("Volatilidade", f"{resultado['volatilidade']*100:.1f}%")
    with col3:
        st.metric("Sharpe", f"{resultado['sharpe']:.2f}")
    
    # Gráfico de alocação
    st.subheader("Alocação Otimizada")
    
    pesos_df = pd.DataFrame({
        'Ativo': list(resultado['pesos'].keys()),
        'Peso': [v*100 for v in resultado['pesos'].values()]
    })
    pesos_df = pesos_df[pesos_df['Peso'] > 0.5]  # Filtra pesos relevantes
    
    fig = px.pie(pesos_df, values='Peso', names='Ativo', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela
    st.dataframe(pesos_df.sort_values('Peso', ascending=False), use_container_width=True)
    
    # Fronteira Eficiente
    st.subheader("Fronteira Eficiente")
    
    with st.spinner("Calculando fronteira..."):
        ef = optimizer.get_efficient_frontier(n_points=30)
    
    fig = go.Figure()
    
    # Fronteira
    fig.add_trace(go.Scatter(
        x=ef['volatilidade']*100,
        y=ef['retorno']*100,
        mode='lines',
        name='Fronteira Eficiente',
        line=dict(color='blue', width=2)
    ))
    
    # Carteira otimizada
    fig.add_trace(go.Scatter(
        x=[resultado['volatilidade']*100],
        y=[resultado['retorno_esperado']*100],
        mode='markers',
        name='Carteira Otimizada',
        marker=dict(color='red', size=15, symbol='star')
    ))
    
    fig.update_layout(
        xaxis_title='Volatilidade (%)',
        yaxis_title='Retorno Esperado (%)',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
'''

with open(f"{base_path}/views/optimization_view.py", "w") as f:
    f.write(content)

print("✅ views/optimization_view.py")
