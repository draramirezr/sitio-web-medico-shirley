#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba simple de envío de email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_simple_email():
    """Prueba simple de envío de email"""
    try:
        print("🧪 Prueba simple de email...")
        print("=" * 40)
        
        # Configuración
        EMAIL_USERNAME = 'dra.ramirezr@gmail.com'
        EMAIL_PASSWORD = 'nqze lbab meit vprt'
        EMAIL_DESTINATARIO = 'dra.ramirezr@gmail.com'
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🧪 Prueba de Email - Sistema Médico'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_DESTINATARIO
        
        # Contenido HTML
        html = """
        <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px;">
            <div style="background: #CEB0B7; padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="color: white; margin: 0;">🧪 Prueba de Email</h2>
            </div>
            <div style="padding: 20px;">
                <p>Este es un email de prueba del sistema médico.</p>
                <p><strong>Si recibes este mensaje, el sistema de emails está funcionando correctamente.</strong></p>
                <hr>
                <p><small>Sistema Médico - Dra. Shirley Ramírez</small></p>
            </div>
        </body>
        </html>
        """
        
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Enviar
        print("📤 Enviando email...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ EMAIL ENVIADO EXITOSAMENTE")
        print("📧 Revisa dra.ramirezr@gmail.com")
        print("=" * 40)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_simple_email()
