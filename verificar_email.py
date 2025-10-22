# -*- coding: utf-8 -*-
"""
Script para verificar la configuración de email
Ejecutar: python verificar_email.py
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("\n" + "=" * 70)
print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DE EMAIL")
print("=" * 70 + "\n")

# 1. Verificar que existe el archivo .env
print("📋 Paso 1: Verificar archivo .env")
if os.path.exists('.env'):
    print("   ✅ Archivo .env encontrado\n")
else:
    print("   ❌ ERROR: Archivo .env NO encontrado")
    print("   ⚠️  Debes crear el archivo .env en la carpeta raíz del proyecto\n")
    print("   Instrucciones:")
    print("   1. Crea un archivo llamado '.env'")
    print("   2. Agrega las siguientes líneas:")
    print("      EMAIL_USERNAME=dra.ramirezr@gmail.com")
    print("      EMAIL_PASSWORD=tu_contraseña_de_aplicacion")
    print("      EMAIL_DESTINATARIO=dra.ramirezr@gmail.com")
    print("\n" + "=" * 70 + "\n")
    sys.exit(1)

# 2. Verificar variables de entorno
print("📋 Paso 2: Verificar variables de entorno")
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_DESTINATARIO = os.getenv('EMAIL_DESTINATARIO', '')

if EMAIL_USERNAME:
    print(f"   ✅ EMAIL_USERNAME: {EMAIL_USERNAME}")
else:
    print("   ❌ ERROR: EMAIL_USERNAME no configurado")

if EMAIL_DESTINATARIO:
    print(f"   ✅ EMAIL_DESTINATARIO: {EMAIL_DESTINATARIO}")
else:
    print("   ❌ ERROR: EMAIL_DESTINATARIO no configurado")

if EMAIL_PASSWORD:
    # Mostrar solo los primeros y últimos 4 caracteres por seguridad
    password_masked = EMAIL_PASSWORD[:4] + " **** " + EMAIL_PASSWORD[-4:]
    print(f"   ✅ EMAIL_PASSWORD: {password_masked} (16 caracteres)")
    
    # Verificar longitud de la contraseña
    password_clean = EMAIL_PASSWORD.replace(' ', '')
    if len(password_clean) == 16:
        print(f"   ✅ Longitud correcta: 16 caracteres")
    else:
        print(f"   ⚠️  ADVERTENCIA: La contraseña tiene {len(password_clean)} caracteres")
        print("      Las contraseñas de aplicación de Gmail tienen 16 caracteres")
else:
    print("   ❌ ERROR: EMAIL_PASSWORD no configurado")

print()

# 3. Verificar que python-dotenv está instalado
print("📋 Paso 3: Verificar python-dotenv")
try:
    import dotenv
    print(f"   ✅ python-dotenv instalado\n")
except ImportError:
    print("   ❌ ERROR: python-dotenv NO está instalado")
    print("   ⚠️  Ejecuta: pip install python-dotenv\n")
    sys.exit(1)

# 4. Verificar que se puede importar smtplib
print("📋 Paso 4: Verificar librerías de email")
try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    print("   ✅ Librerías de email disponibles\n")
except ImportError as e:
    print(f"   ❌ ERROR: No se pueden importar librerías de email: {e}\n")
    sys.exit(1)

# 5. Verificar conexión con Gmail
print("📋 Paso 5: Verificar conexión con Gmail (SMTP)")
if EMAIL_USERNAME and EMAIL_PASSWORD:
    try:
        print("   ⏳ Conectando a smtp.gmail.com:587...")
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        print("   ✅ Conexión establecida")
        
        print("   ⏳ Iniciando TLS...")
        server.starttls()
        print("   ✅ TLS iniciado")
        
        print("   ⏳ Autenticando con Gmail...")
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        print("   ✅ Autenticación exitosa")
        
        server.quit()
        print()
        
        # 6. Preguntar si desea enviar un email de prueba
        print("=" * 70)
        print("✅ CONFIGURACIÓN CORRECTA - TODO ESTÁ LISTO")
        print("=" * 70)
        print()
        
        respuesta = input("¿Deseas enviar un email de prueba? (s/n): ").strip().lower()
        
        if respuesta == 's':
            print("\n📧 Enviando email de prueba...")
            
            # Crear mensaje de prueba
            msg = MIMEMultipart('alternative')
            msg['Subject'] = '✅ Prueba de Configuración - Sitio Web'
            msg['From'] = EMAIL_USERNAME
            msg['To'] = EMAIL_DESTINATARIO
            
            html = """
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #F2E2E6; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                    <h2 style="color: #ACACAD; border-bottom: 3px solid #CEB0B7; padding-bottom: 15px; margin-top: 0;">
                        ✅ Configuración de Email Exitosa
                    </h2>
                    
                    <div style="background-color: #F2E2E6; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <p style="margin: 8px 0; color: #282828; font-size: 16px;">
                            ¡Felicidades! Tu configuración de email está funcionando correctamente.
                        </p>
                    </div>
                    
                    <div style="background-color: #fff; padding: 20px; border-left: 4px solid #CEB0B7; margin: 20px 0;">
                        <p style="margin: 0; color: #282828; line-height: 1.6;">
                            <strong style="color: #ACACAD;">✅ Configuración verificada:</strong><br>
                            • Archivo .env configurado correctamente<br>
                            • Conexión con Gmail establecida<br>
                            • Autenticación exitosa<br>
                            • Email de prueba enviado<br><br>
                            
                            <strong style="color: #ACACAD;">📧 A partir de ahora recibirás emails cuando:</strong><br>
                            • Alguien envíe el formulario de contacto<br>
                            • Alguien solicite una cita<br>
                            • Se solicite recuperación de contraseña<br>
                            • Se generen constancias de pacientes<br>
                        </p>
                    </div>
                    
                    <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px; line-height: 1.5;">
                        Este es un mensaje de prueba automático<br>
                        <strong>Sitio Web - Dra. Shirley Ramírez</strong><br>
                        Ginecóloga y Obstetricia
                    </p>
                </div>
            </body>
            </html>
            """
            
            part = MIMEText(html, 'html')
            msg.attach(part)
            
            # Enviar
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
                server.send_message(msg)
            
            print("\n" + "=" * 70)
            print("✅ EMAIL DE PRUEBA ENVIADO EXITOSAMENTE")
            print("=" * 70)
            print(f"\n📧 Revisa tu bandeja de entrada: {EMAIL_DESTINATARIO}")
            print("⚠️  Si no lo ves, revisa la carpeta de SPAM\n")
        else:
            print("\n✅ Configuración verificada. No se envió email de prueba.\n")
        
    except smtplib.SMTPAuthenticationError:
        print("   ❌ ERROR DE AUTENTICACIÓN")
        print("   ⚠️  La contraseña de Gmail es incorrecta\n")
        print("   Soluciones:")
        print("   1. Ve a: https://myaccount.google.com/security")
        print("   2. Verifica que la verificación en 2 pasos esté activa")
        print("   3. Ve a 'Contraseñas de aplicaciones'")
        print("   4. Genera una nueva contraseña de aplicación")
        print("   5. Actualiza el archivo .env con la nueva contraseña")
        print("   6. Ejecuta este script nuevamente\n")
        sys.exit(1)
        
    except smtplib.SMTPException as e:
        print(f"   ❌ ERROR SMTP: {e}")
        print("   ⚠️  Verifica tu conexión a internet\n")
        sys.exit(1)
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        print("   ⚠️  Revisa la configuración en .env\n")
        sys.exit(1)
else:
    print("   ❌ No se puede verificar: EMAIL_USERNAME o EMAIL_PASSWORD no configurados")
    print()
    sys.exit(1)

print("=" * 70)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 70)
print()

