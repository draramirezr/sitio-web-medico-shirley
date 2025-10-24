#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar el ícono de Consulta Obstétrica
De: fas fa-baby → A: fas fa-person-pregnant
"""

import os
import pymysql
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('railway.env')
load_dotenv('local.env')

def actualizar_icono():
    """Actualiza el ícono de Consulta Obstétrica en la base de datos"""
    
    # Intentar conectar a MySQL (Railway)
    try:
        connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Conectado a MySQL (Railway)")
        
        with connection.cursor() as cursor:
            # Actualizar el ícono
            sql = """
                UPDATE services 
                SET icon = %s 
                WHERE name = %s
            """
            cursor.execute(sql, ('fas fa-person-pregnant', 'Consulta Obstétrica'))
            connection.commit()
            
            print(f"✅ Ícono actualizado: {cursor.rowcount} fila(s) afectada(s)")
            
            # Verificar el cambio
            cursor.execute("SELECT name, icon FROM services WHERE name = 'Consulta Obstétrica'")
            result = cursor.fetchone()
            
            if result:
                print(f"\n📊 Verificación:")
                print(f"   Servicio: {result['name']}")
                print(f"   Nuevo ícono: {result['icon']}")
                print(f"\n🎉 ¡Actualización completada exitosamente!")
            
        connection.close()
        
    except Exception as e:
        print(f"❌ Error al actualizar: {e}")
        print("\nℹ️ Asegúrate de tener las variables de entorno configuradas en railway.env o local.env")
        return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("ACTUALIZAR ÍCONO: CONSULTA OBSTÉTRICA")
    print("=" * 60)
    print("\n🔄 Cambiando ícono:")
    print("   De: fas fa-baby (bebé)")
    print("   A:  fas fa-person-pregnant (mujer embarazada)")
    print("\n" + "=" * 60 + "\n")
    
    actualizar_icono()

