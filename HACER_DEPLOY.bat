@echo off
echo ========================================
echo HACIENDO COMMIT Y PUSH A RAILWAY
echo ========================================
echo.

cd /d "Z:\Pagina web shirley"

echo [1/4] Agregando archivos modificados...
"C:\Program Files\Git\bin\git.exe" add app_simple.py templates/contact.html templates/base.html static/sw.js
if errorlevel 1 (
    echo ERROR: No se pudo agregar archivos
    echo.
    echo Alternativas:
    echo 1. Abre GitHub Desktop y haz commit + push manualmente
    echo 2. Busca "Git Bash" en el menu inicio y ejecuta:
    echo    cd "Z:\Pagina web shirley"
    echo    git add .
    echo    git commit -m "Migracion MySQL completa"
    echo    git push origin main
    pause
    exit /b 1
)

echo [2/4] Haciendo commit...
"C:\Program Files\Git\bin\git.exe" commit -m "Fix: 25 placeholders SQL, remover sqlite3, fix TEXT DEFAULT - Analisis profundo"
if errorlevel 1 (
    echo.
    echo Nota: Si dice "nothing to commit", los archivos ya fueron commiteados
    echo.
)

echo [3/4] Haciendo push a GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main
if errorlevel 1 (
    echo ERROR: No se pudo hacer push
    echo.
    echo Verifica:
    echo - Que estes conectado a Internet
    echo - Que tengas permisos en el repositorio
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ DEPLOY EXITOSO!
echo ========================================
echo.
echo Railway detectara el push y hara deploy automatico (2-3 min)
echo.
echo Accede a tu URL de Railway cuando termine el deploy
echo.
pause

