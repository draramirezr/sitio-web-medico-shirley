-- ============================================
-- SCRIPT DE INICIALIZACIÓN MYSQL - RAILWAY
-- Sistema Web Médico - Dra. Shirley Ramírez
-- ============================================

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS drashirley 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Seleccionar la base de datos
USE drashirley;

-- Limpiar base de datos (CUIDADO: Esto elimina todas las tablas existentes)
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS facturas_detalle;
DROP TABLE IF EXISTS facturas;
DROP TABLE IF EXISTS pacientes;
DROP TABLE IF EXISTS codigo_ars;
DROP TABLE IF EXISTS tipos_servicios;
DROP TABLE IF EXISTS ncf;
DROP TABLE IF EXISTS medicos;
DROP TABLE IF EXISTS ars;
DROP TABLE IF EXISTS contact_messages;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS testimonials;
DROP TABLE IF EXISTS aesthetic_treatments;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS site_visits;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- TABLAS PRINCIPALES
-- ============================================

-- Tabla de Servicios
CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(100),
    price_range VARCHAR(100),
    duration VARCHAR(50),
    active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    perfil VARCHAR(50) NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    password_temporal TINYINT(1) DEFAULT 0,
    token_recuperacion VARCHAR(255),
    token_expiracion TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_email_activo (email, activo),
    INDEX idx_activo (activo),
    INDEX idx_perfil_activo (perfil, activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Testimonios
CREATE TABLE IF NOT EXISTS testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    patient_initials VARCHAR(10),
    testimonial_text TEXT NOT NULL,
    rating INT DEFAULT 5,
    approved TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    display_date DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Mensajes de Contacto
CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `read` TINYINT(1) DEFAULT 0,
    INDEX idx_read_created (`read`, created_at),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Citas
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
    emergency_datetime TEXT,
    reason TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status_created (status, created_at),
    INDEX idx_date (appointment_date),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Tratamientos Estéticos
CREATE TABLE IF NOT EXISTS aesthetic_treatments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Contador de Visitas
CREATE TABLE IF NOT EXISTS site_visits (
    id INT PRIMARY KEY,
    total_visits INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLAS DE FACTURACIÓN
-- ============================================

-- Tabla de ARS (Administradoras de Riesgos de Salud)
CREATE TABLE IF NOT EXISTS ars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_ars VARCHAR(255) NOT NULL,
    rnc VARCHAR(50) NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_activo (activo),
    INDEX idx_nombre (nombre_ars)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Médicos
CREATE TABLE IF NOT EXISTS medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    especialidad VARCHAR(255) NOT NULL,
    cedula VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255),
    exequatur VARCHAR(100),
    factura TINYINT(1) DEFAULT 0,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_activo_factura (activo, factura),
    INDEX idx_email (email),
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Código ARS (relación médico-ars con su código)
CREATE TABLE IF NOT EXISTS codigo_ars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medico_id INT NOT NULL,
    ars_id INT NOT NULL,
    codigo_ars VARCHAR(100) NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medico_id) REFERENCES medicos(id) ON DELETE CASCADE,
    FOREIGN KEY (ars_id) REFERENCES ars(id) ON DELETE CASCADE,
    UNIQUE KEY unique_medico_ars (medico_id, ars_id),
    INDEX idx_medico_ars (medico_id, ars_id, activo),
    INDEX idx_codigo (codigo_ars)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Tipos de Servicios
CREATE TABLE IF NOT EXISTS tipos_servicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL,
    precio_base DECIMAL(10,2) DEFAULT 0,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de NCF (Números de Comprobante Fiscal)
CREATE TABLE IF NOT EXISTS ncf (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    prefijo VARCHAR(50) NOT NULL,
    tamaño INT NOT NULL,
    ultimo_numero INT DEFAULT 0,
    fecha_fin DATE,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_activo (activo),
    INDEX idx_tipo_activo (tipo, activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Pacientes (Maestra)
CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nss VARCHAR(50) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    ars_id INT,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ars_id) REFERENCES ars(id) ON DELETE SET NULL,
    UNIQUE KEY unique_nss_ars (nss, ars_id),
    INDEX idx_nss_ars_activo (nss, ars_id, activo),
    INDEX idx_nombre_activo (nombre, activo),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Facturas (Encabezado)
CREATE TABLE IF NOT EXISTS facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_factura VARCHAR(50),
    ncf VARCHAR(50),
    ncf_id INT,
    ncf_numero VARCHAR(50),
    fecha_factura DATE NOT NULL,
    medico_id INT NOT NULL,
    ars_id INT NOT NULL,
    total DECIMAL(10,2) DEFAULT 0,
    observaciones TEXT,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medico_id) REFERENCES medicos(id) ON DELETE RESTRICT,
    FOREIGN KEY (ars_id) REFERENCES ars(id) ON DELETE RESTRICT,
    INDEX idx_fecha_factura (fecha_factura),
    INDEX idx_medico_activo (medico_id, activo),
    INDEX idx_ars_activo (ars_id, activo),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Detalle de Facturas (Líneas)
CREATE TABLE IF NOT EXISTS facturas_detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT,
    paciente_id INT NOT NULL,
    nss VARCHAR(50) NOT NULL,
    nombre_paciente VARCHAR(255) NOT NULL,
    fecha_servicio DATE NOT NULL,
    autorizacion VARCHAR(100),
    servicio_id INT NOT NULL,
    descripcion_servicio VARCHAR(255) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    medico_id INT NOT NULL,
    ars_id INT NOT NULL,
    estado VARCHAR(50) DEFAULT 'pendiente',
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE SET NULL,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE RESTRICT,
    FOREIGN KEY (servicio_id) REFERENCES tipos_servicios(id) ON DELETE RESTRICT,
    FOREIGN KEY (medico_id) REFERENCES medicos(id) ON DELETE RESTRICT,
    FOREIGN KEY (ars_id) REFERENCES ars(id) ON DELETE RESTRICT,
    INDEX idx_estado_activo (estado, activo),
    INDEX idx_ars_estado (ars_id, estado, activo),
    INDEX idx_medico_estado (medico_id, estado, activo),
    INDEX idx_fecha_servicio (fecha_servicio),
    INDEX idx_nss (nss),
    INDEX idx_factura_id (factura_id, activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- DATOS INICIALES
-- ============================================

-- Inicializar contador de visitas
INSERT INTO site_visits (id, total_visits) VALUES (1, 0);

-- Usuario por defecto: Francisco Paula (Administrador)
INSERT INTO usuarios (nombre, email, password_hash, perfil, activo) 
VALUES ('Francisco Paula', 'ing.fpaula@gmail.com', 'scrypt:32768:8:1$S0LR0eUGAXz1iJKw$2e7f41f91d83c9537a0bdc4f3b0e4c5eae5e3a0d9f3c8e4f1d2a5b6c7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b', 'Administrador', 1);

-- Servicios
INSERT INTO services (name, description, icon, price_range, duration, active) VALUES
('Consulta Ginecológica', 'Consulta ginecológica\nPapanicolau\nColposcopia/biopsias\nCirugías ginecológicas\nIrregularidad menstrual\nGenotipificación y manejo del virus de papiloma humano\nManejo del síndrome de ovario poliquístico\nPlanificación familiar\nMenopausia y climaterio', 'fas fa-female', 'Consultar', '45 min', 1),
('Consulta Obstétrica', 'Consulta de obstetricia\nConsulta preconcepcional\nControl prenatal\nSeguimiento de embarazo de alto riesgo\nPartos y cesáreas\nAsesoría en lactancia materna', 'fas fa-baby', 'Consultar', '60 min', 1),
('Ecografías', 'Estudios de imagen para diagnóstico y seguimiento del embarazo y condiciones ginecológicas.', 'fas fa-heartbeat', 'Consultar', '30 min', 1),
('Cirugía Ginecológica', 'Procedimientos quirúrgicos especializados en ginecología con técnicas avanzadas.', 'fas fa-cut', 'Consultar', 'Variable', 1),
('Planificación Familiar', 'Asesoría sobre métodos anticonceptivos y planificación reproductiva personalizada.', 'fas fa-calendar-check', 'Consultar', '30 min', 1),
('Tratamientos Estéticos Ginecológicos', 'Tecnología láser de última generación para rejuvenecimiento vaginal, blanqueamiento genital, corrección de cicatrices y más. Click para ver todos los tratamientos disponibles.', 'fas fa-wand-magic-sparkles', 'Ver Tratamientos', 'Variable', 1);

-- Tratamientos Estéticos
INSERT INTO aesthetic_treatments (name, description, icon) VALUES
('Rejuvenecimiento vaginal', 'Mejora la elasticidad y tonicidad del canal vaginal.\nReduce la sequedad y mejora la lubricación natural.\nFavorece la producción de colágeno y elastina.', 'fas fa-magic'),
('Blanqueamiento genital', 'Aclara la pigmentación de la vulva, periné o zona anal.\nUnifica el tono de la piel íntima.', 'fas fa-sun'),
('Tensado o lifting vulvar', 'Mejora la apariencia externa de los labios mayores y menores.\nCorrige leve flacidez o laxitud de la vulva.', 'fas fa-compress-arrows-alt'),
('Corrección de cicatrices postparto o episiotomía', 'Suaviza la textura, color y relieve de cicatrices.\nDisminuye molestias o retracciones cicatriciales.', 'fas fa-hand-holding-medical'),
('Atrofia vulvovaginal (Síndrome Genitourinario de la Menopausia)', 'Alivia sequedad, ardor, picazón y dispareunia.\nEstimula la regeneración del epitelio vaginal.', 'fas fa-leaf'),
('Incontinencia urinaria leve a moderada', 'Fortalece las paredes vaginales y la uretra.\nMejora el soporte del suelo pélvico.\nDisminuye las pérdidas de orina al toser o hacer esfuerzo.', 'fas fa-shield-alt'),
('Laxitud vaginal postparto o por envejecimiento', 'Reafirma los tejidos del canal vaginal.\nMejora la sensibilidad y la satisfacción sexual.', 'fas fa-heart'),
('Vulvodinia y vestibulodinia leves', 'Reduce el dolor crónico vulvar mediante la bioestimulación tisular.', 'fas fa-spa'),
('Condilomas vulvares o vaginales (verrugas por VPH)', 'Eliminación precisa de lesiones con mínima lesión tisular.', 'fas fa-exclamation-triangle'),
('Lesiones cervicales leves (ej. NIC I)', 'Vaporización controlada de lesiones benignas o displásicas superficiales.', 'fas fa-stethoscope'),
('Quistes o pólipos pequeños del cuello uterino o vulvares', 'Resección con mínimo sangrado y rápida cicatrización.', 'fas fa-cut'),
('Liquen escleroso vulvar (casos seleccionados)', 'Mejora la textura y síntomas, reduciendo picazón y ardor.\nEstimula la regeneración epitelial.', 'fas fa-microscope'),
('Bartolinitis crónica o recidivante (marsupialización asistida con láser)', 'Facilita drenaje y recuperación más rápida.', 'fas fa-bolt');

-- ============================================
-- FIN DEL SCRIPT
-- ============================================

SELECT 'Base de datos inicializada correctamente' AS status;

