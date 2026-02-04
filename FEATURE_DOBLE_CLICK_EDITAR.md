# ⚡ FEATURE: Doble Click para Editar Pacientes

**Fecha:** 25 de Enero, 2026  
**Estado:** ✅ Implementado

---

## 🎯 **QUÉ HACE:**

Permite **editar pacientes con doble click** durante la facturación sin perder el progreso.

---

## 💡 **FLUJO COMPLETO:**

```
Usuario en: Paso 2 - Selección de Pacientes
        ↓
Ve tabla con 50 pacientes pendientes
        ↓
DOBLE CLICK en "María González"
        ↓
Se abre: /facturacion/paciente/323/editar
Mensaje: "⚡ Edición Rápida desde Facturación"
        ↓
Edita: NSS, Nombre, Fecha, Servicio, Monto
(ARS bloqueada - no se puede cambiar)
        ↓
Click en "Guardar"
        ↓
Mensaje: "Volviendo a Facturación..."
        ↓
VUELVE a: Paso 2 (exactamente donde estaba)
Con: Misma ARS, NCF, Médico, Fecha
        ↓
Usuario continúa facturando ✅
```

---

## 🔧 **IMPLEMENTACIÓN:**

### **1. Tabla clickeable (generar_factura_step2.html):**
```html
<tr data-paciente-id="{{ paciente.id }}"
    ondblclick="editarPacienteRapido({{ paciente.id }})"
    style="cursor: pointer;"
    title="Doble click para editar">
```

### **2. JavaScript:**
```javascript
function editarPacienteRapido(pacienteId) {
    const url = `/facturacion/paciente/${pacienteId}/editar?from_factura=1&ars_id=X&ncf_id=Y...`;
    window.location.href = url;
}
```

### **3. Backend (app_simple.py):**
```python
# Detectar parámetros
from_factura = request.args.get('from_factura') == '1'

# Después de guardar
if from_factura:
    return render_template('volver_facturacion.html', ...)
```

### **4. Página intermedia (volver_facturacion.html):**
```html
<!-- Muestra spinner "Volviendo a Facturación..." -->
<!-- Auto-submit formulario POST después de 500ms -->
<form method="POST" action="/facturacion/generar-factura">
    <input type="hidden" name="ars_id" value="X">
    ...
</form>
```

---

## ✨ **CARACTERÍSTICAS:**

- ✅ **Doble click** en cualquier paciente
- ✅ **ARS bloqueada** (no se puede cambiar)
- ✅ **Vuelve automáticamente** a facturación
- ✅ **Mantiene estado** (ARS, NCF, Médico, Fecha)
- ✅ **Efecto hover** (fila se ilumina)
- ✅ **Mensaje visual** ("Edición Rápida")
- ✅ **Página de transición** (spinner + auto-redirect)

---

## 📊 **ARCHIVOS MODIFICADOS (4):**

1. `app_simple.py` - Detectar parámetros + redirect inteligente
2. `templates/facturacion/generar_factura_step2.html` - Doble click + estilos + hint
3. `templates/facturacion/paciente_editar.html` - Campos hidden + mensaje
4. `templates/facturacion/volver_facturacion.html` - **NUEVO** - Página transición

---

## 🎨 **EXPERIENCIA DE USUARIO:**

**Antes:**
```
1. Notar error en paciente
2. Salir de facturación
3. Ir a pacientes pendientes
4. Buscar el paciente
5. Editar
6. Volver a facturación
7. Volver a seleccionar TODO (ARS, NCF, Médico, Fecha)
8. Continuar
```
**Tiempo:** ~2 minutos

**Ahora:**
```
1. Doble click en paciente
2. Editar
3. Guardar (vuelve automáticamente)
4. Continuar
```
**Tiempo:** ~20 segundos

**Ahorro:** 1min 40seg por edición ⚡

---

## ⚠️ **NOTAS:**

- Campo **ARS ya bloqueado** implícitamente (no está en formulario edición)
- Usuario puede cambiar: NSS, Nombre, Fecha, Autorización, Servicio, Monto
- **NO** puede cambiar: ARS, Médico Consulta (mantiene integridad)

---

**FEATURE IMPLEMENTADA** ✅
