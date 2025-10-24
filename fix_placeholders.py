#!/usr/bin/env python3
"""
Reemplazar TODOS los placeholders ? por %s en app_simple.py
"""
import re

# Leer archivo
with open('app_simple.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('app_simple.py.backup', 'w', encoding='utf-8') as f:
    f.write(content)

print("💾 Backup creado: app_simple.py.backup")

# Contar ? antes
count_before = content.count("'?'")  # Evitar contar ? en comentarios o strings normales
print(f"\n📊 Buscando placeholders SQL...")

# Patrón más agresivo: reemplazar ? en contexto de SQL
# Buscar patrones como: execute('...?...', (...))
# O: execute('''...?...''', (...))

lines_changed = 0
new_lines = []

for line in content.split('\n'):
    original_line = line
    
    # Si la línea contiene execute y ? después de comillas
    if 'execute' in line and '?' in line:
        # Verificar si es un query SQL (tiene palabras clave SQL)
        if any(keyword in line.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'WHERE', 'VALUES', 'SET']):
            # Reemplazar ? por %s solo dentro de strings SQL
            # Buscar ? que esté entre comillas
            line = re.sub(r"(\'\'\')([^\']*)(\?)", lambda m: m.group(1) + m.group(2) + '%s', line)
            line = re.sub(r"(\'\'\')([^\']*)(\?)", lambda m: m.group(1) + m.group(2) + '%s', line)
            line = re.sub(r"(\'\'\')([^\']*)(\?)", lambda m: m.group(1) + m.group(2) + '%s', line)
            line = re.sub(r"(\'\'\')([^\']*)(\?)", lambda m: m.group(1) + m.group(2) + '%s', line)
            line = re.sub(r"(\')([^\']*)(\?)", lambda m: m.group(1) + m.group(2) + '%s', line)
            line = re.sub(r"(\')([^\']*)(\?)", lambda m: m.group(1) + m.group(2) + '%s', line)
            line = re.sub(r"(\')([^\']*)(\?)", lambda m: m.group(1) + m.group(2) + '%s', line)
            line = re.sub(r"(\')([^\']*)(\?)", lambda m: m.group(1) + m.group(2) + '%s', line)
            
            if line != original_line:
                lines_changed += 1
                print(f"✅ Línea {len(new_lines)+1}: ...{original_line.strip()[:60]}...")
    
    new_lines.append(line)

# Escribir archivo
content_new = '\n'.join(new_lines)

with open('app_simple.py', 'w', encoding='utf-8') as f:
    f.write(content_new)

print(f"\n📈 RESULTADO:")
print(f"   ✅ Líneas modificadas: {lines_changed}")
print(f"   ✅ Archivo actualizado: app_simple.py")
print(f"\n🔄 Reinicia el servidor Flask")






