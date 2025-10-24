@echo off
SET GIT="C:\Program Files\Git\bin\git.exe"
SET GIT_PAGER=

%GIT% add static/sitemap.xml
%GIT% commit -m "SEO: Actualizar sitemap.xml con dominio correcto y fecha actual - Cambiar URLs de tu-dominio.railway.app a drashirleyramirez.com - Actualizar lastmod a 2025-10-24 - Agregar ruta tratamientos-esteticos - Corregir rutas de contact y request-appointment"
%GIT% push origin main

echo.
echo ========================================
echo SITEMAP ACTUALIZADO Y SUBIDO
echo ========================================
pause

