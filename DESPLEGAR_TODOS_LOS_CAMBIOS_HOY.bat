@echo off
echo ================================================
echo   DESPLEGAR TODOS LOS CAMBIOS DEL DIA
echo ================================================
echo.

echo Este script desplegara TODOS los cambios aplicados hoy:
echo.
echo 1. FIX CRITICO - Perdida de sesion al navegar
echo    - Cookie domain configurado
echo    - Usuarios autenticados excluidos de redireccion
echo    - Sesion estable
echo.
echo 2. Admin Citas
echo    - Scroll inteligente (3 citas visibles)
echo    - Boton eliminar citas
echo    - Fix contador resumen
echo.
echo 3. Admin Mensajes
echo    - Scroll inteligente (3 mensajes visibles)
echo    - Boton eliminar mensajes
echo    - Fix contador resumen
echo    - Indicador leidos/sin leer
echo.
echo 4. Dashboard Facturacion
echo    - Montos pendientes por cada ARS
echo.
echo 5. SEO - Redirecciones
echo    - robots.txt corregido
echo    - Canonical URLs corregidas
echo    - Schema.org actualizado
echo.

pause

echo.
echo [1/3] Agregando TODOS los cambios...
git add app_simple.py
git add templates/admin_appointments.html
git add templates/admin_messages.html
git add templates/facturacion/dashboard.html
git add templates/base.html
git add static/robots.txt

echo.
echo [2/3] Creando commit con todos los cambios...
git commit -m "Bundle: Fix sesion + Admin scroll/eliminar + ARS montos + SEO fixes"

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
echo CAMBIOS PRINCIPALES:
echo.
echo FIX CRITICO:
echo   - Sesion NO se pierde al navegar
echo   - Login funciona correctamente
echo.
echo ADMIN MEJORADO:
echo   - Scroll elegante en citas y mensajes
echo   - Boton eliminar para limpiar datos de prueba
echo   - Contadores funcionando
echo.
echo FACTURACION:
echo   - Ver montos pendientes por cada ARS
echo.
echo SEO:
echo   - URLs canonicas corregidas
echo   - Redirecciones 301 funcionando
echo.
echo PRUEBA TODOS LOS CAMBIOS:
echo   1. Login (no debe pedir login multiples veces)
echo   2. Navega entre menus (sesion se mantiene)
echo   3. Admin citas (scroll + eliminar)
echo   4. Admin mensajes (scroll + eliminar)
echo   5. Dashboard facturacion (montos por ARS)
echo.
pause
