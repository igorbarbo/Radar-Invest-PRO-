
# ARQUIVO 2: config/settings.py
content = '''"""Configurações globais do Radar Invest PRO"""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CACHE_DIR = os.path.join(DATA_DIR, "cache")
EXPORTS_DIR = os.path.join(DATA_DIR, "exports")

# Cache
CACHE_TTL_PRICES = 3600  # 1 hora
CACHE_TTL_HISTORICAL = 86400  # 24 horas

# Limites
MAX_ATIVOS = 50
MIN_ATIVOS = 2

# Períodos de análise
PERIODOS = {
    "1a": "1y",
    "2a": "2y", 
    "5a": "5y",
    "10a": "10y"
}

# Classes de ativos
CLASSES_ATIVOS = {
    "acoes_br": "Ações Brasileiras",
    "acoes_us": "Ações Americanas",
    "fiis": "Fundos Imobiliários",
    "tesouro": "Tesouro Direto",
    "etf": "ETFs",
    "commodities": "Commodities",
    "cripto": "Criptomoedas"
}

# Estratégias pré-configuradas
ESTRATEGIAS = {
    "conservador": {
        "nome": "Conservador IPCA+",
        "descricao": "Foco em renda fixa IPCA+",
        "alocacao": {
            "tesouro_ipca": 50,
            "acoes_br": 25,
            "fiis": 15,
            "commodities": 10
        },
        "target_retorno": 10.0
    },
    "moderado": {
        "nome": "Moderado Balanceado",
        "descricao": "Balanceado RF/RV",
        "alocacao": {
            "tesouro_ipca": 30,
            "acoes_br": 30,
            "acoes_us": 15,
            "fiis": 15,
            "cripto": 5,
            "commodities": 5
        },
        "target_retorno": 12.0
    },
    "agressivo": {
        "nome": "Agressivo Growth",
        "descricao": "Foco em ações",
        "alocacao": {
            "tesouro_ipca": 10,
            "acoes_br": 40,
            "acoes_us": 25,
            "fiis": 10,
            "cripto": 10,
            "commodities": 5
        },
        "target_retorno": 15.0
    }
}
'''

with open(f"{base_path}/config/settings.py", "w") as f:
    f.write(content)

print("✅ config/settings.py")
