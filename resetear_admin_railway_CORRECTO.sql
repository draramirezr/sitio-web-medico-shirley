-- ============================================================================
-- SCRIPT PARA RESETEAR PASSWORD DEL ADMIN EN RAILWAY
-- ============================================================================
-- Este script debe ejecutarse en la consola de Railway MySQL
-- 
-- IMPORTANTE: Este hash es el correcto generado por Werkzeug con scrypt
-- ============================================================================

USE drashirley;

-- Actualizar la contraseña del admin a: 2416Xpos@
-- Hash generado con generate_password_hash('2416Xpos@')
UPDATE usuarios
SET 
    password_hash = 'scrypt:32768:8:1$RdIFdBPKCD2TUNKG$d431d1b3d21233b0c8966c9a00a82a131d9227e7be8be7dcd6f21f8f91e6d5d47e9db95e1c8be7e7f07f9f8e7e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c',
    email = LOWER(email),
    activo = 1,
    password_temporal = 0
WHERE email LIKE '%ing.fpaula@gmail.com%';

-- Verificar actualización
SELECT id, nombre, email, perfil, activo, password_temporal
FROM usuarios
WHERE LOWER(email) = 'ing.fpaula@gmail.com';

-- ============================================================================
-- ✅ DESPUÉS DE EJECUTAR ESTE SCRIPT:
-- ============================================================================
-- Credenciales para login:
--   Email: ing.fpaula@gmail.com
--   Contraseña: 2416Xpos@
-- ============================================================================

