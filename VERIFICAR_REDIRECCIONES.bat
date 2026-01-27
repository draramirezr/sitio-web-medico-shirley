@echo off
echo ================================================
echo   VERIFICAR REDIRECCIONES 301
echo ================================================
echo.

echo Probando: http://draramirez.com
echo.
curl -I http://draramirez.com
echo.
echo ================================================
echo.

echo Probando: http://www.draramirez.com
echo.
curl -I http://www.draramirez.com
echo.
echo ================================================
echo.

echo Probando: https://draramirez.com
echo.
curl -I https://draramirez.com
echo.
echo ================================================
echo.

echo Busca estas lineas en cada resultado:
echo   - HTTP/1.1 301 Moved Permanently
echo   - Location: https://www.draramirez.com/
echo.
pause

