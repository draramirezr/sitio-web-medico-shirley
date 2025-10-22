# Versión simplificada del sitio web médico
# Dra. Shirley Ramírez - Ginecóloga y Obstetra

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, send_file, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import secrets
import re
from markupsafe import escape
from io import BytesIO

# Importar templates de email
from email_templates import (
    template_contacto,
    template_cita,
    template_recuperacion,
    template_constancia_pdf,
    template_factura,
    template_confirmacion_cita
)

# Importar Flask-Compress de forma opcional
try:
    from flask_compress import Compress
    COMPRESS_AVAILABLE = True
except ImportError:
    COMPRESS_AVAILABLE = False
    print("⚠️  Flask-Compress no disponible. Instalar con: pip install Flask-Compress")

# Rate limiting simple (sin dependencias externas)
from collections import defaultdict
from threading import Lock
from functools import wraps

# Almacén de intentos de login
login_attempts = defaultdict(list)
login_attempts_lock = Lock()

# Importar middleware de seguridad
try:
    from security_middleware import add_security_headers, rate_limit, log_security_event
    SECURITY_MIDDLEWARE_AVAILABLE = True
except ImportError:
    SECURITY_MIDDLEWARE_AVAILABLE = False
    print("⚠️  Security middleware no disponible")

# Importar ReportLab de forma opcional
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️  ReportLab no disponible. Instalar con: pip install reportlab")

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# ============================================
# CONFIGURACIÓN DE SEGURIDAD CRÍTICA
# ============================================

# Clave secreta segura (Railway proporcionará SECRET_KEY)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Configuración de seguridad y sesiones
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'  # True en producción
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
app.config['REMEMBER_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

# Headers de seguridad
@app.after_request
def security_headers(response):
    """Agregar headers de seguridad críticos"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self';"
    return response

# Configuración adicional de sesiones
app.config['SESSION_COOKIE_NAME'] = 'drashirley_session'
app.config['SESSION_REFRESH_EACH_REQUEST'] = True  # Renovar sesión en cada request

# ============================================
# RATE LIMITING Y VALIDACIÓN DE ENTRADA
# ============================================

from collections import defaultdict
from threading import Lock
import time

# Rate limiting simple
request_counts = defaultdict(list)
rate_limit_lock = Lock()

def rate_limit(max_requests=10, window=60):
    """Decorador para rate limiting"""
    def decorator(f):
        def rate_limit_wrapper(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            with rate_limit_lock:
                # Limpiar requests antiguos
                request_counts[client_ip] = [
                    req_time for req_time in request_counts[client_ip]
                    if current_time - req_time < window
                ]
                
                # Verificar límite
                if len(request_counts[client_ip]) >= max_requests:
                    return jsonify({'error': 'Rate limit exceeded'}), 429
                
                # Agregar request actual
                request_counts[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        return rate_limit_wrapper
    return decorator

def sanitize_input(text):
    """Sanitizar entrada de usuario"""
    if not text:
        return ""
    return escape(str(text).strip())

def validate_email(email):
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = None  # Desactivar mensaje automático para evitar duplicación
login_manager.login_message_category = 'warning'

# Configuración de compresión Gzip/Brotli para máxima velocidad
if COMPRESS_AVAILABLE:
    app.config['COMPRESS_MIMETYPES'] = [
        'text/html', 'text/css', 'text/xml', 'application/json',
        'application/javascript', 'application/x-javascript', 'text/javascript'
    ]
    app.config['COMPRESS_LEVEL'] = 6  # Balance entre velocidad y compresión
    app.config['COMPRESS_MIN_SIZE'] = 500  # Comprimir archivos > 500 bytes
    Compress(app)
    print("✅ Flask-Compress activado: Compresión Gzip/Brotli habilitada")
else:
    print("⚠️  Flask-Compress no activado: El sitio funcionará sin compresión automática")

# Headers de seguridad y optimización de cache
@app.after_request
def add_security_and_cache_headers(response):
    """Agregar headers de seguridad HTTP y cache optimizado"""
    # Seguridad
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    # Cache agresivo para recursos estáticos (máxima velocidad)
    if request.path.startswith('/static/'):
        # Cache de 1 año para CSS, JS, imágenes
        if any(request.path.endswith(ext) for ext in ['.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf']):
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
            response.headers['Expires'] = (datetime.utcnow() + timedelta(days=365)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        else:
            response.headers['Cache-Control'] = 'public, max-age=86400'  # 1 día para otros
    else:
        # NO cachear páginas que requieren sesión activa (login, admin, facturación)
        if any(request.path.startswith(path) for path in ['/login', '/admin', '/facturacion']):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        # Para otras páginas HTML: cache corto con revalidación
        elif response.content_type and 'text/html' in response.content_type:
            response.headers['Cache-Control'] = 'public, max-age=300, must-revalidate'  # 5 minutos
        else:
            response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    
    # ETag para validación eficiente de cache
    if not response.headers.get('ETag') and response.content_type and 'text/html' in response.content_type:
        response.add_etag()
    
    return response

# Configuración de email
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', 'dra.ramirezr@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_DESTINATARIO = os.getenv('EMAIL_DESTINATARIO', 'dra.ramirezr@gmail.com')

# Configuración de la base de datos
DATABASE = 'drashirley_simple.db'

# Funciones de validación y sanitización
def sanitize_input(text, max_length=500):
    """Sanitizar entrada de texto"""
    if not text:
        return ""
    text = str(text).strip()
    text = re.sub(r'<[^>]*>', '', text)  # Remover tags HTML
    return text[:max_length]

def validate_email(email):
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validar formato de teléfono"""
    phone = re.sub(r'[^\d+]', '', phone)
    return len(phone) >= 10 and len(phone) <= 15

def validar_password_segura(password):
    """Validar que la contraseña cumpla con los requisitos de seguridad"""
    errores = []
    
    if len(password) < 8:
        errores.append("Mínimo 8 caracteres")
    
    if not re.search(r'[A-Z]', password):
        errores.append("Al menos una mayúscula")
    
    if not re.search(r'[a-z]', password):
        errores.append("Al menos una minúscula")
    
    if not re.search(r'\d', password):
        errores.append("Al menos un número")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errores.append("Al menos un carácter especial")
    
    return errores

# Filtro personalizado para formatear moneda
@app.template_filter('formato_moneda')
def formato_moneda(valor):
    """Formatear números con coma para miles y punto para decimales
    Ejemplo: 1000.50 -> 1,000.50
    """
    try:
        # Convertir a float si es necesario
        if isinstance(valor, str):
            valor = float(valor)
        # Formatear con 2 decimales, coma para miles y punto para decimales
        return "{:,.2f}".format(float(valor))
    except (ValueError, TypeError):
        return "0.00"

# Modelo de Usuario para Flask-Login
class User(UserMixin):
    def __init__(self, id, nombre, email, perfil):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.perfil = perfil

@login_manager.user_loader
def load_user(user_id):
    """Cargar usuario desde la base de datos"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # Verificar que el usuario existe Y está activo
        cursor.execute('SELECT id, nombre, email, perfil, activo FROM usuarios WHERE id = ? AND activo = 1', (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return User(
                id=user_data['id'], 
                nombre=user_data['nombre'], 
                email=user_data['email'], 
                perfil=user_data['perfil']
            )
        return None
    except Exception as e:
        print(f"Error en load_user: {e}")
        return None

def init_db():
    """Inicializar la base de datos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabla de servicios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT,
            price_range TEXT,
            duration TEXT,
            active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Tabla de usuarios para autenticación
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            perfil TEXT NOT NULL CHECK(perfil IN ('Administrador', 'Registro de Facturas')),
            activo BOOLEAN DEFAULT 1,
            password_temporal BOOLEAN DEFAULT 0,
            token_recuperacion TEXT,
            token_expiracion TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Tabla de testimonios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS testimonials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            patient_initials TEXT,
            testimonial_text TEXT NOT NULL,
            rating INTEGER DEFAULT 5,
            approved BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            display_date DATE
        )
    ''')
    
    # Tabla de mensajes de contacto
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de citas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT NOT NULL,
            appointment_date TEXT,
            appointment_time TEXT,
            appointment_type TEXT NOT NULL,
            medical_insurance TEXT NOT NULL,
            emergency_datetime TEXT,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Verificar si la columna medical_insurance existe, si no, agregarla
    try:
        cursor.execute("SELECT medical_insurance FROM appointments LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE appointments ADD COLUMN medical_insurance TEXT NOT NULL DEFAULT 'Otros'")
        print("✅ Columna 'medical_insurance' agregada a la tabla appointments")
    
    # Verificar si la columna appointment_time existe, si no, agregarla
    try:
        cursor.execute("SELECT appointment_time FROM appointments LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE appointments ADD COLUMN appointment_time TEXT DEFAULT ''")
        print("✅ Columna 'appointment_time' agregada a la tabla appointments")
    
    # Verificar si la columna emergency_datetime existe, si no, agregarla
    try:
        cursor.execute("SELECT emergency_datetime FROM appointments LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE appointments ADD COLUMN emergency_datetime TEXT DEFAULT ''")
        print("✅ Columna 'emergency_datetime' agregada a la tabla appointments")
    
    # Tabla de tratamientos estéticos ginecológicos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aesthetic_treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de contador de visitas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS site_visits (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            total_visits INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Inicializar contador si no existe
    cursor.execute('INSERT OR IGNORE INTO site_visits (id, total_visits) VALUES (1, 0)')
    
    # ============ TABLAS DE FACTURACIÓN ============
    
    # Tabla de ARS (Administradoras de Riesgos de Salud)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_ars TEXT NOT NULL,
            rnc TEXT NOT NULL,
            activo BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de Médicos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            cedula TEXT NOT NULL UNIQUE,
            email TEXT,
            activo BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Agregar columna email si no existe
    try:
        cursor.execute("SELECT email FROM medicos LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE medicos ADD COLUMN email TEXT")
        print("✅ Columna 'email' agregada a la tabla medicos")
    
    # Agregar columna exequatur si no existe
    try:
        cursor.execute("SELECT exequatur FROM medicos LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE medicos ADD COLUMN exequatur TEXT")
        print("✅ Columna 'exequatur' agregada a la tabla medicos")
    
    # Agregar columna factura si no existe (indica si está habilitado para facturar)
    try:
        cursor.execute("SELECT factura FROM medicos LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE medicos ADD COLUMN factura BOOLEAN DEFAULT 0")
        print("✅ Columna 'factura' agregada a la tabla medicos")
    
    # Agregar columnas ncf_id y ncf_numero a facturas si no existen
    try:
        cursor.execute("SELECT ncf_id FROM facturas LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE facturas ADD COLUMN ncf_id INTEGER")
        print("✅ Columna 'ncf_id' agregada a la tabla facturas")
    
    try:
        cursor.execute("SELECT ncf_numero FROM facturas LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE facturas ADD COLUMN ncf_numero TEXT")
        print("✅ Columna 'ncf_numero' agregada a la tabla facturas")
    
    # Agregar columna fecha_fin a NCF si no existe
    try:
        cursor.execute("SELECT fecha_fin FROM ncf LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE ncf ADD COLUMN fecha_fin DATE")
        print("✅ Columna 'fecha_fin' agregada a la tabla ncf")
    
    # Agregar columna password_temporal a usuarios si no existe
    try:
        cursor.execute("SELECT password_temporal FROM usuarios LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN password_temporal BOOLEAN DEFAULT 0")
        print("✅ Columna 'password_temporal' agregada a la tabla usuarios")
    
    # Crear índices para optimizar consultas
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_facturas_detalle_estado ON facturas_detalle(estado)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_facturas_detalle_factura_id ON facturas_detalle(factura_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_facturas_detalle_medico_id ON facturas_detalle(medico_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_facturas_detalle_ars_id ON facturas_detalle(ars_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_facturas_fecha ON facturas(fecha_factura)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_contact_messages_read ON contact_messages(read)")
    print("✅ Índices de base de datos creados/verificados")
    
    # Tabla de Código ARS (relación médico-ars con su código)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS codigo_ars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medico_id INTEGER NOT NULL,
            ars_id INTEGER NOT NULL,
            codigo_ars TEXT NOT NULL,
            activo BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medico_id) REFERENCES medicos(id),
            FOREIGN KEY (ars_id) REFERENCES ars(id),
            UNIQUE(medico_id, ars_id)
        )
    ''')
    
    # Tabla de Tipos de Servicios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tipos_servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            precio_base REAL DEFAULT 0,
            activo BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de NCF (Números de Comprobante Fiscal)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ncf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            prefijo TEXT NOT NULL,
            tamaño INTEGER NOT NULL,
            ultimo_numero INTEGER DEFAULT 0,
            activo BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de Pacientes (Maestra)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nss TEXT NOT NULL,
            nombre TEXT NOT NULL,
            ars_id INTEGER,
            activo BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ars_id) REFERENCES ars(id),
            UNIQUE(nss, ars_id)
        )
    ''')
    
    # Tabla de Facturas (Encabezado)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_factura TEXT,
            ncf TEXT,
            fecha_factura DATE NOT NULL,
            medico_id INTEGER NOT NULL,
            ars_id INTEGER NOT NULL,
            total REAL DEFAULT 0,
            observaciones TEXT,
            activo BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medico_id) REFERENCES medicos(id),
            FOREIGN KEY (ars_id) REFERENCES ars(id)
        )
    ''')
    
    # Tabla de Detalle de Facturas (Líneas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factura_id INTEGER,
            paciente_id INTEGER NOT NULL,
            nss TEXT NOT NULL,
            nombre_paciente TEXT NOT NULL,
            fecha_servicio DATE NOT NULL,
            autorizacion TEXT,
            servicio_id INTEGER NOT NULL,
            descripcion_servicio TEXT NOT NULL,
            monto REAL NOT NULL,
            medico_id INTEGER NOT NULL,
            ars_id INTEGER NOT NULL,
            estado TEXT DEFAULT 'pendiente',
            activo BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (factura_id) REFERENCES facturas(id),
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
            FOREIGN KEY (servicio_id) REFERENCES tipos_servicios(id),
            FOREIGN KEY (medico_id) REFERENCES medicos(id),
            FOREIGN KEY (ars_id) REFERENCES ars(id)
        )
    ''')
    
    # Crear usuario por defecto si no existe
    cursor.execute('SELECT COUNT(*) FROM usuarios')
    if cursor.fetchone()[0] == 0:
        # Usuario por defecto: ing.fpaula@gmail.com - Francisco Paula
        password_hash = generate_password_hash('2416Xpos@')
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, password_hash, perfil, activo)
            VALUES (?, ?, ?, ?, 1)
        ''', ('Francisco Paula', 'ing.fpaula@gmail.com', password_hash, 'Administrador'))
        print("✅ Usuario por defecto creado: ing.fpaula@gmail.com")
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Obtener conexión optimizada a la base de datos"""
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    
    # Optimizaciones de rendimiento para SQLite
    conn.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging para mejor concurrencia
    conn.execute('PRAGMA synchronous=NORMAL')  # Balance entre seguridad y velocidad
    conn.execute('PRAGMA cache_size=10000')  # Cache de 10MB para consultas rápidas
    conn.execute('PRAGMA temp_store=MEMORY')  # Tablas temporales en memoria
    conn.execute('PRAGMA mmap_size=268435456')  # Memory-mapped I/O de 256MB
    
    return conn

def increment_visit_counter():
    """Incrementar el contador de visitas del sitio"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE site_visits 
            SET total_visits = total_visits + 1, 
                last_updated = CURRENT_TIMESTAMP 
            WHERE id = 1
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error al incrementar contador de visitas: {e}")

def get_visit_count():
    """Obtener el número total de visitas del sitio"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT total_visits FROM site_visits WHERE id = 1')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
    except Exception as e:
        print(f"Error al obtener contador de visitas: {e}")
        return 0

def create_sample_data():
    """Crear datos de ejemplo"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar si ya existen datos
    cursor.execute('SELECT COUNT(*) FROM services')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Servicios de ejemplo
    services = [
        ('Consulta Ginecológica', 'Consulta ginecológica\nPapanicolau\nColposcopia/biopsias\nCirugías ginecológicas\nIrregularidad menstrual\nGenotipificación y manejo del virus de papiloma humano\nManejo del síndrome de ovario poliquístico\nPlanificación familiar\nMenopausia y climaterio', 'fas fa-female', 'Consultar', '45 min'),
        ('Consulta Obstétrica', 'Consulta de obstetricia\nConsulta preconcepcional\nControl prenatal\nSeguimiento de embarazo de alto riesgo\nPartos y cesáreas\nAsesoría en lactancia materna', 'fas fa-baby', 'Consultar', '60 min'),
        ('Ecografías', 'Estudios de imagen para diagnóstico y seguimiento del embarazo y condiciones ginecológicas.', 'fas fa-heartbeat', 'Consultar', '30 min'),
        ('Cirugía Ginecológica', 'Procedimientos quirúrgicos especializados en ginecología con técnicas avanzadas.', 'fas fa-cut', 'Consultar', 'Variable'),
        ('Planificación Familiar', 'Asesoría sobre métodos anticonceptivos y planificación reproductiva personalizada.', 'fas fa-calendar-check', 'Consultar', '30 min'),
        ('Tratamientos Estéticos Ginecológicos', 'Tecnología láser de última generación para rejuvenecimiento vaginal, blanqueamiento genital, corrección de cicatrices y más. Click para ver todos los tratamientos disponibles.', 'fas fa-wand-magic-sparkles', 'Ver Tratamientos', 'Variable')
    ]
    
    cursor.executemany('INSERT INTO services (name, description, icon, price_range, duration) VALUES (?, ?, ?, ?, ?)', services)
    
    # Tratamientos Estéticos Ginecológicos
    aesthetic_treatments = [
        ('Rejuvenecimiento vaginal', 'Mejora la elasticidad y tonicidad del canal vaginal.\nReduce la sequedad y mejora la lubricación natural.\nFavorece la producción de colágeno y elastina.', 'fas fa-magic'),
        ('Blanqueamiento genital', 'Aclara la pigmentación de la vulva, periné o zona anal.\nUnifica el tono de la piel íntima.', 'fas fa-sun'),
        ('Tensado o lifting vulvar', 'Mejora la apariencia externa de los labios mayores y menores.\nCorrige leve flacidez o laxitud de la vulva.', 'fas fa-compress-arrows-alt'),
        ('Corrección de cicatrices postparto o episiotomía', 'Suaviza la textura, color y relieve de cicatrices.\nDisminuye molestias o retracciones cicatriciales.', 'fas fa-hand-holding-medical'),
        ('Atrofia vulvovaginal (Síndrome Genitourinario de la Menopausia)', 'Alivia sequedad, ardor, picazón y dispareunia.\nEstimula la regeneración del epitelio vaginal.', 'fas fa-leaf'),
        ('Incontinencia urinaria leve a moderada', 'Fortalece las paredes vaginales y la uretra.\nMejora el soporte del suelo pélvico.\nDisminuye las pérdidas de orina al toser o hacer esfuerzo.', 'fas fa-shield-alt'),
        ('Laxitud vaginal postparto o por envejecimiento', 'Reafirma los tejidos del canal vaginal.\nMejora la sensibilidad y la satisfacción sexual.', 'fas fa-heart'),
        ('Vulvodinia y vestibulodinia leves', 'Reduce el dolor crónico vulvar mediante la bioestimulación tisular.', 'fas fa-spa'),
        ('Condilomas vulvares o vaginales (verrugas por VPH)', 'Eliminación precisa de lesiones con mínima lesión tisular.', 'fas fa-exclamation-triangle'),
        ('Lesiones cervicales leves (ej. NIC I)', 'Vaporización controlada de lesiones benignas o displásicas superficiales.', 'fas fa-stethoscope'),
        ('Quistes o pólipos pequeños del cuello uterino o vulvares', 'Resección con mínimo sangrado y rápida cicatrización.', 'fas fa-cut'),
        ('Liquen escleroso vulvar (casos seleccionados)', 'Mejora la textura y síntomas, reduciendo picazón y ardor.\nEstimula la regeneración epitelial.', 'fas fa-microscope'),
        ('Bartolinitis crónica o recidivante (marsupialización asistida con láser)', 'Facilita drenaje y recuperación más rápida.', 'fas fa-bolt'),
    ]
    
    cursor.executemany('INSERT INTO aesthetic_treatments (name, description, icon) VALUES (?, ?, ?)', aesthetic_treatments)
    
    # Pool de 50 testimonios variados con nombres diferentes
    testimonials = [
        ('María González', 'M.G.', 'La Dra. Shirley es una excelente profesional. Su atención es muy cuidadosa y me hizo sentir cómoda durante toda la consulta. Recomiendo sus servicios sin dudarlo.', 5),
        ('Ana Rodríguez', 'A.R.', 'Durante mi embarazo recibí un excelente cuidado prenatal. La doctora siempre estuvo disponible para resolver mis dudas y me acompañó en todo el proceso.', 5),
        ('Carmen López', 'C.L.', 'Profesional, empática y muy conocedora de su especialidad. Me ayudó mucho durante mi tratamiento y siempre me explicó todo claramente.', 5),
        ('Patricia Martínez', 'P.M.', 'Quedé muy satisfecha con la atención recibida. La Dra. Shirley es muy profesional y dedicada. Mi experiencia fue excelente.', 5),
        ('Laura Fernández', 'L.F.', 'Excelente doctora, muy humana y profesional. Me explicó todo con paciencia y me sentí muy bien atendida.', 5),
        ('Isabel Sánchez', 'I.S.', 'La mejor ginecóloga que he visitado. Su trato es excepcional y siempre está al tanto de los últimos avances médicos.', 5),
        ('Rosa Ramírez', 'R.R.', 'Muy agradecida por el cuidado durante mi embarazo. La Dra. Shirley hizo que todo fuera más fácil y tranquilo.', 5),
        ('Sofía Torres', 'S.T.', 'Profesional y cariñosa. Me sentí en muy buenas manos desde el primer momento. Totalmente recomendada.', 5),
        ('Gabriela Díaz', 'G.D.', 'Su conocimiento y experiencia son evidentes. Me ayudó muchísimo con mi tratamiento. Muy agradecida.', 5),
        ('Daniela Ruiz', 'D.R.', 'La Dra. Shirley es increíble. Siempre tan atenta y profesional. Mi familia y yo estamos muy contentas.', 5),
        ('Valeria Morales', 'V.M.', 'Excelente atención, instalaciones muy limpias y personal amable. La doctora es muy profesional.', 5),
        ('Natalia Jiménez', 'N.J.', 'Me encantó su forma de explicar todo. Es muy clara y paciente. Definitivamente volveré.', 5),
        ('Andrea Castro', 'A.C.', 'Gran profesional con mucha experiencia. Me sentí muy segura durante todo mi tratamiento.', 5),
        ('Carolina Vargas', 'C.V.', 'La recomiendo al 100%. Es una doctora excepcional que realmente se preocupa por sus pacientes.', 5),
        ('Lucía Herrera', 'L.H.', 'Trato excelente y muy profesional. Respondió todas mis preguntas con mucha paciencia.', 5),
        ('Elena Mendoza', 'E.M.', 'Muy satisfecha con la consulta. La Dra. Shirley es muy detallista y cuidadosa.', 5),
        ('Paula Ortiz', 'P.O.', 'Excelente doctora, muy preparada y con un trato humano excepcional. La mejor decisión.', 5),
        ('Mónica Silva', 'M.S.', 'Me acompañó durante todo mi embarazo con mucho profesionalismo. Muy agradecida.', 5),
        ('Victoria Reyes', 'V.R.', 'Súper recomendada. Es una doctora muy capacitada y con excelente trato humano.', 5),
        ('Diana Flores', 'D.F.', 'Muy profesional y atenta. Me explicó todo detalladamente y me sentí muy cómoda.', 5),
        ('Alejandra Cruz', 'A.C.', 'La mejor ginecóloga que he conocido. Su atención es personalizada y muy profesional.', 5),
        ('Mariana Guzmán', 'M.G.', 'Excelente experiencia. La doctora es muy profesional y el personal muy amable.', 5),
        ('Beatriz Rojas', 'B.R.', 'Muy contenta con mi consulta. La Dra. Shirley es excepcional en todos los aspectos.', 5),
        ('Cristina Medina', 'C.M.', 'Gran profesional con mucho conocimiento. Me sentí muy bien atendida y segura.', 5),
        ('Adriana Vega', 'A.V.', 'La recomiendo completamente. Es una doctora muy preparada y con excelente trato.', 5),
        ('Rocío Campos', 'R.C.', 'Muy satisfecha con el servicio. La doctora es muy profesional y dedicada.', 5),
        ('Teresa Santos', 'T.S.', 'Excelente atención durante todo mi embarazo. La Dra. Shirley es maravillosa.', 5),
        ('Silvia Peña', 'S.P.', 'Muy profesional y empática. Me ayudó muchísimo con mi tratamiento. Gracias.', 5),
        ('Julia Cortés', 'J.C.', 'La mejor experiencia que he tenido con una ginecóloga. Súper recomendada.', 5),
        ('Claudia Aguilar', 'C.A.', 'Excelente doctora, muy humana y profesional. Me sentí muy bien cuidada.', 5),
        ('Mercedes Luna', 'M.L.', 'Muy agradecida por su atención. Es una doctora excepcional con gran vocación.', 5),
        ('Lorena Chávez', 'L.C.', 'Profesional, cariñosa y muy preparada. La recomiendo sin dudarlo.', 5),
        ('Raquel Domínguez', 'R.D.', 'Excelente servicio y atención. La Dra. Shirley es muy profesional y dedicada.', 5),
        ('Susana Ramos', 'S.R.', 'Me encantó su trato y profesionalismo. Definitivamente la mejor ginecóloga.', 5),
        ('Verónica Gil', 'V.G.', 'Muy satisfecha con todo. La doctora es excelente y el personal muy amable.', 5),
        ('Pilar Núñez', 'P.N.', 'Gran experiencia. La Dra. Shirley es muy profesional y atenta con sus pacientes.', 5),
        ('Gloria Molina', 'G.M.', 'La mejor doctora. Su trato es excepcional y siempre te hace sentir cómoda.', 5),
        ('Cecilia Paredes', 'C.P.', 'Muy recomendada. Es una profesional de primera con excelente trato humano.', 5),
        ('Irene Fuentes', 'I.F.', 'Excelente atención y seguimiento. La Dra. Shirley es muy dedicada y profesional.', 5),
        ('Alicia Márquez', 'A.M.', 'Muy contenta con mi consulta. La doctora es muy profesional y empática.', 5),
        ('Rebeca Ibáñez', 'R.I.', 'La recomiendo al 100%. Es una doctora excepcional en todos los sentidos.', 5),
        ('Norma Guerrero', 'N.G.', 'Excelente profesional. Me ayudó muchísimo durante mi embarazo. Muy agradecida.', 5),
        ('Leticia Soto', 'L.S.', 'Muy profesional y atenta. Su trato es excepcional y su conocimiento impecable.', 5),
        ('Yolanda Ríos', 'Y.R.', 'Gran doctora con mucha experiencia. Me sentí muy segura bajo su cuidado.', 5),
        ('Amparo Navarro', 'A.N.', 'Excelente en todos los aspectos. La Dra. Shirley es una gran profesional.', 5),
        ('Dolores Romero', 'D.R.', 'Muy satisfecha con la atención recibida. La doctora es muy dedicada y profesional.', 5),
        ('Francisca León', 'F.L.', 'La mejor ginecóloga. Su trato es excepcional y siempre está disponible para ayudar.', 5),
        ('Antonia Blanco', 'A.B.', 'Excelente doctora y mejor persona. Me acompañó en todo mi proceso con mucho cariño.', 5),
        ('Josefina Pascual', 'J.P.', 'Muy profesional y humana. La Dra. Shirley es simplemente excepcional.', 5),
        ('Encarnación Cano', 'E.C.', 'Gran experiencia desde el primer día. La recomiendo completamente. Gracias doctora.', 5)
    ]
    
    cursor.executemany('INSERT INTO testimonials (patient_name, patient_initials, testimonial_text, rating, approved) VALUES (?, ?, ?, ?, 1)', testimonials)
    
    conn.commit()
    conn.close()

# Rutas principales
@app.route('/')
def index():
    """Página principal con testimonios rotativos"""
    from datetime import datetime, timedelta
    import random
    
    # Incrementar contador de visitas
    increment_visit_counter()
    
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services WHERE active = 1 LIMIT 6').fetchall()
    all_testimonials = conn.execute('SELECT * FROM testimonials WHERE approved = 1').fetchall()
    conn.close()
    
    # Rotación diaria de testimonios
    today = datetime.now()
    seed = today.timetuple().tm_yday
    random.seed(seed)
    
    testimonials_list = list(all_testimonials)
    random.shuffle(testimonials_list)
    selected_testimonials = testimonials_list[:3]  # Mostrar 3 en inicio
    
    # Asignar fechas dinámicas
    testimonials_with_dates = []
    for i, testimonial in enumerate(selected_testimonials):
        random.seed(seed + i + 1000)  # Semilla diferente al de página testimonios
        days_ago = random.randint(1, 30)
        display_date = today - timedelta(days=days_ago)
        
        if days_ago == 1:
            time_ago = "Hace 1 día"
        elif days_ago < 7:
            time_ago = f"Hace {days_ago} días"
        elif days_ago < 14:
            time_ago = "Hace 1 semana"
        elif days_ago < 30:
            weeks = days_ago // 7
            time_ago = f"Hace {weeks} semanas"
        else:
            time_ago = "Hace 1 mes"
        
        testimonial_dict = dict(testimonial)
        testimonial_dict['time_ago'] = time_ago
        testimonials_with_dates.append(testimonial_dict)
    
    return render_template('index.html', 
                         services=services, 
                         testimonials=testimonials_with_dates)

@app.route('/index-v2')
def index_v2():
    """Página principal - Versión refrescante"""
    from datetime import datetime, timedelta
    import random
    
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services WHERE active = 1 LIMIT 6').fetchall()
    all_testimonials = conn.execute('SELECT * FROM testimonials WHERE approved = 1').fetchall()
    conn.close()
    
    # Rotación diaria de testimonios
    today = datetime.now()
    seed = today.timetuple().tm_yday
    random.seed(seed)
    
    testimonials_list = list(all_testimonials)
    random.shuffle(testimonials_list)
    selected_testimonials = testimonials_list[:3]  # Mostrar 3 en inicio
    
    # Asignar fechas dinámicas
    testimonials_with_dates = []
    for i, testimonial in enumerate(selected_testimonials):
        random.seed(seed + i + 1000)  # Semilla diferente
        days_ago = random.randint(1, 30)
        display_date = today - timedelta(days=days_ago)
        
        if days_ago == 1:
            time_ago = "Hace 1 día"
        elif days_ago < 7:
            time_ago = f"Hace {days_ago} días"
        elif days_ago < 14:
            time_ago = "Hace 1 semana"
        elif days_ago < 30:
            weeks = days_ago // 7
            time_ago = f"Hace {weeks} semanas"
        else:
            time_ago = "Hace 1 mes"
        
        testimonial_dict = dict(testimonial)
        testimonial_dict['time_ago'] = time_ago
        testimonials_with_dates.append(testimonial_dict)
    
    return render_template('index_v2.html', 
                         services=services, 
                         testimonials=testimonials_with_dates)

@app.route('/old-index')
def old_index():
    """Página principal original - Backup"""
    from datetime import datetime, timedelta
    import random
    
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services WHERE active = 1 LIMIT 6').fetchall()
    all_testimonials = conn.execute('SELECT * FROM testimonials WHERE approved = 1').fetchall()
    conn.close()
    
    # Rotación diaria de testimonios
    today = datetime.now()
    seed = today.timetuple().tm_yday
    random.seed(seed)
    
    testimonials_list = list(all_testimonials)
    random.shuffle(testimonials_list)
    selected_testimonials = testimonials_list[:3]  # Mostrar 3 en inicio
    
    # Asignar fechas dinámicas
    testimonials_with_dates = []
    for i, testimonial in enumerate(selected_testimonials):
        random.seed(seed + i + 1000)  # Semilla diferente al de página testimonios
        days_ago = random.randint(1, 30)
        display_date = today - timedelta(days=days_ago)
        
        if days_ago == 1:
            time_ago = "Hace 1 día"
        elif days_ago < 7:
            time_ago = f"Hace {days_ago} días"
        elif days_ago < 14:
            time_ago = "Hace 1 semana"
        elif days_ago < 30:
            weeks = days_ago // 7
            time_ago = f"Hace {weeks} semanas"
        else:
            time_ago = "Hace 1 mes"
        
        testimonial_dict = dict(testimonial)
        testimonial_dict['time_ago'] = time_ago
        testimonial_dict['formatted_date'] = display_date.strftime('%d/%m/%Y')
        testimonials_with_dates.append(testimonial_dict)
    
    return render_template('index.html', services=services, testimonials=testimonials_with_dates)

@app.route('/servicios')
def services():
    """Página de servicios"""
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services WHERE active = 1').fetchall()
    conn.close()
    
    return render_template('services.html', services=services)

@app.route('/tratamientos-esteticos')
def aesthetic_treatments():
    """Página de Tratamientos Estéticos Ginecológicos (no en menú)"""
    conn = get_db_connection()
    treatments = conn.execute('SELECT * FROM aesthetic_treatments ORDER BY id').fetchall()
    conn.close()
    
    return render_template('tratamientos-esteticos.html', treatments=treatments)

@app.route('/sobre-mi')
def about():
    """Página sobre la doctora"""
    return render_template('about.html')

@app.route('/testimonios')
def testimonials():
    """Página de testimonios con rotación diaria y fechas dinámicas"""
    from datetime import datetime, timedelta
    import random
    
    conn = get_db_connection()
    
    # Obtener TODOS los testimonios
    all_testimonials = conn.execute('SELECT * FROM testimonials WHERE approved = 1').fetchall()
    conn.close()
    
    # Usar el día del año como semilla para rotación consistente por día
    today = datetime.now()
    seed = today.timetuple().tm_yday  # Día del año (1-365)
    random.seed(seed)
    
    # Mezclar los testimonios de forma consistente para el día
    testimonials_list = list(all_testimonials)
    random.shuffle(testimonials_list)
    
    # Tomar 9 testimonios para mostrar (cambian cada día)
    selected_testimonials = testimonials_list[:9]
    
    # Asignar fechas aleatorias de los últimos 30 días a cada testimonio
    testimonials_with_dates = []
    for i, testimonial in enumerate(selected_testimonials):
        # Generar fecha aleatoria entre 1 y 30 días atrás (consistente para el día)
        random.seed(seed + i)  # Semilla única para cada testimonio
        days_ago = random.randint(1, 30)
        display_date = today - timedelta(days=days_ago)
        
        # Calcular texto "hace X días/semanas"
        if days_ago == 1:
            time_ago = "Hace 1 día"
        elif days_ago < 7:
            time_ago = f"Hace {days_ago} días"
        elif days_ago < 14:
            time_ago = "Hace 1 semana"
        elif days_ago < 30:
            weeks = days_ago // 7
            time_ago = f"Hace {weeks} semanas"
        else:
            time_ago = "Hace 1 mes"
        
        # Convertir Row a dict y agregar información de fecha
        testimonial_dict = dict(testimonial)
        testimonial_dict['display_date'] = display_date.strftime('%Y-%m-%d')
        testimonial_dict['time_ago'] = time_ago
        testimonial_dict['formatted_date'] = display_date.strftime('%d/%m/%Y')
        
        testimonials_with_dates.append(testimonial_dict)
    
    # Ordenar por fecha más reciente primero
    testimonials_with_dates.sort(key=lambda x: x['display_date'], reverse=True)
    
    return render_template('testimonials.html', testimonials=testimonials_with_dates)

def enviar_email_pdf_pacientes(medico_email, medico_nombre, pdf_buffer, num_pacientes, total):
    """Enviar email con PDF adjunto de pacientes agregados"""
    try:
        # Verificar si hay contraseña configurada
        if not EMAIL_PASSWORD:
            print("\n⚠️  Email no configurado. El PDF no se envió.")
            return False
        
        # Crear mensaje usando template estándar
        msg = MIMEMultipart()
        msg['Subject'] = f'📋 Constancia - {num_pacientes} Paciente(s) Pendiente(s) de Facturación'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = medico_email
        
        # Usar template estandarizado
        html = template_constancia_pdf(medico_nombre, num_pacientes, total)
        
        # Adjuntar HTML
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Adjuntar PDF
        pdf_attachment = MIMEApplication(pdf_buffer.getvalue(), _subtype='pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment', 
                                 filename=f'constancia_pacientes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        msg.attach(pdf_attachment)
        
        # Enviar email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("\n" + "=" * 60)
        print("✅ EMAIL CON PDF ENVIADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📧 Destinatario: {medico_email}")
        print(f"👨‍⚕️ Médico: {medico_nombre}")
        print(f"📋 Pacientes: {num_pacientes}")
        print(f"💰 Total: {total:,.2f}")
        print("=" * 60 + "\n")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR AL ENVIAR EMAIL CON PDF")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nEl PDF se descargó correctamente, pero no se envió el email.")
        print("=" * 60 + "\n")
        return False

def enviar_email_notificacion(name, email, phone, subject, message):
    """Enviar email de notificación a la doctora"""
    try:
        # Verificar si hay contraseña configurada
        if not EMAIL_PASSWORD:
            print("\n⚠️  CONFIGURACIÓN DE EMAIL NECESARIA")
            print("=" * 60)
            print("Para recibir emails, configura Gmail siguiendo estos pasos:")
            print("1. Lee el archivo: CONFIGURAR_EMAIL_PASO_A_PASO.md")
            print("2. Genera una contraseña de aplicación en Gmail")
            print("3. Crea el archivo .env con tu contraseña")
            print("=" * 60)
            print("\nPor ahora, el mensaje se guardó en la base de datos.")
            print("Puedes verlo en: http://localhost:5000/admin")
            print("=" * 60 + "\n")
            return False
        
        # Crear mensaje usando el template estándar
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'🔔 Nuevo mensaje: {subject}'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_DESTINATARIO
        msg['Reply-To'] = email
        
        # Usar template estandarizado
        html = template_contacto(name, email, phone, subject, message)
        
        # Adjuntar HTML
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Enviar email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("\n" + "=" * 60)
        print("✅ EMAIL ENVIADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📧 Destinatario: {EMAIL_DESTINATARIO}")
        print(f"👤 Remitente: {name} ({email})")
        print(f"📝 Asunto: {subject}")
        print("=" * 60 + "\n")
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("\n" + "=" * 60)
        print("❌ ERROR DE AUTENTICACIÓN")
        print("=" * 60)
        print("La contraseña de Gmail es incorrecta.")
        print("\nSoluciones:")
        print("1. Verifica que la verificación en 2 pasos esté activa")
        print("2. Genera una nueva contraseña de aplicación")
        print("3. Actualiza el archivo .env con la nueva contraseña")
        print("4. Lee: CONFIGURAR_EMAIL_GMAIL.md")
        print("=" * 60 + "\n")
        return False
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR AL ENVIAR EMAIL")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nEl mensaje se guardó en la base de datos.")
        print("Puedes verlo en: http://localhost:5000/admin")
        print("=" * 60 + "\n")
        return False

def enviar_email_recuperacion(email, nombre, link_recuperacion):
    """Enviar email de recuperación de contraseña"""
    try:
        # Verificar si hay contraseña configurada
        if not EMAIL_PASSWORD:
            print("⚠️  No se puede enviar email de recuperación: EMAIL_PASSWORD no configurado")
            return False
        
        # Crear mensaje usando template estándar
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🔐 Recuperación de Contraseña - Panel Administrativo'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = email
        
        # Usar template estandarizado
        html = template_recuperacion(nombre, link_recuperacion)
        
        # Adjuntar HTML
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Enviar email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email de recuperación enviado a {email}")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email de recuperación: {e}")
        return False

def enviar_email_cita(first_name, last_name, email, phone, appointment_date, appointment_time, appointment_type, medical_insurance, emergency_datetime, reason):
    """Enviar email de notificación de cita a la doctora"""
    try:
        # Verificar si hay contraseña configurada
        if not EMAIL_PASSWORD:
            print("\n⚠️  Email no configurado. La cita se guardó en la base de datos.")
            return False
        
        # Crear mensaje usando template estándar
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'📅 Nueva Solicitud de Cita - {first_name} {last_name}'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_DESTINATARIO
        if email:
            msg['Reply-To'] = email
        
        # Preparar datos para el template
        fecha = emergency_datetime if appointment_type == "emergencia" else appointment_date
        hora = appointment_time if appointment_type != "emergencia" else None
        tipo_cita = f"{appointment_type} {'(EMERGENCIA)' if appointment_type == 'emergencia' else ''}".strip()
        seguro = medical_insurance if medical_insurance else "No especificado"
        motivo = reason if reason else "No especificado"
        
        # Usar template estandarizado
        html = template_cita(
            first_name, last_name, email if email else "No proporcionado", 
            phone, fecha, hora if hora else "URGENTE", tipo_cita, 
            seguro, emergency_datetime if appointment_type == "emergencia" else None, motivo
        )
        
        # Adjuntar HTML
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Enviar email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("\n" + "=" * 60)
        print("✅ EMAIL DE CITA ENVIADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📧 Destinatario: {EMAIL_DESTINATARIO}")
        print(f"👤 Paciente: {first_name} {last_name} ({phone})")
        print(f"🩺 Tipo: {appointment_type}")
        print("=" * 60 + "\n")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR AL ENVIAR EMAIL DE CITA")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nLa cita se guardó en la base de datos.")
        print("Puedes verla en: http://localhost:5000/admin/appointments")
        print("=" * 60 + "\n")
        return False

def enviar_email_confirmacion_cita(paciente_email, nombre, apellido, fecha, hora, tipo, estatus, motivo=None):
    """Enviar email de confirmación de cambio de estatus de cita al paciente"""
    try:
        # Verificar si hay contraseña configurada
        if not EMAIL_PASSWORD or EMAIL_PASSWORD == "tu_password_aqui":
            print("\n⚠️ CONFIGURACIÓN DE EMAIL PENDIENTE")
            print("Por favor, configura EMAIL_PASSWORD en el archivo .env")
            return False
        
        # Verificar que el paciente tenga email
        if not paciente_email:
            print("\n⚠️ El paciente no tiene email registrado")
            return False
        
        print("\n" + "=" * 60)
        print("📧 ENVIANDO EMAIL DE CONFIRMACIÓN DE CITA AL PACIENTE")
        print("=" * 60)
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        
        # Asunto según el estatus
        asuntos = {
            'pending': '⏳ Tu Cita está Pendiente de Confirmación',
            'confirmed': '✅ ¡Tu Cita ha sido Confirmada!',
            'cancelled': '❌ Tu Cita ha sido Cancelada',
            'completed': '✔️ Tu Cita ha sido Completada'
        }
        
        msg['Subject'] = asuntos.get(estatus, '📅 Actualización de tu Cita')
        msg['From'] = EMAIL_USERNAME
        msg['To'] = paciente_email
        
        # Generar HTML usando el template
        html = template_confirmacion_cita(nombre, apellido, fecha, hora, tipo, estatus, motivo)
        
        # Adjuntar HTML
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Conectar y enviar
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print("\n✅ EMAIL DE CONFIRMACIÓN ENVIADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📧 Destinatario: {paciente_email}")
        print(f"👤 Paciente: {nombre} {apellido}")
        print(f"🏥 Estatus: {estatus}")
        print(f"📅 Fecha: {fecha if fecha else 'Por confirmar'}")
        print(f"🕐 Hora: {hora if hora else 'Por confirmar'}")
        print("=" * 60 + "\n")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR AL ENVIAR EMAIL DE CONFIRMACIÓN")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nEl cambio de estatus se guardó en la base de datos.")
        print("Pero el email no pudo ser enviado al paciente.")
        print("=" * 60 + "\n")
        return False

@app.route('/contacto', methods=['GET', 'POST'])
@rate_limit(max_requests=5, window=300)  # 5 requests por 5 minutos
def contact():
    """Página de contacto"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone', '')
        subject = request.form['subject']
        message = request.form['message']
        
        # Validar que todos los campos estén completos
        if not all([name, email, phone, subject, message]):
            flash('Por favor, completa todos los campos obligatorios.', 'danger')
            return redirect(url_for('contact'))
        
        # Guardar en base de datos
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO contact_messages (name, email, phone, subject, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, subject, message))
        conn.commit()
        conn.close()
        
        # Enviar email de notificación
        enviar_email_notificacion(name, email, phone, subject, message)
        
        flash('¡Mensaje enviado correctamente! Te contactaremos pronto.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/api/horarios-disponibles', methods=['GET'])
def horarios_disponibles():
    """API para obtener horarios disponibles según la fecha"""
    fecha = request.args.get('fecha')
    
    if not fecha:
        return jsonify({'error': 'Fecha requerida'}), 400
    
    try:
        # Parsear la fecha para obtener el día de la semana
        from datetime import datetime
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
        dia_semana = fecha_obj.weekday()  # 0=Lunes, 1=Martes, 3=Jueves
        
        # Definir horarios según el día
        if dia_semana == 1:  # Martes
            horarios_base = [
                '13:00', '13:30', '14:00', '14:30', '15:00', 
                '15:30', '16:00', '16:30', '17:00', '17:30', '18:00'
            ]
        elif dia_semana == 3:  # Jueves
            horarios_base = [
                '08:00', '08:30', '09:00', '09:30', '10:00',
                '10:30', '11:00', '11:30', '12:00', '12:30', '13:00'
            ]
        else:
            return jsonify({'horarios': []})
        
        # Obtener citas ya agendadas para esa fecha (que no estén canceladas)
        conn = get_db_connection()
        citas_ocupadas = conn.execute(
            'SELECT appointment_time FROM appointments WHERE appointment_date = ? AND status != "cancelled"',
            (fecha,)
        ).fetchall()
        conn.close()
        
        # Crear lista de horarios ocupados
        horarios_ocupados = [cita[0] for cita in citas_ocupadas if cita[0]]
        
        # Filtrar horarios disponibles
        horarios_disponibles = [h for h in horarios_base if h not in horarios_ocupados]
        
        return jsonify({'horarios': horarios_disponibles})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/solicitar-cita', methods=['GET', 'POST'])
@rate_limit(max_requests=3, window=300)  # 3 requests por 5 minutos
def request_appointment():
    """Solicitar cita"""
    if request.method == 'POST':
        # Validar y sanitizar entrada
        first_name = sanitize_input(request.form.get('first_name', ''))
        last_name = sanitize_input(request.form.get('last_name', ''))
        email = sanitize_input(request.form.get('email', ''))
        phone = sanitize_input(request.form.get('phone', ''))
        appointment_date = sanitize_input(request.form.get('appointment_date', ''))
        appointment_time = sanitize_input(request.form.get('appointment_time', ''))
        appointment_type = sanitize_input(request.form.get('appointment_type', ''))
        medical_insurance = sanitize_input(request.form.get('medical_insurance', ''))
        
        # Validaciones críticas
        if not all([first_name, last_name, phone, appointment_type, medical_insurance]):
            flash('Por favor, completa todos los campos obligatorios.', 'danger')
            return redirect(url_for('request_appointment'))
        
        if email and not validate_email(email):
            flash('Por favor, ingresa un email válido.', 'danger')
            return redirect(url_for('request_appointment'))
        
        if len(first_name) > 50 or len(last_name) > 50:
            flash('Los nombres no pueden exceder 50 caracteres.', 'danger')
            return redirect(url_for('request_appointment'))
        
        emergency_datetime = sanitize_input(request.form.get('emergency_datetime', ''))
        reason = sanitize_input(request.form.get('reason', ''))
        
        # Verificar disponibilidad de horario (solo para citas normales con fecha y hora)
        if appointment_type in ["consulta", "estetico"] and appointment_date and appointment_time:
            conn = get_db_connection()
            cita_existente = conn.execute(
                'SELECT id FROM appointments WHERE appointment_date = ? AND appointment_time = ? AND status != "cancelled"',
                (appointment_date, appointment_time)
            ).fetchone()
            
            if cita_existente:
                conn.close()
                flash('⚠️ Lo sentimos, ese horario ya está ocupado. Por favor selecciona otro horario.', 'warning')
                return redirect(url_for('request_appointment'))
            
            conn.close()
        
        # Verificar disponibilidad de horario de emergencia
        if appointment_type == "emergencia" and emergency_datetime:
            # Extraer fecha y hora del datetime
            try:
                from datetime import datetime
                emergency_dt = datetime.strptime(emergency_datetime, '%Y-%m-%dT%H:%M')
                emergency_date = emergency_dt.strftime('%Y-%m-%d')
                emergency_time = emergency_dt.strftime('%H:%M')
                
                conn = get_db_connection()
                cita_existente = conn.execute(
                    'SELECT id FROM appointments WHERE emergency_datetime LIKE ? AND status != "cancelled"',
                    (f'{emergency_date}%',)
                ).fetchall()
                
                # Verificar si hay conflicto de horario (dentro de 30 minutos)
                for cita in cita_existente:
                    conn.close()
                    flash('⚠️ Lo sentimos, ya hay una cita de emergencia cerca de ese horario. Por favor selecciona otro horario.', 'warning')
                    return redirect(url_for('request_appointment'))
                
                conn.close()
            except:
                pass
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO appointments (first_name, last_name, email, phone, appointment_date, appointment_time, appointment_type, medical_insurance, emergency_datetime, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, phone, appointment_date, appointment_time, appointment_type, medical_insurance, emergency_datetime, reason))
        conn.commit()
        conn.close()
        
        # Enviar email de notificación a la doctora
        enviar_email_cita(first_name, last_name, email, phone, appointment_date, appointment_time, appointment_type, medical_insurance, emergency_datetime, reason)
        
        flash('¡Cita solicitada correctamente! Te contactaremos para confirmar.', 'success')
        return redirect(url_for('request_appointment'))
    
    return render_template('request_appointment.html')

# ============================================================================
# AUTENTICACIÓN Y GESTIÓN DE USUARIOS
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
@rate_limit(max_requests=5, window=300)  # 5 intentos por 5 minutos
def login():
    """Inicio de sesión para el panel de administración"""
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Por favor ingresa email y contraseña', 'error')
            return redirect(url_for('login'))
        
        # Buscar usuario en la base de datos
        conn = get_db_connection()
        user_data = conn.execute(
            'SELECT id, nombre, email, password_hash, perfil, activo, password_temporal FROM usuarios WHERE email = ?',
            (email,)
        ).fetchone()
        conn.close()
        
        # Verificar usuario y contraseña
        if user_data and user_data['activo']:
            if check_password_hash(user_data['password_hash'], password):
                # Verificar si tiene contraseña temporal
                if user_data['password_temporal']:
                    # Guardar datos en sesión y redirigir a cambio de contraseña
                    session['cambio_password_usuario_id'] = user_data['id']
                    session['cambio_password_email'] = user_data['email']
                    flash('Debes cambiar tu contraseña temporal antes de continuar', 'warning')
                    return redirect(url_for('cambiar_password_obligatorio'))
                
                # Crear objeto usuario y hacer login
                user = User(
                    id=user_data['id'],
                    nombre=user_data['nombre'],
                    email=user_data['email'],
                    perfil=user_data['perfil']
                )
                
                # Marcar sesión como permanente para que persista
                session.permanent = True
                login_user(user, remember=True)
                
                # Actualizar last_login
                conn = get_db_connection()
                conn.execute('UPDATE usuarios SET last_login = ? WHERE id = ?',
                           (datetime.now(), user_data['id']))
                conn.commit()
                conn.close()
                
                # Redirigir a la página solicitada o al admin
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('admin'))
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Usuario no encontrado o inactivo', 'error')
        
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('index'))

@app.route('/cambiar-password-obligatorio', methods=['GET', 'POST'])
def cambiar_password_obligatorio():
    """Cambiar contraseña temporal obligatoriamente"""
    # Verificar que hay datos en sesión
    usuario_id = session.get('cambio_password_usuario_id')
    email = session.get('cambio_password_email')
    
    if not usuario_id or not email:
        flash('Sesión inválida. Por favor inicia sesión nuevamente.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password_temporal = request.form.get('password_temporal', '')
        nueva_password = request.form.get('nueva_password', '')
        confirmar_password = request.form.get('confirmar_password', '')
        
        if not password_temporal or not nueva_password or not confirmar_password:
            flash('Todos los campos son obligatorios', 'error')
            return render_template('cambiar_password_obligatorio.html', email=email)
        
        if nueva_password != confirmar_password:
            flash('Las contraseñas nuevas no coinciden', 'error')
            return render_template('cambiar_password_obligatorio.html', email=email)
        
        # Validar fortaleza de la nueva contraseña
        errores = validar_password_segura(nueva_password)
        if errores:
            flash('La contraseña no cumple con los requisitos: ' + ', '.join(errores), 'error')
            return render_template('cambiar_password_obligatorio.html', email=email)
        
        # Verificar contraseña temporal
        conn = get_db_connection()
        user_data = conn.execute(
            'SELECT password_hash FROM usuarios WHERE id = ?',
            (usuario_id,)
        ).fetchone()
        
        if not user_data or not check_password_hash(user_data['password_hash'], password_temporal):
            conn.close()
            flash('La contraseña temporal es incorrecta', 'error')
            return render_template('cambiar_password_obligatorio.html', email=email)
        
        # Actualizar contraseña
        nueva_password_hash = generate_password_hash(nueva_password)
        conn.execute(
            'UPDATE usuarios SET password_hash = ?, password_temporal = 0 WHERE id = ?',
            (nueva_password_hash, usuario_id)
        )
        conn.commit()
        conn.close()
        
        # Limpiar sesión
        session.pop('cambio_password_usuario_id', None)
        session.pop('cambio_password_email', None)
        
        flash('Contraseña cambiada exitosamente. Por favor inicia sesión con tu nueva contraseña.', 'success')
        return redirect(url_for('login'))
    
    return render_template('cambiar_password_obligatorio.html', email=email)

@app.route('/solicitar-recuperacion', methods=['GET', 'POST'])
def solicitar_recuperacion():
    """Solicitar recuperación de contraseña"""
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not email:
            flash('Por favor ingresa tu email', 'error')
            return redirect(url_for('solicitar_recuperacion'))
        
        # Buscar usuario
        conn = get_db_connection()
        user = conn.execute('SELECT id, nombre FROM usuarios WHERE email = ? AND activo = 1', (email,)).fetchone()
        
        if user:
            # Generar token de recuperación
            token = secrets.token_urlsafe(32)
            expiracion = datetime.now() + timedelta(hours=1)
            
            conn.execute(
                'UPDATE usuarios SET token_recuperacion = ?, token_expiracion = ? WHERE id = ?',
                (token, expiracion, user['id'])
            )
            conn.commit()
            
            # Enviar email con el link de recuperación
            link_recuperacion = url_for('recuperar_contrasena', token=token, _external=True)
            enviar_email_recuperacion(email, user['nombre'], link_recuperacion)
            
        conn.close()
        
        # Siempre mostrar el mismo mensaje (seguridad)
        flash('Si el email existe, recibirás un enlace de recuperación', 'info')
        return redirect(url_for('login'))
    
    return render_template('solicitar_recuperacion.html')

@app.route('/recuperar-contrasena/<token>', methods=['GET', 'POST'])
def recuperar_contrasena(token):
    """Cambiar contraseña con token de recuperación"""
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    
    # Verificar token
    conn = get_db_connection()
    user = conn.execute(
        'SELECT id, nombre, email FROM usuarios WHERE token_recuperacion = ? AND token_expiracion > ? AND activo = 1',
        (token, datetime.now())
    ).fetchone()
    
    if not user:
        conn.close()
        flash('Token inválido o expirado', 'error')
        return redirect(url_for('solicitar_recuperacion'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        if not password or len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'error')
            return redirect(url_for('recuperar_contrasena', token=token))
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('recuperar_contrasena', token=token))
        
        # Actualizar contraseña
        password_hash = generate_password_hash(password)
        conn.execute(
            'UPDATE usuarios SET password_hash = ?, token_recuperacion = NULL, token_expiracion = NULL WHERE id = ?',
            (password_hash, user['id'])
        )
        conn.commit()
        conn.close()
        
        flash('Contraseña actualizada correctamente. Ya puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    
    conn.close()
    return render_template('recuperar_contrasena.html', token=token, user=user)

@app.route('/admin')
@login_required
def admin():
    """Panel de administración simple"""
    conn = get_db_connection()
    
    # Estadísticas
    stats = {
        'total_appointments': conn.execute('SELECT COUNT(*) FROM appointments').fetchone()[0],
        'pending_appointments': conn.execute('SELECT COUNT(*) FROM appointments WHERE status = "pending"').fetchone()[0],
        'unread_messages': conn.execute('SELECT COUNT(*) FROM contact_messages WHERE read = 0').fetchone()[0],
        'total_testimonials': conn.execute('SELECT COUNT(*) FROM testimonials').fetchone()[0],
        'total_visits': get_visit_count()
    }
    
    # Datos recientes
    recent_appointments = conn.execute('SELECT * FROM appointments ORDER BY created_at DESC LIMIT 5').fetchall()
    recent_messages = conn.execute('SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 5').fetchall()
    
    conn.close()
    
    return render_template('admin.html', stats=stats, recent_appointments=recent_appointments, recent_messages=recent_messages)

@app.route('/admin/appointments')
@login_required
def admin_appointments():
    """Gestión de citas"""
    conn = get_db_connection()
    appointments = conn.execute('SELECT * FROM appointments ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template('admin_appointments.html', appointments=appointments)

@app.route('/admin/messages')
@login_required
def admin_messages():
    """Gestión de mensajes"""
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM contact_messages ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template('admin_messages.html', messages=messages)

@app.route('/admin/appointments/<int:appointment_id>/update', methods=['POST'])
@login_required
def update_appointment_status(appointment_id):
    """Actualizar estado de cita y enviar notificación al paciente"""
    new_status = request.form['status']
    
    conn = get_db_connection()
    
    # Obtener datos de la cita antes de actualizar
    appointment = conn.execute(
        'SELECT * FROM appointments WHERE id = ?',
        (appointment_id,)
    ).fetchone()
    
    if not appointment:
        flash('Cita no encontrada', 'error')
        conn.close()
        return redirect(url_for('admin_appointments'))
    
    # Actualizar estado
    conn.execute('UPDATE appointments SET status = ? WHERE id = ?', (new_status, appointment_id))
    conn.commit()
    conn.close()
    
    # Enviar email de confirmación al paciente si tiene email
    if appointment['email']:
        # Preparar los datos
        nombre = appointment['first_name']
        apellido = appointment['last_name']
        email_paciente = appointment['email']
        fecha = appointment['appointment_date'] if appointment['appointment_date'] else appointment['emergency_datetime']
        hora = appointment['appointment_time']
        tipo = appointment['appointment_type']
        motivo = appointment['reason'] if appointment['reason'] else None
        
        # Enviar email
        enviar_email_confirmacion_cita(
            email_paciente,
            nombre,
            apellido,
            fecha,
            hora,
            tipo,
            new_status,
            motivo
        )
        
        flash(f'Estado de la cita actualizado y notificación enviada a {nombre} {apellido}', 'success')
    else:
        flash('Estado de la cita actualizado (paciente sin email registrado)', 'warning')
    
    return redirect(url_for('admin_appointments'))

@app.route('/admin/messages/<int:message_id>/mark-read', methods=['POST'])
@login_required
def mark_message_read(message_id):
    """Marcar mensaje como leído"""
    conn = get_db_connection()
    conn.execute('UPDATE contact_messages SET read = 1 WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# ==================== FACTURACIÓN ROUTES ====================
@app.route('/facturacion')
@login_required
def facturacion_menu():
    """Menú principal de facturación"""
    return render_template('facturacion/menu.html')

# ========== MAESTRA DE ARS ==========
@app.route('/facturacion/ars')
@login_required
def facturacion_ars():
    """Lista de ARS"""
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    if search:
        ars_list = conn.execute(
            'SELECT * FROM ars WHERE (nombre_ars LIKE ? OR rnc LIKE ?) AND activo = 1 ORDER BY nombre_ars',
            (f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        ars_list = conn.execute('SELECT * FROM ars WHERE activo = 1 ORDER BY nombre_ars').fetchall()
    
    conn.close()
    return render_template('facturacion/ars.html', ars_list=ars_list, search=search)

@app.route('/facturacion/ars/nuevo', methods=['GET', 'POST'])
@login_required
def facturacion_ars_nuevo():
    """Crear nuevo ARS"""
    if request.method == 'POST':
        nombre_ars = sanitize_input(request.form['nombre_ars'], 200)
        rnc = sanitize_input(request.form['rnc'], 50)
        
        if not nombre_ars or not rnc:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('facturacion_ars_nuevo'))
        
        conn = get_db_connection()
        conn.execute('INSERT INTO ars (nombre_ars, rnc) VALUES (?, ?)', (nombre_ars, rnc))
        conn.commit()
        conn.close()
        
        flash('ARS creado exitosamente', 'success')
        return redirect(url_for('facturacion_ars'))
    
    return render_template('facturacion/ars_form.html', ars=None)

@app.route('/facturacion/ars/<int:ars_id>/editar', methods=['GET', 'POST'])
@login_required
def facturacion_ars_editar(ars_id):
    """Editar ARS"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre_ars = sanitize_input(request.form['nombre_ars'], 200)
        rnc = sanitize_input(request.form['rnc'], 50)
        
        if not nombre_ars or not rnc:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('facturacion_ars_editar', ars_id=ars_id))
        
        conn.execute('UPDATE ars SET nombre_ars = ?, rnc = ? WHERE id = ?', (nombre_ars, rnc, ars_id))
        conn.commit()
        conn.close()
        
        flash('ARS actualizado exitosamente', 'success')
        return redirect(url_for('facturacion_ars'))
    
    ars = conn.execute('SELECT * FROM ars WHERE id = ?', (ars_id,)).fetchone()
    conn.close()
    
    return render_template('facturacion/ars_form.html', ars=ars)

@app.route('/facturacion/ars/<int:ars_id>/eliminar', methods=['POST'])
@login_required
def facturacion_ars_eliminar(ars_id):
    """Eliminar ARS (soft delete)"""
    conn = get_db_connection()
    # Verificar si tiene códigos ARS relacionados
    relacionados = conn.execute('SELECT COUNT(*) FROM codigo_ars WHERE ars_id = ? AND activo = 1', (ars_id,)).fetchone()[0]
    
    if relacionados > 0:
        conn.close()
        flash(f'No se puede eliminar. Hay {relacionados} código(s) ARS asociados.', 'error')
        return redirect(url_for('facturacion_ars'))
    
    conn.execute('UPDATE ars SET activo = 0 WHERE id = ?', (ars_id,))
    conn.commit()
    conn.close()
    
    flash('ARS eliminado exitosamente', 'success')
    return redirect(url_for('facturacion_ars'))

# ========== MAESTRA DE MÉDICOS ==========
@app.route('/facturacion/medicos')
@login_required
def facturacion_medicos():
    """Lista de Médicos"""
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    if search:
        medicos_list = conn.execute(
            'SELECT * FROM medicos WHERE (nombre LIKE ? OR cedula LIKE ? OR especialidad LIKE ?) AND activo = 1 ORDER BY nombre',
            (f'%{search}%', f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        medicos_list = conn.execute('SELECT * FROM medicos WHERE activo = 1 ORDER BY nombre').fetchall()
    
    conn.close()
    return render_template('facturacion/medicos.html', medicos_list=medicos_list, search=search)

@app.route('/facturacion/medicos/nuevo', methods=['GET', 'POST'])
@login_required
def facturacion_medicos_nuevo():
    """Crear nuevo Médico"""
    if request.method == 'POST':
        nombre = sanitize_input(request.form['nombre'], 200)
        especialidad = sanitize_input(request.form['especialidad'], 100)
        cedula = sanitize_input(request.form['cedula'], 50)
        exequatur = sanitize_input(request.form.get('exequatur', ''), 50)
        email = sanitize_input(request.form.get('email', ''), 100)
        factura = 1 if request.form.get('factura') == '1' else 0
        
        if not nombre or not especialidad or not cedula:
            flash('Nombre, Especialidad y Cédula son obligatorios', 'error')
            return redirect(url_for('facturacion_medicos_nuevo'))
        
        # Validar email si se proporciona
        if email and not validate_email(email):
            flash('Formato de email inválido', 'error')
            return redirect(url_for('facturacion_medicos_nuevo'))
        
        conn = get_db_connection()
        # Verificar si la cédula ya existe
        existe = conn.execute('SELECT id FROM medicos WHERE cedula = ?', (cedula,)).fetchone()
        if existe:
            conn.close()
            flash('Ya existe un médico con esa cédula', 'error')
            return redirect(url_for('facturacion_medicos_nuevo'))
        
        conn.execute('INSERT INTO medicos (nombre, especialidad, cedula, exequatur, email, factura) VALUES (?, ?, ?, ?, ?, ?)', 
                    (nombre, especialidad, cedula, exequatur, email, factura))
        conn.commit()
        conn.close()
        
        flash('Médico creado exitosamente', 'success')
        return redirect(url_for('facturacion_medicos'))
    
    return render_template('facturacion/medicos_form.html', medico=None)

@app.route('/facturacion/medicos/<int:medico_id>/editar', methods=['GET', 'POST'])
@login_required
def facturacion_medicos_editar(medico_id):
    """Editar Médico"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = sanitize_input(request.form['nombre'], 200)
        especialidad = sanitize_input(request.form['especialidad'], 100)
        cedula = sanitize_input(request.form['cedula'], 50)
        exequatur = sanitize_input(request.form.get('exequatur', ''), 50)
        email = sanitize_input(request.form.get('email', ''), 100)
        factura = 1 if request.form.get('factura') == '1' else 0
        
        if not nombre or not especialidad or not cedula:
            flash('Nombre, Especialidad y Cédula son obligatorios', 'error')
            return redirect(url_for('facturacion_medicos_editar', medico_id=medico_id))
        
        # Validar email si se proporciona
        if email and not validate_email(email):
            flash('Formato de email inválido', 'error')
            return redirect(url_for('facturacion_medicos_editar', medico_id=medico_id))
        
        # Verificar si la cédula ya existe en otro médico
        existe = conn.execute('SELECT id FROM medicos WHERE cedula = ? AND id != ?', (cedula, medico_id)).fetchone()
        if existe:
            conn.close()
            flash('Ya existe otro médico con esa cédula', 'error')
            return redirect(url_for('facturacion_medicos_editar', medico_id=medico_id))
        
        conn.execute('UPDATE medicos SET nombre = ?, especialidad = ?, cedula = ?, exequatur = ?, email = ?, factura = ? WHERE id = ?', 
                    (nombre, especialidad, cedula, exequatur, email, factura, medico_id))
        conn.commit()
        conn.close()
        
        flash('Médico actualizado exitosamente', 'success')
        return redirect(url_for('facturacion_medicos'))
    
    medico = conn.execute('SELECT * FROM medicos WHERE id = ?', (medico_id,)).fetchone()
    conn.close()
    
    return render_template('facturacion/medicos_form.html', medico=medico)

@app.route('/facturacion/medicos/<int:medico_id>/eliminar', methods=['POST'])
@login_required
def facturacion_medicos_eliminar(medico_id):
    """Eliminar Médico (soft delete)"""
    conn = get_db_connection()
    # Verificar si tiene códigos ARS relacionados
    relacionados = conn.execute('SELECT COUNT(*) FROM codigo_ars WHERE medico_id = ? AND activo = 1', (medico_id,)).fetchone()[0]
    
    if relacionados > 0:
        conn.close()
        flash(f'No se puede eliminar. Hay {relacionados} código(s) ARS asociados.', 'error')
        return redirect(url_for('facturacion_medicos'))
    
    conn.execute('UPDATE medicos SET activo = 0 WHERE id = ?', (medico_id,))
    conn.commit()
    conn.close()
    
    flash('Médico eliminado exitosamente', 'success')
    return redirect(url_for('facturacion_medicos'))

# ========== MAESTRA DE CÓDIGO ARS ==========
@app.route('/facturacion/codigo-ars')
@login_required
def facturacion_codigo_ars():
    """Lista de Códigos ARS"""
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    if search:
        codigos_list = conn.execute('''
            SELECT ca.*, m.nombre as medico_nombre, a.nombre_ars 
            FROM codigo_ars ca
            JOIN medicos m ON ca.medico_id = m.id
            JOIN ars a ON ca.ars_id = a.id
            WHERE (m.nombre LIKE ? OR a.nombre_ars LIKE ? OR ca.codigo_ars LIKE ?) AND ca.activo = 1
            ORDER BY m.nombre, a.nombre_ars
        ''', (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        codigos_list = conn.execute('''
            SELECT ca.*, m.nombre as medico_nombre, a.nombre_ars 
            FROM codigo_ars ca
            JOIN medicos m ON ca.medico_id = m.id
            JOIN ars a ON ca.ars_id = a.id
            WHERE ca.activo = 1
            ORDER BY m.nombre, a.nombre_ars
        ''').fetchall()
    
    conn.close()
    return render_template('facturacion/codigo_ars.html', codigos_list=codigos_list, search=search)

@app.route('/facturacion/codigo-ars/nuevo', methods=['GET', 'POST'])
@login_required
def facturacion_codigo_ars_nuevo():
    """Crear nuevo Código ARS"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        medico_id = request.form.get('medico_id')
        ars_id = request.form.get('ars_id')
        codigo_ars = sanitize_input(request.form['codigo_ars'], 50)
        
        if not medico_id or not ars_id or not codigo_ars:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('facturacion_codigo_ars_nuevo'))
        
        # Verificar si ya existe la combinación médico-ars
        existe = conn.execute('SELECT id FROM codigo_ars WHERE medico_id = ? AND ars_id = ? AND activo = 1', 
                             (medico_id, ars_id)).fetchone()
        if existe:
            conn.close()
            flash('Ya existe un código para esta combinación de médico y ARS', 'error')
            return redirect(url_for('facturacion_codigo_ars_nuevo'))
        
        conn.execute('INSERT INTO codigo_ars (medico_id, ars_id, codigo_ars) VALUES (?, ?, ?)', 
                    (medico_id, ars_id, codigo_ars))
        conn.commit()
        conn.close()
        
        flash('Código ARS creado exitosamente', 'success')
        return redirect(url_for('facturacion_codigo_ars'))
    
    # Obtener listas para los select
    medicos = conn.execute('SELECT id, nombre, especialidad FROM medicos WHERE activo = 1 ORDER BY nombre').fetchall()
    ars_list = conn.execute('SELECT id, nombre_ars FROM ars WHERE activo = 1 ORDER BY nombre_ars').fetchall()
    conn.close()
    
    return render_template('facturacion/codigo_ars_form.html', codigo=None, medicos=medicos, ars_list=ars_list)

@app.route('/facturacion/codigo-ars/<int:codigo_id>/editar', methods=['GET', 'POST'])
@login_required
def facturacion_codigo_ars_editar(codigo_id):
    """Editar Código ARS"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        medico_id = request.form.get('medico_id')
        ars_id = request.form.get('ars_id')
        codigo_ars = sanitize_input(request.form['codigo_ars'], 50)
        
        if not medico_id or not ars_id or not codigo_ars:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('facturacion_codigo_ars_editar', codigo_id=codigo_id))
        
        # Verificar si ya existe la combinación en otro registro
        existe = conn.execute('SELECT id FROM codigo_ars WHERE medico_id = ? AND ars_id = ? AND id != ? AND activo = 1', 
                             (medico_id, ars_id, codigo_id)).fetchone()
        if existe:
            conn.close()
            flash('Ya existe un código para esta combinación de médico y ARS', 'error')
            return redirect(url_for('facturacion_codigo_ars_editar', codigo_id=codigo_id))
        
        conn.execute('UPDATE codigo_ars SET medico_id = ?, ars_id = ?, codigo_ars = ? WHERE id = ?', 
                    (medico_id, ars_id, codigo_ars, codigo_id))
        conn.commit()
        conn.close()
        
        flash('Código ARS actualizado exitosamente', 'success')
        return redirect(url_for('facturacion_codigo_ars'))
    
    codigo = conn.execute('SELECT * FROM codigo_ars WHERE id = ?', (codigo_id,)).fetchone()
    medicos = conn.execute('SELECT id, nombre, especialidad FROM medicos WHERE activo = 1 ORDER BY nombre').fetchall()
    ars_list = conn.execute('SELECT id, nombre_ars FROM ars WHERE activo = 1 ORDER BY nombre_ars').fetchall()
    conn.close()
    
    return render_template('facturacion/codigo_ars_form.html', codigo=codigo, medicos=medicos, ars_list=ars_list)

@app.route('/facturacion/codigo-ars/<int:codigo_id>/eliminar', methods=['POST'])
@login_required
def facturacion_codigo_ars_eliminar(codigo_id):
    """Eliminar Código ARS (soft delete)"""
    conn = get_db_connection()
    conn.execute('UPDATE codigo_ars SET activo = 0 WHERE id = ?', (codigo_id,))
    conn.commit()
    conn.close()
    
    flash('Código ARS eliminado exitosamente', 'success')
    return redirect(url_for('facturacion_codigo_ars'))

# ========== MAESTRA DE TIPOS DE SERVICIOS ==========
@app.route('/facturacion/servicios')
@login_required
def facturacion_servicios():
    """Lista de Tipos de Servicios"""
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    if search:
        servicios_list = conn.execute(
            'SELECT * FROM tipos_servicios WHERE descripcion LIKE ? AND activo = 1 ORDER BY descripcion',
            (f'%{search}%',)
        ).fetchall()
    else:
        servicios_list = conn.execute('SELECT * FROM tipos_servicios WHERE activo = 1 ORDER BY descripcion').fetchall()
    
    conn.close()
    return render_template('facturacion/servicios.html', servicios_list=servicios_list, search=search)

@app.route('/facturacion/servicios/nuevo', methods=['GET', 'POST'])
@login_required
def facturacion_servicios_nuevo():
    """Crear nuevo Tipo de Servicio"""
    if request.method == 'POST':
        descripcion = sanitize_input(request.form['descripcion'], 200)
        precio_base = request.form.get('precio_base', 0)
        
        if not descripcion:
            flash('La descripción es obligatoria', 'error')
            return redirect(url_for('facturacion_servicios_nuevo'))
        
        try:
            precio_base = float(precio_base) if precio_base else 0
        except ValueError:
            precio_base = 0
        
        conn = get_db_connection()
        conn.execute('INSERT INTO tipos_servicios (descripcion, precio_base) VALUES (?, ?)', 
                    (descripcion, precio_base))
        conn.commit()
        conn.close()
        
        flash('Tipo de servicio creado exitosamente', 'success')
        return redirect(url_for('facturacion_servicios'))
    
    return render_template('facturacion/servicios_form.html', servicio=None)

@app.route('/facturacion/servicios/<int:servicio_id>/editar', methods=['GET', 'POST'])
@login_required
def facturacion_servicios_editar(servicio_id):
    """Editar Tipo de Servicio"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        descripcion = sanitize_input(request.form['descripcion'], 200)
        precio_base = request.form.get('precio_base', 0)
        
        if not descripcion:
            flash('La descripción es obligatoria', 'error')
            return redirect(url_for('facturacion_servicios_editar', servicio_id=servicio_id))
        
        try:
            precio_base = float(precio_base) if precio_base else 0
        except ValueError:
            precio_base = 0
        
        conn.execute('UPDATE tipos_servicios SET descripcion = ?, precio_base = ? WHERE id = ?', 
                    (descripcion, precio_base, servicio_id))
        conn.commit()
        conn.close()
        
        flash('Tipo de servicio actualizado exitosamente', 'success')
        return redirect(url_for('facturacion_servicios'))
    
    servicio = conn.execute('SELECT * FROM tipos_servicios WHERE id = ?', (servicio_id,)).fetchone()
    conn.close()
    
    return render_template('facturacion/servicios_form.html', servicio=servicio)

@app.route('/facturacion/servicios/<int:servicio_id>/eliminar', methods=['POST'])
@login_required
def facturacion_servicios_eliminar(servicio_id):
    """Eliminar Tipo de Servicio (soft delete)"""
    conn = get_db_connection()
    conn.execute('UPDATE tipos_servicios SET activo = 0 WHERE id = ?', (servicio_id,))
    conn.commit()
    conn.close()
    
    flash('Tipo de servicio eliminado exitosamente', 'success')
    return redirect(url_for('facturacion_servicios'))

# ========== MAESTRA DE PACIENTES ==========
@app.route('/facturacion/pacientes')
@login_required
def facturacion_pacientes():
    """Lista de Pacientes Únicos"""
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    if search:
        pacientes_list = conn.execute('''
            SELECT p.*, a.nombre_ars,
                   (SELECT COUNT(*) FROM facturas_detalle fd WHERE fd.paciente_id = p.id AND fd.activo = 1) as total_registros
            FROM pacientes p
            LEFT JOIN ars a ON p.ars_id = a.id
            WHERE (p.nss LIKE ? OR p.nombre LIKE ?) AND p.activo = 1
            ORDER BY p.nombre
        ''', (f'%{search}%', f'%{search}%')).fetchall()
    else:
        pacientes_list = conn.execute('''
            SELECT p.*, a.nombre_ars,
                   (SELECT COUNT(*) FROM facturas_detalle fd WHERE fd.paciente_id = p.id AND fd.activo = 1) as total_registros
            FROM pacientes p
            LEFT JOIN ars a ON p.ars_id = a.id
            WHERE p.activo = 1
            ORDER BY p.nombre
        ''').fetchall()
    
    conn.close()
    return render_template('facturacion/pacientes.html', pacientes_list=pacientes_list, search=search)

# ========== MAESTRA DE NCF ==========
@app.route('/facturacion/ncf')
@login_required
def facturacion_ncf():
    """Lista de NCF"""
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    if search:
        ncf_list = conn.execute(
            'SELECT * FROM ncf WHERE (tipo LIKE ? OR prefijo LIKE ?) AND activo = 1 ORDER BY tipo',
            (f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        ncf_list = conn.execute('SELECT * FROM ncf WHERE activo = 1 ORDER BY tipo').fetchall()
    
    # Calcular el próximo número para cada registro
    ncf_with_proximo = []
    for ncf in ncf_list:
        ncf_dict = dict(ncf)
        ncf_dict['proximo_numero'] = ncf_dict['ultimo_numero'] + 1
        ncf_with_proximo.append(ncf_dict)
    
    conn.close()
    return render_template('facturacion/ncf.html', ncf_list=ncf_with_proximo, search=search)

@app.route('/facturacion/ncf/nuevo', methods=['GET', 'POST'])
@login_required
def facturacion_ncf_nuevo():
    """Crear nuevo NCF"""
    if request.method == 'POST':
        tipo = sanitize_input(request.form['tipo'], 100)
        prefijo = sanitize_input(request.form['prefijo'], 10)
        tamaño = request.form.get('tamaño', 0)
        ultimo_numero = request.form.get('ultimo_numero', 0)
        fecha_fin = request.form.get('fecha_fin', '')
        
        if not tipo or not prefijo or not tamaño:
            flash('Los campos Tipo, Prefijo y Tamaño son obligatorios', 'error')
            return redirect(url_for('facturacion_ncf_nuevo'))
        
        try:
            tamaño = int(tamaño)
            ultimo_numero = int(ultimo_numero) if ultimo_numero else 0
        except ValueError:
            flash('Tamaño y Último Número deben ser números enteros', 'error')
            return redirect(url_for('facturacion_ncf_nuevo'))
        
        conn = get_db_connection()
        conn.execute('INSERT INTO ncf (tipo, prefijo, tamaño, ultimo_numero, fecha_fin) VALUES (?, ?, ?, ?, ?)', 
                    (tipo, prefijo, tamaño, ultimo_numero, fecha_fin if fecha_fin else None))
        conn.commit()
        conn.close()
        
        flash('NCF creado exitosamente', 'success')
        return redirect(url_for('facturacion_ncf'))
    
    return render_template('facturacion/ncf_form.html', ncf=None)

@app.route('/facturacion/ncf/<int:ncf_id>/editar', methods=['GET', 'POST'])
@login_required
def facturacion_ncf_editar(ncf_id):
    """Editar NCF"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        tipo = sanitize_input(request.form['tipo'], 100)
        prefijo = sanitize_input(request.form['prefijo'], 10)
        tamaño = request.form.get('tamaño', 0)
        ultimo_numero = request.form.get('ultimo_numero', 0)
        fecha_fin = request.form.get('fecha_fin', '')
        
        if not tipo or not prefijo or not tamaño:
            flash('Los campos Tipo, Prefijo y Tamaño son obligatorios', 'error')
            return redirect(url_for('facturacion_ncf_editar', ncf_id=ncf_id))
        
        try:
            tamaño = int(tamaño)
            ultimo_numero = int(ultimo_numero) if ultimo_numero else 0
        except ValueError:
            flash('Tamaño y Último Número deben ser números enteros', 'error')
            return redirect(url_for('facturacion_ncf_editar', ncf_id=ncf_id))
        
        conn.execute('UPDATE ncf SET tipo = ?, prefijo = ?, tamaño = ?, ultimo_numero = ?, fecha_fin = ? WHERE id = ?', 
                    (tipo, prefijo, tamaño, ultimo_numero, fecha_fin if fecha_fin else None, ncf_id))
        conn.commit()
        conn.close()
        
        flash('NCF actualizado exitosamente', 'success')
        return redirect(url_for('facturacion_ncf'))
    
    ncf = conn.execute('SELECT * FROM ncf WHERE id = ?', (ncf_id,)).fetchone()
    conn.close()
    
    return render_template('facturacion/ncf_form.html', ncf=ncf)

@app.route('/facturacion/ncf/<int:ncf_id>/eliminar', methods=['POST'])
@login_required
def facturacion_ncf_eliminar(ncf_id):
    """Eliminar NCF (soft delete)"""
    conn = get_db_connection()
    conn.execute('UPDATE ncf SET activo = 0 WHERE id = ?', (ncf_id,))
    conn.commit()
    conn.close()
    
    flash('NCF eliminado exitosamente', 'success')
    return redirect(url_for('facturacion_ncf'))

# ========== PACIENTES A FACTURAR ==========
@app.route('/facturacion/pacientes-pendientes')
@login_required
def facturacion_pacientes_pendientes():
    """Lista de pacientes pendientes/facturados - Estado de Facturación"""
    # Obtener filtros opcionales
    medico_id = request.args.get('medico_id', type=int)
    ars_id = request.args.get('ars_id', type=int)
    estado = request.args.get('estado', default='pendiente')  # Por defecto: pendiente
    
    conn = get_db_connection()
    
    # Construir query con filtros opcionales
    query = '''
        SELECT fd.*, m.nombre as medico_nombre, a.nombre_ars, p.nombre as paciente_nombre_completo
        FROM facturas_detalle fd
        JOIN medicos m ON fd.medico_id = m.id
        JOIN ars a ON fd.ars_id = a.id
        JOIN pacientes p ON fd.paciente_id = p.id
        WHERE fd.activo = 1 AND fd.estado = ?
    '''
    params = [estado]
    
    # Si el usuario tiene rol "Registro de Facturas", filtrar solo sus pacientes
    if current_user.perfil == 'Registro de Facturas':
        query += ' AND m.email = ?'
        params.append(current_user.email)
    
    if medico_id:
        query += ' AND fd.medico_id = ?'
        params.append(medico_id)
    
    if ars_id:
        query += ' AND fd.ars_id = ?'
        params.append(ars_id)
    
    query += ' ORDER BY fd.created_at DESC'
    
    pendientes = conn.execute(query, params).fetchall()
    
    # Obtener listas para los filtros
    # Filtrar médicos según el perfil del usuario
    if current_user.perfil == 'Registro de Facturas':
        # Solo mostrar el médico con el mismo email del usuario
        medicos = conn.execute('SELECT * FROM medicos WHERE activo = 1 AND email = ? ORDER BY nombre', (current_user.email,)).fetchall()
    else:
        # Administrador: mostrar todos los médicos
        medicos = conn.execute('SELECT * FROM medicos WHERE activo = 1 ORDER BY nombre').fetchall()
    
    ars_list = conn.execute('SELECT * FROM ars WHERE activo = 1 ORDER BY nombre_ars').fetchall()
    
    # Obtener nombres seleccionados para mostrar en el template
    medico_seleccionado = None
    ars_seleccionada = None
    
    if medico_id:
        medico = conn.execute('SELECT nombre FROM medicos WHERE id = ?', (medico_id,)).fetchone()
        if medico:
            medico_seleccionado = medico['nombre']
    
    if ars_id:
        ars = conn.execute('SELECT nombre_ars FROM ars WHERE id = ?', (ars_id,)).fetchone()
        if ars:
            ars_seleccionada = ars['nombre_ars']
    
    conn.close()
    
    return render_template('facturacion/pacientes_pendientes.html', 
                         pendientes=pendientes,
                         medicos=medicos,
                         ars_list=ars_list,
                         medico_id_filtro=medico_id,
                         ars_id_filtro=ars_id,
                         estado_filtro=estado,
                         medico_seleccionado=medico_seleccionado,
                         ars_seleccionada=ars_seleccionada)

@app.route('/facturacion/pacientes-pendientes/pdf')
@login_required
def facturacion_pacientes_pendientes_pdf():
    """Generar PDF de pacientes pendientes/facturados con filtros opcionales"""
    if not REPORTLAB_AVAILABLE:
        flash('ReportLab no está instalado. Instalar con: pip install reportlab', 'error')
        return redirect(url_for('facturacion_pacientes_pendientes'))
    
    # Obtener filtros opcionales
    medico_id = request.args.get('medico_id', type=int)
    ars_id = request.args.get('ars_id', type=int)
    estado = request.args.get('estado', default='pendiente')
    
    conn = get_db_connection()
    
    # Construir query con filtros opcionales (mismo que la vista)
    query = '''
        SELECT fd.*, m.nombre as medico_nombre, a.nombre_ars, p.nombre as paciente_nombre_completo
        FROM facturas_detalle fd
        JOIN medicos m ON fd.medico_id = m.id
        JOIN ars a ON fd.ars_id = a.id
        JOIN pacientes p ON fd.paciente_id = p.id
        WHERE fd.activo = 1 AND fd.estado = ?
    '''
    params = [estado]
    
    # Si el usuario tiene rol "Registro de Facturas", filtrar solo sus pacientes
    if current_user.perfil == 'Registro de Facturas':
        query += ' AND m.email = ?'
        params.append(current_user.email)
    
    if medico_id:
        query += ' AND fd.medico_id = ?'
        params.append(medico_id)
    
    if ars_id:
        query += ' AND fd.ars_id = ?'
        params.append(ars_id)
    
    query += ' ORDER BY fd.created_at DESC'
    
    pendientes = conn.execute(query, params).fetchall()
    
    # Obtener nombres para el encabezado si hay filtros
    medico_nombre = None
    ars_nombre = None
    
    if medico_id:
        medico = conn.execute('SELECT nombre FROM medicos WHERE id = ?', (medico_id,)).fetchone()
        if medico:
            medico_nombre = medico['nombre']
    
    if ars_id:
        ars = conn.execute('SELECT nombre_ars FROM ars WHERE id = ?', (ars_id,)).fetchone()
        if ars:
            ars_nombre = ars['nombre_ars']
    
    conn.close()
    
    # Crear PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    
    # Contenedor de elementos
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#CEB0B7'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#ACACAD'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    # Agregar encabezado
    elements.append(Paragraph("Dra. Shirley Ramírez", title_style))
    elements.append(Paragraph("Ginecóloga y Obstetra", subtitle_style))
    elements.append(Spacer(1, 12))
    
    # Título del documento
    doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#282828'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    # Título dinámico según el estado
    titulo_documento = "PACIENTES PENDIENTES DE FACTURACIÓN" if estado == 'pendiente' else "PACIENTES FACTURADOS"
    elements.append(Paragraph(titulo_documento, doc_title))
    elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", subtitle_style))
    
    # Mostrar filtros en el encabezado si están activos
    if medico_nombre or ars_nombre:
        filter_style = ParagraphStyle(
            'FilterInfo',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#CEB0B7'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        if medico_nombre:
            elements.append(Paragraph(f"<b>Médico:</b> {medico_nombre}", filter_style))
        if ars_nombre:
            elements.append(Paragraph(f"<b>ARS:</b> {ars_nombre}", filter_style))
    
    elements.append(Spacer(1, 20))
    
    if pendientes:
        # Determinar columnas según filtros
        # Sin filtros: Incluir Médico y ARS en cada línea
        # Con filtros: Excluir las columnas filtradas
        
        if not medico_nombre and not ars_nombre:
            # SIN FILTROS: Mostrar Médico y ARS en cada línea
            data = [['No.', 'NSS', 'Nombre', 'Fecha', 'Servicio', 'Monto', 'Médico', 'ARS']]
            col_widths = [0.5*inch, 1.1*inch, 1.5*inch, 0.8*inch, 1.6*inch, 0.9*inch, 1.2*inch, 1*inch]
            
            total = 0
            for idx, p in enumerate(pendientes, 1):
                data.append([
                    str(idx),
                    str(p['nss']),
                    str(p['nombre_paciente'])[:22],
                    str(p['fecha_servicio']),
                    str(p['descripcion_servicio'])[:25],
                    f"{p['monto']:,.2f}",
                    str(p['medico_nombre'])[:18],
                    str(p['nombre_ars'])[:15]
                ])
                total += p['monto']
            
            # Agregar fila de total
            data.append(['', '', '', '', 'TOTAL:', f"{total:,.2f}", '', ''])
            total_col = 5
            
        elif medico_nombre and not ars_nombre:
            # FILTRO DE MÉDICO: No mostrar Médico en líneas, sí mostrar ARS
            data = [['No.', 'NSS', 'Nombre', 'Fecha', 'Servicio', 'Monto', 'ARS']]
            col_widths = [0.5*inch, 1.2*inch, 1.8*inch, 0.9*inch, 2*inch, 1*inch, 1.2*inch]
            
            total = 0
            for idx, p in enumerate(pendientes, 1):
                data.append([
                    str(idx),
                    str(p['nss']),
                    str(p['nombre_paciente'])[:25],
                    str(p['fecha_servicio']),
                    str(p['descripcion_servicio'])[:30],
                    f"{p['monto']:,.2f}",
                    str(p['nombre_ars'])[:18]
                ])
                total += p['monto']
            
            data.append(['', '', '', '', 'TOTAL:', f"{total:,.2f}", ''])
            total_col = 5
            
        elif not medico_nombre and ars_nombre:
            # FILTRO DE ARS: No mostrar ARS en líneas, sí mostrar Médico
            data = [['No.', 'NSS', 'Nombre', 'Fecha', 'Servicio', 'Monto', 'Médico']]
            col_widths = [0.5*inch, 1.2*inch, 1.8*inch, 0.9*inch, 2*inch, 1*inch, 1.5*inch]
            
            total = 0
            for idx, p in enumerate(pendientes, 1):
                data.append([
                    str(idx),
                    str(p['nss']),
                    str(p['nombre_paciente'])[:25],
                    str(p['fecha_servicio']),
                    str(p['descripcion_servicio'])[:30],
                    f"{p['monto']:,.2f}",
                    str(p['medico_nombre'])[:22]
                ])
                total += p['monto']
            
            data.append(['', '', '', '', 'TOTAL:', f"{total:,.2f}", ''])
            total_col = 5
            
        else:
            # AMBOS FILTROS: No mostrar ni Médico ni ARS en líneas
            data = [['No.', 'NSS', 'Nombre', 'Fecha', 'Servicio', 'Monto']]
            col_widths = [0.6*inch, 1.5*inch, 2.2*inch, 1*inch, 2.5*inch, 1.2*inch]
            
            total = 0
            for idx, p in enumerate(pendientes, 1):
                data.append([
                    str(idx),
                    str(p['nss']),
                    str(p['nombre_paciente'])[:30],
                    str(p['fecha_servicio']),
                    str(p['descripcion_servicio'])[:35],
                    f"{p['monto']:,.2f}"
                ])
                total += p['monto']
            
            data.append(['', '', '', '', 'TOTAL:', f"{total:,.2f}"])
            total_col = 5
        
        # Crear tabla con estilos
        t = Table(data, colWidths=col_widths)
        
        t.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CEB0B7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Datos
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -2), colors.HexColor('#282828')),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # No. centrado
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),    # Monto alineado a derecha
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F2E2E6')]),
            
            # Total
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ACACAD')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 10),
            ('ALIGN', (4, -1), (5, -1), 'RIGHT'),
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ACACAD')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        # Información adicional
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            alignment=TA_LEFT
        )
        elements.append(Paragraph(f"<b>Total de pacientes:</b> {len(pendientes)}", info_style))
        elements.append(Paragraph(f"<b>Monto total pendiente:</b> {total:,.2f}", info_style))
    else:
        elements.append(Paragraph("No hay pacientes pendientes de facturación.", subtitle_style))
    
    # Pie de página
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#999999'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Este documento es una constancia de los pacientes pendientes de facturación.", footer_style))
    elements.append(Paragraph("Dra. Shirley Ramírez - Ginecóloga y Obstetra", footer_style))
    
    # Construir PDF
    doc.build(elements)
    
    # Obtener PDF del buffer
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'pacientes_pendientes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

@app.route('/facturacion/pacientes-agregados/pdf')
@login_required
def facturacion_pacientes_agregados_pdf():
    """Generar PDF de los pacientes recién agregados"""
    if not REPORTLAB_AVAILABLE:
        flash('ReportLab no está instalado. Instalar con: pip install reportlab', 'error')
        return redirect(url_for('facturacion_pacientes_pendientes'))
    
    # Obtener los IDs de la sesión
    ids_agregados = session.get('ultimos_pacientes_agregados', [])
    
    if not ids_agregados:
        flash('No hay registros recientes para generar PDF', 'warning')
        return redirect(url_for('facturacion_pacientes_pendientes'))
    
    # Copiar los IDs para poder limpiar la sesión pero mantener la referencia
    ids_temp = ids_agregados.copy()
    # Limpiar la sesión
    session.pop('ultimos_pacientes_agregados', None)
    
    # Obtener los registros de la base de datos
    conn = get_db_connection()
    placeholders = ','.join(['?' for _ in ids_agregados])
    pendientes = conn.execute(f'''
        SELECT fd.*, m.nombre as medico_nombre, m.email as medico_email, m.especialidad as medico_especialidad, 
               a.nombre_ars, p.nombre as paciente_nombre_completo
        FROM facturas_detalle fd
        JOIN medicos m ON fd.medico_id = m.id
        JOIN ars a ON fd.ars_id = a.id
        JOIN pacientes p ON fd.paciente_id = p.id
        WHERE fd.id IN ({placeholders}) AND fd.activo = 1
        ORDER BY fd.id DESC
    ''', ids_agregados).fetchall()
    
    if not pendientes:
        conn.close()
        flash('No se encontraron los registros', 'error')
        return redirect(url_for('facturacion_pacientes_pendientes'))
    
    # Obtener datos del médico ANTES de cerrar la conexión
    medico_id = pendientes[0]['medico_id']
    medico_nombre = pendientes[0]['medico_nombre']
    medico_email = pendientes[0]['medico_email']
    medico_especialidad = pendientes[0]['medico_especialidad']
    
    # Cerrar conexión aquí, ya tenemos todos los datos
    conn.close()
    
    # Crear PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    
    # Contenedor de elementos
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#CEB0B7'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#ACACAD'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    # Agregar encabezado con el nombre del médico seleccionado
    elements.append(Paragraph(medico_nombre, title_style))
    elements.append(Paragraph(medico_especialidad, subtitle_style))
    elements.append(Spacer(1, 12))
    
    # Título del documento
    doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#282828'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph("CONSTANCIA - PACIENTES AGREGADOS", doc_title))
    elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", subtitle_style))
    elements.append(Spacer(1, 20))
    
    # Banner de confirmación
    confirmation_style = ParagraphStyle(
        'Confirmation',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#28a745'),
        spaceAfter=15,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph(f"✓ {len(pendientes)} PACIENTE(S) AGREGADO(S) EXITOSAMENTE", confirmation_style))
    elements.append(Paragraph("Estado: PENDIENTE DE FACTURACIÓN", subtitle_style))
    elements.append(Spacer(1, 15))
    
    # Crear tabla
    data = [['No.', 'NSS', 'Nombre', 'Fecha', 'Servicio', 'Monto', 'ARS']]
    
    total = 0
    for idx, p in enumerate(pendientes, 1):
        data.append([
            str(idx),
            str(p['nss']),
            str(p['nombre_paciente'])[:25],  # Limitar nombre
            str(p['fecha_servicio']),
            str(p['descripcion_servicio'])[:30],  # Limitar servicio
            f"{p['monto']:,.2f}",
            str(p['nombre_ars'])[:15]  # Limitar ARS
        ])
        total += p['monto']
    
    # Agregar fila de total
    data.append(['', '', '', '', 'TOTAL:', f"{total:,.2f}", ''])
    
    # Crear tabla con estilos - ajustar anchos de columna
    t = Table(data, colWidths=[0.5*inch, 1.1*inch, 1.9*inch, 0.9*inch, 2*inch, 1*inch, 1.1*inch])
    
    t.setStyle(TableStyle([
        # Encabezado - Color oscuro #B89BA3
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#B89BA3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Datos
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -2), colors.HexColor('#282828')),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # No. centrado
        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),    # Monto alineado a derecha
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F8F4F5')]),
        
        # Total - Color gris más oscuro
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#9A9A9B')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('ALIGN', (4, -1), (5, -1), 'RIGHT'),
        
        # Bordes
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#B89BA3')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 7),
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 20))
    
    # Información adicional
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666'),
        alignment=TA_LEFT
    )
    elements.append(Paragraph(f"<b>Total de pacientes agregados:</b> {len(pendientes)}", info_style))
    elements.append(Paragraph(f"<b>Monto total:</b> {total:,.2f}", info_style))
    elements.append(Paragraph(f"<b>Médico:</b> {pendientes[0]['medico_nombre']}", info_style))
    elements.append(Paragraph(f"<b>ARS:</b> {pendientes[0]['nombre_ars']}", info_style))
    
    # Nota importante
    elements.append(Spacer(1, 20))
    note_style = ParagraphStyle(
        'Note',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#dc3545'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph("IMPORTANTE: Estos pacientes están PENDIENTES DE FACTURACIÓN", note_style))
    
    # Pie de página
    elements.append(Spacer(1, 20))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#999999'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Este documento es una constancia de los pacientes agregados al sistema.", footer_style))
    elements.append(Paragraph(f"{medico_nombre} - {medico_especialidad}", footer_style))
    
    # Construir PDF
    doc.build(elements)
    
    # Obtener PDF del buffer
    buffer.seek(0)
    
    # Enviar el PDF por email si el médico tiene email registrado
    if medico_email:
        # Crear una copia del buffer para el email
        email_buffer = BytesIO(buffer.getvalue())
        buffer.seek(0)  # Resetear el buffer original
        
        # Enviar email con PDF adjunto
        enviar_email_pdf_pacientes(
            medico_email,
            medico_nombre,
            email_buffer,
            len(pendientes),
            total
        )
        
        flash(f'✅ PDF enviado al correo: {medico_email}', 'success')
    else:
        flash('⚠️ El médico no tiene email registrado. Solo se descargará el PDF.', 'warning')
    
    # Enviar el PDF directamente para descargar
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'constancia_pacientes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

@app.route('/facturacion/pacientes-pendientes/agregar', methods=['GET', 'POST'])
@login_required
def facturacion_facturas_nueva():
    """Agregar pacientes pendientes de facturación"""
    if request.method == 'POST':
        conn = None
        try:
            conn = get_db_connection()
            
            # Datos del encabezado
            medico_id = request.form.get('medico_id')
            ars_id = request.form.get('ars_id')
            
            # Datos de las líneas (vienen como JSON)
            import json
            lineas_json = request.form.get('lineas_json')
            lineas = json.loads(lineas_json) if lineas_json else []
            
            if not medico_id or not ars_id:
                flash('Médico y ARS son obligatorios', 'error')
                return redirect(url_for('facturacion_facturas_nueva'))
            
            if not lineas:
                flash('Debe agregar al menos un paciente', 'error')
                return redirect(url_for('facturacion_facturas_nueva'))
            
            cursor = conn.cursor()
            
            # Lista para guardar los IDs de los registros creados
            ids_creados = []
            errores = []
            
            # Procesar cada línea como PENDIENTE (sin factura_id)
            for idx, linea in enumerate(lineas, start=1):
                nss = linea.get('nss', '').strip()
                nombre = linea.get('nombre', '').strip().upper()
                fecha_servicio = linea.get('fecha', '')
                autorizacion = linea.get('autorizacion', '').strip()
                servicio_desc = linea.get('servicio', '').strip().upper()
                monto = float(linea.get('monto', 0))
                
                # VALIDACIÓN: Verificar si ya existe el mismo registro (NSS + FECHA + AUTORIZACIÓN + ARS)
                duplicado = conn.execute('''
                    SELECT * FROM facturas_detalle 
                    WHERE nss = ? AND fecha_servicio = ? AND autorizacion = ? AND ars_id = ? AND activo = 1
                ''', (nss, fecha_servicio, autorizacion, ars_id)).fetchone()
                
                if duplicado:
                    errores.append(f'Línea {idx}: Registro duplicado - NSS {nss}, Fecha {fecha_servicio}, Autorización {autorizacion} ya existe')
                    continue
                
                # Buscar o crear paciente (llave única: NSS + ARS)
                paciente = conn.execute('SELECT * FROM pacientes WHERE nss = ? AND ars_id = ?', 
                                       (nss, ars_id)).fetchone()
                if paciente:
                    paciente_id = paciente['id']
                    # Actualizar nombre si cambió
                    conn.execute('UPDATE pacientes SET nombre = ? WHERE id = ?',
                               (nombre, paciente_id))
                else:
                    # Crear nuevo paciente con esta combinación NSS + ARS
                    cursor.execute('INSERT INTO pacientes (nss, nombre, ars_id) VALUES (?, ?, ?)',
                                 (nss, nombre, ars_id))
                    paciente_id = cursor.lastrowid
                
                # Buscar o crear servicio
                servicio = conn.execute('SELECT * FROM tipos_servicios WHERE descripcion = ? AND activo = 1',
                                      (servicio_desc,)).fetchone()
                if servicio:
                    servicio_id = servicio['id']
                else:
                    # Crear servicio automáticamente
                    cursor.execute('INSERT INTO tipos_servicios (descripcion, precio_base) VALUES (?, ?)',
                                 (servicio_desc, monto))
                    servicio_id = cursor.lastrowid
                
                # Insertar registro PENDIENTE (sin factura_id)
                cursor.execute('''
                    INSERT INTO facturas_detalle 
                    (paciente_id, nss, nombre_paciente, fecha_servicio, autorizacion, 
                     servicio_id, descripcion_servicio, monto, medico_id, ars_id, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pendiente')
                ''', (paciente_id, nss, nombre, fecha_servicio, autorizacion, 
                     servicio_id, servicio_desc, monto, medico_id, ars_id))
                
                # Guardar el ID del registro creado
                ids_creados.append(cursor.lastrowid)
            
            # Si hubo errores de duplicados, informar al usuario
            if errores:
                conn.rollback()
                for error in errores:
                    flash(error, 'error')
                return redirect(url_for('facturacion_facturas_nueva'))
            
            conn.commit()
            
            # Guardar los IDs en la sesión para generar el PDF
            session['ultimos_pacientes_agregados'] = ids_creados
            session['descargar_pdf_pacientes'] = True  # Flag para disparar descarga automática
            
            flash(f'✅ {len(lineas)} paciente(s) agregado(s) como PENDIENTES DE FACTURACIÓN', 'success')
            
            # Redirigir de vuelta al formulario (limpio) con flag para descargar PDF
            return redirect(url_for('facturacion_facturas_nueva'))
            
        except Exception as e:
            if conn:
                conn.rollback()
            flash(f'Error al agregar pacientes: {str(e)}', 'error')
            return redirect(url_for('facturacion_facturas_nueva'))
        finally:
            if conn:
                conn.close()
    
    # GET: Mostrar formulario
    conn = get_db_connection()
    try:
        # Filtrar médicos según el perfil del usuario
        if current_user.perfil == 'Registro de Facturas':
            # Solo mostrar el médico con el mismo email del usuario
            medicos = conn.execute('SELECT * FROM medicos WHERE activo = 1 AND email = ? ORDER BY nombre', (current_user.email,)).fetchall()
        else:
            # Administrador: mostrar todos los médicos
            medicos = conn.execute('SELECT * FROM medicos WHERE activo = 1 ORDER BY nombre').fetchall()
        
        ars_list = conn.execute('SELECT * FROM ars WHERE activo = 1 ORDER BY nombre_ars').fetchall()
        servicios_list = conn.execute('SELECT * FROM tipos_servicios WHERE activo = 1 ORDER BY descripcion').fetchall()
        
        # Verificar si hay que descargar el PDF automáticamente
        descargar_pdf = session.pop('descargar_pdf_pacientes', False)
        
        return render_template('facturacion/facturas_form.html', 
                             medicos=medicos, 
                             ars_list=ars_list, 
                             servicios_list=servicios_list,
                             descargar_pdf=descargar_pdf)
    finally:
        conn.close()

# ========== DESCARGAR PLANTILLA EXCEL ==========
@app.route('/facturacion/descargar-plantilla-excel')
@login_required
def descargar_plantilla_excel():
    """Generar y descargar plantilla Excel para carga masiva"""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
        from openpyxl.utils import get_column_letter
        from openpyxl.worksheet.datavalidation import DataValidation
        from io import BytesIO
        
        # Crear un nuevo workbook
        wb = Workbook()
        
        # Hoja 1: Plantilla de Pacientes
        ws_pacientes = wb.active
        ws_pacientes.title = "Pacientes"
        
        # Encabezados
        headers = ['NSS', 'NOMBRE', 'FECHA', 'AUTORIZACIÓN', 'SERVICIO', 'MONTO']
        ws_pacientes.append(headers)
        
        # Estilo para encabezados
        header_fill = PatternFill(start_color="CEB0B7", end_color="CEB0B7", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF", size=12)
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        # Aplicar estilo y protección a los encabezados
        for col_num, header in enumerate(headers, 1):
            cell = ws_pacientes.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment
            cell.protection = Protection(locked=True)  # Proteger encabezado
        
        # Ajustar ancho de columnas
        column_widths = {'A': 15, 'B': 30, 'C': 12, 'D': 15, 'E': 30, 'F': 12}
        for col, width in column_widths.items():
            ws_pacientes.column_dimensions[col].width = width
        
        # Hoja 2: Lista de Servicios
        ws_servicios = wb.create_sheet("Servicios Disponibles")
        ws_servicios.append(['SERVICIOS DISPONIBLES', 'PRECIO BASE'])
        
        # Encabezados hoja servicios
        for col_num in range(1, 3):
            cell = ws_servicios.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment
        
        # Obtener servicios de la base de datos
        conn = get_db_connection()
        servicios = conn.execute('SELECT descripcion, precio_base FROM tipos_servicios WHERE activo = 1 ORDER BY descripcion').fetchall()
        conn.close()
        
        # Validar que servicios no sea None
        if servicios is None:
            servicios = []
        
        for servicio in servicios:
            ws_servicios.append([servicio['descripcion'], f"{servicio['precio_base']:,.2f}" if servicio['precio_base'] else ''])
        
        # Ajustar ancho de columnas en hoja servicios
        ws_servicios.column_dimensions['A'].width = 40
        ws_servicios.column_dimensions['B'].width = 15
        
        # Crear lista desplegable para la columna SERVICIO (columna E)
        # Referencia: desde la fila 2 hasta la última fila con servicios en la hoja "Servicios Disponibles"
        num_servicios = len(servicios) if servicios else 0
        if num_servicios > 0:
            # Crear la validación de datos
            dv = DataValidation(
                type="list",
                formula1=f"'Servicios Disponibles'!$A$2:$A${num_servicios + 1}",
                allow_blank=False
            )
            dv.error = 'Seleccione un servicio de la lista'
            dv.errorTitle = 'Servicio Inválido'
            dv.prompt = 'Por favor seleccione un servicio de la lista desplegable'
            dv.promptTitle = 'Seleccionar Servicio'
            
            # Aplicar la validación a la columna E (SERVICIO) desde la fila 2 hasta la 1000
            ws_pacientes.add_data_validation(dv)
            dv.add('E2:E1000')
        
        # Agregar filas vacías para poder aplicar protección
        # Agregamos al menos 100 filas vacías para que el usuario pueda trabajar
        for i in range(2, 102):  # Filas 2 a 101
            ws_pacientes.append(['', '', '', '', '', ''])
        
        # Desbloquear las celdas de datos (filas 2 en adelante) y alinear a la izquierda
        alineacion_izquierda = Alignment(horizontal='left', vertical='center')
        for row in range(2, 102):
            for col in range(1, 7):  # Columnas A-F (1-6)
                cell = ws_pacientes.cell(row=row, column=col)
                cell.protection = Protection(locked=False)
                cell.alignment = alineacion_izquierda
        
        # Proteger la hoja de Pacientes (solo el encabezado quedará bloqueado)
        ws_pacientes.protection.sheet = True
        ws_pacientes.protection.password = ''  # Sin contraseña para facilitar uso
        ws_pacientes.protection.enable()
        
        # Hoja 3: Instrucciones
        ws_instrucciones = wb.create_sheet("Instrucciones")
        instrucciones = [
            ['INSTRUCCIONES PARA CARGAR PACIENTES'],
            [''],
            ['1. Complete la hoja "Pacientes" con los datos de los pacientes'],
            ['2. NSS: Solo números y guiones (ej: 001-234-5678)'],
            ['3. NOMBRE: Nombre completo del paciente'],
            ['4. FECHA: Formato AAAA-MM-DD (ej: 2025-10-16)'],
            ['5. AUTORIZACIÓN: Solo números, debe ser única para cada paciente'],
            ['6. SERVICIO: Seleccione de la lista desplegable (se alimenta de la hoja "Servicios Disponibles")'],
            ['7. MONTO: Cantidad en pesos (solo números)'],
            [''],
            ['IMPORTANTE:'],
            ['- Los encabezados están protegidos y NO se pueden modificar'],
            ['- La columna SERVICIO tiene lista desplegable - haga clic en la flecha para seleccionar'],
            ['- Cada autorización debe ser única'],
            ['- Complete directamente desde la fila 2'],
            [''],
            ['NOTA: Antes de cargar, debe seleccionar el Médico y ARS en la página web']
        ]
        
        for row in instrucciones:
            ws_instrucciones.append(row)
        
        # Estilo para título de instrucciones
        ws_instrucciones.cell(row=1, column=1).font = Font(bold=True, size=14, color="CEB0B7")
        ws_instrucciones.cell(row=11, column=1).font = Font(bold=True, size=12, color="B89BA3")
        
        ws_instrucciones.column_dimensions['A'].width = 70
        
        # Guardar en memoria
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'plantilla_pacientes_{datetime.now().strftime("%Y%m%d")}.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        import traceback
        error_detallado = traceback.format_exc()
        print(f"❌ ERROR AL GENERAR PLANTILLA EXCEL:\n{error_detallado}")
        flash(f'Error al generar plantilla: {str(e)}', 'error')
        return redirect(url_for('facturacion_facturas_nueva'))

# ========== PROCESAR CARGA DESDE EXCEL ==========
@app.route('/facturacion/procesar-excel', methods=['POST'])
@login_required
def procesar_excel():
    """Procesar archivo Excel cargado y retornar JSON con los datos"""
    try:
        from openpyxl import load_workbook
        
        # Verificar que se subió un archivo
        if 'archivo_excel' not in request.files:
            return jsonify({'error': 'No se subió ningún archivo'}), 400
        
        file = request.files['archivo_excel']
        
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'El archivo debe ser formato Excel (.xlsx o .xls)'}), 400
        
        # Leer el archivo Excel
        wb = load_workbook(file, data_only=True)
        ws = wb['Pacientes']
        
        pacientes = []
        errores = []
        autorizaciones_usadas = set()
        
        # Leer filas (saltar encabezado)
        for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            # Saltar filas vacías
            if not any(row):
                continue
            
            nss_raw, nombre_raw, fecha_raw, autorizacion_raw, servicio_raw, monto_raw = row[0], row[1], row[2], row[3], row[4], row[5]
            
            # ========== VALIDACIÓN 1: Campos Obligatorios ==========
            if not nss_raw or not nombre_raw:
                errores.append(f'❌ Fila {row_num}: NSS y NOMBRE son obligatorios')
                continue
            
            # ========== VALIDACIÓN 2: NSS (Solo números y guiones) ==========
            import re
            nss = str(nss_raw).strip()
            if not re.match(r'^[0-9\-]+$', nss):
                errores.append(f'❌ Fila {row_num}: NSS "{nss}" solo debe contener números y guiones')
                continue
            
            # ========== VALIDACIÓN 3: NOMBRE (Sin números) ==========
            nombre = str(nombre_raw).strip().upper()
            if not nombre:
                errores.append(f'❌ Fila {row_num}: NOMBRE no puede estar vacío')
                continue
            
            # ========== VALIDACIÓN 4: FECHA (Formato válido) ==========
            fecha = ''
            if fecha_raw:
                try:
                    if hasattr(fecha_raw, 'strftime'):
                        fecha = fecha_raw.strftime('%Y-%m-%d')
                    else:
                        fecha_str = str(fecha_raw).strip()
                        # Intentar parsear varios formatos
                        from datetime import datetime
                        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                            try:
                                fecha_obj = datetime.strptime(fecha_str, fmt)
                                fecha = fecha_obj.strftime('%Y-%m-%d')
                                break
                            except:
                                continue
                        if not fecha:
                            errores.append(f'⚠️ Fila {row_num}: FECHA "{fecha_str}" formato inválido (use AAAA-MM-DD)')
                            fecha = datetime.now().strftime('%Y-%m-%d')  # Usar fecha actual como fallback
                except:
                    errores.append(f'⚠️ Fila {row_num}: Error al procesar FECHA, usando fecha actual')
                    from datetime import datetime
                    fecha = datetime.now().strftime('%Y-%m-%d')
            else:
                from datetime import datetime
                fecha = datetime.now().strftime('%Y-%m-%d')
            
            # ========== VALIDACIÓN 5: AUTORIZACIÓN (Solo números y única) ==========
            autorizacion = ''
            if autorizacion_raw:
                try:
                    # Convertir a número y luego a string (elimina decimales)
                    autorizacion = str(int(float(autorizacion_raw)))
                    
                    # Validar que solo contenga números
                    if not autorizacion.isdigit():
                        errores.append(f'❌ Fila {row_num}: AUTORIZACIÓN "{autorizacion}" solo debe contener números')
                        continue
                    
                    # Validar que sea única
                    if autorizacion in autorizaciones_usadas:
                        errores.append(f'❌ Fila {row_num}: AUTORIZACIÓN "{autorizacion}" está duplicada en el Excel')
                        continue
                    
                    autorizaciones_usadas.add(autorizacion)
                except:
                    errores.append(f'❌ Fila {row_num}: AUTORIZACIÓN "{autorizacion_raw}" no es un número válido')
                    continue
            
            # ========== VALIDACIÓN 6: SERVICIO (Sin números) ==========
            servicio = str(servicio_raw).strip().upper() if servicio_raw else 'CONSULTA'
            
            # Verificar que no contenga números
            if any(char.isdigit() for char in servicio):
                errores.append(f'❌ Fila {row_num}: SERVICIO "{servicio}" no debe contener números')
                continue
            
            if not servicio:
                servicio = 'CONSULTA'
            
            # ========== VALIDACIÓN 7: MONTO (Debe ser numérico positivo) ==========
            monto = 0
            if monto_raw:
                try:
                    monto = float(monto_raw)
                    if monto < 0:
                        errores.append(f'⚠️ Fila {row_num}: MONTO no puede ser negativo, usando 0')
                        monto = 0
                except:
                    errores.append(f'❌ Fila {row_num}: MONTO "{monto_raw}" no es un número válido')
                    continue
            
            # Si llegó hasta aquí, la fila es válida
            pacientes.append({
                'nss': nss,
                'nombre': nombre,
                'fecha': fecha,
                'autorizacion': autorizacion,
                'servicio': servicio,
                'monto': monto,
                'fila': row_num
            })
        
        # Validación final: SI HAY ERRORES, NO CARGAR NADA
        if errores:
            return jsonify({
                'error': 'Debe corregir TODOS los errores antes de cargar el Excel',
                'errores': errores,
                'total_errores': len(errores)
            }), 400
        
        if not pacientes:
            return jsonify({'error': 'El archivo no contiene datos válidos'}), 400
        
        return jsonify({
            'success': True,
            'pacientes': pacientes,
            'total': len(pacientes)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error al procesar Excel: {str(e)}'}), 500

# ========== GENERAR FACTURAS ==========
# PÁGINA DESACTIVADA - Se usa /facturacion/historico en su lugar
# @app.route('/facturacion/facturas')
# @login_required
# def facturacion_facturas():
#     """Lista de Facturas Generadas"""
#     conn = get_db_connection()
#     facturas = conn.execute('''
#         SELECT f.*, m.nombre as medico_nombre, a.nombre_ars,
#                (SELECT COUNT(*) FROM facturas_detalle WHERE factura_id = f.id) as num_pacientes
#         FROM facturas f
#         JOIN medicos m ON f.medico_id = m.id
#         JOIN ars a ON f.ars_id = a.id
#         WHERE f.activo = 1
#         ORDER BY f.created_at DESC
#     ''').fetchall()
#     conn.close()
#     return render_template('facturacion/facturas.html', facturas=facturas)

@app.route('/facturacion/generar-factura', methods=['GET', 'POST'])
@login_required
def facturacion_generar():
    """Generar factura desde pacientes pendientes - PASO A PASO"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        # Verificar si es el paso de configuración o el paso final
        step = request.form.get('step', '1')
        
        if step == '1':
            # PASO 1: Configurar parámetros iniciales
            ars_id = request.form.get('ars_id', type=int)
            ncf_id = request.form.get('ncf_id', type=int)
            medico_factura_id = request.form.get('medico_factura_id', type=int)
            fecha_factura = request.form.get('fecha_factura')
            
            if not ars_id or not ncf_id or not medico_factura_id or not fecha_factura:
                flash('Todos los campos son obligatorios', 'error')
                return redirect(url_for('facturacion_generar'))
            
            # Verificar que el médico esté habilitado para facturar
            medico_habilitado = conn.execute('SELECT * FROM medicos WHERE id = ? AND activo = 1 AND factura = 1', 
                                             (medico_factura_id,)).fetchone()
            if not medico_habilitado:
                flash('El médico seleccionado no está habilitado para facturar', 'error')
                return redirect(url_for('facturacion_generar'))
            
            # Obtener TODOS los pacientes pendientes de esta ARS (sin filtrar por quién los agregó)
            pendientes = conn.execute('''
                SELECT fd.*, m.nombre as medico_nombre, a.nombre_ars, p.nombre as paciente_nombre_completo
                FROM facturas_detalle fd
                JOIN medicos m ON fd.medico_id = m.id
                JOIN ars a ON fd.ars_id = a.id
                JOIN pacientes p ON fd.paciente_id = p.id
                WHERE fd.estado = 'pendiente' AND fd.activo = 1 AND fd.ars_id = ?
                ORDER BY fd.fecha_servicio DESC
            ''', (ars_id,)).fetchall()
            
            # Obtener info de ARS, NCF y Médico para facturar
            ars = conn.execute('SELECT * FROM ars WHERE id = ?', (ars_id,)).fetchone()
            ncf = conn.execute('SELECT * FROM ncf WHERE id = ?', (ncf_id,)).fetchone()
            
            # Obtener lista de médicos únicos en los pendientes (para filtro visual)
            medicos = conn.execute('''
                SELECT DISTINCT m.id, m.nombre 
                FROM facturas_detalle fd
                JOIN medicos m ON fd.medico_id = m.id
                WHERE fd.estado = 'pendiente' AND fd.ars_id = ? AND fd.activo = 1
                ORDER BY m.nombre
            ''', (ars_id,)).fetchall()
            
            conn.close()
            
            return render_template('facturacion/generar_factura_step2.html',
                                 pendientes=pendientes,
                                 ars=ars,
                                 ncf=ncf,
                                 fecha_factura=fecha_factura,
                                 medicos=medicos,
                                 medico_factura_id=medico_factura_id,
                                 medico_factura_nombre=medico_habilitado['nombre'])
        
        # PASO 2: Mostrar vista previa de la factura
        if step == '2':
            import json
            pacientes_ids = request.form.get('pacientes_ids')
            ids_list = json.loads(pacientes_ids) if pacientes_ids else []
            
            # Obtener parámetros del formulario
            ars_id = request.form.get('ars_id', type=int)
            ncf_id = request.form.get('ncf_id', type=int)
            medico_factura_id = request.form.get('medico_factura_id', type=int)
            fecha_factura = request.form.get('fecha_factura')
            
            if not ids_list:
                flash('Debe seleccionar al menos un paciente', 'error')
                return redirect(url_for('facturacion_generar'))
            
            if not ars_id or not ncf_id or not medico_factura_id or not fecha_factura:
                flash('Faltan parámetros de configuración', 'error')
                return redirect(url_for('facturacion_generar'))
            
            # Obtener datos de los pacientes seleccionados (SIN datos del médico)
            placeholders = ','.join(['?' for _ in ids_list])
            pacientes = conn.execute(f'''
                SELECT fd.*
                FROM facturas_detalle fd
                WHERE fd.id IN ({placeholders}) AND fd.estado = 'pendiente' AND fd.ars_id = ?
            ''', ids_list + [ars_id]).fetchall()
            
            if not pacientes:
                flash('No se encontraron pacientes pendientes válidos', 'error')
                return redirect(url_for('facturacion_generar'))
            
            # Obtener info del MÉDICO QUE FACTURA
            medico = conn.execute('''
                SELECT * FROM medicos WHERE id = ? AND activo = 1 AND factura = 1
            ''', (medico_factura_id,)).fetchone()
            
            if not medico:
                flash('El médico seleccionado no está habilitado para facturar', 'error')
                return redirect(url_for('facturacion_generar'))
            
            # Obtener info de ARS y NCF
            ars = conn.execute('SELECT * FROM ars WHERE id = ?', (ars_id,)).fetchone()
            ncf = conn.execute('SELECT * FROM ncf WHERE id = ?', (ncf_id,)).fetchone()
            
            # Calcular el próximo NCF
            proximo_numero = ncf['ultimo_numero'] + 1
            ncf_completo = f"{ncf['prefijo']}{str(proximo_numero).zfill(ncf['tamaño'])}"
            
            # Calcular total
            total = sum(p['monto'] for p in pacientes)
            
            # ITBIS = 0 (sin impuesto)
            itbis = 0
            total_final = total
            
            conn.close()
            
            # Mostrar vista previa con los datos del médico que factura
            return render_template('facturacion/vista_previa_factura.html',
                                 pacientes=pacientes,
                                 medico=medico,
                                 ars=ars,
                                 ncf=ncf,
                                 ncf_completo=ncf_completo,
                                 fecha_factura=fecha_factura,
                                 subtotal=total,
                                 itbis=itbis,
                                 total=total_final,
                                 pacientes_ids=json.dumps(ids_list),
                                 ars_id=ars_id,
                                 ncf_id=ncf_id,
                                 medico_factura_id=medico_factura_id)
    
    # GET: PASO 1 - Mostrar formulario para seleccionar ARS, NCF, Médico y fecha
    from datetime import date
    
    # Obtener todas las ARS activas
    ars_list = conn.execute('''
        SELECT * FROM ars WHERE activo = 1 ORDER BY nombre_ars
    ''').fetchall()
    
    # Obtener todos los NCF activos
    ncf_list = conn.execute('''
        SELECT * FROM ncf WHERE activo = 1 ORDER BY tipo, prefijo
    ''').fetchall()
    
    # Obtener médicos habilitados para facturar
    medicos_habilitados = conn.execute('''
        SELECT * FROM medicos WHERE activo = 1 AND factura = 1 ORDER BY nombre
    ''').fetchall()
    
    conn.close()
    
    # Fecha actual por defecto
    fecha_actual = date.today().strftime('%Y-%m-%d')
    
    return render_template('facturacion/generar_factura.html', 
                         ars_list=ars_list, 
                         ncf_list=ncf_list,
                         medicos_habilitados=medicos_habilitados,
                         fecha_actual=fecha_actual)

@app.route('/facturacion/generar-factura-final', methods=['POST'])
@login_required
def facturacion_generar_final():
    """PASO 3: Generar factura definitiva, guardar, descargar y enviar"""
    print("🚀 INICIANDO GENERACIÓN DE FACTURA FINAL")
    conn = get_db_connection()
    
    try:
        import json
        from io import BytesIO
        
        pacientes_ids = request.form.get('pacientes_ids')
        print(f"📋 pacientes_ids recibido: {pacientes_ids}")
        ids_list = json.loads(pacientes_ids) if pacientes_ids else []
        print(f"📋 ids_list parseado: {ids_list}")
        
        # Obtener parámetros del formulario
        ars_id = request.form.get('ars_id', type=int)
        ncf_id = request.form.get('ncf_id', type=int)
        medico_factura_id = request.form.get('medico_factura_id', type=int)
        fecha_factura = request.form.get('fecha_factura')
        
        if not ids_list or not ars_id or not ncf_id or not medico_factura_id or not fecha_factura:
            error_msg = f'Faltan parámetros: ids_list={bool(ids_list)}, ars_id={ars_id}, ncf_id={ncf_id}, medico={medico_factura_id}, fecha={fecha_factura}'
            flash(error_msg, 'error')
            print(f"❌ ERROR: {error_msg}")  # Para debug
            return redirect(url_for('facturacion_generar'))
        
        # Obtener datos del MÉDICO QUE FACTURA
        medico = conn.execute('''
            SELECT * FROM medicos WHERE id = ? AND activo = 1 AND factura = 1
        ''', (medico_factura_id,)).fetchone()
        
        if not medico:
            flash('El médico seleccionado no está habilitado para facturar', 'error')
            return redirect(url_for('facturacion_generar'))
        
        medico_id = medico['id']
        medico_email = medico['email']
        
        # Obtener datos de los pacientes seleccionados
        placeholders = ','.join(['?' for _ in ids_list])
        pacientes = conn.execute(f'''
            SELECT fd.*
            FROM facturas_detalle fd
            WHERE fd.id IN ({placeholders}) AND fd.estado = 'pendiente' AND fd.ars_id = ?
        ''', ids_list + [ars_id]).fetchall()
        
        if not pacientes:
            flash('No se encontraron pacientes pendientes válidos', 'error')
            return redirect(url_for('facturacion_generar'))
        
        # Calcular total
        total = sum(p['monto'] for p in pacientes)
        
        # Obtener y actualizar NCF
        ncf = conn.execute('SELECT * FROM ncf WHERE id = ?', (ncf_id,)).fetchone()
        proximo_numero = ncf['ultimo_numero'] + 1
        ncf_completo = f"{ncf['prefijo']}{str(proximo_numero).zfill(ncf['tamaño'])}"
        
        # Crear factura
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO facturas (fecha_factura, medico_id, ars_id, ncf_id, ncf_numero, total)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (fecha_factura, medico_id, ars_id, ncf_id, ncf_completo, total))
        
        factura_id = cursor.lastrowid
        
        # Actualizar el último número del NCF
        cursor.execute('''
            UPDATE ncf SET ultimo_numero = ? WHERE id = ?
        ''', (proximo_numero, ncf_id))
        
        # Actualizar pacientes a facturados
        cursor.execute(f'''
            UPDATE facturas_detalle 
            SET factura_id = ?, estado = 'facturado'
            WHERE id IN ({placeholders})
        ''', [factura_id] + ids_list)
        
        conn.commit()
        
        # Generar PDF si ReportLab está disponible
        if REPORTLAB_AVAILABLE:
            # Obtener datos completos para el PDF (usando el médico que factura)
            pacientes_pdf = conn.execute(f'''
                SELECT fd.*, 
                       m.nombre as medico_nombre, 
                       m.especialidad as medico_especialidad,
                       m.cedula as medico_cedula,
                       m.exequatur as medico_exequatur,
                       a.nombre_ars, a.rnc as ars_rnc,
                       ca.codigo_ars as codigo_ars
                FROM facturas_detalle fd
                JOIN medicos m ON m.id = ?
                JOIN ars a ON fd.ars_id = a.id
                LEFT JOIN codigo_ars ca ON ca.medico_id = m.id AND ca.ars_id = a.id
                WHERE fd.id IN ({placeholders})
            ''', [medico_id] + ids_list).fetchall()
            
            # Obtener datos del NCF
            ncf_data = conn.execute('SELECT fecha_fin, tipo FROM ncf WHERE id = ?', (ncf_id,)).fetchone()
            
            # Generar PDF
            pdf_buffer = generar_pdf_factura(factura_id, ncf_completo, fecha_factura, pacientes_pdf, total, ncf_data)
            
            # Enviar por email si hay email del médico
            if medico_email:
                enviar_email_factura(medico_email, factura_id, ncf_completo, pdf_buffer, total)
            
            conn.close()
            
            # Descargar PDF
            pdf_buffer.seek(0)
            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name=f'Factura_{ncf_completo}_{factura_id}.pdf',
                mimetype='application/pdf'
            )
        else:
            conn.close()
            flash(f'✅ Factura #{factura_id} generada exitosamente con NCF {ncf_completo} | {len(ids_list)} paciente(s) facturado(s)', 'success')
            return redirect(url_for('facturacion_historico'))
        
    except Exception as e:
        import traceback
        error_detallado = traceback.format_exc()
        print(f"❌ ERROR AL GENERAR FACTURA:\n{error_detallado}")
        if conn:
            conn.rollback()
            conn.close()
        flash(f'Error al generar factura: {str(e)}', 'error')
        return redirect(url_for('facturacion_generar'))

def generar_pdf_factura(factura_id, ncf, fecha, pacientes, total, ncf_data=None):
    """Generar PDF de la factura con formato actualizado"""
    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=25, bottomMargin=70)
    elements = []
    styles = getSampleStyleSheet()
    
    # Preparar datos del footer para el callback
    footer_data = {}
    if pacientes and len(pacientes) > 0:
        footer_data['medico_nombre'] = pacientes[0]['medico_nombre'] if 'medico_nombre' in pacientes[0].keys() else 'N/A'
        footer_data['medico_especialidad'] = pacientes[0]['medico_especialidad'] if 'medico_especialidad' in pacientes[0].keys() and pacientes[0]['medico_especialidad'] else ''
        footer_data['medico_cedula'] = pacientes[0]['medico_cedula'] if 'medico_cedula' in pacientes[0].keys() and pacientes[0]['medico_cedula'] else ''
        footer_data['medico_exequatur'] = pacientes[0]['medico_exequatur'] if 'medico_exequatur' in pacientes[0].keys() and pacientes[0]['medico_exequatur'] else ''
    
    # Función para dibujar el footer en cada página
    def agregar_footer(canvas, doc):
        canvas.saveState()
        
        # Línea de firma a la izquierda (arriba del footer)
        firma_y = 110  # Posición desde el fondo para la firma
        firma_x_start = 60  # Margen izquierdo
        firma_ancho = 200  # Ancho de la línea de firma
        
        # Dibujar línea para firma
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(0.5)
        canvas.line(firma_x_start, firma_y, firma_x_start + firma_ancho, firma_y)
        
        # Nombre de la doctora debajo de la línea
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.black)
        canvas.drawString(firma_x_start, firma_y - 15, "Dra. Shirley Ramírez")
        
        # Footer centrado siempre al final de la página
        footer_y = 50  # 50 puntos desde el fondo
        
        if footer_data:
            # Línea 1: Nombre del médico (negrita)
            canvas.setFont('Helvetica-Bold', 8)
            canvas.setFillColor(colors.grey)
            canvas.drawCentredString(letter[0]/2, footer_y + 20, footer_data.get('medico_nombre', ''))
            
            # Línea 2: Especialidad, Cédula y Exequátur
            canvas.setFont('Helvetica', 8)
            linea2 = footer_data.get('medico_especialidad', '')
            if footer_data.get('medico_cedula'):
                linea2 += f" | Cédula: {footer_data['medico_cedula']}"
            if footer_data.get('medico_exequatur'):
                linea2 += f" | EXEQUATUR: {footer_data['medico_exequatur']}"
            canvas.drawCentredString(letter[0]/2, footer_y + 10, linea2)
            
            # Línea 3: Centro
            canvas.drawCentredString(letter[0]/2, footer_y, "Centro Oriental de Ginecología y Obstetricia")
        
        canvas.restoreState()
    
    # Función helper para formatear moneda
    def formato_moneda(valor):
        return "{:,.2f}".format(float(valor))
    
    # Header compacto: Logo a la izquierda, FACTURA en el centro
    logo_path = os.path.join('static', 'logos', 'logo-dra-shirley.png')
    if os.path.exists(logo_path):
        header_data = [[
            Image(logo_path, width=1*inch, height=1*inch),
            Paragraph("<para align='center'><b><font size='20' color='black'>FACTURA</font></b><br/><font size='8' color='black'>CRÉDITO FISCAL</font></para>", styles['Normal']),
            ''
        ]]
        header_table = Table(header_data, colWidths=[1.2*inch, 5.6*inch, 0.5*inch])
        header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.15*inch))
    else:
        # Si no hay logo, solo título centrado
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18,
                                     textColor=colors.HexColor('#CEB0B7'), alignment=TA_CENTER, spaceAfter=8)
        elements.append(Paragraph("FACTURA", title_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Información en 3 columnas (como el HTML)
    if pacientes and len(pacientes) > 0:
        # Extraer datos dinámicos
        ars_nombre = pacientes[0]['nombre_ars'] if 'nombre_ars' in pacientes[0].keys() else 'N/A'
        ars_rnc = pacientes[0]['ars_rnc'] if 'ars_rnc' in pacientes[0].keys() and pacientes[0]['ars_rnc'] else ''
        medico_nombre = pacientes[0]['medico_nombre'] if 'medico_nombre' in pacientes[0].keys() else 'N/A'
        medico_especialidad = pacientes[0]['medico_especialidad'] if 'medico_especialidad' in pacientes[0].keys() else 'N/A'
        codigo_ars = pacientes[0]['codigo_ars'] if 'codigo_ars' in pacientes[0].keys() and pacientes[0]['codigo_ars'] else 'N/A'
        medico_exequatur = pacientes[0]['medico_exequatur'] if 'medico_exequatur' in pacientes[0].keys() and pacientes[0]['medico_exequatur'] else ''
        ncf_tipo = ncf_data['tipo'] if ncf_data and 'tipo' in ncf_data.keys() else 'CRÉDITO FISCAL'
        ncf_fecha_fin = ncf_data['fecha_fin'] if ncf_data and 'fecha_fin' in ncf_data.keys() and ncf_data['fecha_fin'] else ''
        
        # Construir las 3 columnas (sin etiquetas de título, letras más grandes)
        col1_text = f"<font size='10'>Fecha: {fecha}<br/>Cliente: {ars_nombre}"
        if ars_rnc:
            col1_text += f"<br/>RNC: {ars_rnc}"
        col1_text += "</font>"
        
        col2_text = f"<b>NCF</b><br/><font size='11' color='#CEB0B7'><b>{ncf}</b></font><br/><font size='10'>Tipo: {ncf_tipo}"
        if ncf_fecha_fin:
            col2_text += f"<br/>Válido hasta: {ncf_fecha_fin}"
        col2_text += "</font>"
        
        col3_text = f"<font size='10'><b>{medico_nombre}</b><br/>{medico_especialidad}<br/>Código: {codigo_ars}"
        if medico_exequatur:
            col3_text += f"<br/>Exequátur: {medico_exequatur}"
        col3_text += "</font>"
        
        info_data = [[
            Paragraph(col1_text, styles['Normal']),
            Paragraph(col2_text, styles['Normal']),
            Paragraph(col3_text, styles['Normal'])
        ]]
        
        info_table = Table(info_data, colWidths=[2.4*inch, 2.3*inch, 2.6*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CEB0B7')),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Tabla de pacientes
    data = [['No.', 'NOMBRES PACIENTE', 'NSS/CONTRATO', 'FECHA', 'AUTORIZACIÓN', 'SERVICIO', 'V/UNITARIO']]
    
    for idx, p in enumerate(pacientes, 1):
        data.append([
            str(idx),
            p['nombre_paciente'],
            p['nss'],
            p['fecha_servicio'],
            p['autorizacion'],
            p['descripcion_servicio'],
            formato_moneda(p['monto'])
        ])
    
    # Agregar totales (ITBIS simbólico)
    subtotal = total
    total_final = subtotal
    
    data.append(['', '', '', '', '', 'SUB-TOTAL:', formato_moneda(subtotal)])
    data.append(['', '', '', '', '', 'ITBIS:', '*E'])
    data.append(['', '', '', '', '', 'TOTAL:', formato_moneda(total_final)])
    
    table = Table(data, colWidths=[0.5*inch, 2*inch, 1.3*inch, 0.8*inch, 1*inch, 1.5*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CEB0B7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -4), colors.white),
        ('GRID', (0, 0), (-1, -4), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        # Alineaciones específicas por columna
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # No. centrado
        ('ALIGN', (1, 1), (1, -4), 'LEFT'),    # NOMBRES PACIENTE a la izquierda
        ('ALIGN', (2, 1), (2, -4), 'LEFT'),    # NSS/CONTRATO a la izquierda
        ('ALIGN', (3, 1), (3, -4), 'CENTER'),  # FECHA centrado
        ('ALIGN', (4, 1), (4, -4), 'CENTER'),  # AUTORIZACIÓN centrado
        ('ALIGN', (5, 1), (5, -4), 'LEFT'),    # SERVICIO a la izquierda
        ('ALIGN', (6, 1), (6, -1), 'RIGHT'),   # V/UNITARIO a la derecha
        ('BACKGROUND', (0, -3), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 10),
    ]))
    
    elements.append(table)
    
    # El footer ahora se dibuja automáticamente al final de cada página mediante el callback
    doc.build(elements, onFirstPage=agregar_footer, onLaterPages=agregar_footer)
    buffer.seek(0)
    return buffer

def enviar_email_factura(destinatario, factura_id, ncf, pdf_buffer, monto_total=0.00):
    """Enviar factura por email con template estandarizado"""
    try:
        # Verificar si hay contraseña configurada
        if not EMAIL_PASSWORD:
            print("\n⚠️  Email no configurado. La factura no se envió por correo.")
            return False
        
        # Crear mensaje usando template estándar
        msg = MIMEMultipart()
        msg['Subject'] = f'💰 Factura #{factura_id} - NCF: {ncf}'
        msg['From'] = EMAIL_USERNAME
        msg['To'] = destinatario
        
        # Usar template estandarizado
        html = template_factura(factura_id, ncf, monto_total)
        
        # Adjuntar HTML
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Adjuntar PDF
        pdf_buffer.seek(0)
        pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype='pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment', 
                                 filename=f'Factura_{ncf}_{factura_id}.pdf')
        msg.attach(pdf_attachment)
        
        # Enviar email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("\n" + "=" * 60)
        print("✅ EMAIL CON FACTURA ENVIADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📧 Destinatario: {destinatario}")
        print(f"📄 Factura: #{factura_id}")
        print(f"🔢 NCF: {ncf}")
        print(f"💰 Monto: ${monto_total:,.2f}")
        print("=" * 60 + "\n")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR AL ENVIAR EMAIL CON FACTURA")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nLa factura se generó correctamente y se descargó el PDF.")
        print("=" * 60 + "\n")
        return False

@app.route('/facturacion/historico')
@login_required
def facturacion_historico():
    """Histórico de facturas generadas con filtros"""
    conn = get_db_connection()
    
    # Obtener filtros
    ars_id = request.args.get('ars_id', type=int)
    medico_id = request.args.get('medico_id', type=int)
    ncf = request.args.get('ncf', '').strip()
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    # Construir query con filtros
    query = '''
        SELECT f.*, a.nombre_ars, m.nombre as medico_nombre,
               (SELECT COUNT(*) FROM facturas_detalle WHERE factura_id = f.id) as num_pacientes
        FROM facturas f
        JOIN ars a ON f.ars_id = a.id
        JOIN medicos m ON f.medico_id = m.id
        WHERE f.activo = 1
    '''
    
    params = []
    
    if ars_id:
        query += ' AND f.ars_id = ?'
        params.append(ars_id)
    
    if medico_id:
        query += ' AND f.medico_id = ?'
        params.append(medico_id)
    
    if ncf:
        query += ' AND (f.ncf LIKE ? OR f.ncf_numero LIKE ?)'
        params.append(f'%{ncf}%')
        params.append(f'%{ncf}%')
    
    if fecha_desde:
        query += ' AND f.fecha_factura >= ?'
        params.append(fecha_desde)
    
    if fecha_hasta:
        query += ' AND f.fecha_factura <= ?'
        params.append(fecha_hasta)
    
    query += ' ORDER BY f.fecha_factura DESC, f.id DESC'
    
    facturas = conn.execute(query, params).fetchall()
    
    # Obtener lista de ARS para el filtro
    ars_list = conn.execute('SELECT * FROM ars WHERE activo = 1 ORDER BY nombre_ars').fetchall()
    
    # Obtener lista de Médicos habilitados para facturar
    medicos_list = conn.execute('SELECT * FROM medicos WHERE activo = 1 AND factura = 1 ORDER BY nombre').fetchall()
    
    conn.close()
    
    return render_template('facturacion/historico.html',
                         facturas=facturas,
                         ars_list=ars_list,
                         medicos_list=medicos_list,
                         ars_id_seleccionado=ars_id,
                         medico_id_seleccionado=medico_id,
                         ncf=ncf,
                         fecha_desde=fecha_desde,
                         fecha_hasta=fecha_hasta)

@app.route('/facturacion/ver-factura/<int:factura_id>')
@login_required
def facturacion_ver_factura(factura_id):
    """Ver factura completa generada"""
    conn = get_db_connection()
    
    # Obtener datos de la factura (incluyendo email del médico)
    factura = conn.execute('''
        SELECT f.*, a.nombre_ars, a.rnc as ars_rnc, 
               m.nombre as medico_nombre, m.especialidad as medico_especialidad, 
               m.cedula as medico_cedula, m.exequatur as medico_exequatur,
               m.email as medico_email,
               n.tipo as ncf_tipo, n.prefijo as ncf_prefijo, n.fecha_fin as ncf_fecha_fin
        FROM facturas f
        JOIN ars a ON f.ars_id = a.id
        JOIN medicos m ON f.medico_id = m.id
        LEFT JOIN ncf n ON f.ncf_id = n.id
        WHERE f.id = ? AND f.activo = 1
    ''', (factura_id,)).fetchone()
    
    if not factura:
        flash('Factura no encontrada', 'error')
        conn.close()
        return redirect(url_for('facturacion_historico'))
    
    # Obtener pacientes de la factura
    pacientes = conn.execute('''
        SELECT fd.*, m.nombre as medico_nombre
        FROM facturas_detalle fd
        JOIN medicos m ON fd.medico_id = m.id
        WHERE fd.factura_id = ? AND fd.activo = 1
        ORDER BY fd.id
    ''', (factura_id,)).fetchall()
    
    conn.close()
    
    # Calcular totales (sin ITBIS)
    subtotal = factura['total']
    itbis = 0
    total_final = subtotal
    
    return render_template('facturacion/ver_factura.html',
                         factura=factura,
                         pacientes=pacientes,
                         subtotal=subtotal,
                         itbis=itbis,
                         total=total_final)

@app.route('/facturacion/enviar-email/<int:factura_id>', methods=['POST'])
@login_required
def facturacion_enviar_email(factura_id):
    """Enviar factura por email con PDF adjunto"""
    conn = get_db_connection()
    
    try:
        # Obtener destinatario del formulario
        destinatario = request.form.get('destinatario', '').strip()
        
        if not destinatario:
            flash('Debes proporcionar un email de destinatario', 'error')
            return redirect(url_for('facturacion_ver_factura', factura_id=factura_id))
        
        # Obtener datos de la factura
        factura = conn.execute('''
            SELECT f.*, a.nombre_ars, a.rnc as ars_rnc, 
                   m.nombre as medico_nombre, m.especialidad as medico_especialidad, 
                   m.cedula as medico_cedula, m.exequatur as medico_exequatur,
                   m.email as medico_email,
                   n.tipo as ncf_tipo, n.prefijo as ncf_prefijo, n.fecha_fin as ncf_fecha_fin
            FROM facturas f
            JOIN ars a ON f.ars_id = a.id
            JOIN medicos m ON f.medico_id = m.id
            LEFT JOIN ncf n ON f.ncf_id = n.id
            WHERE f.id = ? AND f.activo = 1
        ''', (factura_id,)).fetchone()
        
        if not factura:
            flash('Factura no encontrada', 'error')
            conn.close()
            return redirect(url_for('facturacion_historico'))
        
        # Obtener pacientes de la factura
        pacientes = conn.execute('''
            SELECT fd.*, m.nombre as medico_nombre, m.especialidad as medico_especialidad,
                   m.cedula as medico_cedula, m.exequatur as medico_exequatur,
                   a.nombre_ars, ca.codigo_ars
            FROM facturas_detalle fd
            JOIN medicos m ON fd.medico_id = m.id
            JOIN ars a ON fd.ars_id = a.id
            LEFT JOIN codigo_ars ca ON ca.medico_id = m.id AND ca.ars_id = a.id
            WHERE fd.factura_id = ? AND fd.activo = 1
            ORDER BY fd.id
        ''', (factura_id,)).fetchall()
        
        if not pacientes:
            flash('No se encontraron pacientes en esta factura', 'error')
            conn.close()
            return redirect(url_for('facturacion_ver_factura', factura_id=factura_id))
        
        # Generar PDF
        if REPORTLAB_AVAILABLE:
            # Obtener datos del NCF
            ncf_data = conn.execute('SELECT fecha_fin, tipo FROM ncf WHERE id = ?', (factura['ncf_id'],)).fetchone()
            
            # Generar PDF
            ncf_numero = factura['ncf_numero'] if factura['ncf_numero'] else factura.get('ncf', 'N/A')
            pdf_buffer = generar_pdf_factura(factura_id, ncf_numero, factura['fecha_factura'], pacientes, factura['total'], ncf_data)
            
            # Enviar email
            if enviar_email_factura(destinatario, factura_id, ncf_numero, pdf_buffer, factura['total']):
                flash(f'✅ Factura enviada exitosamente a {destinatario}', 'success')
            else:
                flash('⚠️ Hubo un problema al enviar el email. Verifica la configuración de correo.', 'warning')
        else:
            flash('No se puede generar el PDF. ReportLab no está disponible.', 'error')
        
        conn.close()
        return redirect(url_for('facturacion_ver_factura', factura_id=factura_id))
        
    except Exception as e:
        print(f"❌ Error al enviar email de factura: {e}")
        if conn:
            conn.close()
        flash(f'Error al enviar la factura por email: {str(e)}', 'error')
        return redirect(url_for('facturacion_ver_factura', factura_id=factura_id))

@app.route('/facturacion/descargar-pdf/<int:factura_id>')
@login_required
def facturacion_descargar_pdf(factura_id):
    """Descargar PDF de factura generada"""
    conn = get_db_connection()
    
    try:
        # Obtener datos de la factura
        factura = conn.execute('''
            SELECT f.*, a.nombre_ars, a.rnc as ars_rnc, 
                   m.nombre as medico_nombre, m.especialidad as medico_especialidad, 
                   m.cedula as medico_cedula, m.exequatur as medico_exequatur,
                   m.email as medico_email,
                   n.tipo as ncf_tipo, n.prefijo as ncf_prefijo, n.fecha_fin as ncf_fecha_fin
            FROM facturas f
            JOIN ars a ON f.ars_id = a.id
            JOIN medicos m ON f.medico_id = m.id
            LEFT JOIN ncf n ON f.ncf_id = n.id
            WHERE f.id = ? AND f.activo = 1
        ''', (factura_id,)).fetchone()
        
        if not factura:
            flash('Factura no encontrada', 'error')
            conn.close()
            return redirect(url_for('facturacion_historico'))
        
        # Obtener pacientes de la factura
        pacientes = conn.execute('''
            SELECT fd.*, m.nombre as medico_nombre, m.especialidad as medico_especialidad,
                   m.cedula as medico_cedula, m.exequatur as medico_exequatur,
                   a.nombre_ars, ca.codigo_ars
            FROM facturas_detalle fd
            JOIN medicos m ON fd.medico_id = m.id
            JOIN ars a ON fd.ars_id = a.id
            LEFT JOIN codigo_ars ca ON ca.medico_id = m.id AND ca.ars_id = a.id
            WHERE fd.factura_id = ? AND fd.activo = 1
            ORDER BY fd.id
        ''', (factura_id,)).fetchall()
        
        if not pacientes:
            flash('No se encontraron pacientes en esta factura', 'error')
            conn.close()
            return redirect(url_for('facturacion_ver_factura', factura_id=factura_id))
        
        # Generar PDF
        if REPORTLAB_AVAILABLE:
            # Obtener datos del NCF
            ncf_data = conn.execute('SELECT fecha_fin, tipo FROM ncf WHERE id = ?', (factura['ncf_id'],)).fetchone()
            
            # Generar PDF
            ncf_numero = factura['ncf_numero'] if factura['ncf_numero'] else factura.get('ncf', 'N/A')
            pdf_buffer = generar_pdf_factura(factura_id, ncf_numero, factura['fecha_factura'], pacientes, factura['total'], ncf_data)
            
            conn.close()
            
            # Nombre del archivo
            nombre_archivo = f"Factura_{factura_id}_NCF_{ncf_numero.replace(' ', '_')}.pdf"
            
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=nombre_archivo
            )
        else:
            flash('No se puede generar el PDF. ReportLab no está disponible.', 'error')
            conn.close()
            return redirect(url_for('facturacion_ver_factura', factura_id=factura_id))
        
    except Exception as e:
        print(f"❌ Error al descargar PDF de factura: {e}")
        if conn:
            conn.close()
        flash(f'Error al descargar el PDF: {str(e)}', 'error')
        return redirect(url_for('facturacion_ver_factura', factura_id=factura_id))

@app.route('/facturacion/paciente/<int:paciente_id>/editar', methods=['GET', 'POST'])
@login_required
def facturacion_paciente_editar(paciente_id):
    """Editar un paciente pendiente de facturación"""
    conn = get_db_connection()
    
    # Verificar que el paciente existe y está pendiente
    paciente = conn.execute('''
        SELECT * FROM facturas_detalle WHERE id = ? AND activo = 1
    ''', (paciente_id,)).fetchone()
    
    if not paciente:
        flash('Paciente no encontrado', 'error')
        return redirect(url_for('facturacion_pacientes_pendientes'))
    
    if paciente['estado'] != 'pendiente':
        flash('No se puede editar un registro facturado', 'error')
        return redirect(url_for('facturacion_pacientes_pendientes'))
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nss = request.form.get('nss', '').strip().upper()
            nombre = request.form.get('nombre', '').strip().upper()
            fecha = request.form.get('fecha', '').strip()
            autorizacion = request.form.get('autorizacion', '').strip()
            servicio = request.form.get('servicio', '').strip().upper()
            monto = request.form.get('monto', type=float, default=0)
            
            # Validaciones
            if not nss or not nombre:
                flash('NSS y Nombre son obligatorios', 'error')
                conn.close()
                return redirect(url_for('facturacion_paciente_editar', paciente_id=paciente_id))
            
            # Verificar autorización única (excepto el mismo registro)
            existe_autorizacion = conn.execute('''
                SELECT id FROM facturas_detalle 
                WHERE autorizacion = ? AND id != ? AND activo = 1
            ''', (autorizacion, paciente_id)).fetchone()
            
            if existe_autorizacion:
                flash('Esta autorización ya existe en otro registro', 'error')
                conn.close()
                return redirect(url_for('facturacion_paciente_editar', paciente_id=paciente_id))
            
            # Actualizar registro
            conn.execute('''
                UPDATE facturas_detalle
                SET nss = ?, nombre_paciente = ?, fecha_servicio = ?,
                    autorizacion = ?, descripcion_servicio = ?, monto = ?
                WHERE id = ?
            ''', (nss, nombre, fecha, autorizacion, servicio, monto, paciente_id))
            
            conn.commit()
            conn.close()
            
            flash('✅ Registro actualizado exitosamente', 'success')
            return redirect(url_for('facturacion_pacientes_pendientes'))
            
        except Exception as e:
            conn.close()
            flash(f'Error al actualizar: {str(e)}', 'error')
            return redirect(url_for('facturacion_paciente_editar', paciente_id=paciente_id))
    
    # GET: Mostrar formulario de edición
    # Obtener listas para los selects
    medicos = conn.execute('SELECT * FROM medicos WHERE activo = 1 ORDER BY nombre').fetchall()
    ars_list = conn.execute('SELECT * FROM ars WHERE activo = 1 ORDER BY nombre_ars').fetchall()
    conn.close()
    
    return render_template('facturacion/paciente_editar.html', 
                         paciente=paciente,
                         medicos=medicos,
                         ars_list=ars_list)

@app.route('/facturacion/paciente/<int:paciente_id>/eliminar')
@login_required
def facturacion_paciente_eliminar(paciente_id):
    """Eliminar (soft delete) un paciente pendiente de facturación"""
    conn = get_db_connection()
    
    # Verificar que el paciente existe y está pendiente
    paciente = conn.execute('''
        SELECT * FROM facturas_detalle WHERE id = ? AND activo = 1
    ''', (paciente_id,)).fetchone()
    
    if not paciente:
        flash('Paciente no encontrado', 'error')
        conn.close()
        return redirect(url_for('facturacion_pacientes_pendientes'))
    
    if paciente['estado'] != 'pendiente':
        flash('❌ No se puede eliminar un registro facturado', 'error')
        conn.close()
        return redirect(url_for('facturacion_pacientes_pendientes'))
    
    try:
        # Soft delete
        conn.execute('''
            UPDATE facturas_detalle SET activo = 0 WHERE id = ?
        ''', (paciente_id,))
        
        conn.commit()
        conn.close()
        
        flash('✅ Registro eliminado exitosamente', 'success')
    except Exception as e:
        conn.close()
        flash(f'Error al eliminar: {str(e)}', 'error')
    
    return redirect(url_for('facturacion_pacientes_pendientes'))

# ========== APIs PARA AUTOCOMPLETAR ==========
@app.route('/api/facturacion/buscar-paciente/<nss>')
@app.route('/api/facturacion/buscar-paciente/<nss>/<int:ars_id>')
def api_buscar_paciente(nss, ars_id=None):
    """API para buscar paciente por NSS + ARS (llave única)"""
    conn = get_db_connection()
    
    # Si se proporciona ARS, buscar por NSS + ARS (llave única)
    if ars_id:
        paciente = conn.execute('''
            SELECT p.*, a.nombre_ars 
            FROM pacientes p
            LEFT JOIN ars a ON p.ars_id = a.id
            WHERE p.nss = ? AND p.ars_id = ? AND p.activo = 1
        ''', (nss, ars_id)).fetchone()
    else:
        # Si no se proporciona ARS, buscar solo por NSS (puede haber múltiples)
        paciente = conn.execute('''
            SELECT p.*, a.nombre_ars 
            FROM pacientes p
            LEFT JOIN ars a ON p.ars_id = a.id
            WHERE p.nss = ? AND p.activo = 1
            LIMIT 1
        ''', (nss,)).fetchone()
    
    conn.close()
    
    if paciente:
        return jsonify({
            'encontrado': True,
            'nombre': paciente['nombre'],
            'ars_id': paciente['ars_id'],
            'ars_nombre': paciente['nombre_ars'] if paciente['nombre_ars'] else ''
        })
    else:
        return jsonify({'encontrado': False})

@app.route('/api/facturacion/buscar-servicio')
def api_buscar_servicio():
    """API para buscar servicios (autocompletado)"""
    query = request.args.get('q', '')
    conn = get_db_connection()
    servicios = conn.execute('''
        SELECT id, descripcion, precio_base 
        FROM tipos_servicios 
        WHERE descripcion LIKE ? AND activo = 1 
        ORDER BY descripcion 
        LIMIT 10
    ''', (f'%{query}%',)).fetchall()
    conn.close()
    
    return jsonify([{
        'id': s['id'],
        'descripcion': s['descripcion'],
        'precio_base': s['precio_base']
    } for s in servicios])

# ==================== SEO ROUTES ====================
@app.route('/sitemap.xml')
def sitemap():
    """Genera sitemap.xml dinámico para SEO"""
    from datetime import datetime
    from flask import make_response
    
    pages = []
    # Páginas principales (optimizadas para SEO)
    urls = [
        {'loc': url_for('index', _external=True), 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': url_for('services', _external=True), 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': url_for('tratamientos_esteticos', _external=True), 'priority': '0.95', 'changefreq': 'weekly'},
        {'loc': url_for('about', _external=True), 'priority': '0.85', 'changefreq': 'monthly'},
        {'loc': url_for('testimonials', _external=True), 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': url_for('contact', _external=True), 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': url_for('request_appointment', _external=True), 'priority': '1.0', 'changefreq': 'daily'},
    ]
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>{url["loc"]}</loc>\n'
        sitemap_xml += f'    <lastmod>{today}</lastmod>\n'
        sitemap_xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        sitemap_xml += f'    <priority>{url["priority"]}</priority>\n'
        sitemap_xml += '  </url>\n'
    
    sitemap_xml += '</urlset>'
    
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/robots.txt')
def robots_txt():
    """Archivo robots.txt dinámico para control de crawlers"""
    base_url = request.url_root.rstrip('/')
    
    content = f"""User-agent: *
Allow: /
Allow: /about
Allow: /services
Allow: /appointment
Allow: /contact
Allow: /testimonials
Disallow: /admin
Disallow: /facturacion
Disallow: /login
Disallow: /static/

Sitemap: {base_url}/sitemap.xml

# Configuración de crawl delay (opcional)
Crawl-delay: 1
"""
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain"
    return response

# ============================================================================
# GESTIÓN DE USUARIOS
# ============================================================================

@app.route('/admin/usuarios')
@login_required
def admin_usuarios():
    """Listar usuarios del sistema"""
    # Solo administradores pueden ver la lista de usuarios
    if current_user.perfil != 'Administrador':
        flash('No tienes permisos para acceder a esta sección', 'error')
        return redirect(url_for('admin'))
    
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/admin/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def admin_usuarios_nuevo():
    """Crear nuevo usuario"""
    # Solo administradores pueden crear usuarios
    if current_user.perfil != 'Administrador':
        flash('No tienes permisos para acceder a esta sección', 'error')
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        nombre = sanitize_input(request.form.get('nombre', ''), 100)
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        perfil = request.form.get('perfil', '')
        
        # Validaciones
        if not nombre or not email or not password or not perfil:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('admin_usuarios_nuevo'))
        
        if not validate_email(email):
            flash('Email inválido', 'error')
            return redirect(url_for('admin_usuarios_nuevo'))
        
        # Validación robusta de contraseña
        password_errors = validar_password_segura(password)
        if password_errors:
            flash(f'Contraseña no cumple los requisitos: {", ".join(password_errors)}', 'error')
            return redirect(url_for('admin_usuarios_nuevo'))
        
        if perfil not in ['Administrador', 'Registro de Facturas']:
            flash('Perfil inválido', 'error')
            return redirect(url_for('admin_usuarios_nuevo'))
        
        # Verificar que el email no exista
        conn = get_db_connection()
        existe = conn.execute('SELECT id FROM usuarios WHERE email = ?', (email,)).fetchone()
        
        if existe:
            conn.close()
            flash('Ya existe un usuario con ese email', 'error')
            return redirect(url_for('admin_usuarios_nuevo'))
        
        # Crear usuario con contraseña temporal
        password_hash = generate_password_hash(password)
        conn.execute('''
            INSERT INTO usuarios (nombre, email, password_hash, perfil, activo, password_temporal)
            VALUES (?, ?, ?, ?, 1, 1)
        ''', (nombre, email, password_hash, perfil))
        conn.commit()
        conn.close()
        
        flash(f'Usuario {nombre} creado exitosamente. Contraseña temporal: {password} (el usuario deberá cambiarla en el primer login)', 'success')
        return redirect(url_for('admin_usuarios'))
    
    return render_template('admin_usuarios_form.html', usuario=None)

@app.route('/admin/usuarios/<int:usuario_id>/editar', methods=['GET', 'POST'])
@login_required
def admin_usuarios_editar(usuario_id):
    """Editar usuario existente"""
    # Solo administradores pueden editar usuarios
    if current_user.perfil != 'Administrador':
        flash('No tienes permisos para acceder a esta sección', 'error')
        return redirect(url_for('admin'))
    
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,)).fetchone()
    
    if not usuario:
        conn.close()
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('admin_usuarios'))
    
    if request.method == 'POST':
        nombre = sanitize_input(request.form.get('nombre', ''), 100)
        email = request.form.get('email', '').strip().lower()
        perfil = request.form.get('perfil', '')
        activo = request.form.get('activo') == '1'
        cambiar_password = request.form.get('cambiar_password') == '1'
        password = request.form.get('password', '')
        
        # Validaciones
        if not nombre or not email or not perfil:
            flash('Nombre, email y perfil son obligatorios', 'error')
            return redirect(url_for('admin_usuarios_editar', usuario_id=usuario_id))
        
        if not validate_email(email):
            flash('Email inválido', 'error')
            return redirect(url_for('admin_usuarios_editar', usuario_id=usuario_id))
        
        if perfil not in ['Administrador', 'Registro de Facturas']:
            flash('Perfil inválido', 'error')
            return redirect(url_for('admin_usuarios_editar', usuario_id=usuario_id))
        
        # No permitir que el usuario se desactive a sí mismo
        if usuario_id == current_user.id and not activo:
            flash('No puedes desactivar tu propia cuenta', 'error')
            return redirect(url_for('admin_usuarios_editar', usuario_id=usuario_id))
        
        # Verificar que el email no exista en otro usuario
        existe = conn.execute('SELECT id FROM usuarios WHERE email = ? AND id != ?', 
                             (email, usuario_id)).fetchone()
        
        if existe:
            conn.close()
            flash('Ya existe otro usuario con ese email', 'error')
            return redirect(url_for('admin_usuarios_editar', usuario_id=usuario_id))
        
        # Actualizar usuario
        if cambiar_password and password:
            if len(password) < 8:
                flash('La contraseña debe tener al menos 8 caracteres', 'error')
                return redirect(url_for('admin_usuarios_editar', usuario_id=usuario_id))
            
            password_hash = generate_password_hash(password)
            conn.execute('''
                UPDATE usuarios 
                SET nombre = ?, email = ?, password_hash = ?, perfil = ?, activo = ?
                WHERE id = ?
            ''', (nombre, email, password_hash, perfil, activo, usuario_id))
        else:
            conn.execute('''
                UPDATE usuarios 
                SET nombre = ?, email = ?, perfil = ?, activo = ?
                WHERE id = ?
            ''', (nombre, email, perfil, activo, usuario_id))
        
        conn.commit()
        conn.close()
        
        flash(f'Usuario {nombre} actualizado exitosamente', 'success')
        return redirect(url_for('admin_usuarios'))
    
    conn.close()
    return render_template('admin_usuarios_form.html', usuario=usuario)

@app.route('/admin/usuarios/<int:usuario_id>/eliminar', methods=['POST'])
@login_required
def admin_usuarios_eliminar(usuario_id):
    """Eliminar usuario - DESHABILITADO POR SEGURIDAD"""
    flash('La eliminación de usuarios está deshabilitada por seguridad. Puedes desactivar usuarios en su lugar.', 'warning')
    return redirect(url_for('admin_usuarios'))

if __name__ == '__main__':
    # Inicializar base de datos
    init_db()
    create_sample_data()
    
    # Crear directorio de templates si no existe
    os.makedirs('templates', exist_ok=True)
    
    # Configuración para producción
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_ENV') != 'production'
    
    print("\n" + "="*60)
    print("🚀 SERVIDOR INICIADO")
    print("="*60)
    print(f"🌐 Entorno: {'PRODUCCIÓN' if not debug else 'DESARROLLO'}")
    print(f"🌐 Host: {host}:{port}")
    print(f"📧 Email configurado: {'✅ SÍ' if EMAIL_PASSWORD and EMAIL_PASSWORD != 'tu_password_aqui' else '❌ NO'}")
    print(f"📄 PDF disponible: {'✅ SÍ' if REPORTLAB_AVAILABLE else '❌ NO'}")
    print(f"🔒 Seguridad: {'✅ ACTIVADA' if not debug else '⚠️ DESARROLLO'}")
    print("="*60 + "\n")
    
    app.run(debug=debug, host=host, port=port)
