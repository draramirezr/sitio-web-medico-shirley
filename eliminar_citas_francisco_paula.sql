-- ============================================
-- ELIMINAR CITAS DE PRUEBA: Francisco Paula
-- ============================================
-- Fecha: 18 de Enero, 2026
-- Descripción: Eliminar todas las citas a nombre de Francisco Paula (datos de prueba)

-- 1. Ver primero cuántas citas hay con ese nombre (VERIFICACIÓN)
SELECT 
    id,
    first_name,
    last_name,
    phone,
    email,
    appointment_type,
    appointment_date,
    status,
    created_at
FROM appointments
WHERE first_name LIKE '%Francisco%' 
   OR last_name LIKE '%Paula%'
   OR CONCAT(first_name, ' ', last_name) LIKE '%Francisco Paula%';

-- 2. ELIMINAR las citas (descomentar la línea de abajo después de verificar)
-- DELETE FROM appointments 
-- WHERE first_name LIKE '%Francisco%' 
--    OR last_name LIKE '%Paula%'
--    OR CONCAT(first_name, ' ', last_name) LIKE '%Francisco Paula%';

-- 3. Verificar que se eliminaron (ejecutar después del DELETE)
-- SELECT COUNT(*) as total_citas_restantes FROM appointments;

-- ============================================
-- INSTRUCCIONES:
-- ============================================
-- PASO 1: Ejecuta primero el SELECT (líneas 9-18) para VER las citas
-- PASO 2: Verifica que sean las citas correctas
-- PASO 3: Quita los comentarios (--) de las líneas 21-24 y ejecuta el DELETE
-- PASO 4: Ejecuta el SELECT de verificación (línea 27)
-- ============================================
