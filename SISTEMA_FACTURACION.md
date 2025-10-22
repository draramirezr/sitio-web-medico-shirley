# 🧾 SISTEMA DE FACTURACIÓN - DRA. SHIRLEY RAMÍREZ

## 📅 Fecha de Implementación: Octubre 2025

---

## ✅ ESTADO: COMPLETADO (Fase 1 - Maestras)

Se han implementado exitosamente las **4 maestras fundamentales** del sistema de facturación. Listo para cargar datos y generar facturas.

---

## 🎯 OBJETIVO DEL SISTEMA

Crear un sistema de facturación completo para el consultorio médico que permita:
- Gestionar ARS (Administradoras de Riesgos de Salud)
- Registrar médicos del consultorio
- Asignar códigos ARS por médico
- Catálogo de servicios médicos
- **Próximamente:** Generar facturas como la adjuntada

---

## 🗄️ BASE DE DATOS

### Tablas Creadas:

#### 1. **`ars`** - Administradoras de Riesgos de Salud
```sql
- id (INTEGER, AUTO) - Identificador único
- nombre_ars (TEXT) - Nombre del ARS (ej: ARS UNIVERSAL)
- rnc (TEXT) - RNC del ARS (ej: 124-00560-4)
- activo (BOOLEAN) - Registro activo/inactivo
- created_at (TIMESTAMP) - Fecha de creación
```

#### 2. **`medicos`** - Registro de Médicos
```sql
- id (INTEGER, AUTO) - Identificador único
- nombre (TEXT) - Nombre completo del médico
- especialidad (TEXT) - Especialidad médica
- cedula (TEXT, UNIQUE) - Cédula del médico
- activo (BOOLEAN) - Registro activo/inactivo
- created_at (TIMESTAMP) - Fecha de creación
```

#### 3. **`codigo_ars`** - Códigos de Médicos por ARS
```sql
- id (INTEGER, AUTO) - Identificador único
- medico_id (INTEGER, FK) - Referencia al médico
- ars_id (INTEGER, FK) - Referencia al ARS
- codigo_ars (TEXT) - Código único del médico en ese ARS
- activo (BOOLEAN) - Registro activo/inactivo
- created_at (TIMESTAMP) - Fecha de creación
- UNIQUE(medico_id, ars_id) - Un código por médico/ARS
```

#### 4. **`tipos_servicios`** - Catálogo de Servicios
```sql
- id (INTEGER, AUTO) - Identificador único
- descripcion (TEXT) - Descripción del servicio
- precio_base (REAL) - Precio de referencia
- activo (BOOLEAN) - Registro activo/inactivo
- created_at (TIMESTAMP) - Fecha de creación
```

---

## 🚀 FUNCIONALIDADES IMPLEMENTADAS

### **1. Menú Principal de Facturación** (`/facturacion`)
- Dashboard con 4 tarjetas para acceder a cada maestra
- Diseño moderno con la paleta de colores de la marca
- Iconos de marca como watermarks
- Botón de "Volver al Panel Admin"

---

### **2. Maestra de ARS** (`/facturacion/ars`)

#### ✅ Funcionalidades:
- **Listar** todos los ARS activos
- **Buscar** por nombre o RNC
- **Crear** nuevo ARS
- **Editar** ARS existente
- **Eliminar** (soft delete con validación)

#### 🛡️ Validaciones:
- No se puede eliminar un ARS si tiene códigos asociados
- Formularios con validación de campos requeridos
- Mensajes de éxito/error con Flash

#### 📄 Rutas:
- `GET /facturacion/ars` - Lista
- `GET/POST /facturacion/ars/nuevo` - Crear
- `GET/POST /facturacion/ars/<id>/editar` - Editar
- `POST /facturacion/ars/<id>/eliminar` - Eliminar

---

### **3. Maestra de Médicos** (`/facturacion/medicos`)

#### ✅ Funcionalidades:
- **Listar** todos los médicos activos
- **Buscar** por nombre, cédula o especialidad
- **Crear** nuevo médico
- **Editar** médico existente
- **Eliminar** (soft delete con validación)

#### 🛡️ Validaciones:
- Cédula única (no puede repetirse)
- No se puede eliminar un médico si tiene códigos ARS
- Formularios con validación de campos requeridos

#### 📄 Rutas:
- `GET /facturacion/medicos` - Lista
- `GET/POST /facturacion/medicos/nuevo` - Crear
- `GET/POST /facturacion/medicos/<id>/editar` - Editar
- `POST /facturacion/medicos/<id>/eliminar` - Eliminar

---

### **4. Maestra de Código ARS** (`/facturacion/codigo-ars`)

#### ✅ Funcionalidades:
- **Listar** todos los códigos activos (con JOIN de médicos y ARS)
- **Buscar** por médico, ARS o código
- **Crear** nuevo código (selects de médicos y ARS)
- **Editar** código existente
- **Eliminar** (soft delete)

#### 🛡️ Validaciones:
- Un médico solo puede tener UN código por ARS
- Validación de combinación única médico-ars
- Mensajes informativos si no hay médicos o ARS
- Enlaces para crear médicos/ARS desde el formulario

#### 📄 Rutas:
- `GET /facturacion/codigo-ars` - Lista
- `GET/POST /facturacion/codigo-ars/nuevo` - Crear
- `GET/POST /facturacion/codigo-ars/<id>/editar` - Editar
- `POST /facturacion/codigo-ars/<id>/eliminar` - Eliminar

---

### **5. Maestra de Tipos de Servicios** (`/facturacion/servicios`)

#### ✅ Funcionalidades:
- **Listar** todos los servicios activos
- **Buscar** por descripción
- **Crear** nuevo servicio
- **Editar** servicio existente
- **Eliminar** (soft delete)

#### 💰 Características:
- Campo de precio base (opcional)
- Formato de moneda con separadores de miles
- Descripción de hasta 200 caracteres

#### 📄 Rutas:
- `GET /facturacion/servicios` - Lista
- `GET/POST /facturacion/servicios/nuevo` - Crear
- `GET/POST /facturacion/servicios/<id>/editar` - Editar
- `POST /facturacion/servicios/<id>/eliminar` - Eliminar

---

## 🎨 DISEÑO Y UX

### Paleta de Colores Utilizada:
- ✅ **Silver Pink** (#CEB0B7) - Color principal
- ✅ **Piggy Pink** (#F2E2E6) - Fondos suaves
- ✅ **Silver Chalice** (#ACACAD) - Textos
- ✅ **Gradientes** de la marca

### Elementos de Diseño:
✅ Cards con hover effects  
✅ Botones con gradientes  
✅ Tablas modernas con headers degradados  
✅ Iconos de Font Awesome  
✅ Watermarks del icono de marca  
✅ Animaciones suaves (fadeInUp)  
✅ Badges con estilos personalizados  
✅ Formularios con bordes redondeados  
✅ Mensajes Flash para feedback  

---

## 📂 ESTRUCTURA DE ARCHIVOS CREADOS

### Backend (Python/Flask):
```
app_simple.py
├── Tablas de base de datos (init_db)
├── Ruta: /facturacion (menú)
├── Rutas: /facturacion/ars (CRUD)
├── Rutas: /facturacion/medicos (CRUD)
├── Rutas: /facturacion/codigo-ars (CRUD)
└── Rutas: /facturacion/servicios (CRUD)
```

### Frontend (Templates):
```
templates/facturacion/
├── menu.html (Dashboard principal)
├── ars.html (Lista de ARS)
├── ars_form.html (Formulario ARS)
├── medicos.html (Lista de Médicos)
├── medicos_form.html (Formulario Médicos)
├── codigo_ars.html (Lista de Códigos)
├── codigo_ars_form.html (Formulario Códigos)
├── servicios.html (Lista de Servicios)
└── servicios_form.html (Formulario Servicios)
```

### Panel Admin:
```
templates/admin.html
└── Botón "Facturación" agregado (verde, destacado)
```

---

## 🔐 SEGURIDAD IMPLEMENTADA

✅ **Sanitización de inputs** (sanitize_input)  
✅ **Validación de campos requeridos**  
✅ **Soft delete** (no se eliminan físicamente los registros)  
✅ **Validación de relaciones** (no se puede eliminar si hay dependencias)  
✅ **Unique constraints** en base de datos  
✅ **Mensajes de confirmación** antes de eliminar  

---

## 🔄 FLUJO DE TRABAJO COMPLETO

### Para crear una factura (preparación):

1. **Paso 1:** Crear ARS
   - Ir a `/facturacion/ars`
   - Agregar ARS UNIVERSAL (o el que corresponda)
   - Incluir nombre y RNC

2. **Paso 2:** Crear Médico
   - Ir a `/facturacion/medicos`
   - Agregar la Dra. Shirley Ramírez
   - Incluir nombre, especialidad y cédula

3. **Paso 3:** Asignar Código ARS
   - Ir a `/facturacion/codigo-ars`
   - Seleccionar médico y ARS
   - Ingresar código (ej: 10240)

4. **Paso 4:** Crear Servicios
   - Ir a `/facturacion/servicios`
   - Agregar servicios: "consulta", "cesarea", etc.
   - Opcionalmente incluir precio base

5. **Paso 5:** (Próximamente)
   - Generación de facturas completas
   - Impresión de facturas
   - Reporte de facturación

---

## 📊 EJEMPLO DE DATOS A CARGAR

### ARS:
```
Nombre: ARS UNIVERSAL
RNC: 124-00560-4
```

### Médico:
```
Nombre: DRA. SHIRLEY SCARLETT RAMIREZ MONTERO
Especialidad: GINECOLOGO/OBSTETRA
Cédula: 014-0020410-1
```

### Código ARS:
```
Médico: DRA. SHIRLEY SCARLETT RAMIREZ MONTERO
ARS: ARS UNIVERSAL
Código: 10240
```

### Servicios (de la factura adjuntada):
```
1. consulta (Precio: $500)
```

---

## 🎯 PRÓXIMOS PASOS SUGERIDOS

### Fase 2 - Generación de Facturas:
1. Crear tabla `facturas` con campos:
   - Número de factura (NCF)
   - Fecha
   - Cliente/Paciente
   - ARS
   - Médico
   - Total
   
2. Crear tabla `detalle_factura`:
   - Paciente
   - NSS/Contrato
   - Fecha autorización
   - Servicio
   - Precio unitario
   
3. Pantalla de creación de facturas
4. Vista previa de factura (como la imagen adjuntada)
5. Impresión de facturas (PDF)
6. Reportes de facturación

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] Crear tablas en base de datos
- [x] Implementar CRUD de ARS
- [x] Implementar CRUD de Médicos
- [x] Implementar CRUD de Código ARS
- [x] Implementar CRUD de Tipos de Servicios
- [x] Menú principal de facturación
- [x] Botón en panel admin
- [x] Diseño con paleta de la marca
- [x] Validaciones y seguridad
- [x] Mensajes de feedback
- [ ] Generación de facturas (Pendiente)
- [ ] Impresión de facturas (Pendiente)
- [ ] Reportes (Pendiente)

---

## 🚀 CÓMO USAR EL SISTEMA

### 1. Acceder al Panel Admin:
```
http://localhost:5000/admin
```

### 2. Hacer clic en el botón verde "Facturación"

### 3. Desde el menú puedes:
- Gestionar ARS
- Gestionar Médicos
- Asignar Códigos ARS
- Catálogo de Servicios

### 4. Cada maestra tiene:
- Búsqueda
- Botón "Nuevo"
- Tabla con datos
- Botones "Editar" y "Eliminar"

---

## 🎨 CAPTURAS DE PANTALLA

### Menú de Facturación:
- 4 tarjetas grandes con iconos
- Diseño moderno con gradientes
- Watermark del icono de marca

### Listas (Todas las maestras):
- Header con título e iconos
- Barra de búsqueda
- Tabla con datos
- Botones de acción

### Formularios:
- Diseño limpio y moderno
- Campos con iconos
- Validaciones visuales
- Botones de "Guardar" y "Cancelar"

---

## 📞 SOPORTE

Si necesitas modificar o agregar funcionalidades:
1. Las rutas están en `app_simple.py` (líneas 1143-1532)
2. Los templates están en `templates/facturacion/`
3. Las tablas están documentadas en este archivo

---

## 🎉 ESTADO ACTUAL

**✅ SISTEMA DE MAESTRAS COMPLETO Y FUNCIONAL**

Listo para:
- Cargar datos de ARS
- Registrar médicos
- Asignar códigos
- Crear catálogo de servicios
- **Próximo:** Generar facturas

---

**Desarrollado por:** Cursor AI Assistant  
**Para:** Dra. Shirley Ramírez - Ginecóloga y Obstetra  
**Fecha:** Octubre 2025  
**Versión:** 1.0 - Fase 1 (Maestras)

