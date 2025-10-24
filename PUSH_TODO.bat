@echo off
SET GIT="C:\Program Files\Git\bin\git.exe"
SET GIT_PAGER=

echo ========================================
echo SUBIENDO TODOS LOS CAMBIOS A GITHUB
echo ========================================
echo.

%GIT% add .
%GIT% commit -m "Fix Final + UX: Eliminar Panama y mejorar icono obstetricia - Corregir telefono Panama (+507) en email_templates.py - Cambiar a telefono RD: +1-829-740-5073 - Cambiar icono Consulta Obstetrica: fas fa-baby a fas fa-person-pregnant - Icono mas apropiado: mujer embarazada en vez de bebe - Agregar font-display swap completo para todas las fuentes - Actualizar sitemap.xml con dominio correcto - Script SQL y Python para actualizar icono en base de datos - 100%% referencias a Panama eliminadas"
%GIT% push origin main

echo.
echo ========================================
echo CAMBIOS SUBIDOS EXITOSAMENTE
echo ========================================
echo.
echo CAMBIOS APLICADOS:
echo [X] Telefono Panama eliminado
echo [X] Icono obstetricia mejorado (mujer embarazada)
echo [X] Font-display swap optimizado
echo [X] Sitemap actualizado
echo [X] Google Tag Manager instalado
echo.
echo PROXIMOS PASOS:
echo 1. Ejecutar: python actualizar_icono_obstetricia.py
echo    (Para actualizar el icono en la base de datos)
echo.
pause

