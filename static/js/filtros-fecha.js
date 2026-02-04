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
        const valorActual = input.value; // yyyy-mm-dd
        
        // Convertir a dd/mm/yyyy para mostrar
        if (valorActual) {
            const [ano, mes, dia] = valorActual.split('-');
            input.setAttribute('data-valor-sql', valorActual); // Guardar original
            input.value = `${dia}/${mes}/${ano}`; // Mostrar dd/mm/yyyy
        }
        
        // Cambiar type a text
        input.type = 'text';
        input.placeholder = 'dd/mm/yyyy';
        
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
    inicializarFechasDDMMYYYY();
    mantenerFiltros();
});
