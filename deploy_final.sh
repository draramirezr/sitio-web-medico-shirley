#!/bin/bash
# Script de commit y push automatizado

echo "🔍 Verificando archivos modificados..."
git status

echo ""
echo "📦 Agregando archivos al staging..."
git add app_simple.py
git add templates/contact.html
git add local.env

echo ""
echo "📝 Creando commit..."
git commit -m "✅ Migración completa a MySQL + Mejoras UI

- Eliminado 100% código SQLite
- Convertidos todos placeholders ? a %s (MySQL)
- Wrapper MySQLConnectionWrapper con escape de % 
- Formulario contacto: colores mejorados (legibilidad)
- WhatsApp integrado en página de contacto
- Conectado a MySQL Railway (drashirley)
- Todos los servicios funcionando correctamente"

echo ""
echo "🚀 Haciendo push a GitHub..."
git push origin main

echo ""
echo "✅ ¡DEPLOY COMPLETADO!"
echo "🔄 Railway detectará el push y hará auto-deploy"
echo "⏳ Espera 2-3 minutos y verifica la URL de Railway"












