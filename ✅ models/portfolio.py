
# ARQUIVO 6: models/portfolio.py
content = '''"""Modelo de Carteira"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import numpy as np

from .asset import Asset

@dataclass
class Portfolio:
    nome: str
    ativos: List[Asset] = field(default_factory=list)
    data_criacao: datetime = field(default_factory=datetime.now)
    
    # Alocação target
    alocacao_target: Dict[str, float] = field(default_factory=dict)
    
    @property
    def valor_total(self) -> float:
        return sum(a.valor_atual for a in self.ativos)
    
    @property
    def valor_investido(self) -> float:
        return sum(a.valor_investido for a in self.ativos)
    
    @property
    def retorno_total(self) -> float:
        if self.valor_investido == 0:
            return 0.0
        return (self.valor_total - self.valor_investido) / self.valor_investido
    
    def get_pesos_atuais(self) -> Dict[str, float]:
        """Retorna pesos atuais de cada ativo"""
        total = self.valor_total
        if total == 0:
            return {}
        return {a.ticker: a.valor_atual / total for a in self.ativos}
    
    def get_alocacao_por_classe(self) -> Dict[str, float]:
        """Agrupa por classe de ativo"""
        resultado = {}
        for ativo in self.ativos:
            classe = ativo.classe
            if classe not in resultado:
                resultado[classe] = 0
            resultado[classe] += ativo.valor_atual
        
        total = self.valor_total
        if total > 0:
            resultado = {k: v/total for k, v in resultado.items()}
        return resultado
    
    def get_tickers(self) -> List[str]:
        return [a.ticker for a in self.ativos]
    
    def get_quantidades(self) -> Dict[str, float]:
        return {a.ticker: a.quantidade for a in self.ativos}
    
    def to_dataframe(self) -> pd.DataFrame:
        """Converte para DataFrame"""
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
'''

with open(f"{base_path}/models/portfolio.py", "w") as f:
    f.write(content)

print("✅ models/portfolio.py")
