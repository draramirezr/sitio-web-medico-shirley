-- ====================================================================
-- MODIFICAR TABLA facturas_detalle: Separar medico_consulta y medico_id
-- ====================================================================
-- Fecha: 29 de octubre de 2025
-- 
-- OBJETIVO:
-- - medico_consulta: Médico que ATENDIÓ al paciente (NOT NULL)
-- - medico_id: Médico que FACTURA (NULL hasta generar factura)
-- ====================================================================

USE railway;

-- ====================================================================
-- PASO 1: Agregar columna medico_consulta (si no existe)
-- ====================================================================
ALTER TABLE facturas_detalle 
ADD COLUMN IF NOT EXISTS medico_consulta INTEGER DEFAULT NULL;

-- ====================================================================
-- PASO 2: Copiar datos de medico_id a medico_consulta (registros existentes)
-- ====================================================================
UPDATE facturas_detalle 
SET medico_consulta = medico_id 
WHERE medico_consulta IS NULL;

-- ====================================================================
-- PASO 3: Para registros PENDIENTES, limpiar medico_id (dejarlo NULL)
-- ====================================================================
UPDATE facturas_detalle 
SET medico_id = NULL 
WHERE estado = 'pendiente';

-- ====================================================================
-- PASO 4: Modificar columnas con las restricciones correctas
-- ====================================================================

-- medico_id: Permitir NULL (se llenará al generar factura)
ALTER TABLE facturas_detalle 
MODIFY COLUMN medico_id INTEGER DEFAULT NULL;

-- medico_consulta: NO permitir NULL (siempre se conoce al agregar paciente)
ALTER TABLE facturas_detalle 
MODIFY COLUMN medico_consulta INTEGER NOT NULL;

-- ====================================================================
-- PASO 5: Verificar cambios
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

