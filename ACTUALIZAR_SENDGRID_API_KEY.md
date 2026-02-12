# 📧 ACTUALIZAR SENDGRID_API_KEY EN RAILWAY

**Objetivo:** Corregir error 401 de SendGrid

---

## 🔑 **PASO 1: OBTENER NUEVA API KEY DE SENDGRID**

### **A. Ir a SendGrid:**
```
https://app.sendgrid.com/
```

### **B. Login:**
- Email: dra.ramirezr@gmail.com
- Contraseña: [tu contraseña de SendGrid]

### **C. Crear API Key:**
1. Click en **"Settings"** (menú izquierdo)
2. Click en **"API Keys"**
3. Click en **"Create API Key"**
4. Nombre: `Railway Dra Shirley 2026`
5. Permisos: **"Full Access"** (recomendado)
6. Click en **"Create & View"**
7. **¡IMPORTANTE!** Copia la key INMEDIATAMENTE (solo se muestra una vez)

**Ejemplo de API Key:**
```
SG.xxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

---

## 🚂 **PASO 2: ACTUALIZAR EN RAILWAY**

### **A. Ir a Railway:**
```
https://railway.app/
```

### **B. Seleccionar tu proyecto:**
1. Busca: "sitio-web-medico-shirley" (o el nombre de tu proyecto)
2. Click en el proyecto

### **C. Ir a Variables:**
1. En el menú lateral, click en **"Variables"**
2. O en la pestaña **"Settings"** → **"Variables"**

### **D. Actualizar la variable:**

**OPCIÓN 1: Si la variable YA EXISTE:**
1. Busca: `SENDGRID_API_KEY`
2. Click en el ícono de **lápiz** (editar)
3. **Pega** la nueva API Key
4. Click en **"Update"** o **"Save"**

**OPCIÓN 2: Si NO EXISTE:**
1. Click en **"New Variable"**
2. Variable Name: `SENDGRID_API_KEY`
3. Value: **Pega la API Key** que copiaste
4. Click en **"Add"**

### **E. Redeploy automático:**
Railway **redesplegará automáticamente** cuando cambies una variable.

---

## ⏱️ **PASO 3: VERIFICAR**

### **Espera 2-3 minutos y verifica:**

1. **Ver logs en Railway:**
   - Click en **"Deployments"**
   - Click en el último deployment
   - Click en **"Logs"**
   - Buscar: "✅ Email enviado exitosamente"

2. **Probar en el sistema:**
   - Agregar pacientes pendientes
   - Generar PDF
   - Ver si llega el email ✅

---

## ⚠️ **SI NO TIENES CUENTA DE SENDGRID:**

### **Opción A: Crear cuenta gratis**
```
https://signup.sendgrid.com/
```
- Plan gratuito: 100 emails/día
- Suficiente para tu uso

### **Opción B: Deshabilitar emails temporalmente**

En Railway → Variables:
```
Crear variable:
EMAIL_CONFIGURED = false
```

**Resultado:**
- ❌ No enviará emails
- ✅ Sistema funciona normal
- ✅ PDFs se descargan igual

---

## 🔍 **VERIFICAR VARIABLE ACTUAL:**

En Railway → Variables, busca:
```
SENDGRID_API_KEY = ?
```

¿Qué valor tiene?
- Si empieza con "SG." → Puede estar expirada
- Si está vacía → Necesita crearse
- Si no existe → Necesita agregarse

---

## 📞 **SOPORTE SENDGRID:**

Si tienes problemas:
- Documentación: https://docs.sendgrid.com/
- Crear API Key: https://app.sendgrid.com/settings/api_keys

---

**¿Necesitas ayuda para crear la cuenta de SendGrid o prefieres deshabilitar emails temporalmente?**
