
# ARQUIVO 8: utils/cache_manager.py
content = '''"""Gerenciamento de cache"""
import json
import pickle
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
import os

from config import CACHE_DIR

class CacheManager:
    def __init__(self, cache_dir: str = CACHE_DIR):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_key(self, prefix: str, params: dict) -> str:
        """Gera chave única para cache"""
        param_str = json.dumps(params, sort_keys=True)
        hash_key = hashlib.md5(param_str.encode()).hexdigest()
        return f"{prefix}_{hash_key}"
    
    def _get_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.pkl"
    
    def get(self, key: str, ttl: int = 3600) -> Optional[Any]:
        """Busca do cache se válido"""
        path = self._get_path(key)
        
        if not path.exists():
            return None
        
        # Verifica TTL
        modified_time = datetime.fromtimestamp(path.stat().st_mtime)
        if datetime.now() - modified_time > timedelta(seconds=ttl):
            return None
        
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except:
            return None
    
    def set(self, key: str, value: Any):
        """Salva no cache"""
        path = self._get_path(key)
        try:
            with open(path, 'wb') as f:
                pickle.dump(value, f)
        except Exception as e:
            print(f"Erro ao salvar cache: {e}")
    
    def clear(self):
        """Limpa todo cache"""
        for file in self.cache_dir.glob("*.pkl"):
            file.unlink()
    
    def clear_expired(self, ttl: int = 3600):
        """Remove entradas expiradas"""
        now = datetime.now()
        for file in self.cache_dir.glob("*.pkl"):
            modified_time = datetime.fromtimestamp(file.stat().st_mtime)
            if now - modified_time > timedelta(seconds=ttl):
                file.unlink()

# Instância global
cache = CacheManager()
'''

with open(f"{base_path}/utils/cache_manager.py", "w") as f:
    f.write(content)

print("✅ utils/cache_manager.py")
