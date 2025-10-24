#!/usr/bin/env python3
"""Test simple para reproducir el error"""
import pymysql

class MySQLConnectionWrapper:
    """Wrapper para hacer que PyMySQL se comporte como SQLite con conn.execute()"""
    def __init__(self, connection):
        self._conn = connection
        self._cursor = None
    
    def execute(self, query, params=None):
        """Ejecutar query y devolver cursor"""
        self._cursor = self._conn.cursor()
        if params:
            self._cursor.execute(query, params)
        else:
            self._cursor.execute(query)
        return self._cursor
    
    def close(self):
        if self._cursor:
            self._cursor.close()
        return self._conn.close()

# Conectar
print("🔌 Conectando...")
conn = pymysql.connect(
    host='turntable.proxy.rlwy.net',
    port=33872,
    user='root',
    password='koLhfNrFtiDBdXOIYCmMSOoOeERGUvsX',
    database='drashirley',
    cursorclass=pymysql.cursors.DictCursor
)

wrapper = MySQLConnectionWrapper(conn)

# Probar query simple
print("✅ Probando query simple sin parámetros...")
result = wrapper.execute('SELECT * FROM services WHERE active = 1 LIMIT 1')
services = result.fetchall()
print(f"   Resultado: {services}")

# Probar query con parámetros
print("\n✅ Probando query con parámetros...")
try:
    result = wrapper.execute('SELECT * FROM services WHERE id = %s', (1,))
    service = result.fetchone()
    print(f"   Resultado: {service}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

wrapper.close()
print("\n✅ Test completado")






