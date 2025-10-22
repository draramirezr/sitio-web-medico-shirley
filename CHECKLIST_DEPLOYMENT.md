# ✅ CHECKLIST DE DEPLOYMENT
## Sistema Médico - Dra. Shirley Ramírez

---

## 🚀 PRE-DEPLOYMENT

### Verificación Local
- [x] Base de datos optimizada con índices
- [x] Sistema de facturación funcionando
- [x] PDFs generándose correctamente
- [x] Descarga automática de PDF al agregar pacientes
- [x] Médico que factura seleccionándose correctamente
- [x] Headers de seguridad configurados
- [x] Sitemap.xml accesible
- [x] Robots.txt accesible
- [ ] Todas las páginas funcionando sin errores

### Dependencias
```bash
# Verificar que todo esté instalado
pip install flask flask-login flask-compress reportlab openpyxl python-dotenv werkzeug markupsafe

# Verificar versión de Python (3.8+)
python --version
```

---

## 🌐 DEPLOYMENT EN PRODUCCIÓN

### 1. Servidor
- [ ] Servidor contratado (DigitalOcean, Heroku, AWS, etc.)
- [ ] Python 3.8+ instalado
- [ ] Acceso SSH configurado
- [ ] Firewall configurado (puertos 80, 443)

### 2. Dominio y SSL
- [ ] Dominio registrado (drashirleyramirez.com)
- [ ] DNS apuntando al servidor
- [ ] Certificado SSL instalado (Let's Encrypt)
- [ ] HTTPS funcionando
- [ ] Redirección HTTP → HTTPS activa

### 3. Base de Datos
- [ ] Archivo `drashirley_simple.db` subido al servidor
- [ ] Permisos correctos (chmod 644)
- [ ] Script de optimización ejecutado
- [ ] Backup inicial creado

### 4. Archivos del Proyecto
- [ ] Todo el código subido al servidor
- [ ] Carpeta `static/` con permisos correctos
- [ ] Carpeta `templates/` con permisos correctos
- [ ] `.env` configurado con credenciales reales
- [ ] `security_middleware.py` presente

### 5. Variables de Entorno
```bash
# Crear archivo .env en producción
SECRET_KEY=tu_clave_secreta_super_segura_aqui
FLASK_ENV=production
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=tu_password_de_aplicacion
```

### 6. Servidor Web
```bash
# Opción 1: Gunicorn (recomendado)
pip install gunicorn
gunicorn app_simple:app -w 4 -b 0.0.0.0:8000

# Opción 2: Nginx + Gunicorn
# Configurar nginx como reverse proxy
```

### 7. Proceso Manager
```bash
# Usar supervisor o systemd para auto-restart
sudo apt-get install supervisor

# Crear /etc/supervisor/conf.d/drashirley.conf
```

---

## 🔒 SEGURIDAD POST-DEPLOYMENT

### Configuración Inmediata
- [ ] Cambiar `SECRET_KEY` a valor único y seguro
- [ ] Configurar firewall (ufw o iptables)
- [ ] Deshabilitar acceso root via SSH
- [ ] Configurar fail2ban (opcional)
- [ ] Activar logs de seguridad

### Headers HTTPS
En `app_simple.py`, descomentar:
```python
response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
```

### Rate Limiting
Aplicar en `/login`:
```python
from security_middleware import rate_limit

@app.route('/login', methods=['POST'])
@rate_limit(max_requests=5, window_minutes=15, key_prefix='login')
def login():
    # ...
```

---

## 🎯 SEO POST-DEPLOYMENT

### Google
- [ ] Registrar en Google Search Console
- [ ] Subir sitemap: `https://drashirleyramirez.com/sitemap.xml`
- [ ] Verificar propiedad del sitio
- [ ] Solicitar indexación
- [ ] Configurar Google Analytics (opcional)
- [ ] Registrar Google My Business

### Redes Sociales
- [ ] Verificar que Open Graph funciona (Facebook Debugger)
- [ ] Verificar que Twitter Cards funciona (Twitter Card Validator)
- [ ] Crear/actualizar perfiles en redes sociales

### Herramientas de Test
- [ ] PageSpeed Insights: https://pagespeed.web.dev/
- [ ] Security Headers: https://securityheaders.com/
- [ ] SSL Test: https://www.ssllabs.com/ssltest/
- [ ] Mobile-Friendly Test: https://search.google.com/test/mobile-friendly

---

## 🔄 CONFIGURACIÓN DE BACKUPS

### Backup Automático Diario
```bash
# Crear script /home/user/backup.sh
#!/bin/bash
BACKUP_DIR="/home/user/backups"
DATE=$(date +%Y%m%d)
sqlite3 /path/to/drashirley_simple.db ".backup '$BACKUP_DIR/backup_$DATE.db'"

# Mantener solo últimos 30 días
find $BACKUP_DIR -name "backup_*.db" -mtime +30 -delete
```

### Crontab
```bash
# Agregar a crontab (crontab -e)
0 2 * * * /home/user/backup.sh
```

---

## 📊 MONITOREO

### Uptime Monitoring
- [ ] Registrar en UptimeRobot (gratuito)
- [ ] Configurar alertas por email
- [ ] Monitorear cada 5 minutos

### Error Tracking
- [ ] Configurar Sentry (opcional)
- [ ] Revisar logs diariamente
- [ ] Configurar alertas de errores críticos

### Analytics
- [ ] Google Analytics configurado
- [ ] Eventos de conversión rastreados
- [ ] Dashboard personalizado creado

---

## 📝 POST-DEPLOYMENT INMEDIATO

### Día 1
- [ ] Verificar que todas las páginas cargan
- [ ] Probar formulario de contacto
- [ ] Probar sistema de citas
- [ ] Probar login administrativo
- [ ] Probar generación de facturas
- [ ] Verificar que PDFs se generan
- [ ] Revisar logs de errores

### Semana 1
- [ ] Monitorear velocidad de carga
- [ ] Revisar métricas de Analytics
- [ ] Verificar indexación en Google
- [ ] Revisar logs de seguridad
- [ ] Hacer backup manual

### Mes 1
- [ ] Analizar comportamiento de usuarios
- [ ] Optimizar basado en datos reales
- [ ] Ajustar SEO según keywords
- [ ] Revisar y optimizar conversiones

---

## 🛠️ COMANDOS ÚTILES

### En Producción
```bash
# Ver logs en tiempo real
tail -f /var/log/drashirley/error.log

# Reiniciar servicio
sudo systemctl restart drashirley

# Ver estado
sudo systemctl status drashirley

# Backup manual
sqlite3 drashirley_simple.db ".backup backup_manual.db"

# Optimizar BD
sqlite3 drashirley_simple.db < optimize_database.sql
```

---

## 🚨 TROUBLESHOOTING

### Si el sitio no carga
1. Verificar que el servicio está corriendo
2. Revisar logs de errores
3. Verificar permisos de archivos
4. Verificar configuración de firewall
5. Verificar DNS

### Si hay errores de BD
1. Verificar permisos del archivo .db
2. Re-ejecutar script de optimización
3. Restaurar desde backup si es necesario

### Si los PDFs no se generan
1. Verificar que ReportLab está instalado
2. Verificar permisos de escritura
3. Revisar logs de errores

---

## 📧 NOTIFICACIONES

### Email
Configurar en `.env`:
```
EMAIL_USER=info@drashirleyramirez.com
EMAIL_PASSWORD=password_de_aplicacion
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Alertas
- [ ] Errores críticos → Email inmediato
- [ ] Downtime → SMS/Email
- [ ] Backup exitoso → Email diario
- [ ] Reporte semanal → Email resumen

---

## ✅ VERIFICACIÓN FINAL

### Checklist Crítico
- [ ] ✅ Sitio accesible via HTTPS
- [ ] ✅ Certificado SSL válido
- [ ] ✅ Todas las páginas cargan
- [ ] ✅ Formularios funcionan
- [ ] ✅ Login administrativo funciona
- [ ] ✅ Sistema de facturación funciona
- [ ] ✅ PDFs se generan correctamente
- [ ] ✅ Sitemap.xml accesible
- [ ] ✅ Robots.txt accesible
- [ ] ✅ Backups configurados
- [ ] ✅ Monitoreo activo
- [ ] ✅ Google Search Console configurado

---

## 🎉 ¡LISTO!

```
┌────────────────────────────────────────┐
│                                        │
│  ✅ Sistema en Producción             │
│  🔒 Seguro                            │
│  ⚡ Rápido                            │
│  🎯 SEO Optimizado                    │
│  📊 Monitoreado                       │
│                                        │
│  🚀 OPERATIVO                         │
│                                        │
└────────────────────────────────────────┘
```

---

**Notas:**
- Este checklist debe completarse paso a paso
- Verificar cada punto antes de continuar
- Mantener backups actualizados
- Revisar logs regularmente

---

*Última actualización: 17 de Octubre, 2025*


