# 🚀 Inicio Rápido - Sitio Web Dra. Shirley Ramírez

## ⚡ Instrucciones Simples

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Iniciar el Sitio

**Opción A: Usando el script (Recomendado)**
```
Doble clic en: INICIAR.bat
```

**Opción B: Desde la terminal**
```bash
python app_simple.py
```

### 3. Abrir en el Navegador
```
http://localhost:5000
```

---

## 📱 Páginas Disponibles

- **Inicio**: http://localhost:5000
- **Servicios**: http://localhost:5000/servicios
- **Sobre Mí**: http://localhost:5000/sobre-mi
- **Testimonios**: http://localhost:5000/testimonios
- **Contacto**: http://localhost:5000/contacto
- **Solicitar Cita**: http://localhost:5000/solicitar-cita
- **Panel Admin**: http://localhost:5000/admin

---

## 🔧 Personalización Rápida

### Cambiar Colores
Editar archivos en `static/css/`:
- `piggy-pink-background.css` - Color de fondo
- `silver-pink-elements.css` - Elementos
- `silver-chalice-titles.css` - Títulos

### Cambiar Contenido
Editar archivos en `templates/`:
- `index.html` - Página principal
- `services.html` - Servicios
- `about.html` - Sobre mí
- `contact.html` - Contacto

### Agregar Imágenes
Colocar imágenes en:
- `static/images/` - Imágenes generales
- `static/logos/` - Logos y favicons

---

## 📚 Documentación Completa

Ver: `README.md` para información detallada

Ver carpeta: `DOCS/` para documentación técnica

---

## 🆘 Problemas Comunes

### Python no se encuentra
```bash
# Verificar instalación de Python
python --version

# Si no está instalado, descargar desde:
# https://www.python.org/downloads/
```

### Error de dependencias
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### Puerto 5000 ocupado
```bash
# Cambiar puerto en app_simple.py (última línea)
app.run(debug=True, host='0.0.0.0', port=8000)
```

---

## ✅ Listo!

El sitio debería estar funcionando en http://localhost:5000

Para detener el servidor: **Ctrl + C** en la terminal

