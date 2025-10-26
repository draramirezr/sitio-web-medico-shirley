# -*- coding: utf-8 -*-
"""
Sistema de Templates de Email Unificado
Plantillas HTML profesionales con diseño estándar
"""

def get_email_header():
    """Header estándar para todos los emails"""
    return """
    <div style="background: linear-gradient(135deg, #CEB0B7 0%, #B89CA3 100%); padding: 30px; text-align: center; border-radius: 15px 15px 0 0;">
        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            Dra. Shirley Ramírez
        </h1>
        <p style="color: rgba(255,255,255,0.95); margin: 8px 0 0 0; font-size: 14px; font-weight: 400;">
            Ginecóloga • Obstetra • Salud Femenina
        </p>
    </div>
    """

def get_email_footer():
    """Footer estándar para todos los emails"""
    return """
    <div style="background-color: #F2E2E6; padding: 25px; text-align: center; border-radius: 0 0 15px 15px; margin-top: 20px;">
        <div style="border-top: 2px solid #CEB0B7; padding-top: 20px; margin-bottom: 15px;">
            <p style="color: #ACACAD; font-size: 14px; margin: 8px 0; font-weight: 600;">
                📞 829-740-5073 | 📧 dra.ramirezr@gmail.com
            </p>
            <p style="color: #ACACAD; font-size: 13px; margin: 8px 0;">
                📍 Santo Domingo | República Dominicana
            </p>
        </div>
        <div style="margin-top: 15px;">
            <a href="https://www.linkedin.com/in/shirley-ramirez-montero-a10964168/" 
               style="display: inline-block; margin: 0 8px; color: #CEB0B7; text-decoration: none; font-size: 20px;">
                🔗 LinkedIn
            </a>
            <a href="https://www.instagram.com/dra.ramirezr/" 
               style="display: inline-block; margin: 0 8px; color: #CEB0B7; text-decoration: none; font-size: 20px;">
                📷 Instagram
            </a>
        </div>
        <p style="color: #999; font-size: 11px; margin: 15px 0 0 0; line-height: 1.4;">
            Este email fue enviado desde el sistema de gestión médica<br>
            <strong>Dra. Shirley Ramírez</strong> • &copy; 2025 • Todos los derechos reservados
        </p>
    </div>
    """

def get_base_template(title_icon, title_text, content):
    """Template base para todos los emails"""
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title_text}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #F8F4F5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #F8F4F5; padding: 30px 15px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="max-width: 600px; width: 100%; background-color: white; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                        <tr>
                            <td>
                                {get_email_header()}
                                
                                <div style="padding: 35px 30px;">
                                    <h2 style="color: #ACACAD; border-bottom: 3px solid #CEB0B7; padding-bottom: 15px; margin-top: 0; font-size: 22px; font-weight: 600;">
                                        {title_icon} {title_text}
                                    </h2>
                                    
                                    {content}
                                </div>
                                
                                {get_email_footer()}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

def template_contacto(nombre, email, telefono, asunto, mensaje):
    """Template para emails de contacto"""
    content = f"""
    <div style="background-color: #F2E2E6; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <p style="margin: 10px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">👤 Nombre:</strong> {nombre}
        </p>
        <p style="margin: 10px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">📧 Email:</strong> 
            <a href="mailto:{email}" style="color: #CEB0B7; text-decoration: none; font-weight: 500;">{email}</a>
        </p>
        <p style="margin: 10px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">📱 Teléfono:</strong> 
            <a href="tel:{telefono}" style="color: #CEB0B7; text-decoration: none; font-weight: 500;">{telefono}</a>
        </p>
        <p style="margin: 10px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">📝 Asunto:</strong> {asunto}
        </p>
    </div>
    
    <div style="background-color: #fff; padding: 20px; border-left: 4px solid #CEB0B7; margin: 20px 0; border-radius: 5px;">
        <p style="margin: 0 0 10px 0; color: #ACACAD; font-weight: 600; font-size: 15px;">💬 Mensaje:</p>
        <p style="margin: 0; color: #282828; line-height: 1.7; font-size: 14px; white-space: pre-wrap;">{mensaje}</p>
    </div>
    
    <div style="text-align: center; margin-top: 30px;">
        <a href="mailto:{email}" 
           style="display: inline-block; padding: 14px 35px; background: linear-gradient(135deg, #ACACAD 0%, #949495 100%); color: white !important; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 15px; box-shadow: 0 4px 12px rgba(172, 172, 173, 0.3);">
            📧 Responder a {nombre}
        </a>
    </div>
    """
    
    return get_base_template("📧", "Nuevo Mensaje de Contacto", content)

def template_cita(nombre, apellido, email, telefono, fecha, hora, tipo, seguro, emergencia, motivo):
    """Template para emails de citas"""
    content = f"""
    <div style="background: linear-gradient(135deg, rgba(206, 176, 183, 0.15) 0%, rgba(242, 226, 230, 0.3) 100%); padding: 25px; border-radius: 10px; margin: 20px 0; border: 2px solid #CEB0B7;">
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">👤 Paciente:</strong> {nombre} {apellido}
        </p>
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">📧 Email:</strong> 
            <a href="mailto:{email}" style="color: #CEB0B7; text-decoration: none; font-weight: 500;">{email}</a>
        </p>
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">📱 Teléfono:</strong> 
            <a href="tel:{telefono}" style="color: #CEB0B7; text-decoration: none; font-weight: 500;">{telefono}</a>
        </p>
    </div>
    
    <div style="background-color: #FFF9E6; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #FFC107;">
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #F57C00; font-weight: 600;">📅 Fecha:</strong> {fecha}
        </p>
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #F57C00; font-weight: 600;">🕐 Hora:</strong> {hora}
        </p>
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #F57C00; font-weight: 600;">🏥 Tipo:</strong> {tipo}
        </p>
        {f'<p style="margin: 12px 0; color: #282828; font-size: 15px;"><strong style="color: #F57C00; font-weight: 600;">🏥 Seguro:</strong> {seguro}</p>' if seguro else ''}
        {f'<p style="margin: 12px 0; color: #D32F2F; font-size: 15px;"><strong style="color: #D32F2F; font-weight: 600;">⚠️ EMERGENCIA:</strong> {emergencia}</p>' if emergencia else ''}
    </div>
    
    <div style="background-color: #fff; padding: 20px; border-left: 4px solid #CEB0B7; margin: 20px 0; border-radius: 5px;">
        <p style="margin: 0 0 10px 0; color: #ACACAD; font-weight: 600; font-size: 15px;">💬 Motivo de la Cita:</p>
        <p style="margin: 0; color: #282828; line-height: 1.7; font-size: 14px; white-space: pre-wrap;">{motivo}</p>
    </div>
    
    <div style="text-align: center; margin-top: 30px;">
        <a href="tel:{telefono}" 
           style="display: inline-block; padding: 14px 35px; background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white !important; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 15px; box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3); margin: 5px;">
            📞 Llamar al Paciente
        </a>
        <a href="mailto:{email}" 
           style="display: inline-block; padding: 14px 35px; background: linear-gradient(135deg, #ACACAD 0%, #949495 100%); color: white !important; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 15px; box-shadow: 0 4px 12px rgba(172, 172, 173, 0.3); margin: 5px;">
            📧 Enviar Email
        </a>
    </div>
    """
    
    return get_base_template("📅", f"Nueva Solicitud de Cita - {nombre} {apellido}", content)

def template_recuperacion(nombre, link_recuperacion):
    """Template para emails de recuperación de contraseña"""
    content = f"""
    <div style="color: #282828; line-height: 1.8; margin: 20px 0; font-size: 15px;">
        <p style="margin: 15px 0;">Hola <strong style="color: #ACACAD;">{nombre}</strong>,</p>
        <p style="margin: 15px 0;">
            Has solicitado restablecer tu contraseña del panel administrativo.
        </p>
        <p style="margin: 15px 0;">
            Para crear una nueva contraseña, haz clic en el siguiente botón:
        </p>
    </div>
    
    <div style="text-align: center; margin: 35px 0;">
        <a href="{link_recuperacion}" 
           style="display: inline-block; padding: 16px 45px; background: linear-gradient(135deg, #ACACAD 0%, #949495 100%); color: white !important; text-decoration: none; border-radius: 30px; font-weight: 600; font-size: 16px; box-shadow: 0 6px 16px rgba(172, 172, 173, 0.4);">
            🔐 Restablecer Contraseña
        </a>
    </div>
    
    <div style="background-color: #FFF3E0; padding: 20px; border-radius: 10px; border-left: 4px solid #FF9800; margin: 25px 0;">
        <p style="margin: 0; color: #E65100; font-size: 14px; line-height: 1.6;">
            <strong>⚠️ Importante:</strong><br>
            • Este enlace expira en <strong>1 hora</strong><br>
            • Si no solicitaste este cambio, ignora este email<br>
            • Tu contraseña actual no cambiará hasta que completes el proceso
        </p>
    </div>
    
    <div style="background-color: #F2E2E6; padding: 18px; border-radius: 10px; margin: 25px 0;">
        <p style="margin: 0; color: #666; font-size: 13px; line-height: 1.6;">
            <strong style="color: #ACACAD;">💡 Consejos de seguridad:</strong><br>
            • Usa una contraseña única y segura<br>
            • Combina letras mayúsculas, minúsculas, números y símbolos<br>
            • No compartas tu contraseña con nadie
        </p>
    </div>
    
    <div style="margin-top: 25px; padding-top: 20px; border-top: 2px solid #F2E2E6;">
        <p style="color: #999; font-size: 13px; line-height: 1.5; margin: 0;">
            Si tienes problemas con el botón, copia y pega este enlace en tu navegador:<br>
            <a href="{link_recuperacion}" style="color: #CEB0B7; word-break: break-all; font-size: 12px;">{link_recuperacion}</a>
        </p>
    </div>
    """
    
    return get_base_template("🔐", "Recuperación de Contraseña", content)

def template_constancia_pdf(medico_nombre, num_pacientes, total):
    """Template para emails con constancia PDF"""
    content = f"""
    <div style="background: linear-gradient(135deg, rgba(206, 176, 183, 0.15) 0%, rgba(242, 226, 230, 0.3) 100%); padding: 25px; border-radius: 10px; margin: 20px 0; border: 2px solid #CEB0B7;">
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">👨‍⚕️ Médico:</strong> {medico_nombre}
        </p>
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">📋 Pacientes Pendientes:</strong> {num_pacientes}
        </p>
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">💰 Monto Total:</strong> 
            <span style="color: #4CAF50; font-weight: 700; font-size: 18px;">${total:,.2f}</span>
        </p>
    </div>
    
    <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #2196F3;">
        <p style="margin: 0; color: #1565C0; font-size: 14px; line-height: 1.7;">
            <strong>📎 Archivo Adjunto</strong><br>
            Se ha generado una constancia en PDF con el detalle completo de los pacientes pendientes de facturación.
        </p>
    </div>
    
    <div style="background-color: #fff; padding: 20px; border-left: 4px solid #CEB0B7; margin: 20px 0; border-radius: 5px;">
        <p style="margin: 0 0 10px 0; color: #ACACAD; font-weight: 600; font-size: 15px;">📄 Contenido del PDF:</p>
        <ul style="margin: 10px 0; padding-left: 20px; color: #282828; line-height: 1.8; font-size: 14px;">
            <li>Información del médico</li>
            <li>Listado detallado de pacientes</li>
            <li>Servicios y montos</li>
            <li>Total general</li>
            <li>Fecha de generación</li>
        </ul>
    </div>
    
    <div style="background-color: #FFF9E6; padding: 18px; border-radius: 10px; margin: 25px 0; border-left: 4px solid #FFC107;">
        <p style="margin: 0; color: #F57C00; font-size: 14px; line-height: 1.6;">
            <strong>💡 Próximos pasos:</strong><br>
            1. Descarga y revisa el PDF adjunto<br>
            2. Verifica la información de los pacientes<br>
            3. Procede con la facturación según corresponda
        </p>
    </div>
    """
    
    return get_base_template("📋", f"Constancia - {num_pacientes} Paciente(s) Pendiente(s)", content)

def template_factura(factura_id, ncf, monto_total):
    """Template para emails con factura"""
    content = f"""
    <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(129, 199, 132, 0.2) 100%); padding: 25px; border-radius: 10px; margin: 20px 0; border: 2px solid #4CAF50;">
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #2E7D32; font-weight: 600;">📄 No. Factura:</strong> 
            <span style="font-weight: 700; color: #1B5E20;">#{factura_id}</span>
        </p>
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #2E7D32; font-weight: 600;">🔢 NCF:</strong> 
            <span style="font-weight: 700; color: #1B5E20;">{ncf}</span>
        </p>
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #2E7D32; font-weight: 600;">💰 Monto Total:</strong> 
            <span style="color: #4CAF50; font-weight: 700; font-size: 20px;">${monto_total:,.2f}</span>
        </p>
    </div>
    
    <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #4CAF50;">
        <p style="margin: 0; color: #2E7D32; font-size: 14px; line-height: 1.7;">
            <strong>✅ Factura Generada Exitosamente</strong><br>
            Adjunto encontrarás la factura en formato PDF con todos los detalles de la transacción.
        </p>
    </div>
    
    <div style="background-color: #fff; padding: 20px; border-left: 4px solid #CEB0B7; margin: 20px 0; border-radius: 5px;">
        <p style="margin: 0 0 10px 0; color: #ACACAD; font-weight: 600; font-size: 15px;">📄 La factura incluye:</p>
        <ul style="margin: 10px 0; padding-left: 20px; color: #282828; line-height: 1.8; font-size: 14px;">
            <li>Información del médico</li>
            <li>Información del paciente/ARS</li>
            <li>Detalle de servicios prestados</li>
            <li>Montos y totales</li>
            <li>NCF asignado</li>
        </ul>
    </div>
    
    <div style="background-color: #FFF3E0; padding: 18px; border-radius: 10px; margin: 25px 0; border-left: 4px solid #FF9800;">
        <p style="margin: 0; color: #E65100; font-size: 14px; line-height: 1.6;">
            <strong>📌 Importante:</strong><br>
            • Conserva este email y el PDF adjunto para tus registros<br>
            • El NCF es válido y está registrado oficialmente<br>
            • Para cualquier aclaración, contáctanos
        </p>
    </div>
    """
    
    return get_base_template("💰", f"Factura #{factura_id} - NCF: {ncf}", content)

def template_confirmacion_cita(nombre, apellido, fecha, hora, tipo, estatus, motivo=None):
    """Template para confirmación de cambio de estatus de cita al paciente"""
    
    # Configurar colores y mensajes según el estatus
    estatus_config = {
        'pending': {
            'color': '#FF9800',
            'bg': '#FFF3E0',
            'icon': '⏳',
            'titulo': 'Cita Pendiente de Confirmación',
            'mensaje': 'Tu solicitud de cita ha sido recibida y está <strong>pendiente de confirmación</strong>.',
            'accion': 'Nos pondremos en contacto contigo pronto para confirmar la disponibilidad.'
        },
        'confirmed': {
            'color': '#4CAF50',
            'bg': '#E8F5E9',
            'icon': '✅',
            'titulo': '¡Cita Confirmada!',
            'mensaje': 'Tu cita ha sido <strong>confirmada exitosamente</strong>.',
            'accion': 'Te esperamos en la fecha y hora indicadas. Por favor, llega 10 minutos antes.'
        },
        'cancelled': {
            'color': '#F44336',
            'bg': '#FFEBEE',
            'icon': '❌',
            'titulo': 'Cita Cancelada',
            'mensaje': 'Lamentamos informarte que tu cita ha sido <strong>cancelada</strong>.',
            'accion': 'Si deseas reagendar, contáctanos o solicita una nueva cita desde nuestra página web.'
        },
        'completed': {
            'color': '#2196F3',
            'bg': '#E3F2FD',
            'icon': '✔️',
            'titulo': 'Cita Completada',
            'mensaje': 'Tu cita ha sido <strong>completada</strong>. Gracias por confiar en nosotros.',
            'accion': 'Esperamos haberte brindado una excelente atención. No dudes en contactarnos si tienes alguna pregunta.'
        }
    }
    
    config = estatus_config.get(estatus, estatus_config['pending'])
    
    content = f"""
    <div style="color: #282828; line-height: 1.8; margin: 20px 0; font-size: 15px;">
        <p style="margin: 15px 0;">Hola <strong style="color: #ACACAD;">{nombre} {apellido}</strong>,</p>
        <p style="margin: 15px 0;">
            {config['mensaje']}
        </p>
    </div>
    
    <div style="background: linear-gradient(135deg, {config['bg']} 0%, {config['bg']}dd 100%); padding: 25px; border-radius: 10px; margin: 25px 0; border: 2px solid {config['color']}; text-align: center;">
        <div style="font-size: 48px; margin-bottom: 15px;">
            {config['icon']}
        </div>
        <h3 style="color: {config['color']}; margin: 10px 0; font-size: 20px; font-weight: 700;">
            {config['titulo']}
        </h3>
    </div>
    
    <div style="background-color: #F2E2E6; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <p style="margin: 0 0 10px 0; color: #ACACAD; font-weight: 600; font-size: 15px;">📋 Detalles de tu Cita:</p>
        <p style="margin: 10px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">📅 Fecha:</strong> {fecha if fecha else 'Por confirmar'}
        </p>
        <p style="margin: 10px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">🕐 Hora:</strong> {hora if hora else 'Por confirmar'}
        </p>
        <p style="margin: 10px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">🏥 Tipo:</strong> {tipo}
        </p>
        {f'<p style="margin: 10px 0; color: #282828; font-size: 15px;"><strong style="color: #ACACAD; font-weight: 600;">💬 Motivo:</strong> {motivo}</p>' if motivo else ''}
    </div>
    
    <div style="background-color: #fff; padding: 20px; border-left: 4px solid {config['color']}; margin: 20px 0; border-radius: 5px;">
        <p style="margin: 0; color: #282828; line-height: 1.7; font-size: 14px;">
            {config['accion']}
        </p>
    </div>
    
    <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; margin: 25px 0; border-left: 4px solid #2196F3;">
        <p style="margin: 0 0 10px 0; color: #1565C0; font-weight: 600; font-size: 15px;">📞 ¿Necesitas ayuda?</p>
        <p style="margin: 8px 0; color: #1976D2; font-size: 14px;">
            • Teléfono: <a href="tel:+18297405073" style="color: #2196F3; text-decoration: none; font-weight: 600;">829-740-5073</a>
        </p>
        <p style="margin: 8px 0; color: #1976D2; font-size: 14px;">
            • Email: <a href="mailto:dra.ramirezr@gmail.com" style="color: #2196F3; text-decoration: none; font-weight: 600;">dra.ramirezr@gmail.com</a>
        </p>
    </div>
    
    <div style="text-align: center; margin-top: 30px;">
        <a href="tel:+18297405073" 
           style="display: inline-block; padding: 14px 35px; background: linear-gradient(135deg, #CEB0B7 0%, #B89CA3 100%); color: white !important; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 15px; box-shadow: 0 4px 12px rgba(206, 176, 183, 0.4); margin: 5px;">
            📞 Llamar Ahora
        </a>
        <a href="https://wa.me/18297405073" 
           style="display: inline-block; padding: 14px 35px; background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white !important; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 15px; box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4); margin: 5px;">
            💬 WhatsApp
        </a>
    </div>
    """
    
    return get_base_template(config['icon'], config['titulo'], content)

def template_bienvenida_facturacion(nombre, email, password_temporal, link_admin, puede_generar_facturas=False):
    """Template para email de bienvenida a usuarios de facturación
    
    Args:
        nombre: Nombre del usuario
        email: Email del usuario
        password_temporal: Contraseña temporal
        link_admin: Link al panel de admin
        puede_generar_facturas: Si True, el usuario es Nivel 2 y puede generar facturas finales
    """
    
    # Texto adicional para Nivel 2
    texto_nivel2 = ""
    if puede_generar_facturas:
        texto_nivel2 = """
        <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.2) 0%, rgba(129, 199, 132, 0.3) 100%); padding: 20px; border-radius: 10px; margin: 20px 0; border: 3px solid #4CAF50;">
            <p style="margin: 0 0 10px 0; color: #2E7D32; font-weight: 700; font-size: 16px; text-align: center;">
                🌟 TU PERFIL: NIVEL 2 - PERMISOS COMPLETOS
            </p>
            <p style="margin: 8px 0; color: #1B5E20; font-size: 14px; line-height: 1.8; text-align: center;">
                ¡Tienes acceso COMPLETO al módulo de facturación!<br>
                Puedes <strong>agregar pacientes, ver estados Y generar las facturas finales en PDF</strong>.
            </p>
        </div>
        """
    
    content = f"""
    <div style="color: #282828; line-height: 1.8; margin: 20px 0; font-size: 15px;">
        <p style="margin: 15px 0;">Hola <strong style="color: #ACACAD;">{nombre}</strong>,</p>
        <p style="margin: 15px 0;">
            ¡Bienvenido al <strong>Sistema de Facturación</strong> de la Dra. Shirley Ramírez! 🎉
        </p>
        <p style="margin: 15px 0;">
            Tu cuenta ha sido creada exitosamente con perfil de <strong style="color: #4CAF50;">{"Nivel 2" if puede_generar_facturas else "Registro de Facturas"}</strong>.
        </p>
    </div>
    
    {texto_nivel2}
    
    <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(129, 199, 132, 0.2) 100%); padding: 25px; border-radius: 10px; margin: 25px 0; border: 2px solid #4CAF50; text-align: center;">
        <div style="font-size: 48px; margin-bottom: 15px;">
            🔐
        </div>
        <h3 style="color: #2E7D32; margin: 10px 0; font-size: 20px; font-weight: 700;">
            Acceso al Sistema
        </h3>
    </div>
    
    <div style="background-color: #F2E2E6; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <p style="margin: 0 0 15px 0; color: #ACACAD; font-weight: 600; font-size: 16px;">🔑 Credenciales de Acceso:</p>
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">📧 Email:</strong> 
            <span style="font-family: 'Courier New', monospace; background: #fff; padding: 5px 10px; border-radius: 5px; display: inline-block;">{email}</span>
        </p>
        <p style="margin: 12px 0; color: #282828; font-size: 15px;">
            <strong style="color: #ACACAD; font-weight: 600;">🔒 Contraseña Temporal:</strong> 
            <span style="font-family: 'Courier New', monospace; background: #fff; padding: 5px 10px; border-radius: 5px; display: inline-block; color: #D32F2F; font-weight: 700;">{password_temporal}</span>
        </p>
    </div>
    
    <div style="text-align: center; margin: 30px 0;">
        <a href="{link_admin}" 
           style="display: inline-block; padding: 16px 45px; background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white !important; text-decoration: none; border-radius: 30px; font-weight: 600; font-size: 16px; box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);">
            🚀 Acceder al Sistema
        </a>
    </div>
    
    <div style="background-color: #FFF3E0; padding: 20px; border-radius: 10px; margin: 25px 0; border-left: 4px solid #FF9800;">
        <p style="margin: 0 0 10px 0; color: #E65100; font-weight: 600; font-size: 15px;">⚠️ Importante - Primera Vez:</p>
        <p style="margin: 8px 0; color: #E65100; font-size: 14px; line-height: 1.7;">
            • Al iniciar sesión, el sistema te pedirá <strong>cambiar tu contraseña</strong> por seguridad<br>
            • Elige una contraseña segura que solo tú conozcas<br>
            • No compartas tus credenciales con nadie
        </p>
    </div>
    
    <div style="background-color: #E3F2FD; padding: 25px; border-radius: 10px; margin: 25px 0; border: 2px solid #2196F3;">
        <p style="margin: 0 0 15px 0; color: #1565C0; font-weight: 700; font-size: 17px;">📋 Objetivo del Sistema</p>
        <p style="margin: 10px 0; color: #1976D2; font-size: 14px; line-height: 1.8;">
            Este sistema te permite <strong>gestionar la facturación de pacientes</strong> de manera eficiente:
        </p>
    </div>
    
    <div style="background-color: #fff; padding: 20px; border-left: 4px solid #CEB0B7; margin: 20px 0; border-radius: 5px;">
        <p style="margin: 0 0 15px 0; color: #ACACAD; font-weight: 600; font-size: 15px;">✨ Funciones Principales:</p>
        
        <div style="margin: 15px 0; padding: 15px; background-color: #F8F9FA; border-radius: 8px;">
            <p style="margin: 0 0 8px 0; color: #4CAF50; font-weight: 700; font-size: 15px;">
                📝 1. Agregar Pacientes
            </p>
            <p style="margin: 0; color: #282828; font-size: 14px; line-height: 1.7;">
                Puedes <strong>cargar pacientes de manera masiva desde Excel</strong> o <strong>editar/agregar individualmente</strong>. 
                Incluye información completa: NSS, nombre, servicios, montos, ARS, médico tratante, etc.
            </p>
        </div>
        
        <div style="margin: 15px 0; padding: 15px; background-color: #F8F9FA; border-radius: 8px;">
            <p style="margin: 0 0 8px 0; color: #FF9800; font-weight: 700; font-size: 15px;">
                📊 2. Estado de Facturación
            </p>
            <p style="margin: 0; color: #282828; font-size: 14px; line-height: 1.7;">
                <strong>Da seguimiento en tiempo real</strong> al estado de cada factura: pendiente, en proceso, 
                pagada, rechazada. Filtra por ARS, médico, fecha, monto y más.
            </p>
        </div>
        
        {"" if not puede_generar_facturas else '''
        <div style="margin: 15px 0; padding: 15px; background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(129, 199, 132, 0.15) 100%); border-radius: 8px; border: 2px solid #4CAF50;">
            <p style="margin: 0 0 8px 0; color: #2E7D32; font-weight: 700; font-size: 15px;">
                💰 3. Generar Facturas Finales ⭐ NIVEL 2
            </p>
            <p style="margin: 0; color: #1B5E20; font-size: 14px; line-height: 1.7;">
                <strong>¡Permiso especial!</strong> Puedes generar las <strong>facturas finales en PDF con NCF automático</strong>, 
                listas para imprimir, firmar y enviar a las ARS. Esta función es exclusiva de tu nivel.
            </p>
        </div>
        ''' if puede_generar_facturas else '''
        <div style="margin: 15px 0; padding: 15px; background-color: #F8F9FA; border-radius: 8px;">
            <p style="margin: 0 0 8px 0; color: #2196F3; font-weight: 700; font-size: 15px;">
                💰 3. Generar Facturas
            </p>
            <p style="margin: 0; color: #282828; font-size: 14px; line-height: 1.7;">
                Los usuarios con perfil <strong>Nivel 2</strong> pueden generar facturas profesionales en PDF con NCF automático.
            </p>
        </div>
        '''}
        
        <div style="margin: 15px 0; padding: 15px; background-color: #F8F9FA; border-radius: 8px;">
            <p style="margin: 0 0 8px 0; color: #9C27B0; font-weight: 700; font-size: 15px;">
                📈 4. Reportes y Estadísticas
            </p>
            <p style="margin: 0; color: #282828; font-size: 14px; line-height: 1.7;">
                Consulta el histórico completo de facturación, exporta reportes a Excel, y visualiza estadísticas.
            </p>
        </div>
    </div>
    
    <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin: 25px 0; border-left: 4px solid #4CAF50;">
        <p style="margin: 0 0 10px 0; color: #2E7D32; font-weight: 600; font-size: 15px;">🎯 Cómo Empezar:</p>
        <ol style="margin: 10px 0; padding-left: 25px; color: #282828; line-height: 2; font-size: 14px;">
            <li><strong>Inicia sesión</strong> con tus credenciales</li>
            <li><strong>Cambia tu contraseña temporal</strong> por una segura</li>
            <li>Ve a <strong>"Facturación → Agregar Pacientes"</strong></li>
            <li>Carga pacientes desde Excel o agrégalos manualmente</li>
            <li>Usa <strong>"Estado de Facturación"</strong> para dar seguimiento</li>
            {"<li><strong>Genera facturas finales</strong> desde el menú de facturación</li>" if puede_generar_facturas else ""}
        </ol>
    </div>
    
    <div style="background-color: #FFF9E6; padding: 18px; border-radius: 10px; margin: 25px 0; border-left: 4px solid #FFC107;">
        <p style="margin: 0; color: #F57C00; font-size: 14px; line-height: 1.7;">
            <strong>💡 Consejos Útiles:</strong><br>
            • El sistema guarda automáticamente todos los cambios<br>
            • Puedes exportar reportes a Excel en cualquier momento<br>
            • Los filtros te ayudan a encontrar información rápidamente<br>
            • Cada acción queda registrada en el historial
        </p>
    </div>
    
    <div style="background-color: #FFEBEE; padding: 20px; border-radius: 10px; margin: 25px 0; border-left: 4px solid #F44336;">
        <p style="margin: 0 0 10px 0; color: #C62828; font-weight: 600; font-size: 15px;">🔒 Seguridad y Privacidad:</p>
        <p style="margin: 8px 0; color: #D32F2F; font-size: 14px; line-height: 1.7;">
            • Toda la información está <strong>encriptada</strong> y protegida<br>
            • Solo usuarios autorizados tienen acceso<br>
            • Cumplimos con estándares de privacidad médica<br>
            • Tu sesión expira automáticamente por seguridad
        </p>
    </div>
    
    <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; margin: 25px 0; border-left: 4px solid #2196F3;">
        <p style="margin: 0 0 10px 0; color: #1565C0; font-weight: 600; font-size: 15px;">📞 ¿Necesitas Ayuda?</p>
        <p style="margin: 8px 0; color: #1976D2; font-size: 14px;">
            Si tienes problemas para acceder o necesitas asistencia técnica:
        </p>
        <p style="margin: 8px 0; color: #1976D2; font-size: 14px;">
            • Teléfono: <a href="tel:+18297405073" style="color: #2196F3; text-decoration: none; font-weight: 600;">829-740-5073</a>
        </p>
        <p style="margin: 8px 0; color: #1976D2; font-size: 14px;">
            • Email: <a href="mailto:dra.ramirezr@gmail.com" style="color: #2196F3; text-decoration: none; font-weight: 600;">dra.ramirezr@gmail.com</a>
        </p>
    </div>
    
    <div style="margin-top: 25px; padding-top: 20px; border-top: 2px solid #F2E2E6;">
        <p style="color: #999; font-size: 13px; line-height: 1.5; margin: 0;">
            <strong>Enlace directo al sistema:</strong><br>
            <a href="{link_admin}" style="color: #CEB0B7; word-break: break-all; font-size: 13px; font-weight: 600;">{link_admin}</a>
        </p>
    </div>
    """
    
    return get_base_template("🎉", f"Bienvenido al Sistema de Facturación - {nombre}", content)

def template_nueva_contrasena(nombre, email, password_temporal):
    """
    Template para notificar al usuario que su contraseña ha sido cambiada (VERSIÓN CORTA)
    Args:
        nombre: Nombre completo del usuario
        email: Email del usuario
        password_temporal: Nueva contraseña temporal generada
    """
    content = f"""
    <div style="text-align: center; padding: 20px;">
        <div style="background: linear-gradient(135deg, #FFC107 0%, #FF9800 100%); width: 80px; height: 80px; border-radius: 50%; margin: 0 auto 20px auto; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(255, 152, 0, 0.3);">
            <span style="font-size: 40px;">🔐</span>
        </div>
        <h2 style="color: #282828; font-size: 24px; margin: 15px 0;">
            Nueva Contraseña Temporal
        </h2>
        <p style="color: #666; font-size: 16px; margin: 10px 0;">
            Hola <strong>{nombre}</strong>, tu contraseña ha sido cambiada.
        </p>
    </div>
    
    <div style="background: #F5F5F5; padding: 25px; border-radius: 12px; margin: 20px 0; border: 2px solid #E0E0E0;">
        <p style="margin: 0 0 10px 0; color: #666; font-size: 14px; text-align: center;">
            📧 <strong>Email:</strong> {email}
        </p>
        <p style="margin: 15px 0; color: #666; font-size: 14px; text-align: center;">
            🔑 <strong>Contraseña Temporal:</strong>
        </p>
        <div style="background: #FFECB3; padding: 20px; border-radius: 10px; text-align: center; font-family: 'Courier New', monospace; font-size: 24px; font-weight: 700; color: #F57C00; border: 3px solid #FFA726;">
            {password_temporal}
        </div>
    </div>
    
    <div style="text-align: center; margin: 25px 0;">
        <a href="https://sitio-web-medico-shirley-production.up.railway.app/login" 
           style="display: inline-block; background: #4CAF50; color: white; padding: 16px 50px; text-decoration: none; border-radius: 30px; font-weight: 700; font-size: 18px; box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);">
            🔓 Iniciar Sesión
        </a>
    </div>
    
    <div style="background-color: #FFF3E0; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #FF9800;">
        <p style="margin: 0 0 10px 0; color: #E65100; font-weight: 700; font-size: 16px;">⚠️ Importante:</p>
        <p style="margin: 8px 0; color: #EF6C00; font-size: 14px; line-height: 1.8;">
            • Esta contraseña es <strong>TEMPORAL</strong><br>
            • Debes cambiarla al iniciar sesión<br>
            • El sistema te lo pedirá automáticamente
        </p>
    </div>
    
    <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #2196F3;">
        <p style="margin: 0 0 10px 0; color: #1565C0; font-weight: 700; font-size: 16px;">📞 ¿Necesitas ayuda?</p>
        <p style="margin: 8px 0; color: #1976D2; font-size: 14px;">
            Teléfono: <a href="tel:+18297405073" style="color: #2196F3; text-decoration: none; font-weight: 600;">829-740-5073</a><br>
            Email: <a href="mailto:dra.ramirezr@gmail.com" style="color: #2196F3; text-decoration: none; font-weight: 600;">dra.ramirezr@gmail.com</a>
        </p>
    </div>
    """
    
    return get_base_template("🔐", f"Nueva Contraseña Temporal - {nombre}", content)

# Exportar funciones
__all__ = [
    'template_contacto',
    'template_cita',
    'template_recuperacion',
    'template_constancia_pdf',
    'template_factura',
    'template_confirmacion_cita',
    'template_bienvenida_facturacion',
    'template_nueva_contrasena'
]

