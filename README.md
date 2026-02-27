
readme_content = '''# 🚀 Radar Invest PRO v2.0

Sistema completo de gestão de carteiras híbridas com otimização quantitativa, análise de risco e simulação Monte Carlo.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/seu-usuario/radar-invest-pro/main/app.py)

## ✨ Funcionalidades

### 📊 Dashboard
- Visualização da carteira atual
- Alocação por ativo e por classe
- Acompanhamento de retorno e lucro/prejuízo

### 🎯 Otimização
- **Markowitz**: Fronteira eficiente, máximo Sharpe, mínima variância
- **Risk Parity**: Alocação por contribuição de risco
- **Target Return**: Otimização para retorno alvo (ex: 10% aa)

### ⚠️ Análise de Risco
- VaR (Value at Risk) 95%
- CVaR (Expected Shortfall)
- Monte Carlo com 10.000 simulações
- Drawdown máximo e duração
- Beta vs IBOV

### ⚙️ Configurações
- Editor de carteira
- Estratégias pré-configuradas (Conservador, Moderado, Agressivo)
- Atualização de preços em tempo real

## 🚀 Como usar

### Local
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/radar-invest-pro.git
cd radar-invest-pro

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run app.py
```

### Streamlit Cloud
1. Fork este repositório
2. Vá em [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu GitHub e selecione o repo
4. Clique em "Deploy"

## 📁 Estrutura do Projeto

```
radar-invest-pro/
├── app.py                 # Entry point
├── requirements.txt       # Dependências
├── config/               # Configurações
│   ├── settings.py
│   └── constants.py
├── core/                 # Lógica principal
│   ├── data_fetcher.py   # Busca de dados
│   ├── portfolio_optimizer.py
│   ├── risk_analyzer.py
│   └── rebalance.py
├── models/               # Classes de dados
│   ├── asset.py
│   └── portfolio.py
├── utils/                # Utilitários
│   ├── cache_manager.py
│   └── helpers.py
└── views/                # Interface Streamlit
    ├── dashboard.py
    ├── optimization_view.py
    └── risk_view.py
```

## 🎯 Estratégias Pré-configuradas

| Estratégia | Alocação | Target |
|------------|----------|--------|
| **Conservador IPCA+** | 50% RF IPCA, 25% Ações, 15% FIIs, 10% Commodities | 10% aa |
| **Moderado Balanceado** | 30% RF, 30% Ações BR, 20% Ações US, 15% FIIs, 5% Cripto | 12% aa |
| **Agressivo Growth** | 10% RF, 40% Ações BR, 25% Ações US, 10% FIIs, 10% Cripto | 15% aa |

## 📊 Dados Utilizados

- **Fonte**: Yahoo Finance (yfinance)
- **Ativos**: Ações B3, FIIs, ETFs, Commodities
- **Frequência**: Diária
- **Histórico**: Até 10 anos

## 🛠️ Tecnologias

- [Streamlit](https://streamlit.io/) - Interface web
- [yfinance](https://pypi.org/project/yfinance/) - Dados de mercado
- [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/) - Otimização
- [Plotly](https://plotly.com/) - Visualizações
- [Pandas](https://pandas.pydata.org/) - Manipulação de dados
- [NumPy](https://numpy.org/) - Cálculos numéricos
- [SciPy](https://scipy.org/) - Otimização matemática

## ⚠️ Disclaimer

Este sistema é **apenas para fins educacionais**. Não constitui recomendação de investimento. Sempre consulte um profissional credenciado antes de tomar decisões financeiras.

## 📝 Licença

MIT License - Livre para uso e modificação.

---

**Desenvolvido com ❤️ para investidores brasileiros**
'''

base_path = "/mnt/kimi/output/radar_invest_pro"
with open(f"{base_path}/README.md", "w") as f:
    f.write(readme_content)

print("✅ README.md criado!")
print(f"📄 {len(readme_content)} caracteres")# Radar-Invest-PRO-
