# 🚨 ALERTA DE SEGURIDAD: Credenciales SMTP Expuestas

## ⚠️ PROBLEMA CRÍTICO DETECTADO

GitHub ha detectado que las **credenciales SMTP están expuestas públicamente** en el repositorio.

**Archivo comprometido:** `app_simple.py`  
**Línea problemática:** 
```python
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'nqze lbab meit vprt')
```

**Nivel de riesgo:** 🔴 **CRÍTICO**  
**Estado:** 🔓 **Públicamente expuesto en GitHub**

---

## 🔒 SOLUCIÓN URGENTE (HACER AHORA)

### **PASO 1: Revocar la Contraseña Expuesta** ⚠️

1. Ve a: https://myaccount.google.com/apppasswords
2. Inicia sesión con: `dra.ramirezr@gmail.com`
3. Busca la contraseña de aplicación actual
4. **ELIMÍNALA/REVÓCALA inmediatamente**
5. Esto invalidará la contraseña expuesta (`nqze lbab meit vprt`)

**IMPORTANTE:** Haz esto AHORA para evitar que alguien use tus credenciales.

---

### **PASO 2: Generar Nueva Contraseña de Aplicación**

1. En la misma página (https://myaccount.google.com/apppasswords)
2. Click en **"Crear"** o **"Generar nueva contraseña"**
3. Selecciona:
   - **App:** Correo
   - **Device:** Otro (Personalizado)
   - **Nombre:** "Sitio Web Medico - 2025"
4. Click en **"Generar"**
5. **COPIA la nueva contraseña de 16 caracteres**
6. **Guárdala en un lugar seguro** (no en el código)

---

### **PASO 3: Configurar en Railway**

1. Ve a: https://railway.app/
2. Selecciona tu proyecto
3. Click en **"Variables"**
4. **Actualiza** la variable `EMAIL_PASSWORD` con la nueva contraseña:

```
EMAIL_PASSWORD=[tu_nueva_contraseña_aquí]
```

**IMPORTANTE:** Sin comillas, solo la contraseña.

---

### **PASO 4: Verificar Variables Completas en Railway**

Asegúrate de tener las **6 variables configuradas**:

```
EMAIL_USERNAME=dra.ramirezr@gmail.com
EMAIL_PASSWORD=[tu_nueva_contraseña]
EMAIL_DESTINATARIO=dra.ramirezr@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

---

## ✅ Correcciones Aplicadas al Código

### 1. **Eliminada la Contraseña del Código**

**ANTES (INSEGURO):**
```python
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'nqze lbab meit vprt')
```

**AHORA (SEGURO):**
```python
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Solo desde variables de entorno
```

### 2. **Actualizado env.example**

```
EMAIL_PASSWORD=
```

Ya no incluye contraseñas por defecto.

---

## 🔍 ¿Por Qué Pasó Esto?

### Problema:

El código tenía un "valor por defecto" para desarrollo:
```python
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'nqze lbab meit vprt')
```

Esto significa que si no hay variable de entorno, usa la contraseña hardcodeada.

### Consecuencias:

1. ❌ La contraseña se subió a GitHub
2. ❌ Cualquiera puede verla en el historial
3. ❌ GitHub la detectó como "secreto expuesto"
4. ❌ Tu cuenta de Gmail está en riesgo

---

## 🛡️ Buenas Prácticas de Seguridad

### ✅ **SIEMPRE HACER:**

1. **Nunca** incluir contraseñas, API keys, o secretos en el código
2. **Siempre** usar variables de entorno
3. **Verificar** .gitignore antes de hacer commit
4. **Rotar** credenciales si son expuestas
5. **Usar** contraseñas de aplicación (no contraseña personal)

### ❌ **NUNCA HACER:**

1. Hardcodear contraseñas en el código
2. Subir archivos `.env` a Git
3. Compartir contraseñas por email o chat
4. Usar la misma contraseña en múltiples servicios
5. Ignorar alertas de seguridad de GitHub

---

## 📋 Checklist de Seguridad

Después de aplicar la solución, verifica:

- [ ] Contraseña antigua REVOCADA en Google
- [ ] Nueva contraseña generada
- [ ] Nueva contraseña configurada en Railway
- [ ] Variables de entorno verificadas (6 en total)
- [ ] Código actualizado (sin contraseñas hardcodeadas)
- [ ] Commit y push realizados
- [ ] Railway redeployado
- [ ] Emails funcionando con nueva contraseña
- [ ] Alerta de GitHub resuelta

---

## 🚀 Deploy de la Corrección

```bash
git add app_simple.py env.example
git commit -m "security: eliminar contraseñas expuestas del código"
git push origin main
```

---

## ⚠️ Nota sobre el Historial de Git

**IMPORTANTE:** Aunque eliminamos la contraseña del código actual, **la contraseña antigua todavía existe en el historial de Git**.

### Opciones:

**Opción 1 (Recomendada):** 
- Revocar la contraseña antigua (ya lo hiciste)
- Usar nueva contraseña
- El historial queda pero la contraseña está inválida

**Opción 2 (Avanzada):**
- Limpiar el historial de Git con `git filter-branch`
- **RIESGOSO** - puede romper el repositorio
- **NO recomendado** a menos que sea absolutamente necesario

---

## 🆘 Si Tienes Problemas

### Problema: "Email no se envía después de cambiar contraseña"

**Solución:**
1. Verifica que la nueva contraseña esté en Railway
2. Sin comillas: `EMAIL_PASSWORD=abcd1234efgh5678`
3. Espera 2-3 minutos para el redeploy
4. Revisa los logs de Railway

### Problema: "GitHub sigue mostrando la alerta"

**Solución:**
1. Ve a GitHub → Security → Secret scanning alerts
2. Click en la alerta
3. Click en "Dismiss" o "Mark as resolved"
4. Confirma que la contraseña fue revocada

---

## 📚 Recursos Adicionales

- **Gmail App Passwords:** https://myaccount.google.com/apppasswords
- **GitHub Security:** https://docs.github.com/en/code-security
- **Railway Variables:** https://docs.railway.app/develop/variables
- **Best Practices:** https://12factor.net/config

---

## ✅ Resumen

### Lo Que Pasó:
- ❌ Contraseña hardcodeada en el código
- ❌ Subida a GitHub
- ❌ Detectada por GitHub Security

### Lo Que Hicimos:
- ✅ Eliminamos la contraseña del código
- ✅ Actualizamos env.example
- ✅ Documentamos el problema

### Lo Que DEBES Hacer:
1. ⚠️ **Revocar contraseña antigua en Gmail**
2. ⚠️ **Generar nueva contraseña**
3. ⚠️ **Configurarla en Railway**
4. ✅ Deploy automático

---

**Fecha:** 24 de Octubre, 2025  
**Severidad:** 🔴 CRÍTICA  
**Estado:** ⚠️ REQUIERE ACCIÓN INMEDIATA  
**Tiempo estimado:** 5-10 minutos



