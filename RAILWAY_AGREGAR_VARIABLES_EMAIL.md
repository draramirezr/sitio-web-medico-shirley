# 📧 GUÍA RÁPIDA: Agregar Variables de Email en Railway

## ⚡ Pasos Rápidos

### 1️⃣ Ir a Railway
1. Abre **Railway.app**
2. Selecciona tu proyecto
3. Click en **"Variables"** o **"Variables de Entorno"**

### 2️⃣ Agregar 3 Nuevas Variables

Agrega EXACTAMENTE estas 3 variables (sin comillas):

| Variable | Valor |
|----------|-------|
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |

### 3️⃣ Verificar las Existentes

Asegúrate que estas 3 ya estén configuradas (sin comillas):

| Variable | Valor |
|----------|-------|
| `EMAIL_USERNAME` | `dra.ramirezr@gmail.com` |
| `EMAIL_PASSWORD` | `nqze lbab meit vprt` |
| `EMAIL_DESTINATARIO` | `dra.ramirezr@gmail.com` |

---

## ✅ Checklist Final

Después de agregar, deberías tener **6 variables en total**:

```
✓ EMAIL_USERNAME=dra.ramirezr@gmail.com
✓ EMAIL_PASSWORD=nqze lbab meit vprt
✓ EMAIL_DESTINATARIO=dra.ramirezr@gmail.com
✓ EMAIL_HOST=smtp.gmail.com
✓ EMAIL_PORT=587
✓ EMAIL_USE_TLS=True
```

---

## 🚀 Hacer el Deploy

Después de configurar las variables en Railway:

```bash
git add app_simple.py env.example
git commit -m "feat: configuración SMTP flexible con variables de entorno"
git push origin main
```

Railway se redeployará automáticamente.

---

## ⚠️ MUY IMPORTANTE

1. **SIN COMILLAS**: No pongas comillas alrededor de los valores
   - ❌ MAL: `"smtp.gmail.com"`
   - ✅ BIEN: `smtp.gmail.com`

2. **EMAIL_PORT es un número**:
   - ❌ MAL: `"587"`
   - ✅ BIEN: `587`

3. **EMAIL_USE_TLS con T mayúscula**:
   - ❌ MAL: `true`
   - ✅ BIEN: `True`

---

## 🧪 Probar Después del Deploy

1. Ve a tu sitio web
2. Completa el formulario de contacto
3. Verifica que el email llegue a `dra.ramirezr@gmail.com`

---

## 🆘 Si Sigue Sin Funcionar

### Opción 1: Revisar Logs de Railway
1. Ve a Railway → Deployments → Logs
2. Busca mensajes de error
3. Comparte los logs conmigo

### Opción 2: Migrar a SendGrid (Más Confiable)
SendGrid es más estable en Railway:

```
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USERNAME=apikey
EMAIL_PASSWORD=[tu_sendgrid_api_key]
EMAIL_USE_TLS=True
```

Registrate gratis en: https://sendgrid.com/

---

**Fecha:** 24 de Octubre, 2025  
**Tiempo estimado:** 5 minutos  
**Estado:** ✅ Listo para implementar



