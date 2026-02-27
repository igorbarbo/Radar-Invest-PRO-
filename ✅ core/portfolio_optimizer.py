
# ARQUIVO 12: core/portfolio_optimizer.py
content = '''"""Otimização de carteira - Markowitz, Risk Parity"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict, List, Tuple, Optional
import cvxpy as cp

from utils.helpers import calcular_retornos

class PortfolioOptimizer:
    def __init__(self, df_precos: pd.DataFrame):
        self.df_precos = df_precos
        self.retornos = calcular_retornos(df_precos)
        self.mu = self.retornos.mean() * 252  # Retorno anualizado
        self.sigma = self.retornos.cov() * 252  # Covariância anualizada
        self.tickers = list(df_precos.columns)
        self.n = len(self.tickers)
    
    def optimize_max_sharpe(self, risk_free_rate: float = 0.10) -> Dict:
        """Maximiza Sharpe Ratio"""
        def neg_sharpe(weights):
            port_return = np.dot(weights, self.mu)
            port_vol = np.sqrt(np.dot(weights.T, np.dot(self.sigma, weights)))
            return -(port_return - risk_free_rate) / port_vol
        
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Soma = 1
        ]
        bounds = tuple((0, 1) for _ in range(self.n))  # Sem venda a descoberto
        
        x0 = np.array([1/self.n] * self.n)
        
        result = minimize(neg_sharpe, x0, method='SLSQP', 
                         bounds=bounds, constraints=constraints)
        
        pesos = dict(zip(self.tickers, result.x))
        
        return {
            'pesos': pesos,
            'retorno_esperado': np.dot(result.x, self.mu),
            'volatilidade': np.sqrt(np.dot(result.x.T, np.dot(self.sigma, result.x))),
            'sharpe': -result.fun
        }
    
    def optimize_min_variance(self) -> Dict:
        """Minimiza variância"""
        def portfolio_vol(weights):
            return np.sqrt(np.dot(weights.T, np.dot(self.sigma, weights)))
        
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        ]
        bounds = tuple((0, 1) for _ in range(self.n))
        
        x0 = np.array([1/self.n] * self.n)
        
        result = minimize(portfolio_vol, x0, method='SLSQP',
                         bounds=bounds, constraints=constraints)
        
        pesos = dict(zip(self.tickers, result.x))
        
        return {
            'pesos': pesos,
            'retorno_esperado': np.dot(result.x, self.mu),
            'volatilidade': result.fun,
            'sharpe': np.dot(result.x, self.mu) / result.fun if result.fun > 0 else 0
        }
    
    def optimize_target_return(self, target: float) -> Dict:
        """Minimiza risco para retorno alvo"""
        def portfolio_vol(weights):
            return np.sqrt(np.dot(weights.T, np.dot(self.sigma, weights)))
        
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: np.dot(x, self.mu) - target}
        ]
        bounds = tuple((0, 1) for _ in range(self.n))
        
        x0 = np.array([1/self.n] * self.n)
        
        result = minimize(portfolio_vol, x0, method='SLSQP',
                         bounds=bounds, constraints=constraints)
        
        if not result.success:
            return self.optimize_max_sharpe()
        
        pesos = dict(zip(self.tickers, result.x))
        
        return {
            'pesos': pesos,
            'retorno_esperado': target,
            'volatilidade': result.fun,
            'sharpe': target / result.fun if result.fun > 0 else 0
        }
    
    def optimize_risk_parity(self) -> Dict:
        """Risk Parity - contribuição igual de risco"""
        def risk_parity_objective(weights):
            port_vol = np.sqrt(np.dot(weights.T, np.dot(self.sigma, weights)))
            marginal_risk = np.dot(self.sigma, weights) / port_vol
            risk_contrib = weights * marginal_risk
            target_risk = port_vol / self.n
            return np.sum((risk_contrib - target_risk) ** 2)
        
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        ]
        bounds = tuple((0.01, 1) for _ in range(self.n))  # Mínimo 1%
        
        x0 = np.array([1/self.n] * self.n)
        
        result = minimize(risk_parity_objective, x0, method='SLSQP',
                         bounds=bounds, constraints=constraints)
        
        pesos = dict(zip(self.tickers, result.x))
        
        return {
            'pesos': pesos,
            'retorno_esperado': np.dot(result.x, self.mu),
            'volatilidade': np.sqrt(np.dot(result.x.T, np.dot(self.sigma, result.x))),
            'sharpe': np.dot(result.x, self.mu) / np.sqrt(np.dot(result.x.T, np.dot(self.sigma, result.x)))
        }
    
    def get_efficient_frontier(self, n_points: int = 50) -> pd.DataFrame:
        """Gera pontos da fronteira eficiente"""
        min_vol = self.optimize_min_variance()
        max_sharpe = self.optimize_max_sharpe()
        
        target_returns = np.linspace(min_vol['retorno_esperado'], 
                                     max(self.mu) * 0.9, n_points)
        
        efficient_portfolios = []
        
        for target in target_returns:
            try:
                opt = self.optimize_target_return(target)
                efficient_portfolios.append({
                    'retorno': opt['retorno_esperado'],
                    'volatilidade': opt['volatilidade'],
                    'sharpe': opt['sharpe']
                })
            except:
                continue
        
        return pd.DataFrame(efficient_portfolios)
'''

with open(f"{base_path}/core/portfolio_optimizer.py", "w") as f:
    f.write(content)

print("✅ core/portfolio_optimizer.py")
