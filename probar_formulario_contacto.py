#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el formulario de contacto
"""

import requests
import json

def test_contact_form():
    """Probar el formulario de contacto"""
    try:
        print("🧪 Probando formulario de contacto...")
        print("=" * 50)
        
        # Datos de prueba
        test_data = {
            'name': 'Usuario de Prueba',
            'email': 'test@example.com',
            'phone': '809-123-4567',
            'subject': 'Prueba de Email - Sistema Médico',
            'message': 'Este es un mensaje de prueba para verificar que el sistema de emails funciona correctamente. Si recibes este email, significa que el formulario de contacto está funcionando perfectamente.'
        }
        
        # URL del formulario de contacto
        url = 'http://127.0.0.1:5000/contacto'
        
        print(f"📧 Enviando datos de prueba:")
        print(f"   Nombre: {test_data['name']}")
        print(f"   Email: {test_data['email']}")
        print(f"   Teléfono: {test_data['phone']}")
        print(f"   Asunto: {test_data['subject']}")
        print(f"   Mensaje: {test_data['message'][:50]}...")
        print()
        
        # Enviar POST request
        response = requests.post(url, data=test_data, timeout=10)
        
        print(f"📊 Respuesta del servidor:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ FORMULARIO ENVIADO EXITOSAMENTE")
            print("📧 Revisa la bandeja de entrada de dra.ramirezr@gmail.com")
            print("📧 También revisa la carpeta de SPAM por si acaso")
        else:
            print(f"❌ Error en el formulario: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}...")
        
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar al servidor")
        print("   Asegúrate de que la aplicación esté ejecutándose en http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_contact_form()
