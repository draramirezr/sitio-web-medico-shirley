# 🚀 CONFIGURACIÓN LOCAL - Conexión a MySQL Railway

## ✅ CAMBIOS REALIZADOS

1. **Código modificado:** Ahora el aplicativo busca `MYSQL_URL` primero (no requiere `RAILWAY_ENVIRONMENT`)
2. **Archivo creado:** `local.env` con tu connection string de Railway

---

## 📋 CÓMO USAR (DESARROLLO LOCAL)

### **OPCIÓN 1: Usando el archivo local.env** (Recomendado)

1. **Renombra el archivo:**
   ```
   local.env  →  .env
   ```

2. **Ejecuta la aplicación:**
   ```bash
   python app_simple.py
   ```

3. **Verifica los logs:**
   Deberías ver:
   ```
   ✅ Configurado para usar MySQL en Railway (usando MYSQL_URL)
   🔌 Conectando a: turntable.proxy.rlwy.net
   👤 Usuario: root
   📁 Base de datos: drashirley
   ✅ Base de datos conectada: mysql
   ```

---

### **OPCIÓN 2: Configurar variable de entorno manualmente**

**En PowerShell:**
```powershell
$env:MYSQL_URL="mysql://root:koLhfNrFtiDBdXOIYCmMSOoOeERGUvsX@turntable.proxy.rlwy.net:33872/drashirley"
python app_simple.py
```

**En CMD:**
```cmd
set MYSQL_URL=mysql://root:koLhfNrFtiDBdXOIYCmMSOoOeERGUvsX@turntable.proxy.rlwy.net:33872/drashirley
python app_simple.py
```

---

## 🎯 VENTAJAS DE ESTA CONFIGURACIÓN

✅ **Desarrollo local** con base de datos real de Railway
✅ **No necesitas** tener MySQL instalado localmente
✅ **Pruebas con datos reales** antes de hacer deploy
✅ **Mismo entorno** que producción

---

## ⚠️ IMPORTANTE

- **NO subas el archivo `.env` a Git** (ya está en .gitignore)
- El archivo `local.env` es solo para referencia
- La contraseña en la URL es la misma de Railway

---

## 🔧 SI TIENES PROBLEMAS DE CONEXIÓN

1. **Verifica que el puerto esté abierto:**
   - Puerto: `33872`
   - Host: `turntable.proxy.rlwy.net`

2. **Prueba la conexión desde MySQL Workbench** (como ya lo hiciste)

3. **Verifica los logs** al iniciar la aplicación

---

## ✅ PRÓXIMOS PASOS

1. Renombra `local.env` a `.env`
2. Ejecuta `python app_simple.py`
3. Ve a `http://localhost:5000`
4. ¡Listo! Estarás usando la base de datos de Railway desde tu PC local











