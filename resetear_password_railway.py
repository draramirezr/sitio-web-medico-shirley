"""
Script para resetear la contraseña del admin en Railway MySQL
Email: ing.fpaula@gmail.com
Contraseña: 2416Xpos@
"""

import pymysql
from werkzeug.security import generate_password_hash

# Credenciales de Railway MySQL
MYSQL_HOST = "ballast.proxy.rlwy.net"
MYSQL_PORT = 10669
MYSQL_USER = "root"
MYSQL_PASSWORD = "fmeSFyRCOODoDuPINTxYyzWatYzxxGCt"
MYSQL_DATABASE = "drashirley"

# Nueva contraseña
ADMIN_EMAIL = "ing.fpaula@gmail.com"
NEW_PASSWORD = "2416Xpos@"

print("=" * 60)
print("RESETEANDO CONTRASEÑA DEL ADMIN EN RAILWAY")
print("=" * 60)

try:
    # Conectar a MySQL
    print("\n🔌 Conectando a Railway MySQL...")
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ Conectado exitosamente")
    
    cursor = conn.cursor()
    
    # Generar nuevo hash
    print(f"\n🔐 Generando hash para contraseña: {NEW_PASSWORD}")
    new_hash = generate_password_hash(NEW_PASSWORD)
    print(f"✅ Hash generado: {new_hash[:50]}...")
    
    # Verificar si el usuario existe
    print(f"\n🔍 Verificando usuario: {ADMIN_EMAIL}")
    cursor.execute("SELECT id, nombre, email, perfil FROM usuarios WHERE email = %s", (ADMIN_EMAIL,))
    user = cursor.fetchone()
    
    if user:
        print(f"✅ Usuario encontrado:")
        print(f"   ID: {user['id']}")
        print(f"   Nombre: {user['nombre']}")
        print(f"   Email: {user['email']}")
        print(f"   Perfil: {user['perfil']}")
        
        # Actualizar contraseña
        print(f"\n🔄 Actualizando contraseña...")
        cursor.execute("""
            UPDATE usuarios 
            SET password_hash = %s, 
                password_temporal = 0,
                activo = 1
            WHERE email = %s
        """, (new_hash, ADMIN_EMAIL))
        
        conn.commit()
        print("✅ Contraseña actualizada exitosamente")
        
    else:
        print(f"❌ Usuario no encontrado: {ADMIN_EMAIL}")
        print("\n📝 Creando usuario...")
        
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, password_hash, perfil, activo, password_temporal)
            VALUES (%s, %s, %s, %s, 1, 0)
        """, ('Francisco Paula', ADMIN_EMAIL, new_hash, 'Administrador'))
        
        conn.commit()
        print("✅ Usuario creado exitosamente")
    
    # Verificar actualización
    print("\n✅ Verificando cambios...")
    cursor.execute("SELECT id, nombre, email, perfil, activo, password_temporal FROM usuarios WHERE email = %s", (ADMIN_EMAIL,))
    updated_user = cursor.fetchone()
    
    print(f"\n📋 Usuario actualizado:")
    print(f"   ID: {updated_user['id']}")
    print(f"   Nombre: {updated_user['nombre']}")
    print(f"   Email: {updated_user['email']}")
    print(f"   Perfil: {updated_user['perfil']}")
    print(f"   Activo: {updated_user['activo']}")
    print(f"   Password temporal: {updated_user['password_temporal']}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print(f"\n🔐 Credenciales:")
    print(f"   Email: {ADMIN_EMAIL}")
    print(f"   Contraseña: {NEW_PASSWORD}")
    print("\n🌐 Ahora puedes entrar a:")
    print("   https://tu-app.railway.app/login")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nVerifica que:")
    print("1. Las credenciales de MySQL sean correctas")
    print("2. El host/puerto sean accesibles")
    print("3. La base de datos 'drashirley' exista")





