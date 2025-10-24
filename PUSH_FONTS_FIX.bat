@echo off
SET GIT="C:\Program Files\Git\bin\git.exe"
SET GIT_PAGER=

echo ========================================
echo SUBIENDO CAMBIOS A GITHUB
echo ========================================
echo.

%GIT% add .
%GIT% commit -m "Performance: Mejorar font-display swap para todas las fuentes - Agregar @font-face con font-display swap para Font Awesome 6 (Free y Brands) - Agregar font-display swap para Google Fonts (Poppins y Playfair Display) - Actualizar sitemap.xml con dominio correcto drashirleyramirez.com - Mejora esperada: 40ms adicionales en FCP (First Contentful Paint) - Resolver completamente warning de Visualizacion de fuentes en PageSpeed"
%GIT% push origin main

echo.
echo ========================================
echo CAMBIOS SUBIDOS EXITOSAMENTE
echo ========================================
echo.
pause

