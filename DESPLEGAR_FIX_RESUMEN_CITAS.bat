@echo off
echo ================================================
echo   FIX: Resumen de Citas - Conteo Correcto
echo ================================================
echo.

echo [1/3] Agregando cambios al control de versiones...
git add templates/admin_appointments.html

echo.
echo [2/3] Creando commit...
git commit -m "Fix: Corregir conteo de citas por estado en resumen (usar nombre campo en vez de indice)"

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
echo   https://www.draramirez.com/admin/appointments
echo.
echo El resumen ahora mostrara los conteos correctos!
echo.
pause
