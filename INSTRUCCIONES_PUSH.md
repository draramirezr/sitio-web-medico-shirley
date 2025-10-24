# 🚀 INSTRUCCIONES PARA HACER PUSH

## ⚠️ Git no está configurado en el PATH del sistema

Para hacer el push de los cambios realizados, sigue estos pasos:

---

## 📝 CAMBIOS REALIZADOS HOY:

### Archivos modificados:
1. ✅ `app_simple.py`
2. ✅ `templates/facturacion/ver_factura.html`
3. ✅ `templates/facturacion/dashboard.html`

---

## 🔧 OPCIÓN 1: Usar Git Bash (Recomendado)

1. **Abrir Git Bash** en la carpeta del proyecto
2. Ejecutar estos comandos:

```bash
# Verificar estado
git status

# Agregar archivos modificados
git add app_simple.py
git add templates/facturacion/ver_factura.html
git add templates/facturacion/dashboard.html

# Crear commit
git commit -m "Fix: Corregir placeholders MySQL y mejorar dashboard de facturacion

- Corregir TypeError: cambiar placeholders de SQLite (?) a MySQL (%s) en 11 instancias
- Agregar campo RNC en queries de PDF de facturas (6 queries actualizadas)
- Actualizar botones de email/PDF con colores de linea grafica (#CEB0B7)
- Agregar grafico interactivo: Facturacion por ARS y Mes (lineas multiples)
- Transformar grafico: Facturacion por Medico a barras agrupadas por mes
- Eliminar grafico redundante de Facturacion por ARS
- Mejorar interactividad: tooltips y clicks en graficos del dashboard"

# Hacer push
git push
```

---

## 🔧 OPCIÓN 2: Usar GitHub Desktop

1. Abrir **GitHub Desktop**
2. Verás 3 archivos modificados en el panel izquierdo
3. Escribe el mensaje del commit:
   ```
   Fix: Corregir placeholders MySQL y mejorar dashboard de facturacion
   ```
4. Click en **"Commit to main"**
5. Click en **"Push origin"**

---

## 🔧 OPCIÓN 3: Usar Visual Studio Code

1. Abrir VS Code en la carpeta del proyecto
2. Click en el icono de Source Control (Ctrl+Shift+G)
3. Verás los archivos modificados
4. Click en el **+** junto a cada archivo para "Stage"
5. Escribe el mensaje del commit en el cuadro de texto
6. Click en el ✓ (checkmark) para hacer commit
7. Click en **"..."** → **"Push"**

---

## 📋 MENSAJE DEL COMMIT (Copiar y pegar):

```
Fix: Corregir placeholders MySQL y mejorar dashboard de facturacion

Correcciones críticas:
- Fix TypeError: cambiar placeholders SQLite (?) a MySQL (%s) - 11 instancias
- Fix PDF: agregar campo RNC en 6 queries de generación de facturas

Mejoras de interfaz:
- Botones email/PDF con colores de línea gráfica (#CEB0B7)
- Modal de email con título e ícono en blanco

Dashboard de facturación:
- Nuevo: Gráfico "Facturación por ARS y Mes" (líneas múltiples)
- Mejorado: Gráfico "Facturación por Médico" (barras agrupadas por mes)
- Eliminado: Gráfico redundante "Facturación por ARS"
- Interactividad: Tooltips y clicks con información detallada

Archivos modificados:
- app_simple.py
- templates/facturacion/ver_factura.html
- templates/facturacion/dashboard.html
```

---

## ✅ VERIFICACIÓN ANTES DEL PUSH:

- [x] Sin errores de lint
- [x] Código probado localmente
- [x] Queries MySQL correctas
- [x] Dashboard funcionando
- [x] PDFs generando correctamente

---

## 🎯 DESPUÉS DEL PUSH:

Si tu proyecto está en **Railway** u otro servicio de deployment:
1. El push automáticamente disparará un nuevo deploy
2. Espera 2-5 minutos para que se complete
3. Verifica que todo funcione en producción

---

## 📞 ¿PROBLEMAS?

Si tienes problemas con Git:
1. Verifica que Git esté instalado: https://git-scm.com/download/win
2. Reinicia tu terminal/PowerShell después de instalar
3. Configura Git si es primera vez:
   ```bash
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu@email.com"
   ```

---

**¡Todo está listo para hacer push! 🚀**



