
# ARQUIVO 9: utils/helpers.py
content = '''"""Funções utilitárias"""
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple

def calcular_retornos(df_precos: pd.DataFrame) -> pd.DataFrame:
    """Calcula retornos logarítmicos"""
    return np.log(df_precos / df_precos.shift(1)).dropna()

def calcular_metricas_retorono(retornos: pd.Series) -> Dict:
    """Calcula métricas de retorno"""
    retorno_anual = retornos.mean() * 252
    volatilidade = retornos.std() * np.sqrt(252)
    sharpe = retorno_anual / volatilidade if volatilidade != 0 else 0
    
    return {
        'retorno_anual': retorno_anual,
        'volatilidade': volatilidade,
        'sharpe': sharpe,
        'retorno_total': (1 + retornos).prod() - 1
    }

def formatar_moeda(valor: float) -> str:
    """Formata como R$"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_percentual(valor: float, decimais: int = 2) -> str:
    """Formata como %"""
    return f"{valor:.{decimais}f}%"

def calcular_drawdown(valores: pd.Series) -> pd.Series:
    """Calcula drawdown ao longo do tempo"""
    pico = valores.cummax()
    drawdown = (valores - pico) / pico
    return drawdown

def correlacao_ativos(df_retornos: pd.DataFrame) -> pd.DataFrame:
    """Matriz de correlação"""
    return df_retornos.corr()

def backtest_simples(pesos: Dict[str, float], df_retornos: pd.DataFrame) -> pd.Series:
    """Backtest simples de buy and hold"""
    pesos_series = pd.Series(pesos)
    retorno_carteira = (df_retornos * pesos_series).sum(axis=1)
    return (1 + retorno_carteira).cumprod()
'''

with open(f"{base_path}/utils/helpers.py", "w") as f:
    f.write(content)

print("✅ utils/helpers.py")
