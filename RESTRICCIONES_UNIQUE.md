# 🔒 Restricciones de Unicidad en Base de Datos

## 📋 Resumen de Cambios

Se han agregado restricciones de unicidad (UNIQUE) a las tablas para garantizar la integridad de datos:

### 1. ✅ Tabla `medicos`
- **Cédula**: Ya tenía UNIQUE ✅
- **Email**: Ahora es UNIQUE ✅
- **Exequátur**: Ahora es UNIQUE ✅

### 2. ✅ Tabla `codigo_ars`
- **Combinación (codigo_ars + ars_id)**: Ahora es UNIQUE ✅
- **Combinación (medico_id + ars_id)**: Mantenida como UNIQUE ✅

---

## 📊 Cambios Realizados

### A. Script SQL (`agregar_restricciones_unique.sql`)

Se creó un script SQL para agregar las restricciones a la base de datos MySQL en Railway:

```sql
-- Agregar UNIQUE a email en tabla medicos
ALTER TABLE medicos ADD UNIQUE KEY unique_email (email);

-- Agregar UNIQUE a exequatur en tabla medicos
ALTER TABLE medicos ADD UNIQUE KEY unique_exequatur (exequatur);

-- Cambiar restricción en codigo_ars
ALTER TABLE codigo_ars DROP INDEX medico_id;
ALTER TABLE codigo_ars ADD UNIQUE KEY unique_codigo_ars (codigo_ars, ars_id);
```

### B. Código de la Aplicación (`app_simple.py`)

Se actualizaron 4 funciones para validar duplicados ANTES de insertar/actualizar:

#### 1. `facturacion_medicos_nuevo()` (Líneas 2448-2476)
```python
# Verificar cédula duplicada
existe = conn.execute('SELECT id FROM medicos WHERE cedula = %s', (cedula,)).fetchone()

# Verificar email duplicado (si se proporciona)
if email:
    existe_email = conn.execute('SELECT id FROM medicos WHERE email = %s', (email,)).fetchone()

# Verificar exequatur duplicado (si se proporciona)
if exequatur:
    existe_exequatur = conn.execute('SELECT id FROM medicos WHERE exequatur = %s', (exequatur,)).fetchone()
```

#### 2. `facturacion_medicos_editar()` (Líneas 2506-2532)
```python
# Verificar cédula duplicada en OTRO médico
existe = conn.execute('SELECT id FROM medicos WHERE cedula = %s AND id != %s', (cedula, medico_id)).fetchone()

# Verificar email duplicado en OTRO médico
if email:
    existe_email = conn.execute('SELECT id FROM medicos WHERE email = %s AND id != %s', (email, medico_id)).fetchone()

# Verificar exequatur duplicado en OTRO médico
if exequatur:
    existe_exequatur = conn.execute('SELECT id FROM medicos WHERE exequatur = %s AND id != %s', (exequatur, medico_id)).fetchone()
```

#### 3. `facturacion_codigo_ars_nuevo()` (Líneas 2609-2628)
```python
# Verificar combinación medico_id + ars_id
existe = conn.execute('SELECT id FROM codigo_ars WHERE medico_id = %s AND ars_id = %s AND activo = 1', 
                     (medico_id, ars_id)).fetchone()

# Verificar combinación codigo_ars + ars_id (NUEVO)
existe_codigo = conn.execute('SELECT id FROM codigo_ars WHERE codigo_ars = %s AND ars_id = %s AND activo = 1', 
                             (codigo_ars, ars_id)).fetchone()
```

#### 4. `facturacion_codigo_ars_editar()` (Líneas 2655-2674)
```python
# Verificar combinación medico_id + ars_id en OTRO registro
existe = conn.execute('SELECT id FROM codigo_ars WHERE medico_id = %s AND ars_id = %s AND id != %s AND activo = 1', 
                     (medico_id, ars_id, codigo_id)).fetchone()

# Verificar combinación codigo_ars + ars_id en OTRO registro (NUEVO)
existe_codigo = conn.execute('SELECT id FROM codigo_ars WHERE codigo_ars = %s AND ars_id = %s AND id != %s AND activo = 1', 
                             (codigo_ars, ars_id, codigo_id)).fetchone()
```

---

## 🚀 Cómo Aplicar los Cambios

### Paso 1: Aplicar el Script SQL en Railway

1. **Acceder a Railway:**
   - Ve a https://railway.app
   - Inicia sesión y selecciona tu proyecto
   - Click en la base de datos MySQL

2. **Abrir la consola de MySQL:**
   - Click en "Data"
   - Click en "Query"

3. **Ejecutar el script:**
   - Copia el contenido de `agregar_restricciones_unique.sql`
   - Pega en la consola de Query
   - Ejecuta sección por sección (selecciona y ejecuta cada bloque)

4. **Verificar cambios:**
   ```sql
   -- Ver índices de la tabla medicos
   SHOW INDEX FROM medicos WHERE Key_name LIKE 'unique%';
   
   -- Ver índices de la tabla codigo_ars
   SHOW INDEX FROM codigo_ars WHERE Key_name LIKE 'unique%';
   ```

### Paso 2: Desplegar el Código Actualizado

El código ya está actualizado en `app_simple.py`. Solo necesitas hacer push:

```bash
git add app_simple.py agregar_restricciones_unique.sql
git commit -m "🔒 Add: Restricciones UNIQUE en médicos y código ARS - Email y exequátur únicos en tabla medicos - Combinación codigo_ars + ars_id única - Validaciones en código para evitar duplicados"
git push origin main
```

---

## ✅ Verificación Post-Despliegue

### 1. Verificar Tabla Médicos

**Probar cédula duplicada:**
1. Crear un médico con cédula "001-0001234-5"
2. Intentar crear otro médico con la misma cédula
3. ✅ Debe mostrar: "Ya existe un médico con esa cédula"

**Probar email duplicado:**
1. Crear un médico con email "doctor@ejemplo.com"
2. Intentar crear otro médico con el mismo email
3. ✅ Debe mostrar: "Ya existe un médico con ese correo electrónico"

**Probar exequátur duplicado:**
1. Crear un médico con exequátur "123456"
2. Intentar crear otro médico con el mismo exequátur
3. ✅ Debe mostrar: "Ya existe un médico con ese exequátur"

### 2. Verificar Tabla Código ARS

**Probar código + ARS duplicado:**
1. Crear código ARS "ABC123" para ARS "Senasa"
2. Intentar crear otro código "ABC123" para la misma ARS "Senasa"
3. ✅ Debe mostrar: "Ya existe ese código para la ARS seleccionada"

**Permitir mismo código en diferente ARS:**
1. Crear código "ABC123" para ARS "Senasa"
2. Crear código "ABC123" para ARS "Humano"
3. ✅ Debe permitirlo (diferente ARS)

---

## 📝 Mensajes de Error al Usuario

### Médicos:
- ❌ "Ya existe un médico con esa cédula"
- ❌ "Ya existe un médico con ese correo electrónico"
- ❌ "Ya existe un médico con ese exequátur"
- ❌ "Ya existe otro médico con esa cédula" (al editar)
- ❌ "Ya existe otro médico con ese correo electrónico" (al editar)
- ❌ "Ya existe otro médico con ese exequátur" (al editar)

### Código ARS:
- ❌ "Ya existe un código para esta combinación de médico y ARS"
- ❌ "Ya existe ese código para la ARS seleccionada"

---

## 🎯 Beneficios

### Integridad de Datos:
- ✅ No habrá médicos duplicados con la misma cédula
- ✅ No habrá médicos duplicados con el mismo email
- ✅ No habrá médicos duplicados con el mismo exequátur
- ✅ No habrá códigos ARS duplicados para la misma ARS

### Experiencia de Usuario:
- ✅ Mensajes claros cuando se intenta duplicar
- ✅ Validación tanto en código como en base de datos (doble protección)
- ✅ Previene errores de facturación y administración

### Seguridad:
- ✅ Garantiza unicidad a nivel de base de datos
- ✅ Previene inyección de duplicados
- ✅ Mantiene consistencia de datos

---

## ⚠️ Notas Importantes

### Antes de Ejecutar el Script SQL:

1. **Verificar duplicados existentes:**
   El script incluye queries para verificar si hay duplicados. Si hay duplicados, debes:
   - Limpiarlos manualmente antes de agregar las restricciones
   - O usar el siguiente comando para encontrarlos:
   ```sql
   -- Buscar emails duplicados
   SELECT email, COUNT(*) FROM medicos WHERE email IS NOT NULL AND email != '' GROUP BY email HAVING COUNT(*) > 1;
   
   -- Buscar exequatur duplicados
   SELECT exequatur, COUNT(*) FROM medicos WHERE exequatur IS NOT NULL AND exequatur != '' GROUP BY exequatur HAVING COUNT(*) > 1;
   
   -- Buscar codigo_ars + ars_id duplicados
   SELECT codigo_ars, ars_id, COUNT(*) FROM codigo_ars GROUP BY codigo_ars, ars_id HAVING COUNT(*) > 1;
   ```

2. **Backup recomendado:**
   Railway hace backups automáticos, pero puedes hacer uno manual antes de ejecutar el script.

3. **Orden de ejecución:**
   - Primero ejecuta las verificaciones
   - Limpia duplicados si los hay
   - Luego agrega las restricciones UNIQUE

---

## 📊 Resumen de Archivos

- ✅ `agregar_restricciones_unique.sql` - Script SQL para Railway
- ✅ `app_simple.py` - Código actualizado con validaciones
- ✅ `RESTRICCIONES_UNIQUE.md` - Este documento

---

**Fecha de implementación:** 2025-10-24  
**Estado:** ✅ Listo para aplicar  
**Prioridad:** Alta (Integridad de datos)



