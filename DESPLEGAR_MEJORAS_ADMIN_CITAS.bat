@echo off
echo ================================================
echo   MEJORAS ADMIN CITAS: Scroll + Eliminar + Fix
echo ================================================
echo.

echo Cambios incluidos:
echo   1. Solo 3 citas visibles (scroll para ver mas)
echo   2. Barra de scroll personalizada elegante
echo   3. Indicador de total de citas
echo   4. Boton para eliminar citas
echo   5. Fix: Conteo correcto del resumen
echo.

echo [1/3] Agregando cambios al control de versiones...
git add app_simple.py templates/admin_appointments.html

echo.
echo [2/3] Creando commit...
git commit -m "Feature: Scroll en admin citas + boton eliminar + fix conteo resumen"

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
echo MEJORAS APLICADAS:
echo   - Ahora solo veras 3 citas a la vez
echo   - Scroll elegante para ver las demas
echo   - Boton rojo para eliminar citas
echo   - Contador del resumen funcionando
echo.
echo Visita: https://www.draramirez.com/admin/appointments
echo.
pause
