#!/usr/bin/env python3
"""
Script para inicializar MySQL en Railway con todas las tablas y datos necesarios
"""

import os
import pymysql
from datetime import datetime

# Configuración de conexión MySQL Railway
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'mysql.railway.internal'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'railway'),
    'charset': 'utf8mb4'
}

print("=" * 60)
print("🚀 INICIALIZANDO MYSQL EN RAILWAY")
print("=" * 60)
print(f"Host: {MYSQL_CONFIG['host']}")
print(f"Database: {MYSQL_CONFIG['database']}")
print(f"User: {MYSQL_CONFIG['user']}")
print("=" * 60)

try:
    # Conectar a MySQL
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    print("✅ Conexión exitosa a MySQL")
    
    # Crear todas las tablas
    print("\n📋 Creando tablas...")
    
    tables = {
        'services': '''
            CREATE TABLE IF NOT EXISTS services (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                icon VARCHAR(100),
                active TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'aesthetic_treatments': '''
            CREATE TABLE IF NOT EXISTS aesthetic_treatments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                benefits TEXT,
                image_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'testimonials': '''
            CREATE TABLE IF NOT EXISTS testimonials (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                comment TEXT NOT NULL,
                rating INT DEFAULT 5,
                approved TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'contact_messages': '''
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50),
                subject VARCHAR(255),
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `read` TINYINT DEFAULT 0
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'appointments': '''
            CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50) NOT NULL,
                appointment_date DATE,
                appointment_time TIME,
                appointment_type VARCHAR(50),
                medical_insurance VARCHAR(255),
                emergency_datetime DATETIME,
                reason TEXT,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'usuarios': '''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                perfil VARCHAR(50) DEFAULT 'usuario',
                activo TINYINT DEFAULT 1,
                password_temporal TINYINT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'site_visits': '''
            CREATE TABLE IF NOT EXISTS site_visits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                total_visits INT DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'password_resets': '''
            CREATE TABLE IF NOT EXISTS password_resets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                token VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used TINYINT DEFAULT 0,
                INDEX idx_token (token),
                INDEX idx_email_created (email, created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        # Tablas de facturación
        'ars': '''
            CREATE TABLE IF NOT EXISTS ars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                codigo VARCHAR(50),
                activo TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'medicos': '''
            CREATE TABLE IF NOT EXISTS medicos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                especialidad VARCHAR(255),
                exequatur VARCHAR(100),
                email VARCHAR(255),
                telefono VARCHAR(50),
                puede_facturar TINYINT DEFAULT 1,
                activo TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'ncf': '''
            CREATE TABLE IF NOT EXISTS ncf (
                id INT AUTO_INCREMENT PRIMARY KEY,
                secuencia VARCHAR(50) NOT NULL,
                tipo VARCHAR(20),
                usado TINYINT DEFAULT 0,
                fecha_uso TIMESTAMP NULL,
                activo TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'codigo_ars': '''
            CREATE TABLE IF NOT EXISTS codigo_ars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(50) NOT NULL,
                descripcion VARCHAR(255),
                precio DECIMAL(10, 2),
                ars_id INT,
                medico_id INT,
                activo TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ars_id) REFERENCES ars(id),
                FOREIGN KEY (medico_id) REFERENCES medicos(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'servicios_facturacion': '''
            CREATE TABLE IF NOT EXISTS servicios_facturacion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(50) NOT NULL,
                descripcion VARCHAR(255) NOT NULL,
                precio DECIMAL(10, 2),
                activo TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'pacientes': '''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                nss VARCHAR(50),
                ars_id INT,
                telefono VARCHAR(50),
                email VARCHAR(255),
                direccion TEXT,
                activo TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ars_id) REFERENCES ars(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'facturas': '''
            CREATE TABLE IF NOT EXISTS facturas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                paciente_id INT,
                medico_id INT,
                ars_id INT,
                ncf_id INT,
                fecha_factura DATE,
                subtotal DECIMAL(10, 2),
                itbis DECIMAL(10, 2),
                total DECIMAL(10, 2),
                estado VARCHAR(50) DEFAULT 'pendiente',
                activo TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
                FOREIGN KEY (medico_id) REFERENCES medicos(id),
                FOREIGN KEY (ars_id) REFERENCES ars(id),
                FOREIGN KEY (ncf_id) REFERENCES ncf(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''',
        
        'facturas_detalle': '''
            CREATE TABLE IF NOT EXISTS facturas_detalle (
                id INT AUTO_INCREMENT PRIMARY KEY,
                factura_id INT,
                servicio_id INT,
                codigo_ars_id INT,
                descripcion VARCHAR(255),
                cantidad INT DEFAULT 1,
                precio_unitario DECIMAL(10, 2),
                subtotal DECIMAL(10, 2),
                activo TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (factura_id) REFERENCES facturas(id),
                FOREIGN KEY (servicio_id) REFERENCES servicios_facturacion(id),
                FOREIGN KEY (codigo_ars_id) REFERENCES codigo_ars(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        '''
    }
    
    for table_name, create_sql in tables.items():
        try:
            cursor.execute(create_sql)
            print(f"  ✅ Tabla '{table_name}' creada")
        except Exception as e:
            print(f"  ⚠️ Tabla '{table_name}': {e}")
    
    # Insertar datos iniciales
    print("\n📊 Insertando datos iniciales...")
    
    # Site visits
    cursor.execute("INSERT IGNORE INTO site_visits (id, total_visits) VALUES (1, 0)")
    print("  ✅ Contador de visitas inicializado")
    
    # Servicios con ICONOS
    servicios_data = [
        ('Consulta Ginecológica', 'Atención integral para la salud femenina', 'fas fa-user-md'),
        ('Control Prenatal', 'Seguimiento completo durante el embarazo', 'fas fa-baby'),
        ('Ecografía Obstétrica', 'Imágenes precisas del desarrollo fetal', 'fas fa-heartbeat'),
        ('Planificación Familiar', 'Asesoría en métodos anticonceptivos', 'fas fa-calendar-check'),
        ('Tratamiento de Infecciones', 'Diagnóstico y tratamiento especializado', 'fas fa-pills'),
        ('Cirugía Ginecológica', 'Procedimientos quirúrgicos especializados', 'fas fa-procedures')
    ]
    
    for nombre, desc, icono in servicios_data:
        try:
            cursor.execute(
                "INSERT INTO services (name, description, icon, active) VALUES (%s, %s, %s, 1)",
                (nombre, desc, icono)
            )
        except pymysql.err.IntegrityError:
            pass  # Ya existe
    
    print(f"  ✅ {len(servicios_data)} servicios insertados")
    
    # Testimonios de ejemplo
    testimonios = [
        ('María García', 'Excelente atención y profesionalismo. Me sentí muy cómoda durante toda la consulta.', 5),
        ('Ana López', 'La Dra. Shirley es muy dedicada y atenta. Altamente recomendada.', 5),
        ('Carmen Rodríguez', 'Servicio de primera calidad. El consultorio es muy moderno y limpio.', 5)
    ]
    
    for nombre, comentario, rating in testimonios:
        try:
            cursor.execute(
                "INSERT INTO testimonials (name, comment, rating, approved) VALUES (%s, %s, %s, 1)",
                (nombre, comentario, rating)
            )
        except pymysql.err.IntegrityError:
            pass
    
    print(f"  ✅ {len(testimonios)} testimonios insertados")
    
    # Usuario administrador (si no existe)
    from werkzeug.security import generate_password_hash
    admin_password = generate_password_hash('admin123')
    
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash, perfil, activo) VALUES (%s, %s, %s, %s, 1)",
            ('Administrador', 'admin@drashirley.com', admin_password, 'admin')
        )
        print("  ✅ Usuario administrador creado (admin@drashirley.com / admin123)")
    except pymysql.err.IntegrityError:
        print("  ℹ️ Usuario administrador ya existe")
    
    # Commit de todos los cambios
    conn.commit()
    
    print("\n" + "=" * 60)
    print("✅ INICIALIZACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print("\n📌 PRÓXIMOS PASOS:")
    print("1. El sitio web debería cargar correctamente")
    print("2. Puedes acceder al admin con: admin@drashirley.com / admin123")
    print("3. Los iconos de servicios están configurados correctamente")
    print("=" * 60)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n⚠️ POSIBLES CAUSAS:")
    print("1. Variables de entorno incorrectas")
    print("2. Servicio MySQL no accesible")
    print("3. Credenciales incorrectas")
    exit(1)

