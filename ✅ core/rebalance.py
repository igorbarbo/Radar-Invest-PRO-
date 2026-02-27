
# ARQUIVO 14: core/rebalance.py
content = '''"""Estratégias de rebalanceamento"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class RebalanceSuggestion:
    ticker: str
    acao: str  # 'COMPRAR', 'VENDER', 'MANter'
    quantidade: float
    valor: float
    motivo: str

class RebalanceEngine:
    def __init__(self, portfolio_value: float, current_weights: Dict[str, float],
                 target_weights: Dict[str, float], prices: Dict[str, float]):
        self.portfolio_value = portfolio_value
        self.current_weights = current_weights
        self.target_weights = target_weights
        self.prices = prices
    
    def calculate_drift(self) -> Dict[str, float]:
        """Calcula desvio da alocação target"""
        drift = {}
        all_tickers = set(self.current_weights.keys()) | set(self.target_weights.keys())
        
        for ticker in all_tickers:
            current = self.current_weights.get(ticker, 0)
            target = self.target_weights.get(ticker, 0)
            drift[ticker] = current - target
        
        return drift
    
    def suggest_rebalance(self, threshold: float = 0.05) -> List[RebalanceSuggestion]:
        """Sugere operações de rebalanceamento"""
        suggestions = []
        drift = self.calculate_drift()
        
        for ticker, diff in drift.items():
            if abs(diff) < threshold:
                continue
            
            price = self.prices.get(ticker, 0)
            if price == 0:
                continue
            
            target_value = self.target_weights.get(ticker, 0) * self.portfolio_value
            current_value = self.current_weights.get(ticker, 0) * self.portfolio_value
            diff_value = target_value - current_value
            
            if diff > 0:  # Precisa vender
                acao = 'VENDER'
                quantidade = abs(diff_value) / price
            else:  # Precisa comprar
                acao = 'COMPRAR'
                quantidade = abs(diff_value) / price
            
            suggestions.append(RebalanceSuggestion(
                ticker=ticker,
                acao=acao,
                quantidade=quantidade,
                valor=abs(diff_value),
                motivo=f'Desvio de {abs(diff)*100:.1f}% do target'
            ))
        
        return sorted(suggestions, key=lambda x: x.valor, reverse=True)
    
    def suggest_aporte(self, aporte_valor: float) -> List[RebalanceSuggestion]:
        """Sugere onde aplicar novo aporte"""
        suggestions = []
        
        # Calcula quanto falta para atingir target
        for ticker, target_weight in self.target_weights.items():
            price = self.prices.get(ticker, 0)
            if price == 0:
                continue
            
            target_value = target_weight * (self.portfolio_value + aporte_valor)
            current_value = self.current_weights.get(ticker, 0) * self.portfolio_value
            diff_value = target_value - current_value
            
            if diff_value > 0:  # Precisa comprar mais
                quantidade = diff_value / price
                suggestions.append(RebalanceSuggestion(
                    ticker=ticker,
                    acao='COMPRAR',
                    quantidade=min(quantidade, aporte_valor / price),
                    valor=min(diff_value, aporte_valor),
                    motivo='Abaixo da alocação target'
                ))
        
        # Ordena por maior desvio
        return sorted(suggestions, key=lambda x: x.valor, reverse=True)[:5]
    
    def calculate_turnover(self, new_weights: Dict[str, float]) -> float:
        """Calcula turnover da operação"""
        turnover = 0
        all_tickers = set(self.current_weights.keys()) | set(new_weights.keys())
        
        for ticker in all_tickers:
            current = self.current_weights.get(ticker, 0)
            new = new_weights.get(ticker, 0)
            turnover += abs(new - current)
        
        return turnover / 2  # Divide por 2 pois cada trade conta 2x
'''

with open(f"{base_path}/core/rebalance.py", "w") as f:
    f.write(content)

print("✅ core/rebalance.py")
