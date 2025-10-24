@echo off
SET GIT="C:\Program Files\Git\bin\git.exe"
SET GIT_PAGER=

%GIT% add -A
%GIT% commit -m "Analytics + Performance: Instalar Google Tag Manager y optimizaciones PageSpeed - Agregar Google Tag Manager (GTM-TW8956LR) en head y body - Crear CSS minificado responsive-enhanced.min.css - Implementar font-display swap para Font Awesome - Agregar preload hints para recursos criticos - Optimizar carga diferida de CSS no critico - DNS prefetch y preconnect para CDNs externos - Documentacion en OPTIMIZACIONES_PERFORMANCE_PAGESPEED.md"
%GIT% push origin main

echo.
echo ========================================
echo COMMIT Y PUSH COMPLETADOS
echo ========================================
pause

