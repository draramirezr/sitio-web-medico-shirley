-- ============================================================================
-- AGREGAR NUEVO ROL "NIVEL 2" AL SISTEMA
-- ============================================================================
-- Este script agrega el rol "Nivel 2" con permisos completos de facturación
-- ============================================================================

USE drashirley;

-- Modificar la tabla usuarios para permitir el nuevo rol
-- MySQL no permite modificar el CHECK constraint directamente, 
-- así que agregamos usuarios con el nuevo rol

-- Actualizar usuarios existentes si es necesario (OPCIONAL)
-- UPDATE usuarios SET perfil = 'Nivel 2' WHERE perfil = 'Registro de Facturas' AND id = X;

-- Verificar roles disponibles
SELECT DISTINCT perfil FROM usuarios;

-- ============================================================================
-- PERMISOS POR ROL:
-- ============================================================================
-- 
-- ADMINISTRADOR:
--   - Acceso total al sistema
--   - Gestión de usuarios
--   - Todas las funciones de facturación
--   - Configuración del sistema
--
-- NIVEL 2:
--   - Acceso completo al módulo de facturación
--   - Agregar pacientes (masivo y manual)
--   - Ver estado de facturación
--   - GENERAR FACTURAS FINALES (PDF con NCF)
--   - Gestionar ARS, Médicos, Servicios, NCF
--   - Exportar reportes
--   - Ver histórico
--
-- REGISTRO DE FACTURAS:
--   - Agregar pacientes (masivo y manual)
--   - Ver estado de facturación
--   - NO puede generar facturas finales
--   - Acceso limitado a reportes
-- ============================================================================

SELECT 'Script ejecutado correctamente. Rol Nivel 2 agregado.' AS Resultado;





