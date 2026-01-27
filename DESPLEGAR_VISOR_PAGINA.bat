@echo off
echo ================================================
echo   NUEVO: Visor de Pagina - Mes de la Patria
echo ================================================
echo.

echo FUNCIONALIDAD AGREGADA:
echo   - Nuevo boton "Visor de Pagina" en panel admin
echo   - 2 opciones: Diseno Original y Mes de la Patria
echo   - Borde animado tricolor (solo cuando actives Mes de la Patria)
echo   - Control total desde el admin (sin tocar codigo)
echo.

echo ARCHIVOS MODIFICADOS:
echo   - app_simple.py (tabla + rutas + funciones)
echo   - templates/admin.html (boton nuevo)
echo   - templates/admin_visor_pagina.html (NUEVO)
echo   - templates/index.html (borde animado condicional)
echo.

pause

echo.
echo Abriendo Git Bash...
echo.
echo POR FAVOR EJECUTA ESTOS COMANDOS EN GIT BASH:
echo.
echo git add app_simple.py templates/admin.html templates/admin_visor_pagina.html templates/index.html
echo.
echo git commit -m "Feature: Visor de Pagina - Tema Mes de la Patria con borde animado"
echo.
echo git push origin main
echo.
echo.
echo Despues espera 2-3 minutos y podras usar el Visor de Pagina!
echo.
pause

start "" "C:\Program Files\Git\git-bash.exe" --cd="z:\Pagina web shirley"
