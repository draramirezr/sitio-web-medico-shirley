#!/usr/bin/env python3
"""
Script de diagnóstico para verificar variables de entorno en Railway
"""

import os

print("=" * 70)
print("🔍 DIAGNÓSTICO DE VARIABLES DE ENTORNO EN RAILWAY")
print("=" * 70)

# Variables críticas
vars_to_check = [
    'RAILWAY_ENVIRONMENT',
    'MYSQL_HOST',
    'MYSQL_USER',
    'MYSQL_PASSWORD',
    'MYSQL_DATABASE',
    'DATABASE_URL',
    'MYSQLHOST',
    'MYSQLUSER',
    'MYSQLPASSWORD',
    'MYSQLDATABASE',
    'MYSQLPORT',
]

print("\n📌 VARIABLES ENCONTRADAS:\n")

found_vars = {}
for var in vars_to_check:
    value = os.getenv(var)
    if value:
        # Ocultar contraseñas
        if 'PASSWORD' in var or 'SECRET' in var:
            display_value = value[:4] + "****" + value[-4:] if len(value) > 8 else "****"
        else:
            display_value = value
        print(f"✅ {var} = {display_value}")
        found_vars[var] = value
    else:
        print(f"❌ {var} = (NO DEFINIDA)")

print("\n" + "=" * 70)
print("📊 RESUMEN:")
print("=" * 70)

# Verificar qué patrón está usando Railway
if found_vars.get('MYSQL_HOST'):
    print("✅ Railway está usando el patrón: MYSQL_HOST, MYSQL_USER, etc.")
    print(f"   Host: {found_vars.get('MYSQL_HOST')}")
elif found_vars.get('MYSQLHOST'):
    print("⚠️ Railway está usando el patrón: MYSQLHOST, MYSQLUSER, etc.")
    print(f"   Host: {found_vars.get('MYSQLHOST')}")
    print("   ⚠️ EL CÓDIGO NECESITA SER ACTUALIZADO PARA ESTE PATRÓN")
elif found_vars.get('DATABASE_URL'):
    print("✅ Railway está usando: DATABASE_URL")
    print(f"   URL: {found_vars.get('DATABASE_URL')[:30]}...")
else:
    print("❌ NO SE ENCONTRARON VARIABLES DE MYSQL")

if found_vars.get('RAILWAY_ENVIRONMENT'):
    print(f"✅ RAILWAY_ENVIRONMENT = {found_vars.get('RAILWAY_ENVIRONMENT')}")
else:
    print("❌ RAILWAY_ENVIRONMENT no está definida")
    print("   ⚠️ MySQL NO SE ACTIVARÁ sin esta variable")

print("\n" + "=" * 70)
print("💡 RECOMENDACIONES:")
print("=" * 70)

if not found_vars.get('RAILWAY_ENVIRONMENT'):
    print("1. Agregar: RAILWAY_ENVIRONMENT=1")

if not found_vars.get('MYSQL_HOST') and not found_vars.get('MYSQLHOST'):
    print("2. Verificar que el servicio MySQL esté conectado")
    print("3. Las variables MYSQL_* deberían ser creadas automáticamente")

print("=" * 70)

