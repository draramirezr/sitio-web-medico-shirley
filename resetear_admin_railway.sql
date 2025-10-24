-- ============================================================
-- RESETEAR CONTRASEÑA DEL ADMIN
-- Email: ing.fpaula@gmail.com
-- Nueva contraseña: 2416Xpos@
-- ============================================================

USE drashirley;

-- Actualizar la contraseña del admin
UPDATE usuarios 
SET password_hash = 'scrypt:32768:8:1$d8ZQmxoGrn3kkZyv$862c5c8e5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c5e8f5b5c',
    password_temporal = 0,
    activo = 1
WHERE email = 'ing.fpaula@gmail.com';

-- Verificar que se actualizó
SELECT id, nombre, email, perfil, activo 
FROM usuarios 
WHERE email = 'ing.fpaula@gmail.com';





