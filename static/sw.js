// Service Worker para PWA y cache offline
const CACHE_NAME = 'drashirley-v3.3'; // Bump: limpiar cache viejo (imágenes)
const urlsToCache = [
  '/static/css/critical.min.css',
  '/static/logos/logo-dra-shirley.png',
  // Favicons (Google a veces pide /favicon.ico)
  '/favicon.ico',
  '/static/favicon.ico',
  '/static/favicon.png',
  '/static/favicon-96.png',
  // Imágenes reales (WebP + fallback JPG)
  '/static/images/dra-shirley-profesional.webp',
  '/static/images/dra-shirley-profesional.jpg',
  '/static/images/97472.webp',
  '/static/images/97472.jpg',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Instalar Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache abierto');
        return cache.addAll(urlsToCache);
      })
  );
  // Activar inmediatamente
  self.skipWaiting();
});

// Activar Service Worker y limpiar caches antiguos
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Eliminando cache antiguo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  return self.clients.claim();
});

// Estrategia: Network First, fallback a Cache
self.addEventListener('fetch', event => {
  // Solo cachear GET requests
  if (event.request.method !== 'GET') return;
  
  // No cachear navegación/HTML: evita quedarse con páginas viejas (y romper imágenes)
  if (event.request.mode === 'navigate') {
    return;
  }

  // Ignorar rutas admin y facturación (necesitan autenticación)
  if (event.request.url.includes('/admin') || 
      event.request.url.includes('/facturacion') ||
      event.request.url.includes('/login')) {
    return;
  }
  
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Si la respuesta es válida, clonarla y guardarla en cache
        // Cachear solo recursos estáticos propios para evitar HTML viejo
        const url = new URL(event.request.url);
        const isSameOrigin = url.origin === self.location.origin;
        const isStatic = isSameOrigin && url.pathname.startsWith('/static/');

        if (isStatic && response && response.status === 200 && response.type === 'basic') {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        // Si falla la red, intentar obtener de cache
        return caches.match(event.request);
      })
  );
});

// Background Sync para formularios offline (opcional)
self.addEventListener('sync', event => {
  if (event.tag === 'sync-forms') {
    event.waitUntil(syncForms());
  }
});

async function syncForms() {
  // Lógica para sincronizar formularios pendientes
  console.log('Sincronizando formularios pendientes...');
}


