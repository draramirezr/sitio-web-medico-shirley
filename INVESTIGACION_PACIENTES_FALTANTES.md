# 🔍 INVESTIGACIÓN: Pacientes Faltantes (10 de 13)

**Fecha:** 26 de octubre de 2025  
**Problema:** Solo se muestran 10 de 13 pacientes pendientes en `/facturacion/generar-factura`  
**Ejemplo específico:** Usuario tiene 2 registros de "Santana Bez" pero solo ve 1

---

## 🎯 HIPÓTESIS PRINCIPAL

**El problema más probable:** El `JOIN medicos m ON fd.medico_consulta = m.id` está **excluyendo** registros donde:

1. ❌ `medico_consulta` es `NULL`
2. ❌ `medico_consulta` tiene un ID que **no existe** en la tabla `medicos`

**Cuando usas `JOIN` (INNER JOIN):**
- Solo devuelve filas donde **AMBAS** tablas tienen coincidencias
- Si `medico_consulta = 999` y ese ID no existe en `medicos` → ❌ Fila excluida

**Cuando usas `LEFT JOIN`:**
- Devuelve **TODAS** las filas de la tabla izquierda (`facturas_detalle`)
- Si no hay coincidencia en `medicos` → Devuelve `NULL` en las columnas de médico

---

## ✅ SOLUCIÓN IMPLEMENTADA

### **1. Cambio de JOIN a LEFT JOIN**

**Antes (error):**
```sql
SELECT fd.*, m.nombre as medico_nombre, a.nombre_ars, ...
FROM facturas_detalle fd
JOIN medicos m ON fd.medico_consulta = m.id  ❌ (excluye si no hay match)
JOIN ars a ON fd.ars_id = a.id
LEFT JOIN pacientes p ON fd.paciente_id = p.id
WHERE fd.estado = 'pendiente' AND fd.activo = 1 AND fd.ars_id = %s
```

**Ahora (correcto):**
```sql
SELECT fd.*, 
       COALESCE(m.nombre, 'Sin médico asignado') as medico_nombre,  ✅
       a.nombre_ars, 
       COALESCE(p.nombre, fd.nombre_paciente) as paciente_nombre_completo
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id  ✅ (incluye todos)
JOIN ars a ON fd.ars_id = a.id
LEFT JOIN pacientes p ON fd.paciente_id = p.id
WHERE fd.estado = 'pendiente' AND fd.activo = 1 AND fd.ars_id = %s
ORDER BY fd.fecha_servicio DESC
```

**Cambios clave:**
- ✅ `JOIN medicos` → `LEFT JOIN medicos`
- ✅ `m.nombre` → `COALESCE(m.nombre, 'Sin médico asignado')`
- ✅ Ahora incluye registros aunque `medico_consulta` sea NULL o inválido

---

### **2. Logging de Depuración**

Agregué logs para ver exactamente cuántos registros se recuperan:

```python
# DEBUG: Registrar cuántos pacientes se encontraron
print(f"\n{'='*60}")
print(f"DEBUG - PACIENTES PENDIENTES ENCONTRADOS")
print(f"{'='*60}")
print(f"ARS ID: {ars_id}")
print(f"Total pacientes: {len(pendientes)}")
print(f"IDs de pacientes: {[p['id'] for p in pendientes]}")
if pendientes:
    print(f"Nombres: {[p['nombre_paciente'] for p in pendientes]}")
print(f"{'='*60}\n")
```

**Esto se verá en los logs de Railway:**
```
============================================================
DEBUG - PACIENTES PENDIENTES ENCONTRADOS
============================================================
ARS ID: 3
Total pacientes: 13  ← ESPERAMOS VER 13 AQUÍ
IDs de pacientes: [123, 124, 125, ...]
Nombres: ['Santana Bez', 'Santana Bez', 'Juan Pérez', ...]
============================================================
```

---

### **3. Query de Médicos También Corregido**

**Antes:**
```sql
SELECT DISTINCT m.id, m.nombre 
FROM facturas_detalle fd
JOIN medicos m ON fd.medico_consulta = m.id  ❌
WHERE fd.estado = 'pendiente' AND fd.ars_id = %s AND fd.activo = 1
```

**Ahora:**
```sql
SELECT DISTINCT m.id, m.nombre 
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id  ✅
WHERE fd.estado = 'pendiente' AND fd.ars_id = %s AND fd.activo = 1 
  AND m.id IS NOT NULL  ← Solo médicos válidos en el dropdown
ORDER BY m.nombre
```

---

## 📋 ARCHIVO DE DIAGNÓSTICO SQL

Creé `DIAGNOSTICO_PACIENTES_FALTANTES.sql` con 10 queries para investigar:

1. ✅ Contar todos los registros pendientes
2. ✅ Verificar registros con `medico_consulta NULL`
3. ✅ Verificar médicos con ID inválido
4. ✅ Listar todos los pacientes
5. ✅ Detectar duplicados (mismo NSS + nombre)
6. ✅ Query exacto que usa el código
7. ✅ Query con LEFT JOIN
8. ✅ Agrupar por ARS
9. ✅ Caso específico: "Santana Bez"
10. ✅ Resumen final de IDs

**Instrucciones para el usuario:**
1. Conectarse a MySQL en Railway
2. Copiar y pegar cada query
3. Comparar resultados con lo que ve en la web

---

## 🔬 POSIBLES CAUSAS RAÍZ

### **Causa #1: medico_consulta NULL**
```sql
-- Detectar:
SELECT COUNT(*) FROM facturas_detalle 
WHERE estado = 'pendiente' AND medico_consulta IS NULL;
```

**Solución:** ✅ LEFT JOIN (ya implementado)

---

### **Causa #2: medico_consulta con ID Inválido**
```sql
-- Detectar:
SELECT fd.id, fd.medico_consulta
FROM facturas_detalle fd
LEFT JOIN medicos m ON fd.medico_consulta = m.id
WHERE fd.estado = 'pendiente' 
  AND fd.medico_consulta IS NOT NULL 
  AND m.id IS NULL;
```

**Ejemplo:**
- `facturas_detalle.medico_consulta = 999`
- Pero `medicos.id = 999` **no existe**
- Con `JOIN` → Registro excluido ❌
- Con `LEFT JOIN` → Registro incluido ✅

**Solución:** ✅ LEFT JOIN (ya implementado)

---

### **Causa #3: Duplicados en Base de Datos**
```sql
-- Detectar:
SELECT nss, nombre_paciente, COUNT(*) as veces
FROM facturas_detalle
WHERE estado = 'pendiente' AND activo = 1
GROUP BY nss, nombre_paciente
HAVING COUNT(*) > 1;
```

**Ejemplo:** 2 registros de "Santana Bez" con mismo NSS
- Si el frontend agrupa por NSS → Solo muestra 1 ❌

**Solución:** No aplica - el template hace `{% for paciente in pendientes %}` sin agrupar

---

## 🧪 ESCENARIOS DE PRUEBA

### **Escenario A: 3 registros con medico_consulta inválido**

**Base de datos:**
```
facturas_detalle:
  - id=1, nombre='Juan',    medico_consulta=1  ← Dra. Shirley (existe) ✅
  - id=2, nombre='María',   medico_consulta=1  ← Dra. Shirley (existe) ✅
  - id=3, nombre='Pedro',   medico_consulta=NULL   ← Sin médico ❌
  - id=4, nombre='Ana',     medico_consulta=999    ← Médico no existe ❌
  - id=5, nombre='Luis',    medico_consulta=888    ← Médico no existe ❌

medicos:
  - id=1, nombre='Dra. Shirley Ramírez'
  - id=2, nombre='Dr. Otro Médico'
  (NO existe id=999, NO existe id=888)
```

**Con JOIN (antes):**
```
Resultado: 2 registros (Juan, María)
Excluidos: 3 registros (Pedro, Ana, Luis)
```

**Con LEFT JOIN (ahora):**
```
Resultado: 5 registros (Juan, María, Pedro, Ana, Luis)
Pedro muestra: "Sin médico asignado"
Ana muestra: "Sin médico asignado"
Luis muestra: "Sin médico asignado"
```

---

### **Escenario B: 2 registros de "Santana Bez"**

**Base de datos:**
```
facturas_detalle:
  - id=10, nss='12345', nombre='Santana Bez', medico_consulta=1
  - id=11, nss='12345', nombre='Santana Bez', medico_consulta=1
```

**Con cualquier query:**
```
Resultado: 2 filas (ambos se muestran)
```

**Si solo se ve 1 en la web:**
- ✅ Backend devuelve 2 → Ver logs
- ❌ Frontend los colapsa → Revisar JavaScript
- ❌ Uno tiene medico_consulta inválido → LEFT JOIN soluciona

---

## 🚀 PRÓXIMOS PASOS

### **1. Desplegar (NO DESPLEGADO AÚN)**
```bash
git add app_simple.py
git commit -m "FIX: Usar LEFT JOIN para incluir todos los pacientes pendientes"
git push origin main
```

### **2. Verificar Logs de Railway**
Buscar:
```
DEBUG - PACIENTES PENDIENTES ENCONTRADOS
Total pacientes: 13  ← ¿Cuántos aparecen realmente?
```

### **3. Ejecutar Diagnóstico SQL**
- Copiar queries de `DIAGNOSTICO_PACIENTES_FALTANTES.sql`
- Ejecutar en Railway MySQL
- Comparar con resultados web

### **4. Caso Específico: Santana Bez**
```sql
SELECT id, nss, nombre_paciente, medico_consulta, estado, activo
FROM facturas_detalle
WHERE nombre_paciente LIKE '%Santana%Bez%'
  AND estado = 'pendiente'
  AND activo = 1;
```

**Debe devolver 2 registros**

---

## 📊 MATRIZ DE DIAGNÓSTICO

| Query devuelve | Web muestra | Diagnóstico |
|----------------|-------------|-------------|
| 13 registros | 13 registros | ✅ **RESUELTO** |
| 13 registros | 10 registros | ❌ Problema en frontend/JavaScript |
| 10 registros | 10 registros | ❌ Problema en query SQL (LEFT JOIN debe corregir) |
| 10 registros | 13 registros | ❌ Imposible (frontend no puede crear datos) |

---

## 🔑 CONCLUSIÓN

**Cambio principal:** `JOIN` → `LEFT JOIN` en la columna `medico_consulta`

**Por qué es crítico:**
- `JOIN` excluye filas sin match
- `LEFT JOIN` incluye todas las filas de `facturas_detalle`
- Los 3 pacientes faltantes probablemente tienen `medico_consulta` NULL o inválido

**Confianza en la solución:** ⭐⭐⭐⭐ (4/5)
- Alta probabilidad de que sea medico_consulta NULL/inválido
- Los logs confirmarán si el query devuelve 13 registros
- El diagnóstico SQL revelará la causa exacta

---

**ESTADO: SOLUCIÓN IMPLEMENTADA - PENDIENTE DE DESPLIEGUE**

*Usuario solicitó no desplegar hasta confirmar que es la solución correcta*



