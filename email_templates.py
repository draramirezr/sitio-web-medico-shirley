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
        <div style="border-top: 2px solid #CEB0B7; padding-top: 20px; margin-bottom: 12px;">
            <p style="color: #6B5C62; font-size: 14px; margin: 6px 0; font-weight: 600;">
                (829) 740-5073 &nbsp;·&nbsp; WhatsApp disponible
            </p>
            <p style="color: #8B7A80; font-size: 13px; margin: 6px 0;">
                Av. Sabana Larga 123, Santo Domingo Este 11901
            </p>
            <p style="color: #8B7A80; font-size: 13px; margin: 6px 0;">
                <a href="https://www.draramirez.com" style="color: #8B5A6B; text-decoration: none;">www.draramirez.com</a>
            </p>
        </div>
        <p style="color: #999; font-size: 11px; margin: 12px 0 0 0; line-height: 1.4;">
            Dra. Shirley Ramírez · Ginecóloga y Obstetra
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
           style="display: inline-block; padding: 14px 35px; background: linear-gradient(135deg, #ACACAD 0%, #949495 100%); color: white !important; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 15px; box-shadow: 0 4px 12px rgba(172, 172, 173, 0.3); margin: 5px;">
            📧 Responder a {nombre}
        </a>
        <a href="https://wa.me/{telefono.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')}?text=Hola%20{nombre.replace(' ', '%20')},%20te%20contacto%20desde%20el%20consultorio%20de%20la%20Dra.%20Shirley%20Ram%C3%ADrez" 
           style="display: inline-block; padding: 14px 35px; background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white !important; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 15px; box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4); margin: 5px;">
            💬 Contactar vía WhatsApp
        </a>
    </div>
    """
    
    return get_base_template("📧", "Nuevo Mensaje de Contacto", content)

def template_cita(nombre, apellido, email, telefono, fecha, hora, tipo, seguro, emergencia, motivo, confirm_url=None, cancel_url=None):
    """Template para emails de citas (notificación a la doctora)"""
    tel_wa = telefono.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    seguro_html = (
        f'<p style="margin: 10px 0; color: #282828; font-size: 15px;">'
        f'<strong style="color: #6B5C62;">Seguro:</strong> {seguro}</p>'
        if seguro else ''
    )
    emergencia_html = (
        f'<p style="margin: 10px 0; color: #D32F2F; font-size: 15px;">'
        f'<strong>Urgencia / emergencia:</strong> {emergencia}</p>'
        if emergencia else ''
    )
    acciones_cita = ''
    if confirm_url or cancel_url:
        confirm_btn = (
            f'''<a href="{confirm_url}"
           style="display: inline-block; padding: 14px 36px; background: #2E7D32; color: white !important; text-decoration: none; border-radius: 28px; font-weight: 600; font-size: 15px; margin: 5px;">
            Confirmar cita
        </a>'''
            if confirm_url else ''
        )
        cancel_btn = (
            f'''<a href="{cancel_url}"
           style="display: inline-block; padding: 14px 28px; background: #fff; color: #C62828 !important; text-decoration: none; border-radius: 28px; font-weight: 600; font-size: 15px; margin: 5px; border: 2px solid #C62828;">
            Cancelar cita
        </a>'''
            if cancel_url else ''
        )
        acciones_cita = f'''
    <div style="text-align: center; margin: 28px 0 8px 0; padding: 18px; background: #F1F8F2; border-radius: 10px; border: 1px solid #C8E6C9;">
        <p style="margin: 0 0 14px 0; color: #2E7D32; font-size: 14px; font-weight: 600;">
            Puedes confirmar o cancelar esta cita con un clic:
        </p>
        {confirm_btn}
        {cancel_btn}
    </div>
    '''

    content = f"""
    <div style="color: #282828; line-height: 1.7; margin: 10px 0 22px 0; font-size: 15px;">
        <p style="margin: 0 0 12px 0;">Hola Doctora,</p>
        <p style="margin: 0;">
            Tienes una nueva solicitud de cita de
            <strong style="color: #6B5C62;">{nombre} {apellido}</strong>.
            Aquí tienes el resumen para confirmarla o contactarla:
        </p>
    </div>

    <div style="background-color: #F8F4F5; padding: 20px 22px; border-radius: 10px; margin: 18px 0; border: 1px solid #E8D5DA;">
        <p style="margin: 0 0 12px 0; color: #6B5C62; font-weight: 600; font-size: 14px; text-transform: uppercase; letter-spacing: 0.03em;">Paciente</p>
        <p style="margin: 8px 0; color: #282828; font-size: 15px;">
            <strong style="color: #8B7A80;">Nombre:</strong> {nombre} {apellido}
        </p>
        <p style="margin: 8px 0; color: #282828; font-size: 15px;">
            <strong style="color: #8B7A80;">Teléfono:</strong>
            <a href="tel:{telefono}" style="color: #8B5A6B; text-decoration: none; font-weight: 500;">{telefono}</a>
        </p>
        <p style="margin: 8px 0; color: #282828; font-size: 15px;">
            <strong style="color: #8B7A80;">Email:</strong>
            <a href="mailto:{email}" style="color: #8B5A6B; text-decoration: none; font-weight: 500;">{email}</a>
        </p>
    </div>

    <div style="background-color: #FFF8F0; padding: 20px 22px; border-radius: 10px; margin: 18px 0; border-left: 4px solid #CEB0B7;">
        <p style="margin: 0 0 12px 0; color: #6B5C62; font-weight: 600; font-size: 14px; text-transform: uppercase; letter-spacing: 0.03em;">Cita solicitada</p>
        <p style="margin: 8px 0; color: #282828; font-size: 15px;">
            <strong style="color: #8B7A80;">Fecha:</strong> {fecha}
        </p>
        <p style="margin: 8px 0; color: #282828; font-size: 15px;">
            <strong style="color: #8B7A80;">Hora:</strong> {hora}
        </p>
        <p style="margin: 8px 0; color: #282828; font-size: 15px;">
            <strong style="color: #8B7A80;">Tipo:</strong> {tipo}
        </p>
        {seguro_html}
        {emergencia_html}
    </div>

    <div style="background-color: #fff; padding: 18px 20px; border-left: 4px solid #CEB0B7; margin: 18px 0; border-radius: 4px;">
        <p style="margin: 0 0 8px 0; color: #6B5C62; font-weight: 600; font-size: 14px;">Motivo</p>
        <p style="margin: 0; color: #282828; line-height: 1.7; font-size: 14px; white-space: pre-wrap;">{motivo}</p>
    </div>

    {acciones_cita}

    <div style="text-align: center; margin-top: 20px;">
        <a href="https://wa.me/{tel_wa}?text=Hola%20{nombre}%20{apellido},%20te%20contacto%20desde%20el%20consultorio%20de%20la%20Dra.%20Shirley%20Ram%C3%ADrez%20sobre%20tu%20cita"
           style="display: inline-block; padding: 14px 32px; background: #25D366; color: white !important; text-decoration: none; border-radius: 28px; font-weight: 600; font-size: 15px; margin: 5px;">
            Escribir por WhatsApp
        </a>
        <a href="tel:{telefono}"
           style="display: inline-block; padding: 14px 28px; background: #8B5A6B; color: white !important; text-decoration: none; border-radius: 28px; font-weight: 600; font-size: 15px; margin: 5px;">
            Llamar
        </a>
    </div>
    """

    return get_base_template("", f"Nueva solicitud de cita — {nombre} {apellido}", content)

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
    maps_url = "https://www.google.com/maps/place/Dra.+Shirley+Ramirez/@18.4971899,-69.865084,17z/data=!4m6!3m5!1s0x8eaf89d14db5e76b:0x2a4aedf3ef3c083d!8m2!3d18.4971899!4d-69.865084!16s%2Fg%2F11jzcl6jxk"
    direccion = "Av. Sabana Larga 123, Santo Domingo Este 11901"

    estatus_config = {
        'pending': {
            'color': '#8B5A6B',
            'bg': '#F8F4F5',
            'icon': '',
            'titulo': 'Recibimos tu solicitud',
            'mensaje': (
                '<strong style="color: #6B5C62;">Gracias por confiar en nosotros.</strong><br>'
                'Recibimos tu solicitud de cita. En las próximas horas te confirmamos '
                'la disponibilidad por WhatsApp o llamada.'
            ),
            'accion': (
                '<strong style="color: #6B5C62;">Próximos pasos</strong><br>'
                '1. Revisamos tu solicitud<br>'
                '2. Te confirmamos fecha y hora<br>'
                '3. El día de la cita, llega 10 minutos antes'
            ),
        },
        'confirmed': {
            'color': '#2E7D32',
            'bg': '#E8F5E9',
            'icon': '',
            'titulo': 'Tu cita está confirmada',
            'mensaje': (
                '<strong style="color: #2E7D32;">¡Tu cita está confirmada!</strong> '
                'Gracias por elegirnos. Te esperamos el <strong>{fecha}</strong> '
                'a las <strong>{hora}</strong>.'
            ),
            'accion': (
                'Por favor, llega 10 minutos antes. '
                'Si no puedes asistir, avísanos por WhatsApp para reagendar.'
            ),
        },
        'cancelled': {
            'color': '#C62828',
            'bg': '#FFEBEE',
            'icon': '',
            'titulo': 'Tu cita fue cancelada',
            'mensaje': (
                'Lamentamos informarte que tu cita ha sido <strong>cancelada</strong>. '
                'Si deseas reagendar, escríbenos por WhatsApp o solicita una nueva cita en la web.'
            ),
            'accion': 'Estamos para ayudarte cuando lo necesites.',
        },
        'completed': {
            'color': '#1565C0',
            'bg': '#E3F2FD',
            'icon': '',
            'titulo': 'Gracias por tu visita',
            'mensaje': (
                '<strong style="color: #1565C0;">Gracias por confiar en nosotros.</strong> '
                'Tu cita ha sido completada. Esperamos haberte brindado una excelente atención.'
            ),
            'accion': 'Si tienes alguna pregunta o deseas agendar un seguimiento, contáctanos por WhatsApp.',
        },
    }

    config = estatus_config.get(estatus, estatus_config['pending'])
    mensaje = config['mensaje'].format(fecha=fecha or 'por confirmar', hora=hora or 'por confirmar')
    motivo_html = (
        f'<p style="margin: 10px 0; color: #282828; font-size: 15px;">'
        f'<strong style="color: #8B7A80;">Motivo:</strong> {motivo}</p>'
        if motivo else ''
    )

    content = f"""
    <div style="color: #282828; line-height: 1.75; margin: 8px 0 20px 0; font-size: 15px;">
        <p style="margin: 0 0 14px 0;">Hola <strong style="color: #6B5C62;">{nombre} {apellido}</strong>,</p>
        <p style="margin: 0;">
            {mensaje}
        </p>
    </div>

    <div style="background-color: {config['bg']}; padding: 18px 20px; border-radius: 10px; margin: 22px 0; border-left: 4px solid {config['color']};">
        <p style="margin: 0; color: {config['color']}; font-weight: 700; font-size: 17px;">
            {config['titulo']}
        </p>
    </div>

    <div style="background-color: #F8F4F5; padding: 20px 22px; border-radius: 10px; margin: 20px 0;">
        <p style="margin: 0 0 12px 0; color: #6B5C62; font-weight: 600; font-size: 14px; text-transform: uppercase; letter-spacing: 0.03em;">
            Detalles de tu solicitud
        </p>
        <p style="margin: 8px 0; color: #282828; font-size: 15px;">
            <strong style="color: #8B7A80;">Fecha:</strong> {fecha if fecha else 'Por confirmar'}
        </p>
        <p style="margin: 8px 0; color: #282828; font-size: 15px;">
            <strong style="color: #8B7A80;">Hora:</strong> {hora if hora else 'Por confirmar'}
        </p>
        <p style="margin: 8px 0; color: #282828; font-size: 15px;">
            <strong style="color: #8B7A80;">Tipo:</strong> {tipo}
        </p>
        {motivo_html}
    </div>

    <div style="background-color: #fff; padding: 18px 20px; border-left: 4px solid {config['color']}; margin: 20px 0; border-radius: 4px;">
        <p style="margin: 0; color: #282828; line-height: 1.7; font-size: 14px;">
            {config['accion']}
        </p>
    </div>

    <div style="background-color: #F8F4F5; padding: 18px 20px; border-radius: 10px; margin: 22px 0;">
        <p style="margin: 0 0 8px 0; color: #6B5C62; font-weight: 600; font-size: 14px;">Consultorio</p>
        <p style="margin: 0 0 10px 0; color: #282828; font-size: 14px; line-height: 1.5;">
            {direccion}
        </p>
        <a href="{maps_url}"
           style="color: #8B5A6B; font-size: 14px; font-weight: 600; text-decoration: none;">
            Ver ubicación en Google Maps →
        </a>
    </div>

    <div style="text-align: center; margin-top: 28px;">
        <a href="https://wa.me/18297405073?text=Hola%2C%20necesito%20ayuda%20con%20mi%20cita"
           style="display: inline-block; padding: 14px 36px; background: #25D366; color: white !important; text-decoration: none; border-radius: 28px; font-weight: 600; font-size: 15px; margin: 5px;">
            WhatsApp
        </a>
        <a href="tel:+18297405073"
           style="display: inline-block; padding: 14px 28px; background: #CEB0B7; color: white !important; text-decoration: none; border-radius: 28px; font-weight: 600; font-size: 15px; margin: 5px;">
            Llamar (829) 740-5073
        </a>
    </div>
    """

    return get_base_template(config['icon'], config['titulo'], content)


def template_recordatorio_anual(nombre, apellido, fecha_ultima, cita_url, unsubscribe_url, es_extra=False):
    """Recordatorio anual de chequeo rutinario (solo pacientes con opt-in)."""
    if es_extra:
        cuerpo = f"""
        <p style="margin: 0 0 14px 0;">
            <strong style="color: #6B5C62;">Solo un recordatorio amable.</strong>
            Hace un tiempo te escribimos sobre tu chequeo rutinario
            (última cita el <strong>{fecha_ultima}</strong>).
        </p>
        <p style="margin: 0;">
            Si ya agendaste o no deseas este control ahora, puedes ignorar este mensaje
            o cancelar los recordatorios abajo. Si quieres venir, estamos para ayudarte.
        </p>
        """
        titulo = "Un recordatorio amable"
    else:
        cuerpo = f"""
        <p style="margin: 0 0 14px 0;">
            <strong style="color: #6B5C62;">Gracias por confiar en nosotros.</strong>
            Según nuestros registros, tu última cita fue el
            <strong>{fecha_ultima}</strong>.
        </p>
        <p style="margin: 0;">
            En ginecología, el chequeo rutinario suele corresponder cerca de un año después.
            Si deseas agendar tu control, estamos para ayudarte.
        </p>
        """
        titulo = "Recordatorio de chequeo anual"

    content = f"""
    <div style="color: #282828; line-height: 1.75; margin: 8px 0 20px 0; font-size: 15px;">
        <p style="margin: 0 0 14px 0;">Hola <strong style="color: #6B5C62;">{nombre} {apellido}</strong>,</p>
        {cuerpo}
    </div>

    <div style="background-color: #F8F4F5; padding: 20px 22px; border-radius: 10px; margin: 22px 0; border-left: 4px solid #CEB0B7;">
        <p style="margin: 0; color: #6B5C62; font-weight: 600; font-size: 15px; line-height: 1.6;">
            Este es solo un recordatorio de prevención. No reemplaza una evaluación médica
            y no implica que tengas un problema de salud.
        </p>
    </div>

    <div style="text-align: center; margin-top: 28px;">
        <a href="{cita_url}"
           style="display: inline-block; padding: 14px 36px; background: #8B5A6B; color: white !important; text-decoration: none; border-radius: 28px; font-weight: 600; font-size: 15px; margin: 5px;">
            Solicitar cita
        </a>
        <a href="https://wa.me/18297405073?text=Hola%2C%20me%20gustar%C3%ADa%20agendar%20mi%20chequeo%20rutinario"
           style="display: inline-block; padding: 14px 32px; background: #25D366; color: white !important; text-decoration: none; border-radius: 28px; font-weight: 600; font-size: 15px; margin: 5px;">
            WhatsApp
        </a>
    </div>

    <div style="margin-top: 32px; padding-top: 18px; border-top: 1px solid #E8D5DA; text-align: center;">
        <p style="margin: 0; color: #999; font-size: 12px; line-height: 1.5;">
            Recibes este correo porque aceptaste recordatorios anuales al solicitar una cita.<br>
            <a href="{unsubscribe_url}" style="color: #8B7A80; text-decoration: underline;">
                Cancelar recordatorios anuales
            </a>
        </p>
    </div>
    """
    return get_base_template("", titulo, content)


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

