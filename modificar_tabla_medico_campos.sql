-- ====================================================================
-- MODIFICAR TABLA facturas_detalle: Separar medico_consulta y medico_id
-- ====================================================================
-- Fecha: 29 de octubre de 2025
-- Base de Datos: MySQL (Railway)
-- 
-- OBJETIVO:
-- - medico_consulta: Médico que ATENDIÓ al paciente (NOT NULL)
-- - medico_id: Médico que FACTURA (NULL hasta generar factura)
-- ====================================================================

-- ====================================================================
-- PASO 1: Modificar medico_id para que acepte NULL (PRIMERO)
-- ====================================================================
-- Esto es CRÍTICO: debe hacerse ANTES de intentar poner NULL en los registros
ALTER TABLE facturas_detalle 
MODIFY COLUMN medico_id INTEGER DEFAULT NULL;

-- ====================================================================
-- PASO 2: Agregar columna medico_consulta (si no existe)
-- ====================================================================
-- Si la columna ya existe, este comando fallará (es normal, continúa al siguiente paso)
ALTER TABLE facturas_detalle ADD COLUMN medico_consulta INTEGER DEFAULT NULL;

-- ====================================================================
-- PASO 3: Copiar datos de medico_id a medico_consulta (registros existentes)
-- ====================================================================
UPDATE facturas_detalle 
SET medico_consulta = medico_id 
WHERE medico_consulta IS NULL;

-- ====================================================================
-- PASO 4: Para registros PENDIENTES, limpiar medico_id (dejarlo NULL)
-- ====================================================================
UPDATE facturas_detalle 
SET medico_id = NULL 
WHERE estado = 'pendiente';

-- ====================================================================
-- PASO 5: Modificar medico_consulta para que sea NOT NULL
-- ====================================================================
-- Ahora sí podemos hacer que medico_consulta sea obligatorio
ALTER TABLE facturas_detalle 
MODIFY COLUMN medico_consulta INTEGER NOT NULL;

-- ====================================================================
-- PASO 6: Agregar índice para medico_consulta (optimización)
-- ====================================================================
ALTER TABLE facturas_detalle 
ADD INDEX idx_facturas_detalle_medico_consulta (medico_consulta);

-- ====================================================================
-- PASO 7: Verificar cambios - Ver estructura de la tabla
-- ====================================================================
DESCRIBE facturas_detalle;

-- ====================================================================
-- PASO 8: Ver 10 registros de ejemplo
-- ====================================================================
SELECT 
    id,
    nombre_paciente,
    medico_id as medico_factura,
    medico_consulta as medico_atencion,
    estado,
    fecha_servicio
FROM facturas_detalle
ORDER BY id DESC
LIMIT 10;

-- ====================================================================
-- FIN DEL SCRIPT
-- ====================================================================
-- 
-- NOTAS:
-- - PASO 1 es CRÍTICO: medico_id debe aceptar NULL ANTES de limpiarlo
-- - Si el PASO 2 falla con "Duplicate column name", es normal (la columna ya existe)
-- - Al finalizar, medico_id debe permitir NULL y medico_consulta debe ser NOT NULL
-- ====================================================================

