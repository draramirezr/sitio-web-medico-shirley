# 🚀 FLUJO AUTOMÁTICO - ARS Pendientes Clickeables

## 🎯 **CÓMO FUNCIONARÁ:**

### **ANTES (Manual - 6 pasos):**
```
1. Usuario ve "ARS HUMANO" en pendientes
2. Click en "Generar Factura"
3. Seleccionar fecha (HOY)
4. Seleccionar médico
5. Seleccionar ARS HUMANO
6. Seleccionar NCF Crédito Fiscal
7. Agregar pacientes
```

### **AHORA (Automático - 2 pasos):**
```
1. Usuario hace CLICK en "ARS HUMANO" 
   → Se abre facturación PRE-LLENADA:
     ✅ Fecha: 25/01/2026 (hoy)
     ✅ Médico: [El del usuario logueado]
     ✅ ARS: HUMANO (pre-seleccionada)
     ✅ NCF: Crédito Fiscal (automático)
     
2. Solo agregar pacientes y guardar
```

---

## 🎨 **CÓMO SE VERÁ:**

### **Dashboard:**
```
┌─────────────────────────────────────────┐
│ ⚠️ ARS Pendientes por Facturar          │
├─────────────────────────────────────────┤
│ [ARS UNIVERSAL    $15,000.00] ← CLICK   │
│ [HUMANO           $8,500.50]  ← CLICK   │
│ [SENASA           $3,200.00]  ← CLICK   │
└─────────────────────────────────────────┘
```

### **Al hacer click:**
```
Redirige a: /facturacion/generar-factura?ars=2&auto=1

Formulario se abre con:
✅ Fecha: 25/01/2026 (HOY)
✅ Médico: Dra. Shirley Ramírez
✅ ARS: HUMANO (pre-seleccionada y bloqueada)
✅ NCF: Crédito Fiscal (pre-seleccionado)

Si es SENASA:
✅ NCF: Crédito Gubernamental (automático)
```

---

## 🔧 **IMPLEMENTACIÓN TÉCNICA:**

### **1. Dashboard (tarjeta ARS):**
```html
<!-- ANTES -->
<span>ARS UNIVERSAL $15,000.00</span>

<!-- AHORA -->
<a href="/facturacion/generar-factura?ars_id=1&auto=1" class="ars-pendiente-link">
    ARS UNIVERSAL <span class="monto">$15,000.00</span>
</a>
```

### **2. Ruta nueva:**
```python
@app.route('/facturacion/generar-factura')
def generar_factura():
    # Detectar parámetros
    ars_id = request.args.get('ars_id')
    auto = request.args.get('auto')  # '1' si viene de dashboard
    
    if auto == '1' and ars_id:
        # Pre-llenar datos
        fecha_hoy = date.today()
        medico_usuario = obtener_medico_del_usuario()
        ars_seleccionada = ars_id
        
        # Detectar tipo NCF
        ars = obtener_ars(ars_id)
        if 'SENASA' in ars['nombre_ars'].upper():
            tipo_ncf = 'gubernamental'
        else:
            tipo_ncf = 'credito_fiscal'
    
    return render_template('generar_factura.html',
                         fecha_prefill=fecha_hoy,
                         ars_prefill=ars_seleccionada,
                         tipo_ncf_prefill=tipo_ncf)
```

### **3. JavaScript en formulario:**
```javascript
// Si hay parámetros auto=1, pre-llenar y bloquear
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('auto') === '1') {
    // Pre-llenar campos
    document.getElementById('fecha_factura').value = '{{ fecha_prefill }}';
    document.getElementById('ars').value = '{{ ars_prefill }}';
    document.getElementById('ncf_tipo').value = '{{ tipo_ncf_prefill }}';
    
    // Bloquear para que no cambien (opcional)
    document.getElementById('ars').disabled = true;
}
```

---

## 💡 **VENTAJAS:**

- ✅ Ahorra 5 clicks por factura
- ✅ Reduce errores (todo pre-llenado)
- ✅ Flujo más rápido e intuitivo
- ✅ Detección automática SENASA → Gubernamental
- ✅ No rompe flujo actual (sigue funcionando normal)

---

## ⚠️ **CONSIDERACIONES:**

### **¿Qué hacer si el médico no está asociado al usuario?**
- Opción A: Dejar vacío (usuario selecciona)
- Opción B: Usar el primer médico disponible
- Opción C: Mostrar error

### **¿Bloquear campos pre-llenados?**
- Opción A: Sí (no se pueden cambiar ARS/NCF)
- Opción B: No (se pueden cambiar si quieren)

---

## 📝 **¿QUIERES QUE LO IMPLEMENTE?**

Dime:
1. ¿Te gusta la idea?
2. ¿Qué hacer si no hay médico asociado? (A, B o C)
3. ¿Bloquear campos? (A o B)

Y lo implemento completo.

---

**¿Procedemos con esta mejora?** 🚀
