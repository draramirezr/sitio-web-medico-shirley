# 🚀 GUÍA RÁPIDA: Ejecutar Script SQL en MySQL Railway

## 📋 INSTRUCCIONES PASO A PASO

### 1. Abrir el archivo SQL
- Abre el archivo `export_railway_mysql.sql` en un editor de texto
- Copia **TODO** el contenido (Ctrl+A, luego Ctrl+C)

### 2. En MySQL Workbench (que ya tienes abierto)

**OPCIÓN A: Ejecutar todo el script de una vez**
1. Click en **File** → **New Query Tab** (o presiona `Ctrl+T`)
2. **Pega** el contenido del archivo SQL
3. Click en el ícono del rayo ⚡ o presiona `Ctrl+Shift+Enter` para ejecutar todo
4. Espera a que termine (debería tomar menos de 10 segundos)

**OPCIÓN B: Ejecutar línea por línea (si prefieres)**
1. Click en **File** → **Open SQL Script**
2. Selecciona `export_railway_mysql.sql`
3. Click en el ícono del rayo ⚡ para ejecutar todo

### 3. Verificar que se creó correctamente

Ejecuta esta consulta para verificar:

```sql
-- Ver todas las tablas creadas
SHOW TABLES;

-- Ver cuántos servicios hay
SELECT COUNT(*) FROM services;

-- Ver si el usuario admin existe
SELECT nombre, email, perfil FROM usuarios;
```

**Deberías ver:**
- ✅ 16 tablas creadas
- ✅ 6 servicios
- ✅ 1 usuario (Francisco Paula)

---

## ⚠️ NOTAS IMPORTANTES

1. **Este script ELIMINA todas las tablas existentes** antes de crearlas nuevamente.
   - Si tienes datos importantes, **haz un backup primero**.

2. **Usuario por defecto:**
   - Email: `ing.fpaula@gmail.com`
   - Contraseña: `2416Xpos@`

3. **¿No funciona?** Verifica que estés conectado a la base de datos `railway`.

---

## ✅ DESPUÉS DE EJECUTAR EL SCRIPT

Vuelve a Railway y verifica que la aplicación ya no muestre el error de "no such table".

Los logs deberían mostrar:
```
✅ Base de datos conectada: mysql
✅ Índices de base de datos creados/verificados
✅ Base de datos inicializada correctamente
```

---

## 🆘 SI TIENES PROBLEMAS

Copia el mensaje de error completo que aparezca en MySQL Workbench y pégalo aquí.













