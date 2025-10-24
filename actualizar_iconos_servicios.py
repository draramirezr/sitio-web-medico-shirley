#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar iconos de servicios
Funciona tanto con SQLite (local) como con MySQL (Railway)
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Detectar tipo de base de datos
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

if MYSQL_AVAILABLE and os.getenv('RAILWAY_ENVIRONMENT'):
    import pymysql
    DATABASE_TYPE = 'mysql'
    DATABASE_CONFIG = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', 'drashirley'),
        'charset': 'utf8mb4'
    }
    print("🔧 Usando MySQL (Railway)")
else:
    import sqlite3
    DATABASE_TYPE = 'sqlite'
    DATABASE_CONFIG = 'drashirley_simple.db'
    print("🔧 Usando SQLite (Local)")

def get_connection():
    """Obtener conexión según el tipo de base de datos"""
    if DATABASE_TYPE == 'mysql':
        return pymysql.connect(**DATABASE_CONFIG)
    else:
        conn = sqlite3.connect(DATABASE_CONFIG)
        conn.row_factory = sqlite3.Row
        return conn

def update_service_icons():
    """Actualizar iconos de servicios"""
    
    # Mapeo de nombres de servicios a íconos
    service_icons = {
        'Consulta Ginecológica': 'fas fa-female',
        'Consulta Obstétrica': 'fas fa-baby',
        'Ecografías': 'fas fa-heartbeat',
        'Cirugía Ginecológica': 'fas fa-cut',
        'Planificación Familiar': 'fas fa-calendar-check',
        'Tratamientos Estéticos Ginecológicos': 'fas fa-wand-magic-sparkles'
    }
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("\n" + "="*60)
        print("🔍 ACTUALIZANDO ICONOS DE SERVICIOS")
        print("="*60)
        
        # Obtener servicios actuales
        if DATABASE_TYPE == 'mysql':
            cursor.execute("SELECT id, name, icon FROM services WHERE active = 1")
            services = cursor.fetchall()
        else:
            services = cursor.execute("SELECT id, name, icon FROM services WHERE active = 1").fetchall()
        
        updated_count = 0
        
        for service in services:
            if DATABASE_TYPE == 'mysql':
                service_id = service[0]
                service_name = service[1]
                current_icon = service[2]
            else:
                service_id = service['id']
                service_name = service['name']
                current_icon = service['icon']
            
            print(f"\n📋 Servicio: {service_name}")
            print(f"   ID: {service_id}")
            print(f"   Icono actual: {current_icon if current_icon else 'NINGUNO'}")
            
            # Buscar icono nuevo
            new_icon = service_icons.get(service_name)
            
            if new_icon:
                if current_icon != new_icon:
                    # Actualizar icono
                    if DATABASE_TYPE == 'mysql':
                        cursor.execute("UPDATE services SET icon = %s WHERE id = %s", (new_icon, service_id))
                    else:
                        cursor.execute("UPDATE services SET icon = ? WHERE id = ?", (new_icon, service_id))
                    
                    print(f"   ✅ Actualizado a: {new_icon}")
                    updated_count += 1
                else:
                    print(f"   ✅ Ya está correcto")
            else:
                print(f"   ⚠️ No hay icono definido para este servicio")
        
        # Confirmar cambios
        conn.commit()
        
        print("\n" + "="*60)
        print(f"✅ Actualización completada: {updated_count} servicios actualizados")
        print("="*60)
        
        # Mostrar resumen
        print("\n📊 RESUMEN DE ICONOS:")
        print("-"*60)
        
        if DATABASE_TYPE == 'mysql':
            cursor.execute("SELECT name, icon FROM services WHERE active = 1 ORDER BY id")
            services = cursor.fetchall()
            for service in services:
                print(f"  • {service[0]}: {service[1]}")
        else:
            services = cursor.execute("SELECT name, icon FROM services WHERE active = 1 ORDER BY id").fetchall()
            for service in services:
                print(f"  • {service['name']}: {service['icon']}")
        
        conn.close()
        print("\n✅ Script completado exitosamente")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_service_icons()




