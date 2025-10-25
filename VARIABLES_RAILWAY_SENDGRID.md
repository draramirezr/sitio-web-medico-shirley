# 📧 VARIABLES DE ENTORNO PARA SENDGRID API
**Última actualización:** 25 de Octubre, 2025

---

## ✅ VARIABLES NECESARIAS EN RAILWAY

Con SendGrid API **SOLO necesitas 3 variables**:

### 1️⃣ **SENDGRID_API_KEY** (obligatoria)
```
SENDGRID_API_KEY=SG.tu-api-key-completa-aqui-sin-comillas
```
- **Descripción:** Tu API Key de SendGrid (con permisos "Full Access")
- **Dónde obtenerla:** https://app.sendgrid.com/settings/api_keys
- **Formato:** Debe empezar con `SG.`
- **⚠️ IMPORTANTE:** Pegar SIN comillas

---

### 2️⃣ **EMAIL_FROM** (opcional)
```
EMAIL_FROM=dra.ramirezr@gmail.com
```
- **Descripción:** Email remitente (debe estar verificado en SendGrid)
- **Default:** `dra.ramirezr@gmail.com`
- **⚠️ IMPORTANTE:** Este email debe estar verificado en SendGrid como "Sender"

---

### 3️⃣ **EMAIL_DESTINATARIO** (opcional)
```
EMAIL_DESTINATARIO=dra.ramirezr@gmail.com
```
- **Descripción:** Email donde llegan las notificaciones de contacto/citas
- **Default:** `dra.ramirezr@gmail.com`

---

## ❌ VARIABLES QUE YA NO SE USAN

Estas variables **NO son necesarias** con SendGrid API:

- ~~`EMAIL_USERNAME`~~ ❌ (era para SMTP)
- ~~`EMAIL_PASSWORD`~~ ❌ (ahora usamos `SENDGRID_API_KEY`)
- ~~`EMAIL_HOST`~~ ❌ (era para SMTP)
- ~~`EMAIL_PORT`~~ ❌ (era para SMTP)
- ~~`EMAIL_USE_TLS`~~ ❌ (era para SMTP)
- ~~`EMAIL_USE_SSL`~~ ❌ (era para SMTP)

**Puedes eliminarlas de Railway si existen.**

---

## 🔧 CONFIGURACIÓN EN RAILWAY (Paso a Paso)

### **Paso 1: Ir a Variables de Entorno**
1. Abre tu proyecto en Railway
2. Click en tu servicio
3. Click en "Variables" (pestaña superior)

---

### **Paso 2: Limpiar variables antiguas (opcional)**
Si existen estas variables, **elimínalas**:
- `EMAIL_USERNAME`
- `EMAIL_PASSWORD`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USE_TLS`
- `EMAIL_USE_SSL`

---

### **Paso 3: Agregar/Actualizar variables necesarias**

**3.1 - SENDGRID_API_KEY:**
```
Variable: SENDGRID_API_KEY
Value: SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
⚠️ **SIN comillas**, solo pega la key completa

**3.2 - EMAIL_FROM:**
```
Variable: EMAIL_FROM
Value: dra.ramirezr@gmail.com
```

**3.3 - EMAIL_DESTINATARIO:**
```
Variable: EMAIL_DESTINATARIO
Value: dra.ramirezr@gmail.com
```

---

### **Paso 4: Guardar**
- Click "Add" o "Update"
- Railway reiniciará automáticamente (espera 1-2 minutos)

---

## 🔍 VERIFICAR EN LOGS DE RAILWAY

Después del reinicio, deberías ver en los logs:

✅ **Configuración correcta:**
```
✅ SendGrid API disponible
✅ Email configurado con SendGrid API
   📧 From: dra.ramirezr@gmail.com
   📬 Notificaciones a: dra.ramirezr@gmail.com
   🔑 API Key: SG.6Wmpl...ydM
```

❌ **Error (API Key incorrecta o falta):**
```
⚠️ Email NO configurado - revisa SENDGRID_API_KEY
```

---

## 🧪 PROBAR EMAILS

1. **Espera 1-2 minutos** después de guardar las variables
2. Abre tu sitio en producción
3. Llena el formulario de contacto
4. Envía
5. **Revisa tu email** `dra.ramirezr@gmail.com` en 10-30 segundos

---

## 🔒 SEGURIDAD

✅ **Buenas prácticas:**
- Nunca compartas tu `SENDGRID_API_KEY` públicamente
- No la subas a GitHub
- No la pongas en archivos `.env` que se suban al repo
- Solo configúrala directamente en Railway

---

## 📋 RESUMEN RÁPIDO

**Variables obligatorias:**
```bash
SENDGRID_API_KEY=SG.tu-api-key-sin-comillas
```

**Variables opcionales (tienen defaults):**
```bash
EMAIL_FROM=dra.ramirezr@gmail.com
EMAIL_DESTINATARIO=dra.ramirezr@gmail.com
```

**Variables a eliminar (obsoletas):**
```
EMAIL_USERNAME ❌
EMAIL_PASSWORD ❌
EMAIL_HOST ❌
EMAIL_PORT ❌
EMAIL_USE_TLS ❌
EMAIL_USE_SSL ❌
```

---

## 🆘 TROUBLESHOOTING

### **Error: "UnauthorizedError: 401"**
**Causa:** API Key incorrecta o sin permisos

**Solución:**
1. Genera una **nueva** API Key en SendGrid
2. Asegúrate de darle **"Full Access"**
3. Copia la key **completa** (empieza con `SG.`)
4. Pégala en Railway **sin comillas**

---

### **Error: "Email NO configurado"**
**Causa:** Variable `SENDGRID_API_KEY` no existe o está vacía

**Solución:**
1. Verifica que la variable existe en Railway
2. Verifica que el valor no esté vacío
3. Reinicia el servicio manualmente si es necesario

---

### **Emails no llegan**
**Causa posible:** Email remitente no verificado en SendGrid

**Solución:**
1. Ir a SendGrid → Settings → Sender Authentication
2. Verificar que `dra.ramirezr@gmail.com` está verificado
3. Si no lo está, agrégalo y verifica el email

---

## 📞 CONTACTO

Si tienes problemas, revisa:
1. Logs de Railway (busca errores)
2. SendGrid Activity (ver intentos de envío)
3. Spam folder en tu email

---

**Documentado por:** AI Assistant  
**Última actualización:** 25/10/2025

