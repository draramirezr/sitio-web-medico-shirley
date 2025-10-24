-- =========================================
-- OPTIMIZACIÓN CRÍTICA DE BASE DE DATOS
-- Sistema Médico - Dra. Shirley Ramírez
-- =========================================

-- ÍNDICES CRÍTICOS PARA MEJORAR VELOCIDAD

-- 1. FACTURAS_DETALLE (tabla más consultada)
CREATE INDEX IF NOT EXISTS idx_facturas_detalle_estado_activo 
ON facturas_detalle(estado, activo);

CREATE INDEX IF NOT EXISTS idx_facturas_detalle_ars_estado 
ON facturas_detalle(ars_id, estado, activo);

CREATE INDEX IF NOT EXISTS idx_facturas_detalle_medico_estado 
ON facturas_detalle(medico_id, estado, activo);

CREATE INDEX IF NOT EXISTS idx_facturas_detalle_fecha_servicio 
ON facturas_detalle(fecha_servicio);

CREATE INDEX IF NOT EXISTS idx_facturas_detalle_nss 
ON facturas_detalle(nss);

CREATE INDEX IF NOT EXISTS idx_facturas_detalle_factura_id 
ON facturas_detalle(factura_id, activo);

-- 2. PACIENTES (consultas frecuentes)
CREATE INDEX IF NOT EXISTS idx_pacientes_nss_ars_activo 
ON pacientes(nss, ars_id, activo);

CREATE INDEX IF NOT EXISTS idx_pacientes_nombre_activo 
ON pacientes(nombre, activo);

CREATE INDEX IF NOT EXISTS idx_pacientes_activo 
ON pacientes(activo);

-- 3. FACTURAS (historial y consultas)
CREATE INDEX IF NOT EXISTS idx_facturas_fecha_factura 
ON facturas(fecha_factura);

CREATE INDEX IF NOT EXISTS idx_facturas_medico_activo 
ON facturas(medico_id, activo);

CREATE INDEX IF NOT EXISTS idx_facturas_ars_activo 
ON facturas(ars_id, activo);

CREATE INDEX IF NOT EXISTS idx_facturas_activo 
ON facturas(activo);

-- 4. APPOINTMENTS (citas - consultas frecuentes)
CREATE INDEX IF NOT EXISTS idx_appointments_status_created 
ON appointments(status, created_at);

CREATE INDEX IF NOT EXISTS idx_appointments_date 
ON appointments(appointment_date);

CREATE INDEX IF NOT EXISTS idx_appointments_email 
ON appointments(email);

-- 5. CONTACT_MESSAGES (mensajes - filtrado)
CREATE INDEX IF NOT EXISTS idx_messages_read_created 
ON contact_messages(read, created_at);

CREATE INDEX IF NOT EXISTS idx_messages_email 
ON contact_messages(email);

-- 6. USUARIOS (login frecuente)
CREATE INDEX IF NOT EXISTS idx_usuarios_email_activo 
ON usuarios(email, activo);

CREATE INDEX IF NOT EXISTS idx_usuarios_activo 
ON usuarios(activo);

CREATE INDEX IF NOT EXISTS idx_usuarios_perfil_activo 
ON usuarios(perfil, activo);

-- 7. MÉDICOS (filtrado por factura)
CREATE INDEX IF NOT EXISTS idx_medicos_activo_factura 
ON medicos(activo, factura);

CREATE INDEX IF NOT EXISTS idx_medicos_email 
ON medicos(email);

CREATE INDEX IF NOT EXISTS idx_medicos_nombre 
ON medicos(nombre);

-- 8. ARS (filtrado)
CREATE INDEX IF NOT EXISTS idx_ars_activo 
ON ars(activo);

CREATE INDEX IF NOT EXISTS idx_ars_nombre 
ON ars(nombre_ars);

-- 9. NCF (filtrado)
CREATE INDEX IF NOT EXISTS idx_ncf_activo 
ON ncf(activo);

CREATE INDEX IF NOT EXISTS idx_ncf_tipo_activo 
ON ncf(tipo, activo);

-- 10. CÓDIGO_ARS (búsquedas complejas)
CREATE INDEX IF NOT EXISTS idx_codigo_ars_medico_ars 
ON codigo_ars(medico_id, ars_id, activo);

CREATE INDEX IF NOT EXISTS idx_codigo_ars_codigo 
ON codigo_ars(codigo_ars);

-- OPTIMIZACIONES ADICIONALES PARA SQLITE
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA cache_size=20000;
PRAGMA temp_store=MEMORY;
PRAGMA mmap_size=268435456;  -- 256MB
PRAGMA page_size=4096;
PRAGMA auto_vacuum=INCREMENTAL;

