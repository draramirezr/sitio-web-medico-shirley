@echo off
echo ============================================================
echo   COMMIT Y PUSH - SOLUCION COMILLAS RAILWAY
echo ============================================================
echo.

echo [1/4] Agregando archivos modificados...
git add app_simple.py SOLUCION_COMILLAS_RAILWAY.md RESUMEN_SOLUCION_MYSQL.md inicializar_mysql_railway.py SOLUCION_MYSQL_RAILWAY.md debug_railway_env.py

echo [2/4] Haciendo commit...
git commit -m "fix: eliminar comillas automaticas de variables Railway + scripts diagnostico MySQL"

echo [3/4] Haciendo push a main...
git push origin main

echo.
echo ============================================================
echo   COMPLETADO
echo ============================================================
echo.
echo PROXIMOS PASOS:
echo 1. Esperar 2-3 minutos para auto-deploy en Railway
echo 2. Revisar logs en Railway Dashboard
echo 3. Buscar mensaje: "Conectando a: mysql.railway.internal"
echo 4. Verificar: "Base de datos conectada: mysql"
echo.
pause

