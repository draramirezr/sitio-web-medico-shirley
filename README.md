# Sitio Web - Dra. Shirley Ramírez
## Ginecóloga y Obstetra

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)

---

## 📋 Descripción

Sitio web profesional para la Dra. Shirley Ramírez, especialista en Ginecología y Obstetricia. El sitio incluye información sobre servicios médicos, solicitud de citas, testimonios de pacientes y formulario de contacto.

---

## 🎨 Línea Gráfica

El sitio implementa la línea gráfica oficial con:

### Colores
- **PIGGY PINK** (#F2E2E6) - Fondo principal
- **SILVER PINK** (#CEB0B7) - Sombras y elementos
- **SILVER CHALICE** (#ACACAD) - Títulos y botones
- **RAISIN BLACK** (#282828) - Texto principal

### Tipografía
- **BLANKERS** (Montserrat) - Títulos y menús
- **BE VIETNAM PRO** - Cuerpo de texto

---

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd "Z:\Pagina web shirley"
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar el servidor**
   
   **Opción A: Usando el script batch**
   ```
   Doble clic en: INICIAR_SITIO_LINEA_GRAFICA.bat
   ```
   
   **Opción B: Desde la terminal**
   ```bash
   python app_simple.py
   ```

4. **Abrir en navegador**
   ```
   http://localhost:5000
   ```

---

## 📁 Estructura del Proyecto

```
Pagina web shirley/
│
├── app_simple.py              # Aplicación Flask principal
├── requirements.txt           # Dependencias del proyecto
├── drashirley_simple.db      # Base de datos SQLite
├── env_example.txt           # Ejemplo de variables de entorno
│
├── static/                    # Archivos estáticos
│   ├── css/                  # Hojas de estilo
│   │   ├── typography.css    # Tipografías BLANKERS y BE VIETNAM
│   │   ├── piggy-pink-background.css
│   │   ├── silver-pink-elements.css
│   │   ├── silver-chalice-titles.css
│   │   └── custom-colors.css
│   │
│   ├── images/               # Imágenes del sitio
│   ├── logos/                # Logos y favicons
│   └── uploads/              # Archivos subidos
│
├── templates/                 # Plantillas HTML
│   ├── base.html             # Plantilla base
│   ├── index.html            # Página principal
│   ├── services.html         # Servicios médicos
│   ├── about.html            # Sobre la doctora
│   ├── testimonials.html     # Testimonios
│   ├── contact.html          # Contacto
│   ├── request_appointment.html  # Solicitar cita
│   └── admin.html            # Panel administrativo
│
├── RECURSOS/                  # Recursos de diseño
│   ├── ENTREGABLES/          # Logos, iconos, documentos
│   └── sesion de fotos/      # Fotografías profesionales
│
└── DOCS/                      # Documentación
    ├── LINEA_GRAFICA_IMPLEMENTADA.md
    ├── TIPOGRAFIA_INSTRUCCIONES.md
    └── RESUMEN_CAMBIOS_LINEA_GRAFICA.md
```

---

## 🌟 Características

### Páginas Principales

✅ **Inicio**
- Hero section con información destacada
- Servicios principales
- Testimonios de pacientes
- Llamadas a la acción

✅ **Servicios**
- Consulta Ginecológica
- Consulta Obstétrica
- Ecografías
- Ginecología Estética
- Cirugía Ginecológica
- Planificación Familiar

✅ **Sobre Mí**
- Información profesional de la Dra. Shirley
- Especialidades y certificaciones
- Experiencia y trayectoria

✅ **Testimonios**
- Experiencias de pacientes
- Sistema de calificación
- Comentarios verificados

✅ **Contacto**
- Formulario de contacto
- Información de ubicación
- Horarios de atención
- Teléfono y email

✅ **Solicitar Cita**
- Formulario de solicitud
- Selección de tipo de consulta
- Calendario de disponibilidad

✅ **Panel Admin** (`/admin`)
- Gestión de citas
- Mensajes de contacto
- Estadísticas del sitio

### Funcionalidades Técnicas

- 🎨 Diseño responsive (móvil, tablet, desktop)
- ⚡ Carga rápida y optimizada
- 🔒 Base de datos SQLite integrada
- 📧 Sistema de mensajes de contacto
- 📅 Gestión de citas
- 💬 Sistema de testimonios
- 🔍 SEO optimizado
- ♿ Accesible (WCAG 2.1)

---

## 🎯 Base de Datos

El sitio utiliza SQLite con las siguientes tablas:

- **services** - Servicios médicos ofrecidos
- **testimonials** - Testimonios de pacientes
- **contact_messages** - Mensajes del formulario de contacto
- **appointments** - Citas solicitadas

La base de datos se crea automáticamente al iniciar la aplicación por primera vez.

---

## 🔧 Configuración

### Variables de Entorno (Opcional)

Crear un archivo `.env` basado en `env_example.txt`:

```env
SECRET_KEY=tu-clave-secreta-segura
DATABASE_URL=drashirley_simple.db
DEBUG=False
```

### Personalización de Colores

Editar archivos en `static/css/`:
- `piggy-pink-background.css` - Color de fondo
- `silver-pink-elements.css` - Elementos y sombras
- `silver-chalice-titles.css` - Títulos y botones

### Personalización de Tipografía

Ver: `DOCS/TIPOGRAFIA_INSTRUCCIONES.md`

---

## 📱 Responsive Design

El sitio está optimizado para:
- 📱 Móviles (≤ 576px)
- 📱 Tablets (≤ 768px)
- 💻 Desktop (> 768px)

---

## 🌐 Navegadores Soportados

- ✅ Google Chrome (últimas 2 versiones)
- ✅ Mozilla Firefox (últimas 2 versiones)
- ✅ Microsoft Edge (últimas 2 versiones)
- ✅ Safari (últimas 2 versiones)
- ✅ Navegadores móviles (iOS/Android)

---

## 📚 Documentación Adicional

- 📖 [Línea Gráfica Implementada](DOCS/LINEA_GRAFICA_IMPLEMENTADA.md)
- 📖 [Instrucciones de Tipografía](DOCS/TIPOGRAFIA_INSTRUCCIONES.md)
- 📖 [Resumen de Cambios](DOCS/RESUMEN_CAMBIOS_LINEA_GRAFICA.md)

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 2.3+** - Framework web
- **SQLite 3** - Base de datos
- **Python 3.8+** - Lenguaje de programación

### Frontend
- **Bootstrap 5.3** - Framework CSS
- **Font Awesome 6.4** - Iconos
- **JavaScript ES6+** - Interactividad
- **Google Fonts** - Tipografías

### Tipografías
- **Montserrat** (alternativa a BLANKERS)
- **Be Vietnam Pro**

---

## 📞 Información de Contacto

**Dra. Shirley Ramírez**
- 📍 Centro Oriental de Ginecología y Obstetricia, Zona Oriental
- 📱 (829) 740-5073
- 📧 dra.ramirezr@gmail.com
- ⏰ Lun - Vie: 8:00 - 18:00

---

## 🚨 Panel de Administración

Acceder al panel admin en: `http://localhost:5000/admin`

**Funcionalidades:**
- Ver estadísticas del sitio
- Gestionar citas pendientes
- Revisar mensajes de contacto
- Aprobar testimonios
- Gestionar servicios

---

## 🔄 Actualizaciones

### Versión 1.0 (Octubre 2025)
- ✅ Implementación de línea gráfica oficial
- ✅ Diseño responsive completo
- ✅ Sistema de citas y contacto
- ✅ Panel administrativo
- ✅ Optimización de rendimiento

---

## 📝 Licencia

Este proyecto es privado y confidencial. Todos los derechos reservados © 2024 Dra. Shirley Ramírez.

---

## 🆘 Soporte

Para soporte técnico o consultas:
1. Revisar la documentación en la carpeta `DOCS/`
2. Verificar que todas las dependencias estén instaladas
3. Asegurar que Python 3.8+ esté instalado

---

## 🎉 ¡Gracias!

Sitio web desarrollado con ❤️ para la Dra. Shirley Ramírez
