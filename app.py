
# Criar app.py limpo SEM código de escrita de arquivo
app_py_limpo = '''"""
Radar Invest PRO v2.0
Sistema completo de gestão de carteiras híbridas
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add current dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ESTRATEGIAS
from models import Asset, Portfolio
from core import data_fetcher, PortfolioOptimizer, RiskAnalyzer
from views import render_dashboard, render_optimization, render_risk_analysis
from utils import cache

# Configuração da página
st.set_page_config(
    page_title="Radar Invest PRO v2.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2329; border-radius: 10px; padding: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1e2329; 
        border-radius: 8px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

def init_session():
    """Inicializa sessão"""
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = Portfolio(
            nome="Minha Carteira",
            ativos=[
                Asset(ticker="PETR4", nome="Petrobras", classe="acoes_br", quantidade=100, preco_medio=35.0),
                Asset(ticker="VALE3", nome="Vale", classe="acoes_br", quantidade=50, preco_medio=85.0),
                Asset(ticker="BBAS3", nome="Banco do Brasil", classe="acoes_br", quantidade=80, preco_medio=25.0),
            ]
        )

def atualizar_precos():
    """Atualiza preços dos ativos"""
    portfolio = st.session_state.portfolio
    tickers = [a.ticker for a in portfolio.ativos]
    
    with st.spinner("Atualizando preços..."):
        precos = data_fetcher.get_current_prices(tickers)
        
        for ativo in portfolio.ativos:
            ativo.preco_atual = precos.get(ativo.ticker, ativo.preco_medio)

def sidebar():
    """Menu lateral"""
    st.sidebar.title("🚀 Radar Invest PRO")
    st.sidebar.markdown("---")
    
    # Menu
    page = st.sidebar.radio(
        "Navegação",
        ["📊 Dashboard", "🎯 Otimização", "⚠️ Risco", "⚙️ Configurações"]
    )
    
    st.sidebar.markdown("---")
    
    # Ações rápidas
    if st.sidebar.button("🔄 Atualizar Preços"):
        atualizar_precos()
        st.sidebar.success("Preços atualizados!")
    
    if st.sidebar.button("🗑️ Limpar Cache"):
        cache.clear()
        st.sidebar.success("Cache limpo!")
    
    return page

def page_dashboard():
    """Página dashboard"""
    atualizar_precos()
    render_dashboard(st.session_state.portfolio)

def page_optimization():
    """Página otimização"""
    st.subheader("Selecione os ativos para otimização")
    
    # Busca dados históricos
    tickers = ["PETR4.SA", "VALE3.SA", "BBAS3.SA", "ITUB4.SA", "WEGE3.SA", 
               "ABEV3.SA", "RENT3.SA", "PRIO3.SA", "IVVB11.SA"]
    
    with st.spinner("Carregando dados históricos..."):
        df_precos = data_fetcher.get_historical_prices(tickers, period="2y")
    
    if not df_precos.empty:
        render_optimization(df_precos)
    else:
        st.error("Erro ao carregar dados")

def page_risk():
    """Página risco"""
    st.subheader("Análise de Risco da Carteira")
    
    tickers = [a.ticker for a in st.session_state.portfolio.ativos]
    
    with st.spinner("Carregando dados..."):
        df_precos = data_fetcher.get_historical_prices(tickers, period="2y")
    
    if not df_precos.empty:
        weights = st.session_state.portfolio.get_pesos_atuais()
        render_risk_analysis(df_precos, weights)
    else:
        st.error("Erro ao carregar dados")

def page_settings():
    """Página configurações"""
    st.header("⚙️ Configurações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Carteira Atual")
        
        # Editor de carteira
        dados = []
        for ativo in st.session_state.portfolio.ativos:
            dados.append({
                'Ticker': ativo.ticker,
                'Quantidade': ativo.quantidade,
                'Preço Médio': ativo.preco_medio
            })
        
        df_edit = st.data_editor(
            pd.DataFrame(dados),
            num_rows="dynamic",
            use_container_width=True
        )
        
        if st.button("💾 Salvar Carteira"):
            novos_ativos = []
            for _, row in df_edit.iterrows():
                novos_ativos.append(Asset(
                    ticker=row['Ticker'],
                    nome=row['Ticker'],
                    classe="acoes_br",
                    quantidade=float(row['Quantidade']),
                    preco_medio=float(row['Preço Médio'])
                ))
            st.session_state.portfolio.ativos = novos_ativos
            st.success("Carteira salva!")
    
    with col2:
        st.subheader("Estratégias Pré-configuradas")
        
        for key, estrategia in ESTRATEGIAS.items():
            with st.expander(f"{estrategia['nome']}"):
                st.write(estrategia['descricao'])
                st.write(f"Target: {estrategia['target_retorno']}% ao ano")
                st.json(estrategia['alocacao'])

def main():
    """Função principal"""
    init_session()
    
    page = sidebar()
    
    if page == "📊 Dashboard":
        page_dashboard()
    elif page == "🎯 Otimização":
        page_optimization()
    elif page == "⚠️ Risco":
        page_risk()
    elif page == "⚙️ Configurações":
        page_settings()

if __name__ == "__main__":
    main()
'''

base_path = "/mnt/kimi/output/radar_invest_pro"
with open(f"{base_path}/app.py", "w") as f:
    f.write(app_py_limpo)

print("✅ app.py corrigido!")
print("📝 Removido: código de escrita de arquivo que causava erro")
