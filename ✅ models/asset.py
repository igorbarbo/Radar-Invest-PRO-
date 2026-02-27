
# ARQUIVO 5: models/asset.py
content = '''"""Modelo de Ativo"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Asset:
    ticker: str
    nome: str
    classe: str  # acoes_br, fiis, tesouro, etc
    setor: Optional[str] = None
    preco_atual: float = 0.0
    preco_medio: float = 0.0
    quantidade: float = 0.0
    
    # Fundamentalistas
    pl: Optional[float] = None
    pvp: Optional[float] = None
    dy: Optional[float] = None
    roe: Optional[float] = None
    
    # Histórico
    preco_1a: Optional[float] = None
    preco_5a: Optional[float] = None
    
    @property
    def valor_atual(self) -> float:
        return self.preco_atual * self.quantidade
    
    @property
    def valor_investido(self) -> float:
        return self.preco_medio * self.quantidade
    
    @property
    def retorno(self) -> float:
        if self.preco_medio == 0:
            return 0.0
        return (self.preco_atual - self.preco_medio) / self.preco_medio
    
    @property
    def retorno_absoluto(self) -> float:
        return self.valor_atual - self.valor_investido
'''

with open(f"{base_path}/models/asset.py", "w") as f:
    f.write(content)

print("✅ models/asset.py")
