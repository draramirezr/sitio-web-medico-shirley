#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar el envío de emails
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurar variables de entorno
os.environ['EMAIL_USERNAME'] = 'dra.ramirezr@gmail.com'
os.environ['EMAIL_PASSWORD'] = 'nqze lbab meit vprt'
os.environ['EMAIL_DESTINATARIO'] = 'dra.ramirezr@gmail.com'

EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_DESTINATARIO = os.getenv('EMAIL_DESTINATARIO')

def test_email_sending():
    """Probar el envío de email"""
    try:
        print("🔧 Probando configuración de email...")
        print(f"📧 Usuario: {EMAIL_USERNAME}")
        print(f"📧 Destinatario: {EMAIL_DESTINATARIO}")
        print(f"📧 Password configurado: {'✅ SÍ' if EMAIL_PASSWORD else '❌ NO'}")
        
        if not EMAIL_PASSWORD:
            print("❌ ERROR: EMAIL_PASSWORD no está configurado")
            return False
        
        # Crear mensaje de prueba
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🧪 Prueba de Email - Sistema Médico'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_DESTINATARIO
        
        # Contenido HTML simple
        html = """
        <html>
        <body>
            <h2>🧪 Prueba de Email</h2>
            <p>Este es un email de prueba del sistema médico.</p>
            <p>Si recibes este mensaje, el sistema de emails está funcionando correctamente.</p>
            <hr>
            <p><small>Sistema Médico - Dra. Shirley Ramírez</small></p>
        </body>
        </html>
        """
        
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Enviar email
        print("📤 Enviando email de prueba...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ EMAIL DE PRUEBA ENVIADO EXITOSAMENTE")
        print("📧 Revisa tu bandeja de entrada")
        return True
        
    except Exception as e:
        print(f"❌ ERROR al enviar email: {e}")
        return False

if __name__ == "__main__":
    test_email_sending()

