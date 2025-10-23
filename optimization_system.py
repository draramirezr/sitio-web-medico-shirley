#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Optimización y Caché
Sistema Médico - Dra. Shirley Ramírez
"""

import os
import time
import hashlib
from functools import wraps
from typing import Any, Dict, Optional

# Configuración de caché simple en memoria
_cache: Dict[str, Dict[str, Any]] = {}
_cache_stats = {'hits': 0, 'misses': 0, 'sets': 0}

def cache_result(expiration_seconds: int = 300):
    """
    Decorador para cachear resultados de funciones
    expiration_seconds: Tiempo de expiración en segundos (default: 5 minutos)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Crear clave única para la función y sus argumentos
            key_data = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Verificar si existe en caché y no ha expirado
            if cache_key in _cache:
                cached_data = _cache[cache_key]
                if time.time() - cached_data['timestamp'] < expiration_seconds:
                    _cache_stats['hits'] += 1
                    return cached_data['value']
                else:
                    # Eliminar entrada expirada
                    del _cache[cache_key]
            
            # Ejecutar función y cachear resultado
            result = func(*args, **kwargs)
            _cache[cache_key] = {
                'value': result,
                'timestamp': time.time()
            }
            _cache_stats['misses'] += 1
            _cache_stats['sets'] += 1
            
            return result
        return wrapper
    return decorator

def clear_cache():
    """Limpiar todo el caché"""
    global _cache
    _cache.clear()
    _cache_stats['hits'] = 0
    _cache_stats['misses'] = 0
    _cache_stats['sets'] = 0

def get_cache_stats():
    """Obtener estadísticas del caché"""
    total_requests = _cache_stats['hits'] + _cache_stats['misses']
    hit_rate = (_cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
    
    return {
        'hits': _cache_stats['hits'],
        'misses': _cache_stats['misses'],
        'sets': _cache_stats['sets'],
        'hit_rate': round(hit_rate, 2),
        'cache_size': len(_cache)
    }

def optimize_database_connection():
    """Optimizar configuración de base de datos"""
    optimizations = {
        'sqlite': [
            'PRAGMA journal_mode=WAL',
            'PRAGMA synchronous=NORMAL',
            'PRAGMA cache_size=20000',
            'PRAGMA temp_store=MEMORY',
            'PRAGMA mmap_size=268435456',
            'PRAGMA page_size=4096',
            'PRAGMA auto_vacuum=INCREMENTAL'
        ],
        'mysql': [
            'SET SESSION query_cache_type=ON',
            'SET SESSION query_cache_size=67108864',  # 64MB
            'SET SESSION tmp_table_size=134217728',   # 128MB
            'SET SESSION max_heap_table_size=134217728'  # 128MB
        ]
    }
    return optimizations

def compress_response(response):
    """Comprimir respuesta HTTP"""
    if response.content_type and 'text/' in response.content_type:
        # Comprimir contenido de texto
        content = response.get_data()
        if len(content) > 1024:  # Solo comprimir si es mayor a 1KB
            import gzip
            compressed = gzip.compress(content)
            if len(compressed) < len(content):
                response.set_data(compressed)
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Content-Length'] = str(len(compressed))
    
    return response

def add_security_headers(response):
    """Agregar headers de seguridad"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self';"
    )
    return response

def add_cache_headers(response, max_age: int = 3600):
    """Agregar headers de caché"""
    if response.content_type:
        if 'text/html' in response.content_type:
            # HTML: caché corto
            response.headers['Cache-Control'] = f'public, max-age={max_age}'
        elif any(ext in response.content_type for ext in ['css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg']):
            # Assets estáticos: caché largo
            response.headers['Cache-Control'] = 'public, max-age=2592000'  # 30 días
        else:
            # Otros: sin caché
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    
    return response

def optimize_query(query: str, params: tuple = None) -> str:
    """Optimizar consulta SQL"""
    # Eliminar espacios extra
    query = ' '.join(query.split())
    
    # Optimizaciones específicas
    optimizations = {
        'SELECT *': 'SELECT',  # Evitar SELECT *
        'ORDER BY id': 'ORDER BY id LIMIT 100',  # Limitar resultados por defecto
    }
    
    for old, new in optimizations.items():
        if old in query:
            query = query.replace(old, new)
    
    return query

def get_performance_stats():
    """Obtener estadísticas de rendimiento"""
    import psutil
    import sys
    
    process = psutil.Process()
    
    return {
        'memory_usage_mb': round(process.memory_info().rss / 1024 / 1024, 2),
        'cpu_percent': process.cpu_percent(),
        'cache_stats': get_cache_stats(),
        'python_version': sys.version,
        'uptime_seconds': time.time() - process.create_time()
    }

if __name__ == "__main__":
    # Prueba del sistema de caché
    @cache_result(expiration_seconds=60)
    def expensive_function(n):
        time.sleep(0.1)  # Simular operación costosa
        return n * n
    
    # Probar caché
    start = time.time()
    result1 = expensive_function(5)
    time1 = time.time() - start
    
    start = time.time()
    result2 = expensive_function(5)  # Debería usar caché
    time2 = time.time() - start
    
    print(f"Primera ejecución: {time1:.4f}s")
    print(f"Segunda ejecución (caché): {time2:.4f}s")
    print(f"Estadísticas: {get_cache_stats()}")

