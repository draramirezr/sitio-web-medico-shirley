# 🚀 Guía Rápida - Sistema de Usuarios

## 👤 Acceso al Sistema

### Usuario por Defecto Creado

```
📧 Email: ing.fpaula@gmail.com
👤 Nombre: Francisco Paula
🔒 Contraseña: 2416Xpos@
🔑 Perfil: Administrador (Acceso Total)
```

## 🌐 URLs Importantes

| Función | URL | Descripción |
|---------|-----|-------------|
| 🏠 Inicio | `http://localhost:5000/` | Página principal del sitio |
| 🔐 Login | `http://localhost:5000/login` | Iniciar sesión |
| 🔓 Logout | `http://localhost:5000/logout` | Cerrar sesión |
| 📊 Panel Admin | `http://localhost:5000/admin` | Panel administrativo principal |
| 👥 Gestión Usuarios | `http://localhost:5000/admin/usuarios` | Administrar usuarios |
| 📝 Facturación | `http://localhost:5000/facturacion` | Sistema de facturación |
| 🔄 Recuperar Contraseña | `http://localhost:5000/solicitar-recuperacion` | Recuperar contraseña |

## 📋 Pasos para Comenzar

### 1️⃣ Iniciar la Aplicación

```bash
py app_simple.py
```

### 2️⃣ Acceder al Login

Abre tu navegador y ve a: `http://localhost:5000/login`

### 3️⃣ Iniciar Sesión

Usa las credenciales del usuario por defecto:
- Email: `ing.fpaula@gmail.com`
- Contraseña: `2416Xpos@`

### 4️⃣ Explorar el Panel

Una vez dentro, tendrás acceso a:
- 📊 Dashboard principal
- 👥 Gestión de usuarios
- 📝 Sistema de facturación
- 📅 Citas
- 📧 Mensajes

### 5️⃣ Crear Más Usuarios (Opcional)

1. Ve a: `http://localhost:5000/admin/usuarios`
2. Haz clic en "➕ Nuevo Usuario"
3. Completa el formulario:
   - Nombre completo
   - Email (será el usuario de login)
   - Contraseña (mínimo 8 caracteres)
   - Perfil (Administrador o Registro de Facturas)
4. Guarda los cambios

## 🔑 Perfiles de Usuario

### Administrador
- ✅ Acceso total al sistema
- ✅ Puede gestionar usuarios
- ✅ Acceso a facturación
- ✅ Acceso a todos los módulos

### Registro de Facturas
- ✅ Acceso al módulo de facturación
- ❌ No puede gestionar usuarios
- ❌ Acceso limitado a otros módulos

## 🔒 Seguridad

### ✅ Medidas Implementadas
- Contraseñas encriptadas
- Sesiones seguras con Flask-Login
- Recuperación de contraseña por email
- Validación de permisos por perfil
- Protección contra auto-eliminación

### ⚠️ Recomendaciones
1. **Cambia la contraseña del usuario por defecto**
2. Usa contraseñas fuertes (8+ caracteres, letras, números, símbolos)
3. No compartas tus credenciales
4. Cierra sesión después de usar el panel

## 🆘 Problemas Comunes

### ❌ "No module named 'flask_login'"
**Solución:**
```bash
py -m pip install flask-login
```

### ❌ No puedo iniciar sesión
**Verifica:**
1. Que estás usando el email correcto: `ing.fpaula@gmail.com`
2. Que la contraseña sea exactamente: `2416Xpos@` (con mayúsculas)
3. Que el usuario esté activo en la base de datos

### ❌ No recibo el email de recuperación
**Verifica:**
1. Que tengas configurado el email en `.env`
2. Revisa la carpeta de SPAM
3. Verifica que el email existe en la base de datos

### ❌ Error al acceder a /admin
**Causa:** No has iniciado sesión
**Solución:** Ve a `/login` primero

## 📱 Responsive

El sistema funciona perfectamente en:
- 💻 Computadoras de escritorio
- 💼 Laptops
- 📱 Tablets
- 📲 Teléfonos móviles

## 🎨 Interfaz

Los templates incluyen:
- ✨ Animaciones suaves
- 🎨 Diseño moderno y profesional
- 📊 Indicadores visuales claros
- 🌈 Paleta de colores del sitio
- 📱 Diseño responsive

## 🔄 Flujo de Trabajo Típico

```
1. Usuario abre el navegador
   ↓
2. Va a /login
   ↓
3. Ingresa email y contraseña
   ↓
4. Sistema valida credenciales
   ↓
5. Si es correcto → Redirige a /admin
   ↓
6. Usuario accede a las funciones según su perfil
   ↓
7. Al terminar → Logout
```

## 📞 ¿Necesitas Ayuda?

Si tienes problemas o dudas:
1. Revisa el archivo `SISTEMA_USUARIOS.md` para detalles técnicos
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que la base de datos se haya inicializado correctamente

---

**¡Listo para usar! 🎉**

El sistema de usuarios está completamente funcional y protegiendo tu panel administrativo.

