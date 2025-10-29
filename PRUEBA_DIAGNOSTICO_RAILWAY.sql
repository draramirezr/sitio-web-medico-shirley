-- ============================================================
-- DIAGNÓSTICO: Pacientes Faltantes (10 de 13)
-- EJECUTAR EN MYSQL DE RAILWAY
-- ============================================================

-- ==================================================
-- PASO 1: Contar TODOS los registros pendientes
-- ==================================================
SELECT 
    '=== PASO 1: Total de registros pendientes ===' as paso;

SELECT 
    COUNT(*) as total_registros
FROM facturas_detalle 
WHERE estado = 'pendiente' 
  AND activo = 1;

-- RESULTADO ESPERADO: 13 (según el usuario)


-- ==================================================
-- PASO 2: Verificar registros SIN medico_consulta
-- ==================================================
SELECT 
    '=== PASO 2: Registros con medico_consulta NULL ===' as paso;

SELECT 
    COUNT(*) as sin_medico_asignado
FROM facturas_detalle 
WHERE estado = 'pendiente' 
  AND activo = 1
  AND medico_consulta IS NULL;

-- Si sale > 0, estos se están EXCLUYENDO con JOIN


-- ==================================================
-- PASO 3: Verificar medico_consulta con ID INVÁLIDO
-- ==================================================
SELECT 
    '=== PASO 3: Registros con medico_consulta inválido ===' as paso;

SELECT 
    COUNT(*) as medico_id_invalido,
    GROUP_CONCAT(DISTINCT fd.medico_consulta) as ids_que_no_existen
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
  AND fd.medico_consulta IS NOT NULL
  AND m.id IS NULL;

-- Si sale > 0, esos IDs no existen en tabla 'medicos'


-- ==================================================
-- PASO 4: COMPARACIÓN CRÍTICA - JOIN vs LEFT JOIN
-- ==================================================
SELECT 
    '=== PASO 4A: CON JOIN (código antes del fix) ===' as paso;

SELECT COUNT(*) as registros_con_JOIN
FROM facturas_detalle fd
JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1;

-- ESTO ES LO QUE ESTABAS VIENDO (probablemente 10)

SELECT 
    '=== PASO 4B: CON LEFT JOIN (código después del fix) ===' as paso;

SELECT COUNT(*) as registros_con_LEFT_JOIN
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1;

-- ESTO ES LO QUE VERÁS DESPUÉS DEL FIX (debe ser 13)


-- ==================================================
-- PASO 5: Listar los registros EXCLUIDOS por JOIN
-- ==================================================
SELECT 
    '=== PASO 5: Registros EXCLUIDOS por JOIN ===' as paso;

SELECT 
    fd.id,
    fd.nss,
    fd.nombre_paciente,
    fd.medico_consulta,
    m.nombre as medico_nombre,
    CASE 
        WHEN fd.medico_consulta IS NULL THEN '❌ medico_consulta es NULL'
        WHEN m.id IS NULL THEN '❌ medico_consulta tiene ID que no existe'
        ELSE '✅ OK'
    END as problema
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
  AND (fd.medico_consulta IS NULL OR m.id IS NULL)
ORDER BY fd.id;

-- Estos son los que se estaban PERDIENDO


-- ==================================================
-- PASO 6: CASO ESPECÍFICO - "Santana Bez"
-- ==================================================
SELECT 
    '=== PASO 6: Registros de Santana Bez ===' as paso;

SELECT 
    fd.id,
    fd.nss,
    fd.nombre_paciente,
    fd.medico_consulta,
    m.nombre as medico_nombre,
    fd.fecha_servicio,
    fd.monto,
    CASE 
        WHEN m.id IS NULL THEN '❌ EXCLUIDO POR JOIN'
        ELSE '✅ VISIBLE'
    END as estado_join
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.nombre_paciente LIKE '%Santana%Bez%'
  AND fd.estado = 'pendiente'
  AND fd.activo = 1
ORDER BY fd.id;

-- Debe mostrar 2 registros (según el usuario)


-- ==================================================
-- PASO 7: TODOS los pacientes pendientes (detallado)
-- ==================================================
SELECT 
    '=== PASO 7: LISTADO COMPLETO de pacientes pendientes ===' as paso;

SELECT 
    fd.id,
    fd.nss,
    fd.nombre_paciente,
    fd.medico_consulta,
    COALESCE(m.nombre, '⚠️ SIN MÉDICO') as medico_nombre,
    fd.fecha_servicio,
    fd.monto,
    CASE 
        WHEN m.id IS NOT NULL THEN '✅ Con JOIN'
        ELSE '❌ Solo con LEFT JOIN'
    END as visibilidad
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
ORDER BY fd.id;

-- Este debe mostrar TODOS los 13 registros


-- ==================================================
-- PASO 8: Agrupar por ARS (por si hay filtro)
-- ==================================================
SELECT 
    '=== PASO 8: Pacientes pendientes por ARS ===' as paso;

SELECT 
    a.id as ars_id,
    a.nombre_ars,
    COUNT(*) as total_pendientes
FROM facturas_detalle fd
JOIN ars a ON fd.ars_id = a.id
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
GROUP BY a.id, a.nombre_ars
ORDER BY total_pendientes DESC;

-- ¿Qué ARS tiene los 13 pacientes?


-- ==================================================
-- PASO 9: Detectar duplicados
-- ==================================================
SELECT 
    '=== PASO 9: Detectar registros duplicados ===' as paso;

SELECT 
    fd.nss,
    fd.nombre_paciente,
    COUNT(*) as veces_repetido,
    GROUP_CONCAT(fd.id ORDER BY fd.id) as ids_de_registros
FROM facturas_detalle fd
WHERE fd.estado = 'pendiente' 
  AND fd.activo = 1
GROUP BY fd.nss, fd.nombre_paciente
HAVING COUNT(*) > 1;

-- Si hay duplicados (ej: 2 veces "Santana Bez")


-- ==================================================
-- PASO 10: RESUMEN EJECUTIVO
-- ==================================================
SELECT 
    '=== PASO 10: RESUMEN FINAL ===' as paso;

SELECT 
    (SELECT COUNT(*) 
     FROM facturas_detalle 
     WHERE estado = 'pendiente' AND activo = 1) as total_en_bd,
    
    (SELECT COUNT(*) 
     FROM facturas_detalle fd
     JOIN medicos m ON fd.medico_consulta = m.id
     WHERE fd.estado = 'pendiente' AND fd.activo = 1) as visible_con_JOIN,
    
    (SELECT COUNT(*) 
     FROM facturas_detalle fd
     LEFT JOIN medicos m ON fd.medico_consulta = m.id
     WHERE fd.estado = 'pendiente' AND fd.activo = 1) as visible_con_LEFT_JOIN,
    
    (SELECT COUNT(*) 
     FROM facturas_detalle 
     WHERE estado = 'pendiente' AND activo = 1 AND medico_consulta IS NULL) as sin_medico,
    
    (SELECT COUNT(*) 
     FROM facturas_detalle fd
     LEFT JOIN medicos m ON fd.medico_consulta = m.id
     WHERE fd.estado = 'pendiente' AND fd.activo = 1 
       AND fd.medico_consulta IS NOT NULL AND m.id IS NULL) as medico_invalido;


-- ============================================================
-- INTERPRETACIÓN DE RESULTADOS
-- ============================================================

/*
CASO A: si total_en_bd = 13, visible_con_JOIN = 10, visible_con_LEFT_JOIN = 13
  → ✅ CONFIRMADO: 3 pacientes se están excluyendo por JOIN
  → SOLUCIÓN: Usar LEFT JOIN (ya implementado en el código)

CASO B: si total_en_bd = 10, visible_con_JOIN = 10, visible_con_LEFT_JOIN = 10
  → ❌ El problema NO es el JOIN
  → INVESTIGAR: Filtros de ARS, estado incorrecto, activo=0, etc.

CASO C: si sin_medico > 0
  → Hay pacientes sin medico_consulta asignado
  → Se excluyen con JOIN, se incluyen con LEFT JOIN

CASO D: si medico_invalido > 0
  → Hay pacientes con medico_consulta que apunta a un ID que no existe
  → Se excluyen con JOIN, se incluyen con LEFT JOIN
*/


-- ============================================================
-- INSTRUCCIONES DE USO
-- ============================================================

/*
1. Conéctate a Railway MySQL
2. Selecciona la base de datos correcta: USE drashirley;
3. COPIA Y PEGA todo este archivo
4. Ejecuta paso por paso o todo junto
5. Observa especialmente el PASO 4 (JOIN vs LEFT JOIN)
6. Anota los resultados del PASO 10 (RESUMEN)

RESULTADOS ESPERADOS según tu caso:
- Total en BD: 13
- Visible con JOIN: 10
- Visible con LEFT JOIN: 13
- Diferencia: 3 pacientes excluidos por JOIN

Si los resultados coinciden con lo esperado:
→ La solución con LEFT JOIN es correcta
→ Proceder a desplegar el código actualizado
*/



