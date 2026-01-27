@echo off
echo ================================================
echo   MEJORAS ADMIN MENSAJES: Scroll + Eliminar + Fix
echo ================================================
echo.

echo Cambios incluidos:
echo   1. Solo 3 mensajes visibles (scroll para ver mas)
echo   2. Barra de scroll personalizada elegante
echo   3. Indicador de total de mensajes (leidos/sin leer)
echo   4. Boton para eliminar mensajes
echo   5. Fix: Conteo correcto del resumen
echo.

echo [1/3] Agregando cambios al control de versiones...
git add app_simple.py templates/admin_messages.html

echo.
echo [2/3] Creando commit...
git commit -m "Feature: Scroll en admin mensajes + boton eliminar + fix conteo resumen"

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
echo   - Ahora solo veras 3 mensajes a la vez
echo   - Scroll elegante para ver los demas
echo   - Indicador de leidos vs sin leer en la parte superior
echo   - Boton rojo para eliminar mensajes
echo   - Contador del resumen funcionando correctamente
echo.
echo Visita: https://www.draramirez.com/admin/messages
echo.
pause
