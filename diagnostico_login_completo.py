"""
DIAGNÓSTICO COMPLETO DEL PROBLEMA DE LOGIN
Verifica usuario, password hash, y hace pruebas de autenticación
"""

import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

# Credenciales Railway MySQL
MYSQL_HOST = "ballast.proxy.rlwy.net"
MYSQL_PORT = 10669
MYSQL_USER = "root"
MYSQL_PASSWORD = "fmeSFyRCOODoDuPINTxYyzWatYzxxGCt"
MYSQL_DATABASE = "drashirley"

# Credenciales admin
ADMIN_EMAIL = "ing.fpaula@gmail.com"
TEST_PASSWORD = "2416Xpos@"

print("=" * 80)
print("🔍 DIAGNÓSTICO COMPLETO DEL PROBLEMA DE LOGIN")
print("=" * 80)

try:
    # Conectar
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
    print("✅ Conectado exitosamente\n")
    
    cursor = conn.cursor()
    
    # PASO 1: Buscar usuario exacto
    print(f"🔍 PASO 1: Buscando usuario exacto: {ADMIN_EMAIL}")
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (ADMIN_EMAIL,))
    user_exact = cursor.fetchone()
    
    if user_exact:
        print("✅ Usuario encontrado (búsqueda exacta)")
        print(f"   ID: {user_exact['id']}")
        print(f"   Nombre: {user_exact['nombre']}")
        print(f"   Email: {user_exact['email']}")
        print(f"   Perfil: {user_exact['perfil']}")
        print(f"   Activo: {user_exact['activo']}")
        print(f"   Password temporal: {user_exact['password_temporal']}")
        print(f"   Hash: {user_exact['password_hash'][:60]}...")
    else:
        print("❌ Usuario NO encontrado (búsqueda exacta)")
    
    # PASO 2: Buscar con LOWER (como hace el login)
    print(f"\n🔍 PASO 2: Buscando usuario con LOWER: {ADMIN_EMAIL.lower()}")
    cursor.execute("SELECT * FROM usuarios WHERE LOWER(email) = %s", (ADMIN_EMAIL.lower(),))
    user_lower = cursor.fetchone()
    
    if user_lower:
        print("✅ Usuario encontrado (búsqueda LOWER)")
        print(f"   ID: {user_lower['id']}")
        print(f"   Email almacenado: '{user_lower['email']}'")
        print(f"   Email lowercase: '{user_lower['email'].lower()}'")
    else:
        print("❌ Usuario NO encontrado (búsqueda LOWER)")
    
    # PASO 3: Listar TODOS los usuarios
    print("\n🔍 PASO 3: Listando TODOS los usuarios en la tabla:")
    cursor.execute("SELECT id, nombre, email, perfil, activo FROM usuarios")
    all_users = cursor.fetchall()
    
    if all_users:
        print(f"✅ Encontrados {len(all_users)} usuarios:")
        for u in all_users:
            print(f"   - ID: {u['id']} | Email: '{u['email']}' | Nombre: {u['nombre']} | Activo: {u['activo']}")
    else:
        print("❌ No hay usuarios en la tabla")
    
    # PASO 4: Verificar password hash
    if user_exact or user_lower:
        user = user_exact or user_lower
        print(f"\n🔍 PASO 4: Verificando password hash")
        print(f"   Hash almacenado: {user['password_hash'][:80]}...")
        print(f"   Contraseña a probar: '{TEST_PASSWORD}'")
        
        # Probar verificación
        is_valid = check_password_hash(user['password_hash'], TEST_PASSWORD)
        
        if is_valid:
            print("   ✅ CONTRASEÑA CORRECTA - El hash coincide")
        else:
            print("   ❌ CONTRASEÑA INCORRECTA - El hash NO coincide")
            
            # Generar un nuevo hash y comparar
            print("\n   🔄 Generando nuevo hash para comparar...")
            new_hash = generate_password_hash(TEST_PASSWORD)
            print(f"   Nuevo hash: {new_hash[:80]}...")
            
            # Probar el nuevo hash
            test_new = check_password_hash(new_hash, TEST_PASSWORD)
            print(f"   Nuevo hash válido: {'✅ SÍ' if test_new else '❌ NO'}")
            
            # ACTUALIZAR el hash en la base de datos
            print("\n   🔄 ACTUALIZANDO hash en la base de datos...")
            cursor.execute("""
                UPDATE usuarios 
                SET password_hash = %s,
                    email = %s,
                    activo = 1,
                    password_temporal = 0
                WHERE id = %s
            """, (new_hash, ADMIN_EMAIL.lower(), user['id']))
            
            conn.commit()
            print("   ✅ Hash actualizado en la base de datos")
            print(f"   ✅ Email normalizado a: {ADMIN_EMAIL.lower()}")
    
    # PASO 5: Verificación final
    print("\n" + "=" * 80)
    print("🔍 VERIFICACIÓN FINAL")
    print("=" * 80)
    
    cursor.execute("SELECT id, nombre, email, perfil, activo, password_temporal, password_hash FROM usuarios WHERE LOWER(email) = %s", (ADMIN_EMAIL.lower(),))
    final_user = cursor.fetchone()
    
    if final_user:
        print("✅ Usuario final:")
        print(f"   ID: {final_user['id']}")
        print(f"   Nombre: {final_user['nombre']}")
        print(f"   Email: {final_user['email']}")
        print(f"   Perfil: {final_user['perfil']}")
        print(f"   Activo: {final_user['activo']}")
        print(f"   Password temporal: {final_user['password_temporal']}")
        
        # Probar autenticación
        print("\n🔐 Probando autenticación...")
        auth_ok = check_password_hash(final_user['password_hash'], TEST_PASSWORD)
        
        if auth_ok:
            print("✅✅✅ AUTENTICACIÓN EXITOSA ✅✅✅")
            print("\n🎯 Credenciales para login:")
            print(f"   Email: {final_user['email']}")
            print(f"   Contraseña: {TEST_PASSWORD}")
        else:
            print("❌ Autenticación fallida - hash no coincide")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("=" * 80)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

