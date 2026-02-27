
# ARQUIVO 4: config/__init__.py
content = '''"""Config module"""
from .settings import *
from .constants import *
'''

with open(f"{base_path}/config/__init__.py", "w") as f:
    f.write(content)

print("✅ config/__init__.py")
