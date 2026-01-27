@echo off
echo ================================================
echo   HOTFIX URGENTE - SITIO CAIDO
echo ================================================
echo.
echo El sitio tiene bucle de redireccion infinito
echo YA deshabilite el codigo problematico
echo.
echo ESTE SCRIPT RESTAURARA EL SITIO
echo.
pause

echo.
echo Abriendo Git Bash...
echo.
echo POR FAVOR EJECUTA ESTOS COMANDOS EN GIT BASH:
echo.
echo git add app_simple.py
echo git commit -m "HOTFIX: Deshabilitar redireccion HTTPS - Bucle infinito"
echo git push origin main
echo.
echo.
echo Despues espera 2 minutos y el sitio volvera a funcionar
echo.
pause

start "" "C:\Program Files\Git\git-bash.exe" --cd="z:\Pagina web shirley"
