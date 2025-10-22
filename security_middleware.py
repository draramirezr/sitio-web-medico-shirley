# ==================================================
# MIDDLEWARE DE SEGURIDAD
# Sistema Médico - Dra. Shirley Ramírez
# ==================================================

from functools import wraps
from flask import request, abort, session
from datetime import datetime, timedelta
import hashlib

# ================== RATE LIMITING ==================

# Diccionario para almacenar intentos (en producción usar Redis)
rate_limit_storage = {}

def get_client_ip():
    """Obtener IP real del cliente (considera proxies)"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

def rate_limit(max_requests=5, window_minutes=15, key_prefix='general'):
    """
    Decorator para limitar tasa de requests
    
    Args:
        max_requests: Número máximo de requests permitidos
        window_minutes: Ventana de tiempo en minutos
        key_prefix: Prefijo para diferenciar endpoints
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Obtener identificador único (IP + endpoint)
            client_ip = get_client_ip()
            key = f"{key_prefix}:{client_ip}"
            
            current_time = datetime.now()
            
            # Limpiar entradas antiguas
            if key in rate_limit_storage:
                rate_limit_storage[key] = [
                    timestamp for timestamp in rate_limit_storage[key]
                    if current_time - timestamp < timedelta(minutes=window_minutes)
                ]
            else:
                rate_limit_storage[key] = []
            
            # Verificar límite
            if len(rate_limit_storage[key]) >= max_requests:
                abort(429, description="Demasiadas solicitudes. Por favor, intente más tarde.")
            
            # Registrar request actual
            rate_limit_storage[key].append(current_time)
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

# ================== VALIDACIÓN DE INPUTS ==================

def sanitize_nss(nss):
    """Validar y limpiar NSS (solo números)"""
    if not nss:
        return None
    cleaned = ''.join(filter(str.isdigit, str(nss)))
    if len(cleaned) < 9 or len(cleaned) > 15:
        raise ValueError("NSS debe tener entre 9 y 15 dígitos")
    return cleaned

def sanitize_monto(monto):
    """Validar y limpiar monto (número positivo)"""
    try:
        value = float(monto)
        if value < 0:
            raise ValueError("El monto no puede ser negativo")
        if value > 1000000:  # Límite razonable
            raise ValueError("El monto excede el límite permitido")
        return round(value, 2)
    except (ValueError, TypeError):
        raise ValueError("Monto inválido")

def sanitize_fecha(fecha_str):
    """Validar formato de fecha (YYYY-MM-DD)"""
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return fecha_str
    except ValueError:
        raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")

def sanitize_email(email):
    """Validar formato de email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Formato de email inválido")
    return email.lower().strip()

# ================== HEADERS DE SEGURIDAD ==================

def add_security_headers(response):
    """Agregar headers de seguridad HTTP"""
    
    # Content Security Policy - Prevenir XSS y ataques de inyección
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    
    # Prevenir clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Prevenir MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Protección XSS del navegador
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Forzar HTTPS (solo en producción con HTTPS)
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Control de referrer
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permisos de features
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    return response

# ================== LOGGING DE SEGURIDAD ==================

def log_security_event(event_type, message, user_id=None):
    """
    Registrar eventos de seguridad
    
    Args:
        event_type: Tipo de evento (login_failed, access_denied, etc.)
        message: Mensaje descriptivo
        user_id: ID del usuario (si aplica)
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    client_ip = get_client_ip()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    log_entry = {
        'timestamp': timestamp,
        'type': event_type,
        'message': message,
        'ip': client_ip,
        'user_id': user_id,
        'user_agent': user_agent[:100],  # Limitar longitud
        'endpoint': request.endpoint,
        'method': request.method
    }
    
    # En producción, guardar en archivo o base de datos
    print(f"[SECURITY] {log_entry}")
    
    # Opcional: guardar en archivo
    # with open('security.log', 'a') as f:
    #     f.write(json.dumps(log_entry) + '\n')

# ================== VALIDACIÓN DE ARCHIVOS ==================

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """Verificar si la extensión del archivo es permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_upload(file):
    """
    Validar archivo subido
    
    Returns:
        (bool, str): (es_valido, mensaje_error)
    """
    if not file:
        return False, "No se ha seleccionado ningún archivo"
    
    if file.filename == '':
        return False, "Nombre de archivo vacío"
    
    if not allowed_file(file.filename):
        return False, f"Tipo de archivo no permitido. Solo se admiten: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Verificar tamaño (si es posible)
    file.seek(0, 2)  # Ir al final
    size = file.tell()
    file.seek(0)  # Volver al inicio
    
    if size > MAX_FILE_SIZE:
        return False, f"Archivo demasiado grande. Máximo: {MAX_FILE_SIZE / 1024 / 1024:.1f}MB"
    
    return True, "OK"

# ================== PROTECCIÓN CSRF ADICIONAL ==================

def generate_csrf_token():
    """Generar token CSRF personalizado (Flask ya tiene protección)"""
    if '_csrf_token' not in session:
        session['_csrf_token'] = hashlib.sha256(
            str(datetime.now()).encode()).hexdigest()
    return session['_csrf_token']

def verify_csrf_token(token):
    """Verificar token CSRF"""
    return token == session.get('_csrf_token', '')

# ==================================================
# FUNCIONES DE UTILIDAD
# ==================================================

def is_safe_redirect_url(target):
    """Verificar que la URL de redirección sea segura"""
    from urllib.parse import urlparse, urljoin
    from flask import request
    
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def require_admin(f):
    """Decorator para requerir rol de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask_login import current_user
        if not current_user.is_authenticated or current_user.perfil != 'Administrador':
            log_security_event('access_denied', 'Intento de acceso no autorizado a función de admin')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# ==================================================
# EXPORT
# ==================================================

__all__ = [
    'rate_limit',
    'add_security_headers',
    'sanitize_nss',
    'sanitize_monto',
    'sanitize_fecha',
    'sanitize_email',
    'log_security_event',
    'validate_file_upload',
    'require_admin'
]


