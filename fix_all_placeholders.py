#!/usr/bin/env python3
"""
Reemplazar placeholders ? por %s - SIMPLE Y DIRECTO
"""

# Leer archivo
with open('app_simple.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Backup
with open('app_simple.py.backup', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("💾 Backup creado: app_simple.py.backup\n")

# Procesar línea por línea
count = 0
for i, line in enumerate(lines):
    if 'execute' in line and '?' in line:
        # Reemplazar ? por %s en esta línea
        new_line = line.replace('?', '%s')
        if new_line != line:
            count += 1
            print(f"Línea {i+1}: {line.strip()[:80]}")
            lines[i] = new_line

# Guardar
with open('app_simple.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n✅ {count} líneas modificadas")
print("🔄 Reinicia el servidor Flask ahora")






