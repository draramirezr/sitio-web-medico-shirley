#!/usr/bin/env python3
"""
Convertir todas las llamadas conn.execute() a usar cursor
"""
import re

# Leer archivo
with open('app_simple.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('app_simple.py.backup2', 'w', encoding='utf-8') as f:
    f.write(content)

print("💾 Backup creado: app_simple.py.backup2\n")

# Patrón 1: conn.execute('query').fetchall()
pattern1 = r"(\w+)\s*=\s*conn\.execute\((.*?)\)\.fetchall\(\)"
replacement1 = r"cursor = conn.cursor()\n    cursor.execute(\2)\n    \1 = cursor.fetchall()\n    cursor.close()"

# Patrón 2: conn.execute('query').fetchone()
pattern2 = r"(\w+)\s*=\s*conn\.execute\((.*?)\)\.fetchone\(\)"
replacement2 = r"cursor = conn.cursor()\n    cursor.execute(\2)\n    \1 = cursor.fetchone()\n    cursor.close()"

# Patrón 3: conn.execute('query') (sin fetch)
pattern3 = r"conn\.execute\((.*?)\)"
replacement3 = r"cursor = conn.cursor()\n    cursor.execute(\1)\n    cursor.close()"

count = 0
lines = content.split('\n')
new_lines = []

i = 0
while i < len(lines):
    line = lines[i]
    
    # Si la línea tiene conn.execute
    if 'conn.execute' in line and 'cursor' not in line:
        print(f"Línea {i+1}: {line.strip()[:80]}")
        count += 1
    
    new_lines.append(line)
    i += 1

print(f"\n❌ Encontradas {count} líneas con conn.execute()")
print(f"\n⚠️ Este script solo cuenta. La conversión es muy compleja.")
print(f"\n💡 Mejor solución: RESTAURAR el wrapper pero ARREGLARLO correctamente")






