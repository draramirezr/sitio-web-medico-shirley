# 🔒 SEGURIDAD: Invalidación de Sesiones al Cambiar Contraseña

**Fecha:** 26 de octubre de 2025  
**Tipo:** Mejora de seguridad crítica

---

## 🎯 **PROBLEMA**

### **Escenario vulnerable:**

1. **Usuario A** tiene sesión activa en una PC
2. **Admin** le cambia la contraseña a **Usuario A**
3. **Usuario A** sigue navegando con la sesión antigua
4. ❌ **Brecha de seguridad:** Usuario A puede seguir usando el sistema con credenciales comprometidas

**Ejemplo real:**
```
1. Juan está logueado en la PC del trabajo (10:00 AM)
2. Admin le cambia la contraseña porque sospecha que su cuenta fue comprometida (10:05 AM)
3. Juan sigue trabajando normalmente sin enterarse (10:06 AM - 5:00 PM)
4. ❌ La contraseña vieja sigue siendo válida en su sesión activa
```

---

## ✅ **SOLUCIÓN IMPLEMENTADA**

### **Comportamiento nuevo:**

1. **Admin** le cambia la contraseña a **Usuario A**
2. **Sistema** marca `password_temporal = 1` en la BD
3. **Usuario A** hace cualquier petición (click, recargar página)
4. ✅ **Sistema lo redirige** automáticamente a cambiar contraseña
5. **Usuario A** debe usar la nueva contraseña temporal
6. **Usuario A** crea su nueva contraseña personal

---

## 🔧 **CAMBIOS IMPLEMENTADOS**

### **1. Middleware `@app.before_request` (línea 525)**

```python
@app.before_request
def check_password_temporal():
    """Verificar si el usuario tiene contraseña temporal y forzar cambio"""
    # Solo para usuarios autenticados
    if current_user.is_authenticated:
        # Excluir rutas de cambio de contraseña y logout para evitar loops
        if request.endpoint not in ['cambiar_password_obligatorio', 'logout', 'static']:
            # Verificar si tiene password_temporal
            if hasattr(current_user, 'password_temporal') and current_user.password_temporal:
                # Redirigir a cambio de contraseña obligatorio
                session['cambio_password_usuario_id'] = current_user.id
                session['cambio_password_email'] = current_user.email
                return redirect(url_for('cambiar_password_obligatorio'))
```

**¿Qué hace?**
- Se ejecuta **ANTES** de cada petición HTTP
- Verifica si `password_temporal = 1`
- Si es `1` → Redirige a `/cambiar-password-obligatorio`
- Excluye rutas específicas para evitar loops infinitos

---

### **2. User Loader actualizado (línea 497)**

```python
@login_manager.user_loader
def load_user(user_id):
    """Cargar usuario desde la base de datos"""
    cursor.execute('SELECT id, nombre, email, perfil, activo, password_temporal FROM usuarios WHERE id = %s AND activo = 1', (user_id,))
    user_data = cursor.fetchone()
    
    if user_data:
        user = User(...)
        # Guardar flag para verificar en cada petición
        user.password_temporal = user_data.get('password_temporal', 0)  # ← NUEVO
        return user
```

**¿Qué hace?**
- Carga el campo `password_temporal` de la BD
- Lo guarda en el objeto `user`
- Disponible en `current_user.password_temporal`

---

### **3. Logout automático si admin cambia su propia contraseña (línea 5735)**

```python
# Si es el mismo usuario que está editando, cerrar su sesión
if usuario_id == current_user.id:
    conn.commit()
    conn.close()
    logout_user()  # ← Cerrar sesión inmediatamente
    flash('Tu contraseña ha sido cambiada. Inicia sesión con la nueva contraseña temporal.', 'warning')
    return redirect(url_for('login'))
```

**¿Qué hace?**
- Si el admin se cambia su propia contraseña
- Cierra su sesión **inmediatamente**
- Lo redirige al login
- Debe iniciar sesión con la nueva contraseña

---

## 📊 **FLUJO COMPLETO**

### **Caso 1: Admin cambia contraseña de otro usuario**

```
1. Admin va a /admin/usuarios/5/editar
2. Marca "Cambiar contraseña"
3. Genera contraseña temporal: "Abcd1234"
4. Guarda cambios
5. Sistema ejecuta:
   UPDATE usuarios SET password_temporal = 1 WHERE id = 5

6. Usuario 5 está navegando en /admin/dashboard
7. Hace click en cualquier botón
8. Sistema ejecuta @app.before_request
9. Detecta password_temporal = 1
10. Redirige a /cambiar-password-obligatorio
11. Usuario 5 ve: "Debes cambiar tu contraseña temporal"
12. Ingresa contraseña temporal: "Abcd1234"
13. Crea nueva contraseña: "MiPassword2025!"
14. Sistema ejecuta:
    UPDATE usuarios SET password_temporal = 0 WHERE id = 5
15. ✅ Usuario 5 puede continuar con su nueva contraseña
```

---

### **Caso 2: Admin cambia su propia contraseña**

```
1. Admin (ID=1) va a /admin/usuarios/1/editar
2. Marca "Cambiar contraseña"
3. Genera contraseña temporal: "Xyz9876"
4. Guarda cambios
5. Sistema detecta: usuario_id == current_user.id
6. logout_user() ← Cerrar sesión INMEDIATAMENTE
7. Redirige a /login
8. Admin ve: "Tu contraseña ha sido cambiada. Inicia sesión..."
9. Ingresa email + contraseña temporal: "Xyz9876"
10. Sistema detecta password_temporal = 1
11. Redirige a /cambiar-password-obligatorio
12. Admin crea nueva contraseña
13. ✅ Admin puede continuar
```

---

## 🔒 **SEGURIDAD**

### **¿Qué ataques previene?**

1. ✅ **Sesión comprometida:**
   - Si un atacante tiene acceso a la sesión activa
   - Admin cambia contraseña → Atacante pierde acceso

2. ✅ **Contraseña filtrada:**
   - Si la contraseña fue compartida accidentalmente
   - Admin cambia contraseña → Contraseña vieja inútil

3. ✅ **Cuenta comprometida:**
   - Si detectas actividad sospechosa
   - Admin cambia contraseña → Usuario real debe verificar identidad

4. ✅ **Empleado despedido:**
   - Si alguien deja de trabajar
   - Admin cambia contraseña → No puede seguir usando cuenta

---

## 📋 **RUTAS EXCLUIDAS DEL MIDDLEWARE**

```python
if request.endpoint not in ['cambiar_password_obligatorio', 'logout', 'static']:
```

**¿Por qué?**
- `cambiar_password_obligatorio` → Evitar loop infinito
- `logout` → Permitir cerrar sesión sin validar
- `static` → Archivos CSS/JS/imágenes no necesitan validación

---

## 🎯 **CASOS DE USO**

### **Uso 1: Rotación de contraseñas**
```
Admin: "Es política cambiar contraseñas cada 90 días"
- Cambiar contraseña de todos los usuarios
- Cada uno crea su nueva contraseña al iniciar sesión
```

### **Uso 2: Sospecha de brecha de seguridad**
```
Admin: "Creo que la cuenta de Juan fue hackeada"
- Cambiar contraseña de Juan inmediatamente
- Juan pierde acceso a su sesión actual
- Debe usar la contraseña temporal para verificar su identidad
```

### **Uso 3: Usuario olvidó contraseña**
```
Usuario: "No recuerdo mi contraseña"
Admin: "Te generaré una temporal"
- Admin cambia contraseña
- Usuario recibe email con contraseña temporal
- Usuario crea nueva contraseña
```

---

## ⚠️ **IMPORTANTE**

### **¿Qué pasa con sesiones en múltiples dispositivos?**

Flask-Login **NO puede** cerrar sesiones en otros dispositivos automáticamente porque:
- Las sesiones son cookies almacenadas en el navegador del cliente
- El servidor no tiene control directo sobre esas cookies

**Solución implementada:**
- No cerramos la sesión, pero la **invalidamos**
- En la próxima petición del usuario (cualquier click)
- El middleware detecta `password_temporal = 1`
- Y lo redirige a cambiar contraseña

**Resultado:**
- ✅ Usuario no puede continuar con contraseña vieja
- ✅ Debe usar contraseña temporal para verificar identidad
- ✅ Crea nueva contraseña personal

---

## 🚀 **DESPLIEGUE**

```bash
✅ Commit: "SEGURIDAD: Forzar cambio de contraseña e invalidar sesiones"
✅ Push exitoso
✅ Railway desplegando... (2-3 minutos)
```

**Archivos modificados:**
- `app_simple.py` (3 secciones modificadas)

---

## ✅ **VERIFICACIÓN**

### **Test 1: Usuario con sesión activa**

1. Abre 2 navegadores (Chrome y Firefox)
2. Inicia sesión como Usuario A en ambos
3. En Chrome (como admin), cambia la contraseña de Usuario A
4. En Firefox, haz click en cualquier enlace
5. ✅ Debe redirigir a `/cambiar-password-obligatorio`
6. Ingresa contraseña temporal
7. Crea nueva contraseña
8. ✅ Usuario A puede continuar

### **Test 2: Admin cambia su propia contraseña**

1. Inicia sesión como Admin
2. Ve a `/admin/usuarios/<tu_id>/editar`
3. Marca "Cambiar contraseña"
4. Genera contraseña temporal
5. Guarda
6. ✅ Debe cerrar sesión inmediatamente
7. ✅ Debe redirigir a `/login`
8. Inicia sesión con contraseña temporal
9. ✅ Debe pedir cambiar contraseña

---

## 📝 **NOTAS TÉCNICAS**

### **Flask-Login Sessions**
- Las sesiones se almacenan como cookies firmadas
- La cookie contiene el `user_id`
- `user_loader` se llama en cada petición para cargar el usuario
- `before_request` se ejecuta antes de cada ruta

### **Password Temporal Flag**
- `password_temporal = 0` → Contraseña normal
- `password_temporal = 1` → Debe cambiar contraseña

### **Seguridad adicional**
```python
# En cambiar_password_obligatorio
# Verificar que la contraseña temporal sea correcta
if not check_password_hash(user_data['password_hash'], password_temporal):
    flash('La contraseña temporal es incorrecta', 'error')
```

---

## 🎓 **MEJORES PRÁCTICAS**

### **1. Notificar al usuario**
✅ Email enviado con contraseña temporal  
✅ Flash message al cambiar contraseña  
✅ Pantalla clara de "Debes cambiar contraseña"

### **2. Validar contraseña temporal**
✅ Usuario debe ingresar contraseña temporal  
✅ No puede usar contraseña vieja  
✅ Debe crear contraseña nueva (mín. 8 caracteres)

### **3. Auditoría**
📝 Considerar agregar logs:
- Quién cambió la contraseña
- Cuándo se cambió
- IP del admin
- IP del usuario al cambiar

---

**¡MEJORA DE SEGURIDAD DESPLEGADA!** 🔒

**Resultado:** Sesiones activas se invalidan cuando un admin cambia la contraseña de un usuario, forzando el uso de la contraseña temporal.



