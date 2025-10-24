-- Actualizar ícono de Consulta Obstétrica
-- Cambiar de bebé a mujer embarazada para mejor representación

UPDATE services 
SET icon = 'fas fa-person-pregnant' 
WHERE name = 'Consulta Obstétrica';

-- Verificar el cambio
SELECT name, icon, description 
FROM services 
WHERE name = 'Consulta Obstétrica';

