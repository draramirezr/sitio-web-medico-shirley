-- ============================================================
-- SCRIPT SQL COMPLETO PARA MYSQL - DRA. SHIRLEY RAMIREZ
-- Base de datos: drashirley
-- Actualizado: 23 Octubre 2025
-- ============================================================

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS drashirley;
USE drashirley;

-- ============================================================
-- TABLA: USUARIOS
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    perfil TEXT NOT NULL CHECK(perfil IN ('Administrador', 'Registro de Facturas')),
    activo BOOLEAN DEFAULT 1,
    password_temporal BOOLEAN DEFAULT 0,
    token_recuperacion TEXT,
    token_expiracion TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: SERVICES
-- ============================================================
CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    icon TEXT,
    price_range TEXT,
    duration TEXT,
    active BOOLEAN DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: TESTIMONIALS
-- ============================================================
CREATE TABLE IF NOT EXISTS testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name TEXT NOT NULL,
    patient_initials TEXT,
    testimonial_text TEXT NOT NULL,
    rating INT DEFAULT 5,
    approved BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    display_date DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: CONTACT_MESSAGES
-- ============================================================
CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone TEXT,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    `read` BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_read_created (`read`, created_at),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: APPOINTMENTS
-- ============================================================
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email VARCHAR(255),
    phone TEXT NOT NULL,
    appointment_date VARCHAR(10),
    appointment_time VARCHAR(10),
    appointment_type TEXT NOT NULL,
    medical_insurance TEXT NOT NULL,
    emergency_datetime VARCHAR(50),
    reason TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status_created (status, created_at),
    INDEX idx_date (appointment_date),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: SITE_VISITS
-- ============================================================
CREATE TABLE IF NOT EXISTS site_visits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total_visits INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: ARS
-- ============================================================
CREATE TABLE IF NOT EXISTS ars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_ars VARCHAR(255) NOT NULL,
    rnc TEXT NOT NULL,
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_activo (activo),
    INDEX idx_nombre (nombre_ars)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: MEDICOS
-- ============================================================
CREATE TABLE IF NOT EXISTS medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    especialidad TEXT NOT NULL,
    cedula VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255),
    exequatur TEXT,
    factura BOOLEAN DEFAULT 0,
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: TIPOS_SERVICIOS
-- ============================================================
CREATE TABLE IF NOT EXISTS tipos_servicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: NCF
-- ============================================================
CREATE TABLE IF NOT EXISTS ncf (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo TEXT NOT NULL,
    prefijo TEXT NOT NULL,
    tamaño INT NOT NULL DEFAULT 8,
    ultimo_numero INT NOT NULL DEFAULT 0,
    fecha_fin DATE,
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_activo (activo),
    INDEX idx_tipo_activo (tipo, activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: PACIENTES
-- ============================================================
CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nss VARCHAR(50) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    ars_id INT,
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ars_id) REFERENCES ars(id),
    UNIQUE(nss, ars_id),
    INDEX idx_nombre_activo (nombre, activo),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: FACTURAS
-- ============================================================
CREATE TABLE IF NOT EXISTS facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_factura TEXT,
    ncf TEXT,
    ncf_id INT,
    ncf_numero TEXT,
    fecha_factura DATE NOT NULL,
    medico_id INT NOT NULL,
    ars_id INT NOT NULL,
    total REAL DEFAULT 0,
    observaciones TEXT,
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medico_id) REFERENCES medicos(id),
    FOREIGN KEY (ars_id) REFERENCES ars(id),
    INDEX idx_fecha_factura (fecha_factura),
    INDEX idx_medico_activo (medico_id, activo),
    INDEX idx_ars_activo (ars_id, activo),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: FACTURAS_DETALLE
-- ============================================================
CREATE TABLE IF NOT EXISTS facturas_detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT,
    paciente_id INT NOT NULL,
    nss VARCHAR(50) NOT NULL,
    nombre_paciente TEXT NOT NULL,
    fecha_servicio DATE NOT NULL,
    autorizacion TEXT,
    servicio_id INT NOT NULL,
    descripcion_servicio TEXT NOT NULL,
    monto REAL NOT NULL,
    medico_id INT NOT NULL,
    ars_id INT NOT NULL,
    estado VARCHAR(50) DEFAULT 'pendiente',
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (factura_id) REFERENCES facturas(id),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (servicio_id) REFERENCES tipos_servicios(id),
    FOREIGN KEY (medico_id) REFERENCES medicos(id),
    FOREIGN KEY (ars_id) REFERENCES ars(id),
    INDEX idx_estado_activo (estado, activo),
    INDEX idx_ars_estado (ars_id, estado, activo),
    INDEX idx_medico_estado (medico_id, estado, activo),
    INDEX idx_fecha_servicio (fecha_servicio),
    INDEX idx_nss (nss),
    INDEX idx_factura_id (factura_id, activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: CODIGO_ARS
-- ============================================================
CREATE TABLE IF NOT EXISTS codigo_ars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ars_id INT NOT NULL,
    medico_id INT NOT NULL,
    codigo_ars TEXT NOT NULL,
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ars_id) REFERENCES ars(id),
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- INSERTAR USUARIO ADMIN POR DEFECTO
-- ============================================================
INSERT INTO usuarios (nombre, email, password_hash, perfil, activo)
SELECT 'Francisco Paula', 'ing.fpaula@gmail.com', 
       'scrypt:32768:8:1$iupLo7bsgOmGjpVR$39eeed0f26c2a4f4c5ee4ddc27e3f726bd5c7d58e8b4a4c26c7c8f0f84e0e9f9f5b9c9f0f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8',
       'Administrador', 1
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE email = 'ing.fpaula@gmail.com');

-- ============================================================
-- INSERTAR CONTADOR DE VISITAS
-- ============================================================
INSERT INTO site_visits (id, total_visits)
SELECT 1, 0
WHERE NOT EXISTS (SELECT 1 FROM site_visits WHERE id = 1);

-- ============================================================
-- FIN DEL SCRIPT
-- ============================================================





