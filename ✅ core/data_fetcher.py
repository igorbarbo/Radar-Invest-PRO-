
# ARQUIVO 11: core/data_fetcher.py
content = '''"""Busca dados de múltiplas fontes com fallback"""
import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Optional, Dict
import time
import requests

from utils import cache
from config import CACHE_TTL_PRICES, CACHE_TTL_HISTORICAL

class DataFetcher:
    def __init__(self):
        self.session = requests.Session()
        
    def get_historical_prices(self, tickers: List[str], period: str = "5y") -> pd.DataFrame:
        """Busca preços históricos com cache"""
        cache_key = f"hist_{'_'.join(sorted(tickers))}_{period}"
        cached = cache.get(cache_key, CACHE_TTL_HISTORICAL)
        
        if cached is not None:
            return cached
        
        try:
            # Adiciona .SA se não tiver
            tickers_yf = [t if '.SA' in t else f"{t}.SA" for t in tickers]
            
            df = yf.download(tickers_yf, period=period, progress=False)
            
            # Ajusta colunas se for um único ticker
            if len(tickers_yf) == 1:
                df.columns = pd.MultiIndex.from_product([df.columns, tickers_yf])
            
            # Pega apenas Close
            df_close = df['Close'] if 'Close' in df.columns else df
            
            # Remove .SA dos nomes das colunas
            df_close.columns = [c.replace('.SA', '') for c in df_close.columns]
            
            cache.set(cache_key, df_close)
            return df_close
            
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            return pd.DataFrame()
    
    def get_current_prices(self, tickers: List[str]) -> Dict[str, float]:
        """Busca preços atuais"""
        cache_key = f"current_{'_'.join(sorted(tickers))}"
        cached = cache.get(cache_key, CACHE_TTL_PRICES)
        
        if cached is not None:
            return cached
        
        prices = {}
        
        for ticker in tickers:
            try:
                ticker_yf = ticker if '.SA' in ticker else f"{ticker}.SA"
                stock = yf.Ticker(ticker_yf)
                info = stock.info
                price = info.get('regularMarketPrice', info.get('previousClose', 0))
                prices[ticker.replace('.SA', '')] = price
                time.sleep(0.1)  # Rate limiting
            except:
                prices[ticker.replace('.SA', '')] = 0
        
        cache.set(cache_key, prices)
        return prices
    
    def get_fundamental_data(self, ticker: str) -> Dict:
        """Busca dados fundamentalistas"""
        try:
            ticker_yf = ticker if '.SA' in ticker else f"{ticker}.SA"
            stock = yf.Ticker(ticker_yf)
            info = stock.info
            
            return {
                'nome': info.get('longName', ticker),
                'setor': info.get('sector', 'N/A'),
                'pl': info.get('trailingPE'),
                'pvp': info.get('priceToBook'),
                'dy': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                'margem_liquida': info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0,
                'divida_patrimonio': info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else 0,
                'market_cap': info.get('marketCap', 0)
            }
        except:
            return {'nome': ticker, 'setor': 'N/A'}
    
    def get_benchmark(self, benchmark: str = "^BVSP", period: str = "5y") -> pd.Series:
        """Busca dados de benchmark"""
        try:
            df = yf.download(benchmark, period=period, progress=False)
            return df['Close'] if 'Close' in df.columns else df.iloc[:, 0]
        except:
            return pd.Series()

# Instância global
data_fetcher = DataFetcher()
'''

with open(f"{base_path}/core/data_fetcher.py", "w") as f:
    f.write(content)

print("✅ core/data_fetcher.py")
