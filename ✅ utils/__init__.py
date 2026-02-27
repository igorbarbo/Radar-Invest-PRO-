
# ARQUIVO 10: utils/__init__.py
content = '''"""Utils module"""
from .cache_manager import cache
from .helpers import *
'''

with open(f"{base_path}/utils/__init__.py", "w") as f:
    f.write(content)

print("✅ utils/__init__.py")
