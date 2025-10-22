# 📧 Guía para Recibir Emails en dra.ramirezr@gmail.com

## 🚀 Configuración Rápida (5 minutos)

### Paso 1: Configurar Gmail

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Click en **"Seguridad"** (menú izquierdo)
3. Busca **"Verificación en 2 pasos"**
   - Si NO está activada, actívala primero
4. Una vez activada, busca **"Contraseñas de aplicaciones"**
5. Genera una nueva contraseña:
   - Selecciona "Correo"
   - Selecciona "Otro (nombre personalizado)" → escribe: "Sitio Web"
   - Click en **"Generar"**
6. **Copia la contraseña generada** (ejemplo: `abcd efgh ijkl mnop`)
   - ⚠️ Guárdala, solo se muestra una vez

---

### Paso 2: Crear archivo de configuración

Crea un archivo llamado `.env` en la carpeta del proyecto:

```env
# Configuración de Email
EMAIL_USERNAME=dra.ramirezr@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
EMAIL_DESTINATARIO=dra.ramirezr@gmail.com
```

**⚠️ Reemplaza** `abcd efgh ijkl mnop` con la contraseña que generaste.

---

### Paso 3: Instalar librería

Abre la terminal y ejecuta:

```bash
pip install python-dotenv
```

---

### Paso 4: Actualizar el código

Abre el archivo `app_simple.py` y reemplaza la función `enviar_email_notificacion` con esta:

```python
def enviar_email_notificacion(name, email, phone, subject, message):
    """Enviar email de notificación a la doctora"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', 'dra.ramirezr@gmail.com')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
        
        if not EMAIL_PASSWORD:
            print("⚠️ Contraseña de email no configurada. Ver CONFIGURAR_EMAIL_GMAIL.md")
            return False
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'🔔 Nuevo mensaje: {subject}'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_DESTINATARIO
        msg['Reply-To'] = email
        
        # Contenido HTML
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #F2E2E6; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                <h2 style="color: #ACACAD; border-bottom: 3px solid #CEB0B7; padding-bottom: 15px; margin-top: 0;">
                    📧 Nuevo Mensaje de Contacto
                </h2>
                
                <div style="background-color: #F2E2E6; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">👤 Nombre:</strong> {name}
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">📧 Email:</strong> 
                        <a href="mailto:{email}" style="color: #CEB0B7; text-decoration: none;">{email}</a>
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">📱 Teléfono:</strong> 
                        <a href="tel:{phone}" style="color: #CEB0B7; text-decoration: none;">{phone}</a>
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">📝 Asunto:</strong> {subject}
                    </p>
                </div>
                
                <div style="background-color: #fff; padding: 20px; border-left: 4px solid #CEB0B7; margin: 20px 0;">
                    <p style="margin: 0 0 10px 0; color: #ACACAD; font-weight: bold;">💬 Mensaje:</p>
                    <p style="margin: 0; color: #282828; line-height: 1.6; white-space: pre-wrap;">{message}</p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #F2E2E6;">
                    <a href="mailto:{email}" style="display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #ACACAD 0%, #949495 100%); color: white; text-decoration: none; border-radius: 25px; font-weight: bold;">
                        Responder a {name}
                    </a>
                </div>
                
                <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px; line-height: 1.5;">
                    Este mensaje fue enviado desde el formulario de contacto<br>
                    <strong>Sitio Web - Dra. Shirley Ramírez</strong><br>
                    Ginecóloga y Obstetricia
                </p>
            </div>
        </body>
        </html>
        """
        
        # Adjuntar HTML
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Enviar email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email enviado exitosamente a {EMAIL_DESTINATARIO}")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        print("Revisa CONFIGURAR_EMAIL_GMAIL.md para más información")
        return False
```

---

### Paso 5: Reiniciar el servidor

1. Detén el servidor (Ctrl+C)
2. Inicia nuevamente: `python app_simple.py`
3. Prueba el formulario de contacto

---

## ✅ Verificar que Funciona

1. Ve a: http://localhost:5000/contacto
2. Llena el formulario y envía
3. Deberías recibir un email en **dra.ramirezr@gmail.com** en 1-2 minutos
4. También verás en la consola: `✅ Email enviado exitosamente`

---

## 🔧 Solución de Problemas

### ❌ Error: "Username and Password not accepted"
- Verifica que la verificación en 2 pasos esté ACTIVA
- Genera una nueva contraseña de aplicación
- Verifica que copiaste la contraseña sin espacios

### ❌ Error: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### ❌ No llega el email
- Revisa la carpeta de SPAM
- Verifica que el email en `.env` sea correcto
- Revisa la consola para ver errores

---

## 📧 Formato del Email que Recibirás

Cuando alguien envíe el formulario, recibirás un email bonito con:
- 👤 Nombre del remitente
- 📧 Email (clickeable para responder)
- 📱 Teléfono (clickeable)
- 📝 Asunto
- 💬 Mensaje completo
- Botón para responder directamente

---

## 🔐 Seguridad

✅ **Nunca compartas** el archivo `.env` con nadie
✅ **No subas** el archivo `.env` a GitHub o internet
✅ Usa **contraseña de aplicación**, no tu contraseña real de Gmail
✅ Si cambias tu contraseña de Gmail, genera una nueva contraseña de aplicación

---

## 💡 Alternativa Más Simple

Si no quieres configurar Gmail, puedes usar el **Panel Admin** que ya funciona:

```
http://localhost:5000/admin
```

Ahí verás todos los mensajes y podrás:
- Ver nombre, email, teléfono
- Leer el mensaje completo
- Copiar el email para responder manualmente
- Ver la fecha y hora

---

¿Necesitas ayuda con algún paso? ¡Avísame!

