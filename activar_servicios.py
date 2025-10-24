#!/usr/bin/env python3
"""Script para activar todos los servicios"""
import pymysql

print("🔌 Conectando a MySQL Railway...")
conn = pymysql.connect(
    host='turntable.proxy.rlwy.net',
    port=33872,
    user='root',
    password='koLhfNrFtiDBdXOIYCmMSOoOeERGUvsX',
    database='drashirley'
)
cursor = conn.cursor()

print("✅ Conexión exitosa\n")

# Actualizar todos los servicios a active = 1
cursor.execute('UPDATE services SET active = 1')
print(f"✅ {cursor.rowcount} servicios activados")

# Actualizar todos los tratamientos estéticos
cursor.execute('UPDATE aesthetic_treatments SET active = 1')
print(f"✅ {cursor.rowcount} tratamientos activados")

conn.commit()
conn.close()

print("\n🎉 TODOS LOS SERVICIOS ESTÁN ACTIVOS")
print("🔄 Recarga la página /servicios")






