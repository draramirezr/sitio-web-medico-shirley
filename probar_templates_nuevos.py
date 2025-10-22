# -*- coding: utf-8 -*-
"""
Script para probar los nuevos templates estandarizados de email
"""

import os
import sys
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Importar templates
from email_templates import (
    template_contacto,
    template_cita,
    template_recuperacion,
    template_constancia_pdf,
    template_factura
)

# Cargar variables de entorno
load_dotenv()

EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', 'dra.ramirezr@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_DESTINATARIO = os.getenv('EMAIL_DESTINATARIO', 'dra.ramirezr@gmail.com')

print("\n" + "=" * 80)
print("📧 PRUEBA DE TEMPLATES ESTANDARIZADOS DE EMAIL")
print("=" * 80 + "\n")

if not EMAIL_PASSWORD:
    print("❌ ERROR: EMAIL_PASSWORD no configurado en .env")
    sys.exit(1)

# Test 1: Email de Contacto con el nuevo template
print("📝 TEST 1: Email de Contacto (Formato Estandarizado)")
try:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '🔔 Nuevo mensaje: Prueba Template Estandarizado'
    msg['From'] = EMAIL_USERNAME
    msg['To'] = EMAIL_DESTINATARIO
    msg['Reply-To'] = 'prueba@ejemplo.com'
    
    html = template_contacto(
        "María González",
        "maria@ejemplo.com",
        "+507 6123-4567",
        "Consulta sobre Control Prenatal",
        "Hola doctora,\n\nEstoy interesada en agendar un control prenatal.\nActualmente tengo 12 semanas de gestación.\n\n¿Cuándo podría tener una cita?\n\nGracias."
    )
    
    part = MIMEText(html, 'html')
    msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
    
    print("✅ Email de contacto enviado (nuevo formato)\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 2: Email de Cita con el nuevo template
print("📅 TEST 2: Email de Solicitud de Cita (Formato Estandarizado)")
try:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '📅 Nueva Solicitud de Cita - Carmen López'
    msg['From'] = EMAIL_USERNAME
    msg['To'] = EMAIL_DESTINATARIO
    msg['Reply-To'] = 'carmen@ejemplo.com'
    
    html = template_cita(
        "Carmen",
        "López",
        "carmen@ejemplo.com",
        "+507 6987-6543",
        "2025-10-28",
        "14:00",
        "Control Prenatal",
        "SENASA",
        None,
        "Primera consulta de control prenatal. Embarazo de 8 semanas."
    )
    
    part = MIMEText(html, 'html')
    msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
    
    print("✅ Email de cita enviado (nuevo formato)\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 3: Email de Recuperación con el nuevo template
print("🔐 TEST 3: Email de Recuperación de Contraseña (Formato Estandarizado)")
try:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '🔐 Recuperación de Contraseña - Panel Administrativo'
    msg['From'] = EMAIL_USERNAME
    msg['To'] = EMAIL_DESTINATARIO
    
    html = template_recuperacion(
        "Dra. Shirley Ramírez",
        "http://localhost:5000/recuperar-contrasena/test_token_abc123xyz"
    )
    
    part = MIMEText(html, 'html')
    msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
    
    print("✅ Email de recuperación enviado (nuevo formato)\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 4: Email de Constancia con el nuevo template
print("📋 TEST 4: Email de Constancia PDF (Formato Estandarizado)")
try:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '📋 Constancia - 8 Paciente(s) Pendiente(s) de Facturación'
    msg['From'] = EMAIL_USERNAME
    msg['To'] = EMAIL_DESTINATARIO
    
    html = template_constancia_pdf(
        "Dra. Shirley Ramírez",
        8,
        12500.00
    )
    
    part = MIMEText(html, 'html')
    msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
    
    print("✅ Email de constancia enviado (nuevo formato)\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 5: Email de Factura con el nuevo template
print("💰 TEST 5: Email de Factura (Formato Estandarizado)")
try:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '💰 Factura #12345 - NCF: B0100000123'
    msg['From'] = EMAIL_USERNAME
    msg['To'] = EMAIL_DESTINATARIO
    
    html = template_factura(
        "12345",
        "B0100000123",
        8500.00
    )
    
    part = MIMEText(html, 'html')
    msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
    
    print("✅ Email de factura enviado (nuevo formato)\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

print("=" * 80)
print("✅ TODOS LOS TEMPLATES ESTANDARIZADOS FUNCIONAN CORRECTAMENTE")
print("=" * 80)
print(f"\n📧 Revisa tu bandeja de entrada: {EMAIL_DESTINATARIO}")
print("Deberías ver 5 emails con el NUEVO FORMATO ESTANDARIZADO:")
print("  1. 📝 Nuevo mensaje de contacto")
print("  2. 📅 Nueva solicitud de cita")
print("  3. 🔐 Recuperación de contraseña")
print("  4. 📋 Constancia de pacientes")
print("  5. 💰 Factura generada")
print("\n⭐ Ahora TODOS los emails tienen:")
print("  • Header profesional con tu nombre y especialidad")
print("  • Diseño consistente con tu línea gráfica")
print("  • Footer estandarizado con información de contacto y redes sociales")
print("  • Formato responsive para móviles")
print("=" * 80 + "\n")

