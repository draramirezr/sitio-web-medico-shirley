#!/usr/bin/env python3
"""Verificar estructura de la tabla services"""
import pymysql

conn = pymysql.connect(
    host='turntable.proxy.rlwy.net',
    port=33872,
    user='root',
    password='koLhfNrFtiDBdXOIYCmMSOoOeERGUvsX',
    database='drashirley'
)
cursor = conn.cursor()

cursor.execute('DESCRIBE services')
columns = cursor.fetchall()

print("📋 ESTRUCTURA DE LA TABLA 'services':\n")
for col in columns:
    print(f"  - {col}")

print("\n" + "="*50)
print("📋 DATOS EN LA TABLA:\n")

cursor.execute('SELECT * FROM services LIMIT 3')
services = cursor.fetchall()
for s in services:
    print(f"  {s}")

conn.close()






