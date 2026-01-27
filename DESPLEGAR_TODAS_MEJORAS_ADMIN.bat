@echo off
echo ================================================
echo   DESPLEGAR TODAS LAS MEJORAS DEL ADMIN
echo ================================================
echo.

echo Este script desplegara TODAS las mejoras aplicadas hoy:
echo.
echo ADMIN DE CITAS:
echo   - Scroll inteligente (3 citas visibles)
echo   - Boton eliminar citas
echo   - Fix contador resumen
echo   - Barra scroll personalizada
echo.
echo ADMIN DE MENSAJES:
echo   - Scroll inteligente (3 mensajes visibles)
echo   - Boton eliminar mensajes
echo   - Fix contador resumen
echo   - Indicador de leidos/sin leer
echo   - Barra scroll personalizada
echo.
echo DASHBOARD DE FACTURACION:
echo   - Montos pendientes por ARS
echo.

pause

echo.
echo [1/3] Agregando TODOS los cambios al control de versiones...
git add app_simple.py
git add templates/admin_appointments.html
git add templates/admin_messages.html
git add templates/facturacion/dashboard.html

echo.
echo [2/3] Creando commit con todas las mejoras...
git commit -m "Feature Bundle: Scroll + Eliminar + Fix en Admin Citas/Mensajes + Montos ARS"

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
echo PAGINAS MEJORADAS:
echo   - https://www.draramirez.com/admin/appointments
echo   - https://www.draramirez.com/admin/messages
echo   - https://www.draramirez.com/facturacion/dashboard
echo.
echo AHORA PODRAS:
echo   1. Ver solo 3 elementos a la vez (scroll elegante)
echo   2. Eliminar citas de Francisco Paula
echo   3. Eliminar mensajes de prueba
echo   4. Ver montos pendientes por cada ARS
echo   5. Contadores funcionando correctamente
echo.
pause
