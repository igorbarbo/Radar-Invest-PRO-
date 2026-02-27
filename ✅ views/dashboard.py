
# ARQUIVO 16: views/dashboard.py
content = '''"""Dashboard principal"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from models import Portfolio, Asset
from core import data_fetcher
from config import ESTRATEGIAS

def render_dashboard(portfolio: Portfolio):
    """Renderiza dashboard da carteira"""
    
    st.header(f"📊 {portfolio.nome}")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Valor Total",
            f"R$ {portfolio.valor_total:,.2f}",
            f"{portfolio.retorno_total*100:.1f}%"
        )
    
    with col2:
        st.metric(
            "Valor Investido",
            f"R$ {portfolio.valor_investido:,.2f}"
        )
    
    with col3:
        st.metric(
            "Lucro/Prejuízo",
            f"R$ {portfolio.valor_total - portfolio.valor_investido:,.2f}"
        )
    
    with col4:
        st.metric(
            "Nº de Ativos",
            len(portfolio.ativos)
        )
    
    st.divider()
    
    # Gráficos
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Alocação por Ativo")
        pesos = portfolio.get_pesos_atuais()
        
        fig = px.pie(
            values=list(pesos.values()),
            names=list(pesos.keys()),
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("Alocação por Classe")
        alocacao = portfolio.get_alocacao_por_classe()
        
        fig = px.bar(
            x=list(alocacao.keys()),
            y=[v*100 for v in alocacao.values()],
            labels={'x': 'Classe', 'y': '%'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de ativos
    st.subheader("Detalhamento")
    df = portfolio.to_dataframe()
    st.dataframe(df, use_container_width=True)
'''

with open(f"{base_path}/views/dashboard.py", "w") as f:
    f.write(content)

print("✅ views/dashboard.py")
