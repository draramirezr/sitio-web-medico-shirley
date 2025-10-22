# -*- coding: utf-8 -*-
"""
Script para probar TODOS los tipos de email del sistema
Ejecutar: python probar_todos_los_emails.py
"""

import os
import sys
import sqlite3
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from io import BytesIO

# Importar reportlab para PDFs
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️  ReportLab no disponible - No se probarán emails con PDF")

# Cargar variables de entorno
load_dotenv()

EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', 'dra.ramirezr@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_DESTINATARIO = os.getenv('EMAIL_DESTINATARIO', 'dra.ramirezr@gmail.com')

print("\n" + "=" * 80)
print("📧 PRUEBA COMPLETA DE EMAILS DEL SISTEMA")
print("=" * 80 + "\n")

if not EMAIL_PASSWORD:
    print("❌ ERROR: EMAIL_PASSWORD no configurado en .env")
    sys.exit(1)

# ============================================================================
# TEST 1: Email de Formulario de Contacto
# ============================================================================
def test_email_contacto():
    print("\n" + "=" * 80)
    print("📝 TEST 1: Email de Formulario de Contacto")
    print("=" * 80)
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🔔 Nuevo mensaje: Prueba de Contacto'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_DESTINATARIO
        msg['Reply-To'] = 'prueba@ejemplo.com'
        
        html = """
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #F2E2E6; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                <h2 style="color: #ACACAD; border-bottom: 3px solid #CEB0B7; padding-bottom: 15px; margin-top: 0;">
                    📧 Nuevo Mensaje de Contacto
                </h2>
                
                <div style="background-color: #F2E2E6; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">👤 Nombre:</strong> Juan Pérez (PRUEBA)
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">📧 Email:</strong> 
                        <a href="mailto:prueba@ejemplo.com" style="color: #CEB0B7; text-decoration: none;">prueba@ejemplo.com</a>
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">📱 Teléfono:</strong> +507 6123-4567
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">📝 Asunto:</strong> Prueba de Sistema
                    </p>
                </div>
                
                <div style="background-color: #fff; padding: 20px; border-left: 4px solid #CEB0B7; margin: 20px 0;">
                    <p style="margin: 0 0 10px 0; color: #ACACAD; font-weight: bold;">💬 Mensaje:</p>
                    <p style="margin: 0; color: #282828; line-height: 1.6;">Este es un email de prueba del sistema de contacto.</p>
                </div>
                
                <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px;">
                    Email de Prueba - Sistema de Notificaciones
                </p>
            </div>
        </body>
        </html>
        """
        
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ Email de contacto enviado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email de contacto: {e}")
        return False

# ============================================================================
# TEST 2: Email de Solicitud de Cita
# ============================================================================
def test_email_cita():
    print("\n" + "=" * 80)
    print("📅 TEST 2: Email de Solicitud de Cita")
    print("=" * 80)
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '📅 Nueva Solicitud de Cita - María González'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_DESTINATARIO
        
        html = """
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #F2E2E6; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                <h2 style="color: #ACACAD; border-bottom: 3px solid #CEB0B7; padding-bottom: 15px; margin-top: 0;">
                    📅 Nueva Solicitud de Cita
                </h2>
                
                <div style="background-color: #F2E2E6; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">👤 Paciente:</strong> María González (PRUEBA)
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">📧 Email:</strong> maria@ejemplo.com
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">📱 Teléfono:</strong> +507 6987-6543
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">📅 Fecha:</strong> 2025-10-25
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">🕐 Hora:</strong> 10:00 AM
                    </p>
                </div>
                
                <div style="background-color: #fff; padding: 20px; border-left: 4px solid #CEB0B7; margin: 20px 0;">
                    <p style="margin: 0 0 10px 0; color: #ACACAD; font-weight: bold;">💬 Motivo:</p>
                    <p style="margin: 0; color: #282828; line-height: 1.6;">Control prenatal - Prueba de sistema</p>
                </div>
                
                <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px;">
                    Email de Prueba - Sistema de Citas
                </p>
            </div>
        </body>
        </html>
        """
        
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ Email de cita enviado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email de cita: {e}")
        return False

# ============================================================================
# TEST 3: Email de Recuperación de Contraseña
# ============================================================================
def test_email_recuperacion():
    print("\n" + "=" * 80)
    print("🔐 TEST 3: Email de Recuperación de Contraseña")
    print("=" * 80)
    
    try:
        token = "test_token_123456789"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🔐 Recuperación de Contraseña - Panel Administrativo'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_DESTINATARIO
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #F2E2E6; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                <h2 style="color: #ACACAD; border-bottom: 3px solid #CEB0B7; padding-bottom: 15px; margin-top: 0;">
                    🔐 Recuperación de Contraseña
                </h2>
                
                <div style="color: #282828; line-height: 1.8; margin: 20px 0;">
                    <p>Has solicitado restablecer tu contraseña.</p>
                    <p>Haz clic en el siguiente botón para crear una nueva contraseña:</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5000/recuperar-contrasena/{token}" 
                       style="display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #ACACAD 0%, #949495 100%); color: white !important; text-decoration: none; border-radius: 25px; font-weight: bold;">
                        Restablecer Contraseña
                    </a>
                </div>
                
                <div style="background-color: #FFF9E6; padding: 15px; border-radius: 10px; border-left: 4px solid #FFC107; margin: 20px 0;">
                    <p style="margin: 0; color: #282828; font-size: 14px;">
                        ⚠️ Este enlace expira en <strong>1 hora</strong>
                    </p>
                </div>
                
                <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px;">
                    Email de Prueba - Sistema de Recuperación
                </p>
            </div>
        </body>
        </html>
        """
        
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ Email de recuperación enviado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email de recuperación: {e}")
        return False

# ============================================================================
# TEST 4: Email con PDF de Constancia
# ============================================================================
def test_email_constancia():
    print("\n" + "=" * 80)
    print("📋 TEST 4: Email con PDF de Constancia")
    print("=" * 80)
    
    if not REPORTLAB_AVAILABLE:
        print("⚠️  Saltando prueba - ReportLab no disponible")
        return None
    
    try:
        # Crear PDF simple de prueba
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "CONSTANCIA DE PACIENTES PENDIENTES")
        c.setFont("Helvetica", 12)
        c.drawString(100, 700, "Este es un PDF de prueba")
        c.drawString(100, 680, "Total: 5 Pacientes")
        c.drawString(100, 660, "Monto Total: $5,000.00")
        c.showPage()
        c.save()
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Crear mensaje
        msg = MIMEMultipart()
        msg['Subject'] = '📋 Constancia - 5 Paciente(s) Pendiente(s) de Facturación'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_DESTINATARIO
        
        html = """
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #F2E2E6; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                <h2 style="color: #ACACAD; border-bottom: 3px solid #CEB0B7; padding-bottom: 15px; margin-top: 0;">
                    📋 Constancia de Pacientes Pendientes
                </h2>
                
                <div style="background-color: #F2E2E6; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">👨‍⚕️ Médico:</strong> Dra. Shirley Ramírez (PRUEBA)
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">📋 Pacientes:</strong> 5
                    </p>
                    <p style="margin: 8px 0; color: #282828;">
                        <strong style="color: #ACACAD;">💰 Total:</strong> $5,000.00
                    </p>
                </div>
                
                <div style="background-color: #fff; padding: 20px; border-left: 4px solid #CEB0B7; margin: 20px 0;">
                    <p style="margin: 0; color: #282828;">
                        📎 Adjunto encontrarás la constancia en PDF con el detalle completo.
                    </p>
                </div>
                
                <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px;">
                    Email de Prueba - Sistema de Facturación
                </p>
            </div>
        </body>
        </html>
        """
        
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)
        
        # Adjuntar PDF
        pdf_part = MIMEApplication(pdf_data, _subtype='pdf')
        pdf_part.add_header('Content-Disposition', 'attachment', filename='constancia_prueba.pdf')
        msg.attach(pdf_part)
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ Email con PDF enviado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email con PDF: {e}")
        return False

# ============================================================================
# EJECUTAR TODAS LAS PRUEBAS
# ============================================================================
print(f"📧 Enviando emails de prueba a: {EMAIL_DESTINATARIO}")
print("⏳ Este proceso puede tomar 30-60 segundos...\n")

resultados = []

# Test 1: Contacto
resultados.append(('Formulario de Contacto', test_email_contacto()))

# Test 2: Cita
resultados.append(('Solicitud de Cita', test_email_cita()))

# Test 3: Recuperación
resultados.append(('Recuperación de Contraseña', test_email_recuperacion()))

# Test 4: PDF
result_pdf = test_email_constancia()
if result_pdf is not None:
    resultados.append(('Constancia con PDF', result_pdf))

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "=" * 80)
print("📊 RESUMEN DE PRUEBAS")
print("=" * 80 + "\n")

exitosos = sum(1 for _, r in resultados if r)
total = len(resultados)

for nombre, resultado in resultados:
    icono = "✅" if resultado else "❌"
    print(f"{icono} {nombre}")

print("\n" + "-" * 80)
print(f"Total: {exitosos}/{total} emails enviados exitosamente")
print("-" * 80)

if exitosos == total:
    print("\n🎉 ¡TODOS LOS EMAILS FUNCIONAN CORRECTAMENTE!")
    print(f"\n📧 Revisa tu bandeja de entrada: {EMAIL_DESTINATARIO}")
    print("⚠️  Si no los ves, revisa la carpeta de SPAM\n")
else:
    print("\n⚠️  Algunos emails fallaron. Revisa los errores arriba.\n")

print("=" * 80 + "\n")

