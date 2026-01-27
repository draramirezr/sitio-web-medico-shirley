@echo off
echo ================================================
echo   NUEVA FUNCIONALIDAD: Eliminar Citas
echo ================================================
echo.

echo [1/3] Agregando cambios al control de versiones...
git add app_simple.py templates/admin_appointments.html

echo.
echo [2/3] Creando commit...
git commit -m "Feature: Agregar boton de eliminar citas en panel admin con confirmacion"

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
echo Ahora podras eliminar las citas de Francisco Paula desde:
echo   https://www.draramirez.com/admin/appointments
echo.
echo PASOS PARA ELIMINAR:
echo   1. Busca las citas de "Francisco Paula"
echo   2. Click en "Eliminar Cita" (boton rojo)
echo   3. Confirma la eliminacion
echo.
pause
