# Carga Masiva de Pacientes desde Excel

## 📅 Fecha de Implementación
16 de octubre, 2025

## 🎯 Objetivo
Permitir a los médicos cargar múltiples pacientes desde un archivo Excel para agilizar la facturación masiva.

---

## ✅ Funcionalidades Implementadas

### 1. **Descargar Plantilla Excel**
- **Ruta**: `/facturacion/descargar-plantilla-excel`
- **Botón**: "Descargar Plantilla Excel"
- **Descripción**: Genera un archivo Excel con 3 hojas:
  1. **Pacientes**: Plantilla con encabezados y ejemplos
  2. **Servicios Disponibles**: Lista completa de servicios registrados
  3. **Instrucciones**: Guía paso a paso para llenar la plantilla

#### Estructura del Excel:

**Hoja 1: Pacientes**
| NSS | NOMBRE | FECHA | AUTORIZACIÓN | SERVICIO | MONTO |
|-----|--------|-------|--------------|----------|-------|
| 001-234-5678 | JUAN PÉREZ | 2025-10-16 | 12345 | CONSULTA | 500 |

**Hoja 2: Servicios Disponibles**
| SERVICIOS DISPONIBLES | PRECIO BASE |
|----------------------|-------------|
| CONSULTA | RD$ 500.00 |
| ULTRASONIDO | RD$ 800.00 |
| ... | ... |

**Hoja 3: Instrucciones**
- Explicación detallada de cada campo
- Validaciones y reglas
- Recordatorios importantes

---

### 2. **Cargar Excel con Pacientes**
- **Ruta**: `/facturacion/procesar-excel` (POST)
- **Botón**: "Cargar Excel con Pacientes"
- **Descripción**: Procesa el archivo Excel y carga los pacientes automáticamente a la tabla

#### Flujo de Carga:

```
1. Usuario selecciona Médico y ARS (obligatorio)
   ↓
2. Click en "Cargar Excel con Pacientes"
   ↓
3. Selecciona archivo .xlsx o .xls
   ↓
4. Sistema procesa y valida datos
   ↓
5. Pacientes se agregan automáticamente a la tabla
   ↓
6. Usuario revisa y puede editar antes de guardar
```

---

## 🔧 Componentes Técnicos

### Backend (Python/Flask)

#### Librerías Necesarias:
```python
openpyxl==3.1.2  # Manejo de archivos Excel
```

#### Rutas Creadas:

**1. Generar Plantilla Excel**
```python
@app.route('/facturacion/descargar-plantilla-excel')
def descargar_plantilla_excel():
    # Genera Excel con openpyxl
    # Incluye estilos (colores, fuentes, alineación)
    # Hoja 1: Plantilla con ejemplos
    # Hoja 2: Servicios disponibles
    # Hoja 3: Instrucciones
    # Retorna archivo para descarga
```

**2. Procesar Excel Cargado**
```python
@app.route('/facturacion/procesar-excel', methods=['POST'])
def procesar_excel():
    # Recibe archivo Excel
    # Lee hoja "Pacientes"
    # Valida cada fila
    # Convierte fechas y formatos
    # Retorna JSON con pacientes y errores
```

---

### Frontend (JavaScript)

#### Función Principal:
```javascript
async function procesarExcel(input) {
    // 1. Validar Médico y ARS seleccionados
    // 2. Mostrar loading spinner
    // 3. Enviar archivo al servidor vía FormData
    // 4. Procesar respuesta JSON
    // 5. Poblar tabla con pacientes
    // 6. Calcular total
    // 7. Mostrar mensaje de éxito/error
}
```

---

## 📋 Validaciones Implementadas

### ⚡ **VALIDACIONES COMPLETAS DEL BACKEND:**

#### ✅ **Validación 1: Campos Obligatorios**
- NSS y NOMBRE son obligatorios
- Error: `❌ Fila X: NSS y NOMBRE son obligatorios`

#### ✅ **Validación 2: NSS (Solo números y guiones)**
- Regex: `^[0-9\-]+$`
- Válidos: `001-234-5678`, `12345678`, `001-234`
- Inválidos: `ABC123`, `001.234`, `001 234`
- Error: `❌ Fila X: NSS "ABC123" solo debe contener números y guiones`

#### ✅ **Validación 3: NOMBRE (No puede estar vacío)**
- Se convierte automáticamente a mayúsculas
- Error: `❌ Fila X: NOMBRE no puede estar vacío`

#### ✅ **Validación 4: FECHA (Formato válido)**
- Formatos aceptados: `AAAA-MM-DD`, `DD/MM/AAAA`, `DD-MM-AAAA`
- Si es inválida, usa fecha actual como fallback
- Advertencia: `⚠️ Fila X: FECHA "32/13/2025" formato inválido (use AAAA-MM-DD)`

#### ✅ **Validación 5: AUTORIZACIÓN (Solo números y única)**
- Solo acepta dígitos numéricos
- NO puede repetirse en el Excel
- Se eliminan decimales automáticamente
- Errores:
  - `❌ Fila X: AUTORIZACIÓN "ABC" solo debe contener números`
  - `❌ Fila X: AUTORIZACIÓN "12345" está duplicada en el Excel`
  - `❌ Fila X: AUTORIZACIÓN "XYZ" no es un número válido`

#### ✅ **Validación 6: SERVICIO (Sin números)**
- NO puede contener dígitos
- Se convierte automáticamente a mayúsculas
- Si está vacío, usa "CONSULTA" por defecto
- Válidos: `CONSULTA`, `ULTRASONIDO`, `COLPOSCOPIA`
- Inválidos: `CONSULTA1`, `SERVICIO 123`, `ULTRA50NIDO`
- Error: `❌ Fila X: SERVICIO "CONSULTA1" no debe contener números`

#### ✅ **Validación 7: MONTO (Numérico positivo)**
- Debe ser un número válido
- NO puede ser negativo
- Si es negativo, usa 0
- Errores:
  - `❌ Fila X: MONTO "ABC" no es un número válido`
  - `⚠️ Fila X: MONTO no puede ser negativo, usando 0`

---

### 🛡️ **Validación de Duplicados:**
- Se verifica que cada número de AUTORIZACIÓN sea único dentro del Excel
- Si hay duplicados, ambas filas son rechazadas
- El usuario debe corregir el Excel y volverlo a cargar

---

### 📊 **Comportamiento con Errores:**

**Caso 1: Todas las filas válidas**
```
✅ 10 paciente(s) cargado(s) exitosamente
```

**Caso 2: Algunas filas con errores**
```
✅ 7 paciente(s) cargado(s) exitosamente

⚠️ Advertencias (3):
❌ Fila 5: NSS "ABC123" solo debe contener números y guiones
❌ Fila 8: AUTORIZACIÓN "54321" está duplicada en el Excel
⚠️ Fila 12: FECHA "32/13/2025" formato inválido (use AAAA-MM-DD)

ℹ️ Las filas con errores fueron omitidas. 
   Revise los datos y puede agregarlos manualmente.
```

**Caso 3: Todas las filas con errores**
```
❌ No se pudieron cargar pacientes debido a errores de validación

Errores:
❌ Fila 2: NSS "ABC" solo debe contener números y guiones
❌ Fila 3: SERVICIO "CONSULTA1" no debe contener números
❌ Fila 4: AUTORIZACIÓN "12345" está duplicada en el Excel
```

---

### 🎨 **Interfaz de Resultados:**

El sistema muestra un **modal elegante** con:
- ✅ Cantidad de pacientes cargados (verde)
- ⚠️ Lista de advertencias/errores (amarillo)
- 📋 Número de fila con el error
- 💡 Sugerencias para corregir
- 🔘 Botón "Entendido" para cerrar

---

### En el Frontend:
- ✅ Médico y ARS deben estar seleccionados antes de cargar
- ✅ Solo archivos .xlsx o .xls
- ✅ Loading spinner mientras procesa
- ✅ Modal con resultados detallados

---

## 🎨 Interfaz de Usuario

### Sección de Carga Masiva:

```
┌─────────────────────────────────────────────────────┐
│ 📊 Carga Masiva desde Excel                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│ [📥 Descargar Plantilla Excel]  [📤 Cargar Excel] │
│                                                     │
│ ℹ️ Primero seleccione Médico y ARS, luego cargue  │
│    el Excel. Los pacientes se agregarán           │
│    automáticamente a la tabla.                     │
└─────────────────────────────────────────────────────┘
```

**Colores:**
- Fondo: Gradiente rosa claro (#CEB0B7 → #F2E2E6)
- Borde: Rosa (#CEB0B7)
- Botón Descargar: Blanco con borde rosa
- Botón Cargar: Gradiente rosa (#CEB0B7 → #B89BA3)

---

## 📊 Ejemplo de Uso Paso a Paso

### Paso 1: Preparar Plantilla
1. Click en "Descargar Plantilla Excel"
2. Abrir el archivo en Excel
3. Revisar hoja "Servicios Disponibles"
4. Completar hoja "Pacientes" con los datos
5. Eliminar filas de ejemplo
6. Guardar archivo

### Paso 2: Cargar Pacientes
1. En la página web, seleccionar **Médico**
2. Seleccionar **ARS**
3. Click en "Cargar Excel con Pacientes"
4. Seleccionar archivo .xlsx guardado
5. Esperar procesamiento (spinner)
6. Revisar pacientes cargados en la tabla
7. Editar si es necesario
8. Click en "Agregar como Pendientes"

---

## ⚠️ Manejo de Errores

### Errores Comunes y Soluciones:

| Error | Causa | Solución |
|-------|-------|----------|
| "Seleccione primero Médico y ARS" | No se seleccionaron antes de cargar | Seleccionar Médico y ARS primero |
| "Formato Excel inválido" | Archivo no es .xlsx/.xls | Usar archivo Excel válido |
| "Hoja 'Pacientes' no existe" | Se modificó el nombre de la hoja | No renombrar hojas de la plantilla |
| "Fila X: NSS y Nombre obligatorios" | Campos vacíos | Completar todos los campos requeridos |
| "Autorización duplicada" | Misma autorización en dos filas | Cada autorización debe ser única |

---

## 🔄 Proceso de Validación de Autorizaciones

```javascript
// Al cargar desde Excel
for (paciente in pacientes_excel) {
    // Se agregan todos con sus autorizaciones
}

// Luego, al hacer blur en cada campo autorización
function validarAutorizacionUnica(input) {
    // Busca duplicados en toda la tabla
    // Si encuentra duplicado:
    //   - Campo se pone rojo
    //   - Muestra mensaje de error
    //   - Se limpia automáticamente después de 3 segundos
}
```

---

## 📁 Archivos Modificados

### Backend:
1. **`app_simple.py`**:
   - Línea 2394-2509: Ruta `descargar_plantilla_excel()`
   - Línea 2511-2584: Ruta `procesar_excel()`

2. **`requirements.txt`**:
   - Agregado: `openpyxl==3.1.2`

### Frontend:
1. **`templates/facturacion/facturas_form.html`**:
   - Línea 185-207: Sección UI de carga masiva
   - Línea 451-580: Función JavaScript `procesarExcel()`

---

## 🎯 Ventajas del Sistema

### ✅ Eficiencia:
- Carga de **múltiples pacientes** en segundos
- No más entrada manual repetitiva
- Reducción de errores de tipeo

### ✅ Facilidad de Uso:
- Plantilla Excel con ejemplos
- Lista de servicios disponibles incluida
- Instrucciones claras y detalladas

### ✅ Flexibilidad:
- Edición post-carga permitida
- Combinación de carga Excel + manual
- Validaciones en tiempo real

### ✅ Robustez:
- Manejo de errores completo
- Validaciones frontend y backend
- Feedback visual claro (loading, alertas)

---

## 🧪 Casos de Prueba

### Test 1: Descarga de Plantilla
1. Click en "Descargar Plantilla Excel"
2. **Resultado esperado**: Archivo Excel descargado con 3 hojas

### Test 2: Carga Excel Vacío
1. Seleccionar Médico y ARS
2. Cargar plantilla sin datos (solo encabezados)
3. **Resultado esperado**: Error "No contiene datos válidos"

### Test 3: Carga Excel con Datos
1. Seleccionar Médico y ARS
2. Cargar Excel con 5 pacientes
3. **Resultado esperado**: 5 pacientes en la tabla

### Test 4: Autorización Duplicada
1. Cargar Excel con dos pacientes con misma autorización
2. **Resultado esperado**: 
   - Ambos se cargan inicialmente
   - Al hacer blur, se detecta duplicado
   - Campo se marca en rojo

### Test 5: Sin Seleccionar Médico/ARS
1. Intentar cargar Excel sin seleccionar Médico o ARS
2. **Resultado esperado**: Alert "Seleccione primero Médico y ARS"

---

## 💡 Mejoras Futuras (Opcional)

1. **Validación de Servicios**: Advertir si un servicio no existe en la base de datos antes de guardar
2. **Preview antes de agregar**: Mostrar resumen de pacientes antes de agregarlos
3. **Plantilla Personalizada**: Permitir al médico descargar plantilla con sus servicios más usados pre-llenados
4. **Historial de Cargas**: Guardar registro de cuándo y qué se cargó desde Excel
5. **Validación Avanzada**: Verificar NSS contra formatos estándar dominicanos

---

## 📞 Soporte

### Si hay problemas con la carga:
1. Verificar que la plantilla no fue modificada (nombres de columnas/hojas)
2. Revisar que las fechas estén en formato correcto
3. Asegurar que no hay filas completamente vacías en medio de los datos
4. Validar que todos los números de autorización son únicos

---

## ✨ Resumen

### ¿Qué se logró?
✅ Carga masiva de pacientes desde Excel  
✅ Plantilla descargable con servicios y ejemplos  
✅ Validaciones completas frontend y backend  
✅ Interfaz intuitiva y feedback visual  
✅ Manejo robusto de errores  
✅ Integración perfecta con sistema existente  

### ¿Cómo beneficia al usuario?
- **Ahorra tiempo**: 50+ pacientes en minutos vs horas
- **Reduce errores**: Validaciones automáticas
- **Más control**: Revisión antes de guardar
- **Fácil de usar**: Plantilla con guía incluida

**¡Sistema de carga masiva completamente funcional!** 🚀📊✨

