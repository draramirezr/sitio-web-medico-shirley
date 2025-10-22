# 🚀 GUÍA COMPLETA: CREAR REPOSITORIO GIT PARA RAILWAY

## 📋 Paso 1: Instalar Git (si no está instalado)

### Windows:
1. Descargar Git desde: https://git-scm.com/download/win
2. Instalar con configuración por defecto
3. Reiniciar PowerShell/Terminal

### Verificar instalación:
```bash
git --version
```

## 📋 Paso 2: Configurar Git (primera vez)

```bash
# Configurar tu nombre
git config --global user.name "Tu Nombre"

# Configurar tu email
git config --global user.email "tu-email@gmail.com"

# Verificar configuración
git config --list
```

## 📋 Paso 3: Crear Repositorio Local

```bash
# Navegar a tu carpeta del proyecto
cd "Z:\Pagina web shirley"

# Inicializar repositorio Git
git init

# Verificar que se creó
ls -la
# Deberías ver una carpeta .git
```

## 📋 Paso 4: Agregar Archivos al Repositorio

```bash
# Agregar todos los archivos (excepto los del .gitignore)
git add .

# Verificar qué archivos se agregaron
git status

# Hacer el primer commit
git commit -m "Sitio web médico optimizado para Railway - Versión inicial"
```

## 📋 Paso 5: Crear Repositorio en GitHub

### Opción A: Desde GitHub.com
1. Ir a https://github.com
2. Iniciar sesión
3. Click en "New repository"
4. Nombre: `sitio-web-medico-shirley`
5. Descripción: `Sitio web médico de Dra. Shirley Ramírez - Optimizado para Railway`
6. **NO** marcar "Initialize with README"
7. Click "Create repository"

### Opción B: Desde Terminal (si tienes GitHub CLI)
```bash
# Instalar GitHub CLI si no lo tienes
# https://cli.github.com/

# Crear repositorio desde terminal
gh repo create sitio-web-medico-shirley --public --description "Sitio web médico de Dra. Shirley Ramírez"
```

## 📋 Paso 6: Conectar Repositorio Local con GitHub

```bash
# Agregar el repositorio remoto
git remote add origin https://github.com/TU-USUARIO/sitio-web-medico-shirley.git

# Verificar conexión
git remote -v

# Subir código a GitHub
git branch -M main
git push -u origin main
```

## 📋 Paso 7: Verificar en GitHub

1. Ir a tu repositorio en GitHub
2. Verificar que todos los archivos estén ahí
3. Verificar que el .gitignore esté funcionando

## 📋 Paso 8: Conectar con Railway

### Desde Railway Dashboard:
1. Ir a https://railway.app
2. Iniciar sesión
3. Click "New Project"
4. Seleccionar "Deploy from GitHub repo"
5. Conectar tu cuenta de GitHub
6. Seleccionar `sitio-web-medico-shirley`
7. Click "Deploy"

### Configurar Variables de Entorno en Railway:
```env
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-aqui
FLASK_ENV=production
EMAIL_USERNAME=dra.ramirezr@gmail.com
EMAIL_PASSWORD=nqze lbab meit vprt
EMAIL_DESTINATARIO=dra.ramirezr@gmail.com
```

## 🔧 Comandos Git Útiles

### Ver estado del repositorio:
```bash
git status
```

### Ver historial de commits:
```bash
git log --oneline
```

### Hacer cambios y subirlos:
```bash
# Después de hacer cambios
git add .
git commit -m "Descripción del cambio"
git push
```

### Ver diferencias:
```bash
git diff
```

### Crear nueva rama:
```bash
git checkout -b nueva-funcionalidad
```

## 🚨 Solución de Problemas Comunes

### Error: "fatal: not a git repository"
```bash
# Asegúrate de estar en la carpeta correcta
cd "Z:\Pagina web shirley"
git init
```

### Error: "fatal: remote origin already exists"
```bash
# Remover y volver a agregar
git remote remove origin
git remote add origin https://github.com/TU-USUARIO/sitio-web-medico-shirley.git
```

### Error: "fatal: Authentication failed"
```bash
# Usar token de GitHub en lugar de contraseña
# Crear token en: GitHub → Settings → Developer settings → Personal access tokens
git remote set-url origin https://TU-TOKEN@github.com/TU-USUARIO/sitio-web-medico-shirley.git
```

## 📁 Estructura Final del Repositorio

```
sitio-web-medico-shirley/
├── .gitignore
├── .env (NO se sube - está en .gitignore)
├── app_simple.py
├── email_templates.py
├── requirements.txt
├── Procfile
├── railway.env
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── contact.html
│   ├── admin.html
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   ├── robots.txt
│   └── sitemap.xml
└── *.md (documentación)
```

## ✅ Checklist Final

- [ ] Git instalado y configurado
- [ ] Repositorio local inicializado
- [ ] .gitignore creado
- [ ] Primer commit realizado
- [ ] Repositorio creado en GitHub
- [ ] Repositorio local conectado con GitHub
- [ ] Código subido a GitHub
- [ ] Railway conectado con GitHub
- [ ] Variables de entorno configuradas en Railway
- [ ] Sitio web desplegado y funcionando

## 🎯 Resultado Esperado

Al final tendrás:
- ✅ Repositorio Git local funcionando
- ✅ Repositorio en GitHub con todo el código
- ✅ Sitio web desplegado en Railway
- ✅ Dominio personalizado (opcional)
- ✅ SSL habilitado automáticamente

---

**¡Tu sitio web estará online en Railway!** 🚀
