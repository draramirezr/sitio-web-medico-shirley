# 🎨 SISTEMA DE TEMAS PARA LA PÁGINA PRINCIPAL

**Fecha:** 18 de Enero, 2026  
**Propuesta:** Control de tema desde el panel admin

---

## 🎯 **¿QUÉ ES ESTO?**

Un sistema que te permite **cambiar el tema de la página de inicio** desde el panel administrativo con solo hacer click.

**SIN editar código, SIN desplegar, SIN complicaciones.**

---

## 📋 **ARCHIVOS QUE SE VAN A MODIFICAR:**

| Archivo | Qué se modifica | Líneas aprox. |
|---------|-----------------|---------------|
| `app_simple.py` | Agregar rutas y lógica del tema | +80 líneas |
| `templates/admin.html` | Agregar botón "Configurar Tema" | +5 líneas |
| `templates/admin_configuracion_tema.html` | **NUEVO** - Página del selector | +200 líneas |
| `templates/index.html` | Agregar borde animado condicional | +40 líneas |

**Total:** 4 archivos (3 modificados + 1 nuevo)

---

## 🔧 **CÓMO FUNCIONARÁ:**

### **PASO 1: Base de Datos**

Se creará una tabla nueva:

```sql
CREATE TABLE configuracion_sitio (
    id INTEGER PRIMARY KEY,
    clave VARCHAR(100) UNIQUE,     -- "tema_principal"
    valor VARCHAR(255),             -- "original" o "mes_patria"
    fecha_activacion TIMESTAMP,
    fecha_desactivacion TIMESTAMP,  -- Auto-desactivar después de febrero
    updated_at TIMESTAMP
);
```

**Registro inicial:**
```sql
INSERT INTO configuracion_sitio (clave, valor) 
VALUES ('tema_principal', 'original');
```

---

### **PASO 2: Nueva Ruta en Flask**

```python
@app.route('/admin/configuracion-tema')
@login_required
def admin_configuracion_tema():
    """Página para configurar el tema de la página principal"""
    # Obtener tema actual de la base de datos
    tema_actual = obtener_configuracion('tema_principal')
    return render_template('admin_configuracion_tema.html', 
                         tema_actual=tema_actual)

@app.route('/admin/configuracion-tema/guardar', methods=['POST'])
@login_required
def guardar_configuracion_tema():
    """Guardar el tema seleccionado"""
    nuevo_tema = request.form['tema']
    
    # Validar que sea un tema válido
    if nuevo_tema not in ['original', 'mes_patria']:
        flash('Tema inválido', 'error')
        return redirect(url_for('admin_configuracion_tema'))
    
    # Guardar en base de datos
    actualizar_configuracion('tema_principal', nuevo_tema)
    
    flash(f'✅ Tema actualizado a: {nuevo_tema}', 'success')
    return redirect(url_for('admin_configuracion_tema'))
```

---

### **PASO 3: Modificar Página de Inicio**

En `templates/index.html`, la imagen cambiará según el tema:

**CÓDIGO ACTUAL:**
```html
<div class="hero-image-container">
    <picture>
        <source srcset="{{ url_for('static', filename='images/97472.webp') }}" type="image/webp">
        <img src="{{ url_for('static', filename='images/97472.jpg') }}" 
             alt="Dra. Shirley Ramírez">
    </picture>
</div>
```

**CÓDIGO NUEVO:**
```html
<div class="hero-image-container {% if tema == 'mes_patria' %}with-patriotic-border{% endif %}">
    {% if tema == 'mes_patria' %}
    <!-- Borde animado tricolor -->
    <div class="borde-tricolor-rotante"></div>
    {% endif %}
    
    <picture>
        <source srcset="{{ url_for('static', filename='images/97472.webp') }}" type="image/webp">
        <img src="{{ url_for('static', filename='images/97472.jpg') }}" 
             alt="Dra. Shirley Ramírez">
    </picture>
</div>

{% if tema == 'mes_patria' %}
<style>
    /* Estilos del borde animado - solo se cargan si el tema está activo */
    .borde-tricolor-rotante {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 50%;
        background: conic-gradient(
            #002D62 0deg 120deg,
            white 120deg 180deg,
            #CE1126 180deg 300deg,
            white 300deg 360deg
        );
        z-index: 1;
        animation: rotar 8s linear infinite;
    }
    
    @keyframes rotar {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
</style>
{% endif %}
```

---

### **PASO 4: Agregar Botón en Admin Principal**

En `templates/admin.html`, se agregará un nuevo botón:

```html
<a href="{{ url_for('admin_configuracion_tema') }}" class="menu-item">
    <i class="fas fa-palette"></i> 
    🇩🇴 Configuración de Tema
</a>
```

---

## 🎬 **FLUJO COMPLETO DE USO:**

```
┌────────────────────────────────────────────┐
│ 1. LOGIN en /admin                         │
│    Usuario: dra.ramirezr@gmail.com         │
│    Password: ********                      │
└─────────────────┬──────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│ 2. PANEL ADMIN                             │
│    [📅 Citas]                              │
│    [📧 Mensajes]                           │
│    [💰 Facturación]                        │
│    [🎨 Configuración de Tema] ← NUEVO      │
└─────────────────┬──────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│ 3. SELECTOR DE TEMA                        │
│    Tema Actual: ✅ Diseño Original         │
│                                            │
│    ○ Diseño Original                       │
│    ● Mes de la Patria 🇩🇴                  │
│                                            │
│    [👁️ Vista Previa]                       │
│    [💾 Guardar Cambios]                    │
└─────────────────┬──────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│ 4. CONFIRMACIÓN                            │
│    ✅ Tema actualizado exitosamente        │
│                                            │
│    Los visitantes ahora verán:            │
│    🇩🇴 Borde animado tricolor              │
└─────────────────┬──────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│ 5. PÁGINA DE INICIO (www.draramirez.com)  │
│    [Foto con borde animado 🇩🇴]            │
│    Girando con colores de la bandera      │
└────────────────────────────────────────────┘
```

---

## ⏰ **DESACTIVACIÓN AUTOMÁTICA:**

El sistema detectará automáticamente cuando llegue Marzo:

```python
# En la ruta de index
def index():
    # Obtener tema configurado
    tema = obtener_configuracion('tema_principal')
    
    # Si es Mes de la Patria pero ya pasó febrero, volver a original
    if tema == 'mes_patria' and datetime.now().month > 2:
        actualizar_configuracion('tema_principal', 'original')
        tema = 'original'
    
    return render_template('index.html', tema=tema, ...)
```

**Resultado:**
- ✅ Del 1 al 28 de Febrero: Muestra borde animado
- ✅ Desde 1 de Marzo: Vuelve automáticamente al diseño original

---

## 📊 **VENTAJAS DEL SISTEMA:**

| Ventaja | Descripción |
|---------|-------------|
| **🎛️ Control Total** | Activa/desactiva con 1 click |
| **⚡ Instantáneo** | Sin necesidad de desplegar código |
| **🔄 Reversible** | Vuelve al original cuando quieras |
| **📅 Automático** | Se desactiva solo después de febrero |
| **🔮 Expandible** | Puedes agregar más temas en el futuro |
| **👥 Multi-usuario** | Todos los admins pueden cambiar el tema |
| **📱 Responsive** | Funciona en móvil, tablet y desktop |

---

## 🚀 **TEMAS FUTUROS POSIBLES:**

Una vez implementado, podrás agregar más temas:

```
✅ Diseño Original (siempre disponible)
🇩🇴 Mes de la Patria (Febrero)
🎄 Navidad (Diciembre)
🌸 Día de la Mujer (Marzo)
💖 Día de las Madres (Mayo)
🎃 Halloween (Octubre) - opcional
🎉 Aniversario del Consultorio
```

**Todos desde el mismo panel admin, sin tocar código.**

---

## 📝 **ARCHIVOS QUE CREARÉ:**

### **1. app_simple.py** (Modificar)
```python
# Línea ~7350: Agregar estas funciones

def obtener_configuracion(clave):
    """Obtener valor de configuración"""
    conn = get_db_connection()
    config = conn.execute(
        'SELECT valor FROM configuracion_sitio WHERE clave = %s',
        (clave,)
    ).fetchone()
    conn.close()
    return config['valor'] if config else 'original'

def actualizar_configuracion(clave, valor):
    """Actualizar configuración"""
    conn = get_db_connection()
    # Usar INSERT ... ON DUPLICATE KEY UPDATE
    conn.execute('''
        INSERT INTO configuracion_sitio (clave, valor, updated_at) 
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        ON DUPLICATE KEY UPDATE 
            valor = %s, 
            updated_at = CURRENT_TIMESTAMP
    ''', (clave, valor, valor))
    conn.commit()
    conn.close()

# Modificar la ruta index para pasar el tema
@app.route('/')
def index():
    tema = obtener_configuracion('tema_principal')
    
    # Auto-desactivar después de febrero
    if tema == 'mes_patria' and datetime.now().month > 2:
        actualizar_configuracion('tema_principal', 'original')
        tema = 'original'
    
    # ... resto del código
    return render_template('index.html', 
                         tema=tema,  # ← NUEVO
                         services=services)
```

### **2. templates/admin.html** (Modificar)
```html
<!-- Agregar después de "Gestión de Usuarios" -->
<a href="{{ url_for('admin_configuracion_tema') }}" class="menu-item">
    <i class="fas fa-palette"></i> 
    🇩🇴 Configuración de Tema
</a>
```

### **3. templates/admin_configuracion_tema.html** (NUEVO)
- Página completa con selector de tema
- Vista previa de cada opción
- Botón guardar
- Indicador de tema actual

### **4. templates/index.html** (Modificar)
```html
<!-- Modificar la sección hero-image-container -->
<div class="hero-image-container {% if tema == 'mes_patria' %}with-patriotic-border{% endif %}">
    {% if tema == 'mes_patria' %}
    <div class="borde-tricolor-rotante"></div>
    {% endif %}
    
    <!-- Imagen normal (sin cambios) -->
    <picture>...</picture>
</div>
```

---

## 🎓 **VENTAJAS vs MODIFICAR MANUALMENTE:**

| Aspecto | Manual (Actual) | Con Sistema de Temas |
|---------|-----------------|----------------------|
| **Cambiar tema** | Editar código + Git push | 1 click en admin |
| **Tiempo** | 10 minutos | 5 segundos |
| **Conocimiento técnico** | Alto (Git, Flask, HTML) | Ninguno (solo click) |
| **Reversión** | Editar código de nuevo | 1 click |
| **Programar activación** | Manual (recordar fecha) | Automático |
| **Múltiples temas** | Complicado | Fácil (solo agregar opciones) |

---

## 📂 **ARCHIVOS DEMO PARA VER:**

1. **`DEMO_ADMIN_SELECTOR_TEMA.html`**
   - Abre este archivo para ver el selector en el admin
   - Prueba hacer click en las opciones
   - Ve cómo cambia el preview

2. **`DEMO_PROPUESTA_BORDE_ANIMADO.html`**
   - Ya lo tienes - muestra cómo se verá la página con el tema

---

## ✅ **SI QUIERES QUE LO IMPLEMENTE:**

Te crearé **PRIMERO** una versión completa del código en un archivo separado para que lo revises ANTES de aplicarlo.

---

## 🎯 **RESUMEN EJECUTIVO:**

```
┌─────────────────────────────────────────┐
│ ACTUAL (Manual):                        │
│ Quiero cambiar tema → Editar código     │
│ → Git add/commit/push → Esperar 3 min   │
│                                         │
│ CON SISTEMA:                            │
│ Quiero cambiar tema → Login admin       │
│ → Click en tema → Guardar → ¡Listo!    │
│ (5 segundos)                            │
└─────────────────────────────────────────┘
```

---

## ❓ **¿QUIERES QUE LO IMPLEMENTE?**

Dime:
- ✅ ¿Te gusta la idea?
- ✅ ¿Quieres que lo implemente?
- ✅ ¿Algún ajuste antes de empezar?

**Si dices que sí, te mostraré el código COMPLETO antes de aplicarlo.**

---

**Abre primero:** `DEMO_ADMIN_SELECTOR_TEMA.html` para ver cómo se verá el selector en el admin.

