
# ARQUIVO 13: core/risk_analyzer.py
content = '''"""Análise de risco - VaR, CVaR, Monte Carlo"""
import numpy as np
import pandas as pd
from typing import Dict, Tuple
from scipy import stats

from utils.helpers import calcular_retornos, calcular_drawdown

class RiskAnalyzer:
    def __init__(self, df_precos: pd.DataFrame):
        self.df_precos = df_precos
        self.retornos = calcular_retornos(df_precos)
        self.tickers = list(df_precos.columns)
    
    def calculate_var(self, weights: Dict[str, float], 
                     confidence: float = 0.95, 
                     method: str = 'historical') -> float:
        """Value at Risk"""
        pesos_array = np.array([weights.get(t, 0) for t in self.tickers])
        
        # Retorno da carteira
        port_returns = (self.retornos * pesos_array).sum(axis=1)
        
        if method == 'historical':
            return np.percentile(port_returns, (1 - confidence) * 100)
        elif method == 'parametric':
            mean = port_returns.mean()
            std = port_returns.std()
            return stats.norm.ppf(1 - confidence, mean, std)
        
        return 0
    
    def calculate_cvar(self, weights: Dict[str, float], 
                      confidence: float = 0.95) -> float:
        """Conditional Value at Risk (Expected Shortfall)"""
        var = self.calculate_var(weights, confidence, 'historical')
        pesos_array = np.array([weights.get(t, 0) for t in self.tickers])
        port_returns = (self.retornos * pesos_array).sum(axis=1)
        
        return port_returns[port_returns <= var].mean()
    
    def calculate_drawdown_stats(self, weights: Dict[str, float]) -> Dict:
        """Estatísticas de drawdown"""
        pesos_array = np.array([weights.get(t, 0) for t in self.tickers])
        
        # Valor da carteira ao longo do tempo
        port_returns = (self.retornos * pesos_array).sum(axis=1)
        cumulative = (1 + port_returns).cumprod()
        
        drawdown = calcular_drawdown(cumulative)
        
        return {
            'max_drawdown': drawdown.min(),
            'avg_drawdown': drawdown[drawdown < 0].mean(),
            'max_dd_duration': self._max_drawdown_duration(drawdown),
            'current_drawdown': drawdown.iloc[-1]
        }
    
    def _max_drawdown_duration(self, drawdown: pd.Series) -> int:
        """Calcula duração do maior drawdown em dias"""
        is_drawdown = drawdown < 0
        durations = []
        current_duration = 0
        
        for in_dd in is_drawdown:
            if in_dd:
                current_duration += 1
            else:
                if current_duration > 0:
                    durations.append(current_duration)
                current_duration = 0
        
        return max(durations) if durations else 0
    
    def monte_carlo_simulation(self, weights: Dict[str, float], 
                              n_simulations: int = 10000,
                              n_days: int = 252,
                              initial_value: float = 100000) -> Dict:
        """Simulação Monte Carlo"""
        pesos_array = np.array([weights.get(t, 0) for t in self.tickers])
        
        # Parâmetros
        mu = self.retornos.mean().values
        sigma = self.retornos.cov().values
        
        # Simulações
        np.random.seed(42)
        results = np.zeros((n_simulations, n_days))
        
        for i in range(n_simulations):
            daily_returns = np.random.multivariate_normal(mu, sigma, n_days)
            port_returns = daily_returns @ pesos_array
            cumulative = np.cumprod(1 + port_returns)
            results[i, :] = initial_value * cumulative
        
        # Estatísticas
        final_values = results[:, -1]
        
        return {
            'mean': np.mean(final_values),
            'median': np.median(final_values),
            'std': np.std(final_values),
            'min': np.min(final_values),
            'max': np.max(final_values),
            'percentile_5': np.percentile(final_values, 5),
            'percentile_95': np.percentile(final_values, 95),
            'prob_profit': np.mean(final_values > initial_value),
            'simulations': results
        }
    
    def calculate_beta(self, weights: Dict[str, float], 
                      benchmark_returns: pd.Series) -> float:
        """Beta da carteira vs benchmark"""
        pesos_array = np.array([weights.get(t, 0) for t in self.tickers])
        port_returns = (self.retornos * pesos_array).sum(axis=1)
        
        # Alinha datas
        common_dates = port_returns.index.intersection(benchmark_returns.index)
        port_aligned = port_returns.loc[common_dates]
        bench_aligned = benchmark_returns.loc[common_dates]
        
        covariance = np.cov(port_aligned, bench_aligned)[0, 1]
        benchmark_variance = np.var(bench_aligned)
        
        return covariance / benchmark_variance if benchmark_variance != 0 else 1
    
    def calculate_all_metrics(self, weights: Dict[str, float]) -> Dict:
        """Calcula todas as métricas de risco"""
        pesos_array = np.array([weights.get(t, 0) for t in self.tickers])
        port_returns = (self.retornos * pesos_array).sum(axis=1)
        
        return {
            'volatilidade_anual': port_returns.std() * np.sqrt(252),
            'var_95': self.calculate_var(weights, 0.95),
            'cvar_95': self.calculate_cvar(weights, 0.95),
            'skewness': port_returns.skew(),
            'kurtosis': port_returns.kurtosis(),
            'sharpe': (port_returns.mean() * 252) / (port_returns.std() * np.sqrt(252)),
            **self.calculate_drawdown_stats(weights)
        }
'''

with open(f"{base_path}/core/risk_analyzer.py", "w") as f:
    f.write(content)

print("✅ core/risk_analyzer.py")
