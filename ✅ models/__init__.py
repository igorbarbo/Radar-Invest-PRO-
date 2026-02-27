
# ARQUIVO 7: models/__init__.py
content = '''"""Models module"""
from .asset import Asset
from .portfolio import Portfolio
'''

with open(f"{base_path}/models/__init__.py", "w") as f:
    f.write(content)

print("✅ models/__init__.py")
