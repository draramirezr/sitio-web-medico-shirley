# 🔧 FIX: Rate Limit en Formularios

## ❌ PROBLEMA ANTERIOR:

Los formularios de contacto y citas tenían rate limiting aplicado a **TODAS las peticiones** (GET + POST):
- `/contacto`: 5 requests totales por 5 minutos
- `/solicitar-cita`: 3 requests totales por 5 minutos

**Esto bloqueaba a los usuarios** al simplemente:
- Recargar la página
- Navegar entre páginas
- Ver el formulario sin enviarlo

---

## ✅ SOLUCIÓN IMPLEMENTADA:

### 1. Rate Limit SOLO para POST (envío de formulario)

**Antes:**
```python
@app.route('/contacto', methods=['GET', 'POST'])
@rate_limit(max_requests=5, window=300)  # ❌ Afecta GET y POST
def contact():
    ...
```

**Ahora:**
```python
@app.route('/contacto', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # ✅ Rate limit SOLO aquí (envío real)
        client_ip = request.remote_addr
        ...
```

### 2. Límites Ajustados

| Ruta | Método | Límite Anterior | Límite Nuevo |
|------|--------|----------------|--------------|
| `/contacto` | GET | 5 / 5 min | ∞ (sin límite) |
| `/contacto` | POST | 5 / 5 min | 5 / 5 min ✅ |
| `/solicitar-cita` | GET | 3 / 5 min | ∞ (sin límite) |
| `/solicitar-cita` | POST | 3 / 5 min | 3 / 5 min ✅ |

### 3. Mensajes de Error Amigables

**Antes:**
```json
{"error": "Rate limit exceeded"}  // ❌ JSON en página HTML
```

**Ahora:**
```python
flash('⚠️ Has enviado demasiados mensajes. Por favor espera 5 minutos.', 'warning')
```

---

## 🎯 BENEFICIOS:

1. ✅ Los usuarios pueden **ver el formulario** sin límites
2. ✅ Solo se aplica rate limit al **enviar** (POST)
3. ✅ Mensajes de error más amigables (flash messages)
4. ✅ Rate limiting por IP con sufijos únicos (`_contact`, `_appointment`)
5. ✅ Protección contra spam sigue activa

---

## 📝 ARCHIVOS MODIFICADOS:

- `app_simple.py`:
  - Líneas 1625-1649: `/contacto` - Rate limit solo POST
  - Líneas 1705-1729: `/solicitar-cita` - Rate limit solo POST

---

## 🧪 PRUEBAS:

1. **Ver formulario múltiples veces:** ✅ Sin bloqueo
2. **Enviar formulario 5 veces rápido:** ✅ Bloquea en el 6to intento
3. **Esperar 5 minutos:** ✅ Se resetea el límite
4. **Mensaje de error:** ✅ Flash message visible en el navegador

---

**Fecha:** 23 de Octubre 2025  
**Commit:** Próximo deploy





