-- =========================================
-- OPTIMIZACIÓN DE BASE DE DATOS
-- Sistema Médico - Dra. Shirley Ramírez
-- =========================================

-- ÍNDICES PARA MEJORAR RENDIMIENTO DE CONSULTAS

-- Facturas Detalle (tabla más consultada)
CREATE INDEX IF NOT EXISTS idx_facturas_detalle_estado 
ON facturas_detalle(estado, activo);

CREATE INDEX IF NOT EXISTS idx_facturas_detalle_ars 
ON facturas_detalle(ars_id, estado, activo);

CREATE INDEX IF NOT EXISTS idx_facturas_detalle_medico 
ON facturas_detalle(medico_id, estado);

CREATE INDEX IF NOT EXISTS idx_facturas_detalle_fecha 
ON facturas_detalle(fecha_servicio);

CREATE INDEX IF NOT EXISTS idx_facturas_detalle_nss 
ON facturas_detalle(nss);

-- Pacientes
CREATE INDEX IF NOT EXISTS idx_pacientes_nss_ars 
ON pacientes(nss, ars_id);

CREATE INDEX IF NOT EXISTS idx_pacientes_activo 
ON pacientes(activo);

-- Facturas
CREATE INDEX IF NOT EXISTS idx_facturas_fecha 
ON facturas(fecha_factura);

CREATE INDEX IF NOT EXISTS idx_facturas_medico 
ON facturas(medico_id);

CREATE INDEX IF NOT EXISTS idx_facturas_ars 
ON facturas(ars_id);

CREATE INDEX IF NOT EXISTS idx_facturas_activo 
ON facturas(activo);

-- Appointments
CREATE INDEX IF NOT EXISTS idx_appointments_status 
ON appointments(status, created_at);

CREATE INDEX IF NOT EXISTS idx_appointments_date 
ON appointments(appointment_date);

-- Contact Messages
CREATE INDEX IF NOT EXISTS idx_messages_read 
ON contact_messages(read, created_at);

-- Usuarios
CREATE INDEX IF NOT EXISTS idx_usuarios_email 
ON usuarios(email);

CREATE INDEX IF NOT EXISTS idx_usuarios_activo 
ON usuarios(activo);

-- Médicos
CREATE INDEX IF NOT EXISTS idx_medicos_activo 
ON medicos(activo);

CREATE INDEX IF NOT EXISTS idx_medicos_email 
ON medicos(email);

CREATE INDEX IF NOT EXISTS idx_medicos_factura 
ON medicos(factura, activo);

-- ARS
CREATE INDEX IF NOT EXISTS idx_ars_activo 
ON ars(activo);

-- NCF
CREATE INDEX IF NOT EXISTS idx_ncf_activo 
ON ncf(activo);

-- Servicios
CREATE INDEX IF NOT EXISTS idx_servicios_activo 
ON tipos_servicios(activo);

-- =========================================
-- VACUUM Y ANALYZE PARA OPTIMIZACIÓN
-- =========================================

-- Recuperar espacio no utilizado
VACUUM;

-- Actualizar estadísticas para el optimizador de consultas
ANALYZE;

-- =========================================
-- CONFIGURACIONES DE RENDIMIENTO
-- =========================================

-- Write-Ahead Logging para mejor concurrencia
PRAGMA journal_mode=WAL;

-- Balance entre seguridad y velocidad
PRAGMA synchronous=NORMAL;

-- Cache de 10MB
PRAGMA cache_size=10000;

-- Tablas temporales en memoria
PRAGMA temp_store=MEMORY;

-- Memory-mapped I/O de 256MB
PRAGMA mmap_size=268435456;

-- Auto-vacuum
PRAGMA auto_vacuum=INCREMENTAL;

-- =========================================
-- NOTAS
-- =========================================
-- Ejecutar este script con:
-- sqlite3 drashirley_simple.db < optimize_database.sql
--
-- O desde Python:
-- conn.executescript(open('optimize_database.sql').read())
-- =========================================


