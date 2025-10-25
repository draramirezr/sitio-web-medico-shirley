# 🔧 GUÍA PASO A PASO: Configurar Variables en Railway

## 🎯 OBJETIVO
Agregar las variables MySQL a tu **APLICACIÓN WEB** (no al servicio MySQL)

---

## 📋 PASO 1: Identificar tu Aplicación Web

1. Ve a **Railway Dashboard**: https://railway.app
2. Abre tu proyecto
3. Verás **DOS servicios**:
   - 🐬 **MySQL** (con logo de MySQL/base de datos)
   - 🌐 **Tu aplicación** (con logo de Python/Flask o sin logo)

4. **Click en TU APLICACIÓN** (la que tiene el código Python)

---

## 📋 PASO 2: Abrir Variables

Una vez dentro de tu aplicación:

1. En el **menú lateral izquierdo**, busca:
   - **"Variables"** o
   - **"Settings"** → luego **"Variables"**

2. Click en **"Variables"**

---

## 📋 PASO 3: Verificar Variables Actuales

**¿Qué deberías ver?**

Si ya configuraste variables antes, verás algo como:
```
SECRET_KEY = clave-secreta-muy-larga...
FLASK_ENV = production
EMAIL_USERNAME = dra.ramirezr@gmail.com
...
```

**❌ Lo que probablemente NO verás (y necesitas agregar):**
```
MYSQL_HOST
MYSQL_USER
MYSQL_PASSWORD
MYSQL_DATABASE
```

---

## 📋 PASO 4: Agregar Variables MySQL

### Opción A: Agregar una por una (RECOMENDADO)

1. Click en **"+ New Variable"** o **"Add Variable"**
2. Aparecerá un formulario con dos campos:
   - **Name** (nombre de la variable)
   - **Value** (valor de la variable)

3. Agrega cada variable **UNA POR UNA**:

#### Variable 1:
```
Name:  MYSQL_HOST
Value: mysql.railway.internal
```
Click **"Add"** o **"Save"**

#### Variable 2:
```
Name:  MYSQL_USER
Value: root
```
Click **"Add"** o **"Save"**

#### Variable 3:
```
Name:  MYSQL_PASSWORD
Value: koLhfNrFtiDBdXOIYCmMSOoOeERGUvsX
```
Click **"Add"** o **"Save"**

#### Variable 4:
```
Name:  MYSQL_DATABASE
Value: railway
```
Click **"Add"** o **"Save"**

---

### Opción B: Editor RAW (si está disponible)

Si ves un botón **"Raw Editor"** o **"Editar como texto"**:

1. Click en **"Raw Editor"**
2. Pega estas líneas **AL FINAL** (sin borrar las existentes):

```
MYSQL_HOST=mysql.railway.internal
MYSQL_USER=root
MYSQL_PASSWORD=koLhfNrFtiDBdXOIYCmMSOoOeERGUvsX
MYSQL_DATABASE=railway
```

3. Click **"Save"** o **"Update Variables"**

---

## 📋 PASO 5: Verificar que se Guardaron

Deberías ver **10 variables en total**:

```
✅ SECRET_KEY = clave-secreta-muy-larga-y-segura-para-produccion-2025
✅ FLASK_ENV = production
✅ EMAIL_USERNAME = dra.ramirezr@gmail.com
✅ EMAIL_PASSWORD = nqze lbab meit vprt
✅ EMAIL_DESTINATARIO = dra.ramirezr@gmail.com
✅ RAILWAY_ENVIRONMENT = 1
✅ MYSQL_HOST = mysql.railway.internal          ← NUEVA
✅ MYSQL_USER = root                            ← NUEVA
✅ MYSQL_PASSWORD = koLhfNrFtiDBdXOIYCmMSOoO... ← NUEVA
✅ MYSQL_DATABASE = railway                     ← NUEVA
```

---

## 📋 PASO 6: Esperar Redeploy Automático

1. Railway detectará el cambio automáticamente
2. Iniciará un nuevo **deployment** (2-3 minutos)
3. Ve a **"Deployments"** para ver el progreso

---

## 📋 PASO 7: Verificar en Logs

Una vez que el deployment termine:

1. Ve a **"Deployments"**
2. Click en el deployment más reciente
3. **Busca estas líneas en los logs:**

```
✅ Configurado para usar MySQL en Railway
   🔌 Conectando a: mysql.railway.internal    ← DEBE DECIR ESTO
   👤 Usuario: root
   📁 Base de datos: railway                   ← DEBE DECIR ESTO
```

**Si aún dice `localhost` o `drashirley`** → Las variables NO se guardaron correctamente

---

## ⚠️ ERRORES COMUNES

### Error 1: Agregaste las variables en el servicio MySQL
**Solución:** Repite los pasos pero asegúrate de estar en **TU APLICACIÓN WEB**

### Error 2: Railway agregó comillas automáticas
**Solución:** No te preocupes, el código las elimina automáticamente

### Error 3: No ves la opción "New Variable"
**Solución:** Busca un botón de **"+"** o **"Add"** cerca del título "Variables"

---

## 🆘 SI NADA FUNCIONA

Copia **TODAS** las variables que veas en tu aplicación y pégalas aquí, así verifico qué falta.

**Formato:**
```
VARIABLE1=valor1
VARIABLE2=valor2
...
```











