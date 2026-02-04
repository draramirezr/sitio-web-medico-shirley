# 🚀 FEATURE: ARS Pendientes Clickeables - Auto-Fill Facturación

**Fecha:** 25 de Enero, 2026  
**Estado:** ✅ Implementado - Listo para desplegar

---

## 🎯 **QUÉ HACE:**

Permite hacer **click en las ARS pendientes** del dashboard para ir directamente a facturación con **todo pre-llenado**.

---

## ✨ **FLUJO COMPLETO:**

### **ANTES (6 pasos manuales):**
```
1. Ver "ARS HUMANO $8,500" en dashboard
2. Click en "Generar Factura" (menú)
3. Seleccionar fecha manualmente
4. Seleccionar médico manualmente
5. Seleccionar ARS HUMANO manualmente
6. Seleccionar NCF manualmente
7. Agregar pacientes
```

### **AHORA (2 pasos automáticos):**
```
1. Click en "ARS HUMANO $8,500" en dashboard
   ↓
   Se abre formulario PRE-LLENADO con:
   ✅ Fecha: 25/01/2026 (HOY)
   ✅ Médico: Dra. Shirley Ramírez (asociado al usuario)
   ✅ ARS: HUMANO (la que clickeaste)
   ✅ NCF: Crédito Fiscal (detectado automáticamente)
   
2. Solo agregar pacientes y guardar
```

**Ahorro:** 4 pasos = ~30 segundos por factura

---

## 🔧 **IMPLEMENTACIÓN TÉCNICA:**

### **1. Backend (app_simple.py):**

```python
# En facturacion_dashboard():
# Ahora envía ars_id además de nombre y monto
ars_pendientes_detalle = [
    {'id': 1, 'nombre': 'HUMANO', 'monto': 8500.50},
    {'id': 2, 'nombre': 'SENASA', 'monto': 3200.00}
]

# En facturacion_generar():
# Detecta parámetros ?ars_id=X&auto=1
if auto_mode:
    # 1. Buscar médico del usuario (email match)
    # 2. Si NO existe → Usar primer médico
    # 3. Detectar si es SENASA → NCF Gubernamental
    # 4. Otras ARS → NCF Crédito Fiscal
```

### **2. Dashboard (tarjetas clickeables):**

```html
<!-- ANTES -->
<div>ARS HUMANO $8,500</div>

<!-- AHORA -->
<a href="/facturacion/generar-factura?ars_id=2&auto=1">
    <i class="fas fa-external-link-alt"></i> ARS HUMANO $8,500
</a>
```

### **3. Formulario (pre-selección):**

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Si auto_mode = true, pre-seleccionar:
    document.getElementById('ars_id').value = {{ ars_id_prefill }};
    document.getElementById('medico_factura_id').value = {{ medico_id_prefill }};
    document.getElementById('ncf_id').value = {{ ncf_id_prefill }};
});
```

---

## 🎨 **CÓMO SE VE:**

### **Dashboard:**
```
┌─────────────────────────────────────────┐
│ ⚠️ ARS Pendientes por Facturar          │
├─────────────────────────────────────────┤
│ [🔗 ARS UNIVERSAL    $15,000.00] ← HOVER│
│ [🔗 HUMANO           $8,500.50]  ← HOVER│
│ [🔗 SENASA           $3,200.00]  ← HOVER│
└─────────────────────────────────────────┘
```
*Efecto hover: Se ilumina y se mueve ligeramente*

### **Formulario (al hacer click):**
```
┌────────────────────────────────────────────┐
│ ✅ Formulario pre-llenado para: ARS HUMANO │
│ Los campos se pre-llenaron automáticamente │
├────────────────────────────────────────────┤
│ Fecha: [25/01/2026] ✅ Pre-llenada         │
│ Médico: [Dra. Shirley] ✅ Pre-seleccionado │
│ ARS: [HUMANO] ✅ Pre-seleccionada          │
│ NCF: [Crédito Fiscal] ✅ Pre-seleccionado  │
│                                            │
│ [Continuar a Selección de Pacientes]      │
└────────────────────────────────────────────┘
```

---

## ⚙️ **LÓGICA DE MÉDICO:**

```python
Buscar médico con email = current_user.email

SI EXISTE:
    → Usar ese médico ✅
    
SI NO EXISTE:
    → Usar primer médico con factura=1 ✅ (Opción B elegida)
```

---

## 🔍 **LÓGICA DE NCF (Automática):**

```python
Si ARS contiene "SENASA":
    → NCF: Crédito Gubernamental ✅
    
Otras ARS:
    → NCF: Crédito Fiscal ✅
```

---

## 📱 **RESPONSIVE:**

- ✅ Funciona en desktop
- ✅ Funciona en tablet
- ✅ Funciona en móvil (táctil)

---

## ⚠️ **IMPORTANTE:**

### **Campos pre-llenados son EDITABLES:**
- ✅ Usuario puede cambiar cualquier campo
- ✅ No hay bloqueos
- ✅ Total flexibilidad (Opción B elegida)

### **Disponible solo para:**
- ✅ Administrador
- ✅ Nivel 2
- ❌ Registro de Facturas (no ve el dashboard)

---

## 📊 **ARCHIVOS MODIFICADOS (3):**

1. `app_simple.py` - Lógica auto-fill
2. `templates/facturacion/dashboard.html` - Links clickeables
3. `templates/facturacion/generar_factura.html` - Pre-selección

---

## ✅ **VENTAJAS:**

- ⚡ Ahorra ~30 segundos por factura
- ✅ Reduce errores (todo pre-llenado)
- ✅ Flujo más intuitivo
- ✅ Detección automática SENASA
- ✅ Compatible con flujo normal (no rompe nada)

---

**IMPLEMENTACIÓN COMPLETA** ✅
