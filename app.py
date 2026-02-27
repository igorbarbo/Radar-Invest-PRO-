


Radar Invest PRO v2.0 - Versão Monolítica
Todas as funcionalidades em um único arquivo
"""
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from scipy.optimize import minimize
import plotly.express as px
import plotly.graph_objects as go
import hashlib
import pickle
from pathlib import Path

# ============================================================
# CONFIGURAÇÕES
# ============================================================

ESTRATEGIAS = {
    "conservador": {
        "nome": "Conservador IPCA+",
        "descricao": "Foco em renda fixa IPCA+",
        "alocacao": {"tesouro_ipca": 50, "acoes_br": 25, "fiis": 15, "commodities": 10},
        "target_retorno": 10.0
    },
    "moderado": {
        "nome": "Moderado Balanceado",
        "descricao": "Balanceado RF/RV",
        "alocacao": {"tesouro_ipca": 30, "acoes_br": 30, "acoes_us": 15, "fiis": 15, "cripto": 5, "commodities": 5},
        "target_retorno": 12.0
    },
    "agressivo": {
        "nome": "Agressivo Growth",
        "descricao": "Foco em ações",
        "alocacao": {"tesouro_ipca": 10, "acoes_br": 40, "acoes_us": 25, "fiis": 10, "cripto": 10, "commodities": 5},
        "target_retorno": 15.0
    }
}

# ============================================================
# CACHE
# ============================================================

class CacheManager:
    def __init__(self):
        self.cache_dir = Path(".cache")
        self.cache_dir.mkdir(exist_ok=True)
    
    def get(self, key: str, ttl: int = 3600) -> Optional:
        path = self.cache_dir / f"{key}.pkl"
        if not path.exists():
            return None
        modified_time = datetime.fromtimestamp(path.stat().st_mtime)
        if datetime.now() - modified_time > timedelta(seconds=ttl):
            return None
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except:
            return None
    
    def set(self, key: str, value):
        path = self.cache_dir / f"{key}.pkl"
        try:
            with open(path, 'wb') as f:
                pickle.dump(value, f)
        except:
            pass
    
    def clear(self):
        for file in self.cache_dir.glob("*.pkl"):
            file.unlink()

cache = CacheManager()

# ============================================================
# DATA FETCHER
# ============================================================

class DataFetcher:
    def get_historical_prices(self, tickers: List[str], period: str = "2y") -> pd.DataFrame:
        cache_key = f"hist_{'_'.join(sorted(tickers))}_{period}"
        cached = cache.get(cache_key, 86400)
        if cached is not None:
            return cached
        
        try:
            tickers_yf = [t if '.SA' in t else f"{t}.SA" for t in tickers]
            df = yf.download(tickers_yf, period=period, progress=False)
            if len(tickers_yf) == 1:
                df.columns = pd.MultiIndex.from_product([df.columns, tickers_yf])
            df_close = df['Close'] if 'Close' in df.columns else df
            df_close.columns = [c.replace('.SA', '') for c in df_close.columns]
            cache.set(cache_key, df_close)
            return df_close
        except:
            return pd.DataFrame()
    
    def get_current_prices(self, tickers: List[str]) -> Dict[str, float]:
        cache_key = f"current_{'_'.join(sorted(tickers))}"
        cached = cache.get(cache_key, 3600)
        if cached is not None:
            return cached
        
        prices = {}
        for ticker in tickers:
            try:
                ticker_yf = ticker if '.SA' in ticker else f"{ticker}.SA"
                stock = yf.Ticker(ticker_yf)
                info = stock.info
                price = info.get('regularMarketPrice', info.get('previousClose', 0))
                prices[ticker.replace('.SA', '')] = price
            except:
                prices[ticker.replace('.SA', '')] = 0
        
        cache.set(cache_key, prices)
        return prices

data_fetcher = DataFetcher()

# ============================================================
# MODELOS
# ============================================================

class Asset:
    def __init__(self, ticker: str, nome: str, classe: str, quantidade: float = 0, 
                 preco_medio: float = 0, preco_atual: float = 0):
        self.ticker = ticker
        self.nome = nome
        self.classe = classe
        self.quantidade = quantidade
        self.preco_medio = preco_medio
        self.preco_atual = preco_atual
    
    @property
    def valor_atual(self):
        return self.preco_atual * self.quantidade
    
    @property
    def valor_investido(self):
        return self.preco_medio * self.quantidade
    
    @property
    def retorno(self):
        if self.preco_medio == 0:
            return 0.0
        return (self.preco_atual - self.preco_medio) / self.preco_medio

class Portfolio:
    def __init__(self, nome: str, ativos: List[Asset] = None):
        self.nome = nome
        self.ativos = ativos or []
    
    @property
    def valor_total(self):
        return sum(a.valor_atual for a in self.ativos)
    
    @property
    def valor_investido(self):
        return sum(a.valor_investido for a in self.ativos)
    
    @property
    def retorno_total(self):
        if self.valor_investido == 0:
            return 0.0
        return (self.valor_total - self.valor_investido) / self.valor_investido
    
    def get_pesos_atuais(self):
        total = self.valor_total
        if total == 0:
            return {}
        return {a.ticker: a.valor_atual / total for a in self.ativos}
    
    def to_dataframe(self):
        data = []
        for ativo in self.ativos:
            data.append({
                'ticker': ativo.ticker,
                'nome': ativo.nome,
                'classe': ativo.classe,
                'quantidade': ativo.quantidade,
                'preco_medio': ativo.preco_medio,
                'preco_atual': ativo.preco_atual,
                'valor_investido': ativo.valor_investido,
                'valor_atual': ativo.valor_atual,
                'retorno_%': ativo.retorno * 100,
                'peso_%': (ativo.valor_atual / self.valor_total * 100) if self.valor_total > 0 else 0
            })
        return pd.DataFrame(data)

# ============================================================
# OTIMIZADOR
# ============================================================

class PortfolioOptimizer:
    def __init__(self, df_precos: pd.DataFrame):
        self.df_precos = df_precos
        self.retornos = np.log(df_precos / df_precos.shift(1)).dropna()
        self.mu = self.retornos.mean() * 252
        self.sigma = self.retornos.cov() * 252
        self.tickers = list(df_precos.columns)
        self.n = len(self.tickers)
    
    def optimize_max_sharpe(self, risk_free_rate: float = 0.10):
        def neg_sharpe(weights):
            port_return = np.dot(weights, self.mu)
            port_vol = np.sqrt(np.dot(weights.T, np.dot(self.sigma, weights)))
            return -(port_return - risk_free_rate) / port_vol
        
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        bounds = tuple((0, 1) for _ in range(self.n))
        x0 = np.array([1/self.n] * self.n)
        
        result = minimize(neg_sharpe, x0, method='SLSQP', bounds=bounds, constraints=constraints)
        pesos = dict(zip(self.tickers, result.x))
        
        return {
            'pesos': pesos,
            'retorno_esperado': np.dot(result.x, self.mu),
            'volatilidade': np.sqrt(np.dot(result.x.T, np.dot(self.sigma, result.x))),
            'sharpe': -result.fun
        }
    
    def optimize_min_variance(self):
        def portfolio_vol(weights):
            return np.sqrt(np.dot(weights.T, np.dot(self.sigma, weights)))
        
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        bounds = tuple((0, 1) for _ in range(self.n))
        x0 = np.array([1/self.n] * self.n)
        
        result = minimize(portfolio_vol, x0, method='SLSQP', bounds=bounds, constraints=constraints)
        pesos = dict(zip(self.tickers, result.x))
        
        return {
            'pesos': pesos,
            'retorno_esperado': np.dot(result.x, self.mu),
            'volatilidade': result.fun,
            'sharpe': np.dot(result.x, self.mu) / result.fun if result.fun > 0 else 0
        }

# ============================================================
# RISK ANALYZER
# ============================================================

class RiskAnalyzer:
    def __init__(self, df_precos: pd.DataFrame):
        self.df_precos = df_precos
        self.retornos = np.log(df_precos / df_precos.shift(1)).dropna()
    
    def calculate_var(self, weights: Dict[str, float], confidence: float = 0.95):
        pesos_array = np.array([weights.get(t, 0) for t in self.df_precos.columns])
        port_returns = (self.retornos * pesos_array).sum(axis=1)
        return np.percentile(port_returns, (1 - confidence) * 100)
    
    def monte_carlo_simulation(self, weights: Dict[str, float], n_simulations: int = 5000, 
                               n_days: int = 2520, initial_value: float = 100000):
        pesos_array = np.array([weights.get(t, 0) for t in self.df_precos.columns])
        mu = self.retornos.mean().values
        sigma = self.retornos.cov().values
        
        np.random.seed(42)
        results = np.zeros((n_simulations, n_days))
        
        for i in range(n_simulations):
            daily_returns = np.random.multivariate_normal(mu, sigma, n_days)
            port_returns = daily_returns @ pesos_array
            cumulative = np.cumprod(1 + port_returns)
            results[i, :] = initial_value * cumulative
        
        final_values = results[:, -1]
        
        return {
            'mean': np.mean(final_values),
            'percentile_5': np.percentile(final_values, 5),
            'percentile_95': np.percentile(final_values, 95),
            'prob_profit': np.mean(final_values > initial_value),
            'simulations': results
        }

# ============================================================
# STREAMLIT APP
# ============================================================

st.set_page_config(page_title="Radar Invest PRO v2.0", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2329; border-radius: 10px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

def init_session():
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = Portfolio(
            nome="Minha Carteira",
            ativos=[
                Asset("PETR4", "Petrobras", "acoes_br", 100, 35.0),
                Asset("VALE3", "Vale", "acoes_br", 50, 85.0),
                Asset("BBAS3", "Banco do Brasil", "acoes_br", 80, 25.0),
            ]
        )

def sidebar():
    st.sidebar.title("🚀 Radar Invest PRO")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Navegação", ["📊 Dashboard", "🎯 Otimização", "⚠️ Risco", "⚙️ Configurações"])
    
    if st.sidebar.button("🗑️ Limpar Cache"):
        cache.clear()
        st.sidebar.success("Cache limpo!")
    
    return page

def page_dashboard():
    st.header("📊 Dashboard")
    portfolio = st.session_state.portfolio
    
    # Atualiza preços
    tickers = [a.ticker for a in portfolio.ativos]
    precos = data_fetcher.get_current_prices(tickers)
    for ativo in portfolio.ativos:
        ativo.preco_atual = precos.get(ativo.ticker, ativo.preco_medio)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Valor Total", f"R$ {portfolio.valor_total:,.2f}", f"{portfolio.retorno_total*100:.1f}%")
    col2.metric("Valor Investido", f"R$ {portfolio.valor_investido:,.2f}")
    col3.metric("Lucro/Prejuízo", f"R$ {portfolio.valor_total - portfolio.valor_investido:,.2f}")
    col4.metric("Nº Ativos", len(portfolio.ativos))
    
    # Gráficos
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Alocação")
        pesos = portfolio.get_pesos_atuais()
        fig = px.pie(values=list(pesos.values()), names=list(pesos.keys()), hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Detalhamento")
        st.dataframe(portfolio.to_dataframe(), use_container_width=True)

def page_optimization():
    st.header("🎯 Otimização")
    
    tickers = ["PETR4.SA", "VALE3.SA", "BBAS3.SA", "ITUB4.SA", "WEGE3.SA", 
               "ABEV3.SA", "RENT3.SA", "PRIO3.SA", "IVVB11.SA"]
    
    with st.spinner("Carregando dados..."):
        df_precos = data_fetcher.get_historical_prices(tickers, period="2y")
    
    if df_precos.empty:
        st.error("Erro ao carregar dados")
        return
    
    optimizer = PortfolioOptimizer(df_precos)
    
    estrategia = st.selectbox("Estratégia", ["max_sharpe", "min_variance"],
                              format_func=lambda x: "Máximo Sharpe" if x == "max_sharpe" else "Mínima Variância")
    
    if estrategia == "max_sharpe":
        resultado = optimizer.optimize_max_sharpe()
    else:
        resultado = optimizer.optimize_min_variance()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Retorno Esperado", f"{resultado['retorno_esperado']*100:.1f}%")
    col2.metric("Volatilidade", f"{resultado['volatilidade']*100:.1f}%")
    col3.metric("Sharpe", f"{resultado['sharpe']:.2f}")
    
    # Alocação
    pesos_df = pd.DataFrame({'Ativo': list(resultado['pesos'].keys()), 
                             'Peso': [v*100 for v in resultado['pesos'].values()]})
    pesos_df = pesos_df[pesos_df['Peso'] > 0.5]
    
    fig = px.pie(pesos_df, values='Peso', names='Ativo', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(pesos_df.sort_values('Peso', ascending=False), use_container_width=True)

def page_risk():
    st.header("⚠️ Análise de Risco")
    
    tickers = [a.ticker for a in st.session_state.portfolio.ativos]
    df_precos = data_fetcher.get_historical_prices(tickers, period="2y")
    
    if df_precos.empty:
        st.error("Erro ao carregar dados")
        return
    
    weights = st.session_state.portfolio.get_pesos_atuais()
    analyzer = RiskAnalyzer(df_precos)
    
    var = analyzer.calculate_var(weights)
    
    col1, col2 = st.columns(2)
    col1.metric("VaR 95%", f"{var*100:.2f}%")
    
    with st.spinner("Simulando Monte Carlo..."):
        mc = analyzer.monte_carlo_simulation(weights)
    
    col2.metric("Prob. Lucro", f"{mc['prob_profit']*100:.1f}%")
    
    st.metric("Valor Médio (10 anos)", f"R$ {mc['mean']:,.0f}")
    
    fig = px.histogram(x=mc['simulations'][:, -1], nbins=50, 
                       labels={'x': 'Valor Final (R$)'}, title='Distribuição Monte Carlo')
    st.plotly_chart(fig, use_container_width=True)

def page_settings():
    st.header("⚙️ Configurações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Carteira")
        portfolio = st.session_state.portfolio
        dados = [{'Ticker': a.ticker, 'Qtd': a.quantidade, 'PM': a.preco_medio} for a in portfolio.ativos]
        df_edit = st.data_editor(pd.DataFrame(dados), num_rows="dynamic", use_container_width=True)
        
        if st.button("💾 Salvar"):
            novos_ativos = [Asset(row['Ticker'], row['Ticker'], "acoes_br", float(row['Qtd']), float(row['PM'])) 
                           for _, row in df_edit.iterrows()]
            st.session_state.portfolio.ativos = novos_ativos
            st.success("Salvo!")
    
    with col2:
        st.subheader("Estratégias")
        for key, est in ESTRATEGIAS.items():
            with st.expander(est['nome']):
                st.write(f"Target: {est['target_retorno']}% aa")
                st.json(est['alocacao'])

def main():
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

# Salvar
base_path = "/mnt/kimi/output/radar_invest_pro"
with open(f"{base_path}/app.py", "w") as f:
    f.write(app_monolitico)

print("✅ app.py monolítico criado!")
print(f"📄 Tamanho: {len(app_monolitico)} caracteres")
print("\n🎉 AGORA É SÓ SUBIR ESSE ÚNICO ARQUIVO pro GitHub!")
print("   - Não precisa de pastas")
print("   - Não precisa de __init__.py")
print("   - Só app.py + requirements.txt")
