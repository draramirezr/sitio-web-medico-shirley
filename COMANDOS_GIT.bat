@echo off
echo ========================================
echo   COMANDOS GIT PARA DEPLOYMENT
echo ========================================
echo.
echo OPCION 1: Si tienes GitHub Desktop o Git GUI
echo   - Abrir la aplicacion
echo   - Stage todos los archivos
echo   - Commit con mensaje: "Fix: Iconos de servicios + Mejoras CSP y optimizacion"
echo   - Push
echo.
echo OPCION 2: Si tienes Git Bash instalado
echo   - Abrir Git Bash en esta carpeta
echo   - Copiar y pegar los comandos de abajo:
echo.
echo   git add app_simple.py
echo   git add templates/base.html
echo   git add templates/services.html  
echo   git add templates/test_icons.html
echo   git add actualizar_iconos_servicios.py
echo   git add CHANGELOG_ICONOS.md
echo   git add INSTRUCCIONES_DEPLOYMENT.md
echo   git add RESUMEN_FINAL_DEPLOYMENT.txt
echo   git commit -m "Fix: Iconos de servicios + Mejoras CSP y optimizacion"
echo   git push origin main
echo.
echo OPCION 3: Visual Studio Code
echo   - Presionar Ctrl+Shift+G
echo   - Click en + para stage
echo   - Escribir mensaje de commit
echo   - Click en checkmark para commit
echo   - Click en ... ^> Push
echo.
echo ========================================
echo   DESPUES DE PUSH A GIT
echo ========================================
echo.
echo 1. Railway hara auto-deploy (esperar 5-10 min)
echo 2. IMPORTANTE: Ejecutar en Railway:
echo    python actualizar_iconos_servicios.py
echo 3. Verificar sitio funcionando
echo.
echo ========================================
pause







