@echo off
echo ============================================================
echo PUBLICANDO CORRECION DE LOGIN A GIT Y RAILWAY
echo ============================================================

echo.
echo Agregando archivos...
git add app_simple.py
git add diagnostico_login_completo.py
git add resetear_admin_railway_CORRECTO.sql

echo.
echo Haciendo commit...
git commit -m "Fix: Correccion critica de password hash y normalizacion de email en login"

echo.
echo Subiendo a GitHub...
git push origin main

echo.
echo ============================================================
echo ✅ PUBLICACION COMPLETADA
echo ============================================================
echo.
echo 📋 SIGUIENTE PASO:
echo    Railway detectara los cambios automaticamente y hara redeploy
echo.
echo 🔐 Credenciales:
echo    Email: ing.fpaula@gmail.com
echo    Contrasena: 2416Xpos@
echo.
echo ============================================================
pause





