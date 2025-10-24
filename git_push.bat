@echo off
echo ========================================
echo PUSH DE CAMBIOS AL REPOSITORIO
echo ========================================
echo.

cd /d "Z:\Pagina web shirley"

echo [1/4] Verificando estado de Git...
git status
echo.

echo [2/4] Agregando archivos modificados...
git add app_simple.py
git add templates/facturacion/ver_factura.html
git add templates/facturacion/dashboard.html
echo.

echo [3/4] Creando commit...
git commit -m "Fix: Corregir placeholders MySQL y mejorar dashboard de facturacion - Corregir TypeError: cambiar placeholders de SQLite (?) a MySQL (%%s) en 11 instancias - Agregar campo RNC en queries de PDF de facturas - Actualizar botones de factura con colores de linea grafica - Agregar grafico Facturacion por ARS y Mes con lineas multiples - Transformar grafico Facturacion por Medico a barras agrupadas por mes - Eliminar grafico redundante de Facturacion por ARS - Mejorar interactividad con tooltips y clicks en graficos"
echo.

echo [4/4] Enviando cambios al repositorio...
git push
echo.

echo ========================================
echo PROCESO COMPLETADO
echo ========================================
pause



