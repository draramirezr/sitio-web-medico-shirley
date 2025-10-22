#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar directamente la función de email de contacto
"""

import os
import sys

# Agregar el directorio actual al path para importar app_simple
sys.path.append('.')

# Configurar variables de entorno
os.environ['EMAIL_USERNAME'] = 'dra.ramirezr@gmail.com'
os.environ['EMAIL_PASSWORD'] = 'nqze lbab meit vprt'
os.environ['EMAIL_DESTINATARIO'] = 'dra.ramirezr@gmail.com'

def test_email_function():
    """Probar directamente la función de email"""
    try:
        print("🧪 Probando función de email directamente...")
        print("=" * 50)
        
        # Importar la función de email
        from app_simple import enviar_email_notificacion
        
        # Datos de prueba
        test_data = {
            'name': 'Usuario de Prueba',
            'email': 'test@example.com',
            'phone': '809-123-4567',
            'subject': 'Prueba de Email - Sistema Médico',
            'message': 'Este es un mensaje de prueba para verificar que el sistema de emails funciona correctamente. Si recibes este email, significa que el formulario de contacto está funcionando perfectamente.'
        }
        
        print(f"📧 Enviando email de prueba:")
        print(f"   Nombre: {test_data['name']}")
        print(f"   Email: {test_data['email']}")
        print(f"   Teléfono: {test_data['phone']}")
        print(f"   Asunto: {test_data['subject']}")
        print(f"   Mensaje: {test_data['message'][:50]}...")
        print()
        
        # Llamar la función directamente
        result = enviar_email_notificacion(
            test_data['name'],
            test_data['email'],
            test_data['phone'],
            test_data['subject'],
            test_data['message']
        )
        
        if result:
            print("✅ EMAIL ENVIADO EXITOSAMENTE")
            print("📧 Revisa la bandeja de entrada de dra.ramirezr@gmail.com")
            print("📧 También revisa la carpeta de SPAM por si acaso")
        else:
            print("❌ ERROR: No se pudo enviar el email")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_email_function()
