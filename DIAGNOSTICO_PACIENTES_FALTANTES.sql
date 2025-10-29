-- DIAGNÓSTICO: Por qué solo se muestran 10 de 13 pacientes pendientes
-- EJECUTAR ESTOS QUERIES DIRECTAMENTE EN MYSQL PARA INVESTIGAR

-- ==================================================
-- 1. CONTAR TODOS LOS REGISTROS PENDIENTES (sin filtros)
-- ==================================================
SELECT 
    COUNT(*) as total_registros,
    COUNT(DISTINCT id) as registros_unicos
FROM facturas_detalle 
WHERE estado = 'pendiente' 
  AND activo = 1;

-- Resultado esperado: 13 (según el usuario)
-- Si sale menos, hay registros con activo = 0 o estado != 'pendiente'


-- ==================================================
-- 2. VERIFICAR SI HAY REGISTROS CON medico_consulta NULL
-- ==================================================
SELECT 
    COUNT(*) as registros_sin_medico_consulta
FROM facturas_detalle 
WHERE estado = 'pendiente' 
  AND activo = 1
  AND medico_consulta IS NULL;

-- Si sale > 0, esos registros se están excluyendo por el JOIN


-- ==================================================
-- 3. VERIFICAR SI HAY medico_consulta que NO existe en tabla medicos
-- ==================================================
SELECT 
    COUNT(*) as registros_con_medico_invalido,
    GROUP_CONCAT(DISTINCT medico_consulta) as medicos_invalidos
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
  AND m.id IS NULL
  AND fd.medico_consulta IS NOT NULL;

-- Si sale > 0, hay medico_consulta con ID que no existe


-- ==================================================
-- 4. LISTAR TODOS LOS 13 PACIENTES (o los que sean)
-- ==================================================
SELECT 
    fd.id,
    fd.nss,
    fd.nombre_paciente,
    fd.medico_consulta,
    m.nombre as medico_nombre,
    fd.ars_id,
    fd.estado,
    fd.activo
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
ORDER BY fd.nombre_paciente;

-- Esto debe mostrar TODOS los registros


-- ==================================================
-- 5. DETECTAR DUPLICADOS (mismo NSS + nombre)
-- ==================================================
SELECT 
    fd.nss,
    fd.nombre_paciente,
    COUNT(*) as veces_repetido,
    GROUP_CONCAT(fd.id ORDER BY fd.id) as ids_registros
FROM facturas_detalle fd
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
GROUP BY fd.nss, fd.nombre_paciente
HAVING COUNT(*) > 1;

-- Si sale algo, hay duplicados (ej: 2 registros de "Santana Bez")


-- ==================================================
-- 6. QUERY EXACTO QUE USA EL CÓDIGO (sin filtro de ARS)
-- ==================================================
SELECT 
    fd.id,
    fd.nss,
    fd.nombre_paciente,
    m.nombre as medico_nombre,
    a.nombre_ars,
    COALESCE(p.nombre, fd.nombre_paciente) as paciente_nombre_completo
FROM facturas_detalle fd
JOIN medicos m ON fd.medico_consulta = m.id
JOIN ars a ON fd.ars_id = a.id
LEFT JOIN pacientes p ON fd.paciente_id = p.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
ORDER BY fd.fecha_servicio DESC;

-- ¿Cuántos registros devuelve? ¿10 o 13?


-- ==================================================
-- 7. QUERY CON LEFT JOIN en medicos (en caso de que falte alguno)
-- ==================================================
SELECT 
    fd.id,
    fd.nss,
    fd.nombre_paciente,
    fd.medico_consulta,
    m.nombre as medico_nombre,
    a.nombre_ars,
    COALESCE(p.nombre, fd.nombre_paciente) as paciente_nombre_completo,
    CASE 
        WHEN m.id IS NULL THEN '⚠️ MÉDICO NO EXISTE'
        ELSE '✅ OK'
    END as estado_medico
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
JOIN ars a ON fd.ars_id = a.id
LEFT JOIN pacientes p ON fd.paciente_id = p.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
ORDER BY fd.fecha_servicio DESC;

-- Esto SIEMPRE debe mostrar todos los registros


-- ==================================================
-- 8. VERIFICAR SI EL PROBLEMA ES POR ARS ESPECÍFICO
-- ==================================================
SELECT 
    a.nombre_ars,
    COUNT(*) as total_pendientes
FROM facturas_detalle fd
JOIN ars a ON fd.ars_id = a.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
GROUP BY a.nombre_ars
ORDER BY total_pendientes DESC;

-- ¿Qué ARS tiene los 13 registros?


-- ==================================================
-- 9. CASO ESPECÍFICO: "Santana Bez" (2 registros según el usuario)
-- ==================================================
SELECT 
    fd.id,
    fd.nss,
    fd.nombre_paciente,
    fd.fecha_servicio,
    fd.autorizacion,
    fd.monto,
    fd.medico_consulta,
    m.nombre as medico_nombre,
    a.nombre_ars,
    fd.created_at
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
LEFT JOIN ars a ON fd.ars_id = a.id
WHERE fd.nombre_paciente LIKE '%Santana%Bez%'
  AND fd.estado = 'pendiente'
  AND fd.activo = 1
ORDER BY fd.created_at DESC;

-- Debe mostrar los 2 registros de Santana Bez


-- ==================================================
-- 10. RESUMEN FINAL: TODOS LOS IDs PENDIENTES
-- ==================================================
SELECT 
    GROUP_CONCAT(id ORDER BY id) as todos_los_ids_pendientes,
    COUNT(*) as total
FROM facturas_detalle
WHERE estado = 'pendiente' 
  AND activo = 1;

-- Anota estos IDs para verificar cuáles aparecen en la web



