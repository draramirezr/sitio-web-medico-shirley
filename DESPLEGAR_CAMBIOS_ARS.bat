@echo off
echo ================================================
echo   DESPLEGAR MEJORA: ARS con Montos Pendientes
echo ================================================
echo.

echo [1/3] Agregando cambios al control de versiones...
git add app_simple.py templates/facturacion/dashboard.html

echo.
echo [2/3] Creando commit...
git commit -m "Feature: Mostrar monto pendiente por ARS en Dashboard de Facturacion"

echo.
echo [3/3] Subiendo a Railway...
git push origin main

echo.
echo ================================================
echo   DESPLIEGUE COMPLETADO
echo ================================================
echo.
echo Espera 2-3 minutos para que Railway actualice.
echo.
echo Luego visita:
echo   https://www.draramirez.com/facturacion/dashboard
echo.
echo Y veras los montos pendientes por cada ARS!
echo.
pause
