
# ARQUIVO 15: core/__init__.py
content = '''"""Core module"""
from .data_fetcher import data_fetcher
from .portfolio_optimizer import PortfolioOptimizer
from .risk_analyzer import RiskAnalyzer
from .rebalance import RebalanceEngine, RebalanceSuggestion
'''

with open(f"{base_path}/core/__init__.py", "w") as f:
    f.write(content)

print("✅ core/__init__.py")
