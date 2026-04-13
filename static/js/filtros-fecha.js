/**
 * Sistema de Filtros de Fecha dd/mm/yyyy
 * Autor: Sistema Dra. Shirley
 * Fecha: 2026
 */

/**
 * Habilitar selector de calendario (input type="date")
 *
 * Nota:
 * - Antes este script convertía los inputs a type="text" para forzar dd/mm/yyyy,
 *   lo cual deshabilitaba el calendario nativo del navegador.
 * - Ahora mantenemos type="date" para que el usuario pueda elegir desde el calendario.
 */
function inicializarCalendariosFecha() {
    document.querySelectorAll('input[data-formato="dd/mm/yyyy"]').forEach((input) => {
        // Garantizar input type="date"
        if (input.type !== 'date') input.type = 'date';

        const raw = (input.value || '').toString().trim();
        if (!raw) return;

        // Si viene como dd/mm/yyyy, convertir a yyyy-mm-dd
        const m = raw.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
        if (m) {
            const dd = m[1];
            const mm = m[2];
            const yyyy = m[3];
            input.value = `${yyyy}-${mm}-${dd}`;
            return;
        }

        // Si viene como datetime string, usar solo la parte ISO de fecha
        if (raw.length > 10 && raw.includes('-') && raw.slice(0, 10).match(/^\d{4}-\d{2}-\d{2}$/)) {
            input.value = raw.slice(0, 10);
        }
    });
}

/**
 * Mantener filtros en la página (persistencia)
 */
function mantenerFiltros() {
    // Los filtros se mantienen automáticamente porque se pasan en la URL
    // Solo asegurarse de que el formulario use method="GET"
    console.log('Filtros persistentes activados');
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando calendarios de fecha...');
    inicializarCalendariosFecha();
    mantenerFiltros();
    
    // Forzar conversión después de un pequeño delay (por si hay pre-llenado dinámico)
    setTimeout(function() {
        console.log('🔄 Re-inicializando calendarios (verificación)...');
        inicializarCalendariosFecha();
    }, 500);
});
