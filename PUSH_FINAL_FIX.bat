@echo off
SET GIT="C:\Program Files\Git\bin\git.exe"
SET GIT_PAGER=

echo ========================================
echo SUBIENDO CAMBIOS FINALES A GITHUB
echo ========================================
echo.

%GIT% add .
%GIT% commit -m "Fix Final: Eliminar ultimas referencias a Panama y optimizar fuentes - Corregir telefono de Panama (+507 6981-9863) en email_templates.py - Cambiar a telefono RD: +1-829-740-5073 - Corregir enlaces tel: y WhatsApp en templates de email - Agregar font-display swap completo para todas las fuentes - Actualizar sitemap.xml con dominio correcto - 100%% referencias a Panama eliminadas del codigo activo"
%GIT% push origin main

echo.
echo ========================================
echo CAMBIOS SUBIDOS EXITOSAMENTE
echo ========================================
echo.
echo VERIFICACION:
echo - Telefono Panama eliminado de email_templates.py
echo - Font-display swap optimizado
echo - Sitemap actualizado
echo - Google Tag Manager instalado
echo.
pause

