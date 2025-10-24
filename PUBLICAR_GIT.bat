@echo off
echo ============================================================
echo PUBLICANDO CAMBIOS EN GIT
echo ============================================================
echo.

REM Agregar todos los archivos modificados
git add .

echo.
echo Archivos agregados. Haciendo commit...
echo.

REM Commit con mensaje descriptivo
git commit -m "Fix: Migracion MySQL completa - Indices a nombres de columnas + Bug fixes"

echo.
echo Commit realizado. Subiendo a GitHub...
echo.

REM Push a la rama main
git push origin main

echo.
echo ============================================================
echo PUBLICACION COMPLETADA
echo ============================================================
echo.
pause





