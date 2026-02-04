/**
 * Sistema de Filtros de Fecha dd/mm/yyyy
 * Autor: Sistema Dra. Shirley
 * Fecha: 2026
 */

/**
 * Convertir input type="date" a formato dd/mm/yyyy visible
 */
function inicializarFechasDDMMYYYY() {
    // Buscar todos los inputs de fecha con clase especial
    document.querySelectorAll('input[data-formato="dd/mm/yyyy"]').forEach(input => {
        const valorActual = input.value; // yyyy-mm-dd o vacío
        
        console.log('🔍 Procesando campo fecha:', input.id, 'Valor:', valorActual);
        
        // Convertir a dd/mm/yyyy para mostrar
        if (valorActual && valorActual.includes('-')) {
            try {
                const [ano, mes, dia] = valorActual.split('-');
                if (ano && mes && dia) {
                    const fechaFormateada = `${dia}/${mes}/${ano}`;
                    input.setAttribute('data-valor-sql', valorActual); // Guardar original
                    input.value = fechaFormateada; // Mostrar dd/mm/yyyy
                    console.log('✅ Fecha convertida:', valorActual, '→', fechaFormateada);
                }
            } catch (e) {
                console.error('❌ Error al convertir fecha:', e);
            }
        }
        
        // Cambiar type a text
        input.type = 'text';
        input.placeholder = 'dd/mm/yyyy';
        input.title = 'Formato: dd/mm/yyyy (ejemplo: 04/02/2026)';
        
        // Validación en tiempo real
        input.addEventListener('input', function(e) {
            let value = this.value.replace(/[^0-9/]/g, '');
            
            // Auto-agregar barras
            if (value.length === 2 && !value.includes('/')) {
                value += '/';
            } else if (value.length === 5 && value.split('/').length === 2) {
                value += '/';
            }
            
            if (value.length > 10) {
                value = value.substring(0, 10);
            }
            
            this.value = value;
        });
        
        // Validar antes de enviar formulario
        input.form.addEventListener('submit', function(e) {
            const fecha = input.value.trim();
            if (!fecha && input.required) {
                alert('La fecha es obligatoria');
                e.preventDefault();
                input.focus();
                return;
            }
            
            if (fecha) {
                const regex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
                const match = fecha.match(regex);
                
                if (!match) {
                    alert('Formato de fecha incorrecto. Use: dd/mm/yyyy');
                    e.preventDefault();
                    input.focus();
                    return;
                }
                
                const [, dia, mes, ano] = match;
                
                // Convertir a yyyy-mm-dd para enviar al servidor
                const fechaSQL = `${ano}-${mes}-${dia}`;
                input.value = fechaSQL;
            }
        });
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
    console.log('🚀 Inicializando sistema de fechas dd/mm/yyyy...');
    inicializarFechasDDMMYYYY();
    mantenerFiltros();
    
    // Forzar conversión después de un pequeño delay (por si hay pre-llenado dinámico)
    setTimeout(function() {
        console.log('🔄 Re-inicializando fechas (verificación)...');
        inicializarFechasDDMMYYYY();
    }, 500);
});
