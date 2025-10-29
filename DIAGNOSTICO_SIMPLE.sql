-- ============================================================
-- DIAGNÓSTICO SIMPLIFICADO - EJECUTAR UNA POR UNA
-- ============================================================

-- QUERY 1: Total de registros pendientes
-- (Debe ser 13 según el usuario)
SELECT COUNT(*) as total_registros
FROM facturas_detalle 
WHERE estado = 'pendiente' 
  AND activo = 1;


-- QUERY 2: Con JOIN (lo que estás viendo ahora - probablemente 10)
SELECT COUNT(*) as registros_con_JOIN
FROM facturas_detalle fd
JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1;


-- QUERY 3: Con LEFT JOIN (lo que verás después del fix - debe ser 13)
SELECT COUNT(*) as registros_con_LEFT_JOIN
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1;


-- QUERY 4: ¿Cuántos tienen medico_consulta NULL?
SELECT COUNT(*) as con_medico_null
FROM facturas_detalle 
WHERE estado = 'pendiente' 
  AND activo = 1
  AND medico_consulta IS NULL;


-- QUERY 5: ¿Cuántos tienen medico_consulta con ID inválido?
SELECT COUNT(*) as con_medico_invalido
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
  AND fd.medico_consulta IS NOT NULL
  AND m.id IS NULL;


-- QUERY 6: Listar los pacientes EXCLUIDOS por JOIN
SELECT 
    fd.id,
    fd.nss,
    fd.nombre_paciente,
    fd.medico_consulta,
    m.nombre as medico_nombre
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
  AND (fd.medico_consulta IS NULL OR m.id IS NULL)
ORDER BY fd.id;


-- QUERY 7: Caso específico "Santana Bez"
SELECT 
    fd.id,
    fd.nss,
    fd.nombre_paciente,
    fd.medico_consulta,
    m.nombre as medico_nombre
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.nombre_paciente LIKE '%Santana%Bez%'
  AND fd.estado = 'pendiente'
  AND fd.activo = 1
ORDER BY fd.id;


-- QUERY 8: TODOS los pacientes pendientes (con LEFT JOIN)
SELECT 
    fd.id,
    fd.nss,
    fd.nombre_paciente,
    fd.medico_consulta,
    COALESCE(m.nombre, 'SIN MEDICO') as medico_nombre,
    fd.monto
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
ORDER BY fd.id;


-- ============================================================
-- INTERPRETACIÓN:
-- ============================================================
-- Si QUERY 1 = 13 y QUERY 2 = 10:
--   → HAY 3 PACIENTES EXCLUIDOS POR EL JOIN
--   → SOLUCIÓN: Usar LEFT JOIN (ya implementado)
--   → DESPLEGAR EL CÓDIGO
--
-- Si QUERY 1 = 10 y QUERY 2 = 10:
--   → NO ES PROBLEMA DEL JOIN
--   → INVESTIGAR OTRAS CAUSAS
-- ============================================================



