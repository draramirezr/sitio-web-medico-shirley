@echo off
echo ================================================
echo   FIX CRITICO: Perdida de Sesion al Navegar
echo ================================================
echo.

echo PROBLEMA IDENTIFICADO:
echo   - Usuarios pierden sesion al navegar entre menus
echo   - Tienen que hacer login multiples veces
echo   - Causado por redirecciones HTTPS + cookie domain
echo.

echo SOLUCION APLICADA:
echo   1. Cookie domain configurado (.draramirez.com)
echo   2. Usuarios autenticados NO son redirigidos
echo   3. LoginManager con proteccion fuerte
echo   4. Sesion se mantiene al navegar
echo.

pause

echo.
echo [1/3] Agregando cambios al control de versiones...
git add app_simple.py

echo.
echo [2/3] Creando commit...
git commit -m "Fix CRITICAL: Perdida de sesion - Cookie domain + excluir usuarios auth de redireccion"

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
echo PRUEBA EL FIX:
echo   1. Ir a https://www.draramirez.com/login
echo   2. Iniciar sesion
echo   3. Navegar a /admin/appointments
echo   4. Navegar a /admin/messages
echo   5. Navegar a /facturacion/dashboard
echo.
echo RESULTADO ESPERADO:
echo   - NO debe pedir login en ningun momento
echo   - Navegacion fluida sin interrupciones
echo   - Sesion se mantiene estable
echo.
echo Si el problema persiste:
echo   1. Limpiar cookies del navegador
echo   2. Hacer login de nuevo
echo   3. Probar navegacion
echo.
pause
