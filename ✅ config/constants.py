
# ARQUIVO 3: config/constants.py
content = '''"""Constantes e tickers padrão"""

# Tickers brasileiros populares
ACOES_BR = [
    "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA",
    "WEGE3.SA", "RENT3.SA", "ABEV3.SA", "PRIO3.SA", "LREN3.SA",
    "MGLU3.SA", "VBBR3.SA", "SUZB3.SA", "JBSS3.SA", "RADL3.SA",
    "RAIL3.SA", "GGBR4.SA", "CSNA3.SA", "USIM5.SA", "GOAU4.SA"
]

# FIIs populares
FIIS = [
    "HGLG11.SA", "XPML11.SA", "KNRI11.SA", "MXRF11.SA", "BTLG11.SA",
    "HGRE11.SA", "XPLG11.SA", "HGRU11.SA", "VISC11.SA", "HSML11.SA"
]

# ETFs brasileiros
ETFS_BR = [
    "BOVA11.SA", "SMAL11.SA", "MATB11.SA", "IVVB11.SA", "NASD11.SA",
    "EURP11.SA", "ASIA11.SA", "GOLD11.SA", "BITI11.SA"
]

# Ações US (via ETFs ou ADRs)
ACOES_US_ETFS = [
    "IVVB11.SA",  # S&P 500
    "NASD11.SA",  # Nasdaq
    "EURP11.SA",  # Europa
    "ASIA11.SA"   # Ásia
]

# Commodities
COMMODITIES = [
    "GOLD11.SA",  # Ouro
]

# Cripto ( ETFs)
CRIPTOS = [
    "BITI11.SA",  # Bitcoin ETF
]

# Tesouro (simulados via ETFs de RF)
TESOURO_ETFS = [
    "IMAB11.SA",  # Índice de preços
    "B5P211.SA",  # Pré 2 anos
    "B5P511.SA",  # Pré 5 anos
]

# Benchmarks
BENCHMARKS = {
    "ibov": "^BVSP",
    "sp500": "^GSPC",
    "nasdaq": "^IXIC",
    "cdi": "CDI"
}

# Setores
SETORES = {
    "PETR4.SA": "Petróleo",
    "VALE3.SA": "Mineração",
    "ITUB4.SA": "Financeiro",
    "BBDC4.SA": "Financeiro",
    "BBAS3.SA": "Financeiro",
    "WEGE3.SA": "Indústria",
    "RENT3.SA": "Consumo",
    "ABEV3.SA": "Bebidas",
    "PRIO3.SA": "Petróleo",
    "LREN3.SA": "Varejo"
}
'''

with open(f"{base_path}/config/constants.py", "w") as f:
    f.write(content)

print("✅ config/constants.py")
