#!/usr/bin/env python3
"""
Script para convertir placeholders de SQLite (?) a MySQL (%s)
"""
import re

# Leer el archivo
with open('app_simple.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Contar cuántos ? hay actualmente
count_before = content.count('?')
print(f"📊 Placeholders '?' encontrados: {count_before}")

# Patrón para encontrar queries SQL con placeholders ?
# Buscar dentro de comillas simples o triples que contengan SQL
pattern = r"(execute(?:many)?\s*\(['\"])(.*?)(['\"])"

def replace_placeholders(match):
    prefix = match.group(1)
    query = match.group(2)
    suffix = match.group(3)
    
    # Reemplazar ? por %s solo si parece SQL
    if any(keyword in query.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'WHERE', 'VALUES']):
        query_fixed = query.replace('?', '%s')
        if '?' in query:
            print(f"✅ Convertido: ...{query[:50]}...")
        return prefix + query_fixed + suffix
    return match.group(0)

# Aplicar el reemplazo
content_fixed = re.sub(pattern, replace_placeholders, content, flags=re.DOTALL)

# Contar cuántos ? quedan
count_after = content_fixed.count('?')
converted = count_before - count_after

print(f"\n📈 RESULTADO:")
print(f"   ✅ Convertidos: {converted}")
print(f"   ⚠️ Restantes: {count_after}")

if converted > 0:
    # Guardar el archivo modificado
    with open('app_simple.py', 'w', encoding='utf-8') as f:
        f.write(content_fixed)
    print(f"\n✅ Archivo actualizado: app_simple.py")
else:
    print(f"\n⚠️ No se encontraron placeholders para convertir")







