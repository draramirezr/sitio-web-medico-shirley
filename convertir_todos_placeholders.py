#!/usr/bin/env python3
"""
Reemplazar TODOS los ? por %s en queries SQL de forma GLOBAL
"""
import re

# Leer archivo
with open('app_simple.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('app_simple.py.backup_final', 'w', encoding='utf-8') as f:
    f.write(content)

print("💾 Backup creado: app_simple.py.backup_final\n")

# Contar ? antes (excluyendo comentarios y strings normales)
count_before = content.count('?')
print(f"📊 Total de '?' en el archivo: {count_before}")

# Estrategia: Reemplazar ? por %s SOLO en contextos SQL
# Buscar patrones como: execute('...?...')  o execute('''...?...''')

# Patrón 1: WHERE ... = ?
content = re.sub(r"WHERE\s+(\w+)\s*=\s*\?", r"WHERE \1 = %s", content)

# Patrón 2: AND ... = ?
content = re.sub(r"AND\s+(\w+)\s*=\s*\?", r"AND \1 = %s", content)

# Patrón 3: SET ... = ?
content = re.sub(r"SET\s+(\w+)\s*=\s*\?", r"SET \1 = %s", content)

# Patrón 4: LIKE ?
content = re.sub(r"LIKE\s+\?", r"LIKE %s", content)

# Patrón 5: IN (?)
content = re.sub(r"IN\s+\(\?\)", r"IN (%s)", content)

# Patrón 6: != ?
content = re.sub(r"!=\s*\?", r"!= %s", content)

# Patrón 7: > ?
content = re.sub(r">\s*\?", r"> %s", content)

# Patrón 8: < ?
content = re.sub(r"<\s*\?", r"< %s", content)

# Patrón 9: >= ?
content = re.sub(r">=\s*\?", r">= %s", content)

# Patrón 10: <= ?
content = re.sub(r"<=\s*\?", r"<= %s", content)

# Patrón 11: , ?  (en listas de parámetros)
content = re.sub(r",\s*\?(?=\s*[,)])", r", %s", content)

# Patrón 12: (? al inicio
content = re.sub(r"\(\?(?=\s*[,)])", r"(%s", content)

# Contar después
count_after = content.count('?')
converted = count_before - count_after

print(f"\n📈 RESULTADO:")
print(f"   ✅ '?' restantes: {count_after}")
print(f"   ✅ Convertidos: {converted}")

# Guardar
with open('app_simple.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Archivo actualizado: app_simple.py")
print(f"🔄 Reinicia el servidor Flask")






