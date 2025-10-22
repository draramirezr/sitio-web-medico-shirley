# 📧 CONFIGURAR EMAIL PARA RECIBIR NOTIFICACIONES

## 🎯 **OBJETIVO**
Configurar Gmail para que tu página web pueda enviar emails cuando:
- ✉️ Alguien envía el formulario de contacto
- 📅 Alguien solicita una cita
- 🔐 Alguien solicita recuperación de contraseña
- 📋 Se generan constancias de pacientes

---

## ⚡ **CONFIGURACIÓN RÁPIDA (10 MINUTOS)**

### **📌 PASO 1: Activar Verificación en 2 Pasos en Gmail**

1. **Abre tu navegador** e ingresa a:
   ```
   https://myaccount.google.com/security
   ```

2. **Inicia sesión** con tu cuenta: `dra.ramirezr@gmail.com`

3. **Busca la sección** "Cómo inicias sesión en Google"

4. **Haz clic en** "Verificación en 2 pasos"

5. **Si NO está activada:**
   - Haz clic en "Empezar"
   - Sigue los pasos (te pedirá tu número de teléfono)
   - Completa la activación

6. **Si YA está activada:**
   - Verás un mensaje: "La verificación en 2 pasos está activada" ✅
   - Continúa al siguiente paso

---

### **📌 PASO 2: Generar Contraseña de Aplicación**

1. **Después de activar** la verificación en 2 pasos, busca:
   ```
   "Contraseñas de aplicaciones"
   ```
   (Aparece en la misma página de seguridad)

2. **Haz clic en** "Contraseñas de aplicaciones"

3. **Google te pedirá** que ingreses tu contraseña de nuevo (seguridad)

4. **Verás una pantalla** para generar la contraseña:
   - En "Selecciona la app": Elige **"Correo"**
   - En "Selecciona el dispositivo": Elige **"Otro (nombre personalizado)"**
   - Escribe: **"Sitio Web Dra Shirley"**

5. **Haz clic en** "GENERAR"

6. **Google mostrará** una contraseña de 16 caracteres:
   ```
   ejemplo: abcd efgh ijkl mnop
   ```

7. **⚠️ ¡MUY IMPORTANTE!**
   - **COPIA esta contraseña** (la necesitarás en el paso 3)
   - Esta contraseña **SOLO se muestra una vez**
   - Si la pierdes, tendrás que generar una nueva

---

### **📌 PASO 3: Crear Archivo de Configuración (.env)**

1. **Abre tu proyecto** en Cursor/VS Code

2. **Crea un nuevo archivo** en la carpeta raíz del proyecto:
   - Nombre del archivo: `.env` (con el punto al inicio)
   - Ubicación: `Z:\Pagina web shirley\.env`

3. **Copia y pega** este contenido en el archivo:

```env
# ========================================
# CONFIGURACIÓN DE EMAIL GMAIL
# ========================================
# Email que ENVÍA los correos (tu Gmail)
EMAIL_USERNAME=dra.ramirezr@gmail.com

# Contraseña de aplicación de Gmail (16 caracteres)
# ⚠️ REEMPLAZA "xxxx xxxx xxxx xxxx" con la contraseña que generaste en el Paso 2
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx

# Email que RECIBE las notificaciones (tu Gmail)
EMAIL_DESTINATARIO=dra.ramirezr@gmail.com
```

4. **⚠️ REEMPLAZA** `xxxx xxxx xxxx xxxx` con la contraseña que copiaste en el Paso 2

5. **Ejemplo de cómo debe quedar:**
```env
EMAIL_USERNAME=dra.ramirezr@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
EMAIL_DESTINATARIO=dra.ramirezr@gmail.com
```

6. **Guarda el archivo** (Ctrl+S)

---

### **📌 PASO 4: Verificar que python-dotenv está instalado**

1. **Abre la terminal** en tu proyecto (Terminal → Nueva Terminal en Cursor)

2. **Ejecuta este comando:**
   ```bash
   pip list | findstr dotenv
   ```

3. **Si NO aparece nada**, instálalo:
   ```bash
   pip install python-dotenv
   ```

4. **Deberías ver:**
   ```
   python-dotenv    1.0.0
   ```

---

### **📌 PASO 5: Reiniciar el Servidor**

1. **Si tu servidor está corriendo**, deténlo:
   - Presiona `Ctrl + C` en la terminal

2. **Inicia el servidor nuevamente:**
   ```bash
   python app_simple.py
   ```

3. **Verás en la consola:**
   ```
   * Running on http://127.0.0.1:5000
   ```

---

### **📌 PASO 6: PROBAR QUE FUNCIONA**

#### **Prueba 1: Formulario de Contacto**

1. **Abre tu navegador** y ve a:
   ```
   http://localhost:5000/contacto
   ```

2. **Llena el formulario** con tus datos de prueba:
   - Nombre: Tu nombre
   - Email: Tu email personal
   - Teléfono: Tu teléfono
   - Asunto: "Prueba de email"
   - Mensaje: "Esto es una prueba"

3. **Haz clic en** "Enviar Mensaje"

4. **Revisa la consola** (terminal donde corre el servidor):
   - ✅ Deberías ver: `✅ EMAIL ENVIADO EXITOSAMENTE`
   - ❌ Si ves un error, ve a "Solución de Problemas" abajo

5. **Revisa tu Gmail** (`dra.ramirezr@gmail.com`):
   - Deberías recibir un email con el título: `🔔 Nuevo mensaje: Prueba de email`
   - **Revisa también** la carpeta de SPAM (por si acaso)

#### **Prueba 2: Solicitud de Cita**

1. **Ve a:**
   ```
   http://localhost:5000/solicitar-cita
   ```

2. **Llena el formulario** y envía

3. **Revisa tu Gmail**: Deberías recibir un email con `📅 Nueva Solicitud de Cita`

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### ❌ **Error: "Username and Password not accepted"**

**Causa:** La contraseña de aplicación es incorrecta

**Solución:**
1. Ve a: https://myaccount.google.com/security
2. Ve a "Contraseñas de aplicaciones"
3. **Elimina** la contraseña anterior (si existe)
4. **Genera una nueva** contraseña
5. **Actualiza** el archivo `.env` con la nueva contraseña
6. **Reinicia** el servidor

---

### ❌ **Error: "Contraseñas de aplicaciones no está disponible"**

**Causa:** La verificación en 2 pasos NO está activada

**Solución:**
1. Ve a: https://myaccount.google.com/security
2. Activa "Verificación en 2 pasos"
3. Completa el proceso (necesitarás tu teléfono)
4. Una vez activada, aparecerá "Contraseñas de aplicaciones"

---

### ❌ **Error: "No module named 'dotenv'"**

**Causa:** La librería python-dotenv no está instalada

**Solución:**
```bash
pip install python-dotenv
```

---

### ❌ **Error: "EMAIL_PASSWORD no configurado"**

**Causa:** El archivo `.env` no existe o está mal configurado

**Solución:**
1. Verifica que el archivo se llame **exactamente** `.env` (con el punto)
2. Verifica que esté en la **carpeta raíz** del proyecto
3. Verifica que tenga el contenido correcto (Paso 3)
4. Verifica que no haya espacios extra

---

### ❌ **El email NO llega**

**Posibles causas y soluciones:**

1. **Revisa la carpeta de SPAM** en Gmail

2. **Revisa la consola** del servidor:
   - Si dice `✅ EMAIL ENVIADO` → el email se envió correctamente
   - Si dice `❌ ERROR` → lee el mensaje de error

3. **Verifica el archivo .env:**
   - Email correcto: `dra.ramirezr@gmail.com`
   - Contraseña sin errores de tipeo
   - Sin espacios extra al inicio o final

4. **Espera 1-2 minutos:**
   - A veces Gmail tarda un poco

5. **Prueba con otro email:**
   - Cambia `EMAIL_DESTINATARIO` en `.env` a otro email tuyo
   - Reinicia el servidor
   - Prueba de nuevo

---

### ❌ **El servidor no inicia**

**Solución:**
1. Cierra todos los procesos de Python
2. Abre una nueva terminal
3. Ve a la carpeta del proyecto:
   ```bash
   cd "Z:\Pagina web shirley"
   ```
4. Inicia el servidor:
   ```bash
   python app_simple.py
   ```

---

## 📧 **FORMATO DE LOS EMAILS QUE RECIBIRÁS**

### **Email de Contacto:**
```
De: Sitio Web Dra. Shirley
Para: dra.ramirezr@gmail.com
Asunto: 🔔 Nuevo mensaje: [Asunto del contacto]

┌─────────────────────────────────┐
│ 📧 Nuevo Mensaje de Contacto    │
├─────────────────────────────────┤
│ 👤 Nombre: Juan Pérez           │
│ 📧 Email: juan@ejemplo.com      │
│ 📱 Teléfono: +507 6123-4567     │
│ 📝 Asunto: Consulta             │
├─────────────────────────────────┤
│ 💬 Mensaje:                     │
│ Quisiera agendar una cita...    │
├─────────────────────────────────┤
│   [Responder a Juan Pérez]      │
└─────────────────────────────────┘
```

### **Email de Solicitud de Cita:**
```
De: Sitio Web Dra. Shirley
Para: dra.ramirezr@gmail.com
Asunto: 📅 Nueva Solicitud de Cita

┌─────────────────────────────────┐
│ 📅 Nueva Solicitud de Cita      │
├─────────────────────────────────┤
│ 👤 Paciente: María González     │
│ 📧 Email: maria@ejemplo.com     │
│ 📱 Teléfono: +507 6987-6543     │
│ 📅 Fecha: 2025-10-20            │
│ 🕐 Hora: 10:00 AM               │
│ 💬 Motivo: Control prenatal     │
└─────────────────────────────────┘
```

### **Email de Recuperación de Contraseña:**
```
De: Sitio Web Dra. Shirley
Para: usuario@ejemplo.com
Asunto: 🔐 Recuperación de Contraseña

┌─────────────────────────────────┐
│ 🔐 Recuperación de Contraseña   │
├─────────────────────────────────┤
│ Has solicitado restablecer tu   │
│ contraseña. Haz clic en el      │
│ botón para continuar:           │
│                                 │
│   [Restablecer Contraseña]      │
│                                 │
│ ⚠️ Este enlace expira en 1 hora │
└─────────────────────────────────┘
```

---

## 🔐 **SEGURIDAD - MUY IMPORTANTE**

### ✅ **LO QUE DEBES HACER:**

1. **Nunca compartas** el archivo `.env` con nadie
2. **No subas** el archivo `.env` a GitHub o internet
3. **Usa contraseña de aplicación**, no tu contraseña real de Gmail
4. **Guarda** la contraseña de aplicación en un lugar seguro
5. Si alguien obtiene acceso al archivo `.env`:
   - Ve a Google → Seguridad → Contraseñas de aplicaciones
   - **Revoca** la contraseña comprometida
   - **Genera** una nueva

### ⚠️ **LO QUE NO DEBES HACER:**

1. ❌ NO uses tu contraseña real de Gmail en `.env`
2. ❌ NO compartas el archivo `.env` por WhatsApp/email
3. ❌ NO subas `.env` a repositorios públicos
4. ❌ NO escribas la contraseña en código directamente

---

## 💡 **ALTERNATIVA SIN CONFIGURAR EMAIL**

Si **NO quieres configurar** el email o tienes problemas, puedes usar el **Panel Admin**:

1. **Ve a:**
   ```
   tusitio.com/admin
   ```

2. **Inicia sesión** con tus credenciales

3. **Verás todos los mensajes** en el panel:
   - Formularios de contacto
   - Solicitudes de citas
   - Fecha y hora
   - Toda la información del remitente

4. **Puedes:**
   - Leer mensajes completos
   - Copiar emails para responder manualmente
   - Marcar como leídos
   - Ver estadísticas

---

## 📊 **VERIFICACIÓN FINAL**

✅ **Checklist completo:**

- [ ] Verificación en 2 pasos activada en Gmail
- [ ] Contraseña de aplicación generada
- [ ] Archivo `.env` creado en la carpeta raíz
- [ ] Contraseña copiada correctamente en `.env`
- [ ] python-dotenv instalado
- [ ] Servidor reiniciado
- [ ] Prueba de email enviada
- [ ] Email recibido en Gmail

---

## 🆘 **¿NECESITAS AYUDA?**

Si después de seguir todos los pasos **aún tienes problemas**:

1. **Copia el mensaje de error** completo de la consola
2. **Verifica** que seguiste TODOS los pasos en orden
3. **Revisa** la sección "Solución de Problemas"
4. **Contáctame** con:
   - El mensaje de error exacto
   - Qué paso estás intentando
   - Captura de pantalla (si es posible)

---

## ✅ **CONCLUSIÓN**

Una vez configurado, **tu sitio web podrá**:

- ✉️ Enviarte emails cuando alguien te contacte
- 📅 Notificarte de nuevas solicitudes de citas
- 🔐 Enviar enlaces de recuperación de contraseña
- 📋 Enviar constancias de pacientes a médicos

**Todo funcionará automáticamente** sin que tengas que hacer nada más. 🚀

---

**Última actualización:** 18 de octubre de 2025  
**Configuración válida para:** Gmail con Verificación en 2 pasos  
**Tiempo estimado:** 10-15 minutos

