# 👥 Sistema de Autenticación y Gestión de Usuarios

## 📋 Resumen

Se ha implementado un sistema completo de autenticación y gestión de usuarios para el panel administrativo del sitio web de la Dra. Shirley Ramírez.

## 🔐 Características Implementadas

### 1. **Sistema de Login**
- Inicio de sesión con email y contraseña
- Opción "Recordarme" para mantener la sesión activa
- Protección de todas las rutas administrativas
- Mensajes de error claros y seguros

### 2. **Gestión de Contraseñas**
- Contraseñas encriptadas con hash seguro (Werkzeug)
- Sistema de recuperación de contraseña por email
- Links de recuperación con expiración de 1 hora
- Validación de fortaleza de contraseña

### 3. **Perfiles de Usuario**
Se han definido 2 perfiles de usuario:

#### 🔑 **Administrador**
- Acceso total a todas las funciones del panel
- Puede gestionar usuarios (crear, editar, eliminar)
- Acceso a facturación y todas las secciones

#### 📝 **Registro de Facturas**
- Acceso solo al módulo de facturación
- No puede gestionar usuarios
- Ideal para personal de facturación

### 4. **CRUD de Usuarios**
- **Crear**: Agregar nuevos usuarios con nombre, email, contraseña y perfil
- **Leer**: Listar todos los usuarios con su información
- **Actualizar**: Editar datos de usuarios existentes
- **Eliminar**: Eliminar usuarios (con protecciones)

## 👤 Usuario por Defecto

Al iniciar el sistema por primera vez, se crea automáticamente un usuario administrador:

```
Email: ing.fpaula@gmail.com
Nombre: Francisco Paula
Contraseña: 2416Xpos@
Perfil: Administrador
```

**⚠️ IMPORTANTE:** Por seguridad, se recomienda cambiar la contraseña después del primer inicio de sesión.

## 🚀 Cómo Usar el Sistema

### Iniciar Sesión

1. Navega a: `http://localhost:5000/login`
2. Ingresa tu email y contraseña
3. Opcionalmente, marca "Recordarme" para mantener la sesión
4. Haz clic en "Iniciar Sesión"

### Recuperar Contraseña

1. En la página de login, haz clic en "¿Olvidaste tu contraseña?"
2. Ingresa tu email
3. Recibirás un enlace por email (válido por 1 hora)
4. Haz clic en el enlace y crea tu nueva contraseña

### Gestionar Usuarios (Solo Administradores)

1. Inicia sesión como administrador
2. Ve al panel de administración
3. Haz clic en "Gestión de Usuarios" o navega a `/admin/usuarios`
4. Desde ahí puedes:
   - Ver la lista de todos los usuarios
   - Crear nuevos usuarios
   - Editar usuarios existentes
   - Activar/desactivar usuarios
   - Eliminar usuarios (excepto tu propia cuenta)

### Cerrar Sesión

1. Haz clic en "Cerrar Sesión" en el panel administrativo
2. O navega a: `http://localhost:5000/logout`

## 🔒 Medidas de Seguridad

### Implementadas

✅ **Contraseñas encriptadas** - Nunca se almacenan en texto plano
✅ **Tokens de recuperación** - Links únicos con expiración
✅ **Validación de sesiones** - Flask-Login gestiona las sesiones
✅ **Protección de rutas** - Todas las rutas admin requieren login
✅ **Permisos por perfil** - Control de acceso basado en roles
✅ **Validaciones de entrada** - Sanitización y validación de datos
✅ **Cookies seguras** - HttpOnly, SameSite
✅ **Protecciones contra auto-eliminación** - No puedes eliminar tu propia cuenta

### Recomendaciones Adicionales

🔒 **Para Producción:**
- Cambiar `SECRET_KEY` en variables de entorno
- Activar HTTPS (cambiar `SESSION_COOKIE_SECURE = True`)
- Configurar límites de intentos de login
- Implementar 2FA (autenticación de dos factores)
- Usar una base de datos más robusta (PostgreSQL, MySQL)

## 📁 Archivos Creados/Modificados

### Backend (Python)
- `app_simple.py` - Rutas de autenticación y gestión de usuarios

### Frontend (Templates)
- `templates/login.html` - Página de inicio de sesión
- `templates/solicitar_recuperacion.html` - Solicitar recuperación de contraseña
- `templates/recuperar_contrasena.html` - Restablecer contraseña con token
- `templates/admin_usuarios.html` - Lista de usuarios
- `templates/admin_usuarios_form.html` - Formulario crear/editar usuario

### Base de Datos
- Tabla `usuarios` con los campos:
  - `id` - Identificador único
  - `nombre` - Nombre completo
  - `email` - Email (único) - usado para login
  - `password_hash` - Contraseña encriptada
  - `perfil` - Administrador o Registro de Facturas
  - `activo` - Estado del usuario (activo/inactivo)
  - `token_recuperacion` - Token para recuperar contraseña
  - `token_expiracion` - Fecha de expiración del token
  - `created_at` - Fecha de creación
  - `last_login` - Último inicio de sesión

## 🛠️ Dependencias Instaladas

```bash
Flask-Login==0.6.3
```

Ya instaladas previamente:
- Flask
- Werkzeug (para hash de contraseñas)
- SQLite3 (base de datos)

## 🌐 Rutas Disponibles

### Públicas
- `/login` - Inicio de sesión
- `/logout` - Cerrar sesión
- `/solicitar-recuperacion` - Solicitar recuperación de contraseña
- `/recuperar-contrasena/<token>` - Restablecer contraseña

### Protegidas (requieren login)
- `/admin` - Panel de administración principal
- `/admin/usuarios` - Lista de usuarios
- `/admin/usuarios/nuevo` - Crear nuevo usuario
- `/admin/usuarios/<id>/editar` - Editar usuario
- `/admin/usuarios/<id>/eliminar` - Eliminar usuario
- `/facturacion/*` - Todas las rutas de facturación

## 📧 Configuración de Email

Para que funcione la recuperación de contraseña, necesitas tener configurado el email en el archivo `.env`:

```env
EMAIL_USERNAME=tu-email@gmail.com
EMAIL_PASSWORD=tu-contraseña-de-aplicacion
```

**Nota:** Lee `CONFIGURAR_EMAIL_GMAIL.md` para instrucciones detalladas.

## 🎨 Diseño

Los templates siguen la paleta de colores del sitio:
- **#CEB0B7** - Rosa principal
- **#ACACAD** - Gris
- **#F2E2E6** - Rosa claro
- **#282828** - Gris oscuro

Diseño moderno, responsive y con animaciones suaves.

## ✅ Estado del Proyecto

Todas las funcionalidades de autenticación y gestión de usuarios están **completamente implementadas y funcionando**.

### Funcionalidades Completas:
✅ Sistema de login/logout
✅ Recuperación de contraseña por email
✅ Gestión completa de usuarios (CRUD)
✅ Perfiles de usuario (Administrador, Registro de Facturas)
✅ Protección de rutas administrativas
✅ Templates modernos y responsivos
✅ Validaciones y seguridad

## 🚦 Próximos Pasos (Opcional)

Mejoras futuras que se pueden implementar:
- [ ] Logs de auditoría de accesos
- [ ] Límite de intentos de login
- [ ] Autenticación de dos factores (2FA)
- [ ] Notificaciones por email al crear/modificar usuarios
- [ ] Historial de cambios de contraseña
- [ ] Sesiones simultáneas por usuario

## 📞 Soporte

Si necesitas ayuda o tienes preguntas sobre el sistema de usuarios, contacta al desarrollador del sistema.

---

**Desarrollado para:** Dra. Shirley Ramírez - Ginecóloga y Obstetra
**Fecha:** Octubre 2025
**Versión:** 1.0

