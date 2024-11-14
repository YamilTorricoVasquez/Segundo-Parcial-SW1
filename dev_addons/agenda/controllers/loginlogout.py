from odoo import http
from odoo.http import request
import json
import logging
from datetime import datetime


_logger = logging.getLogger(__name__)

class LoginAPI(http.Controller):
    @http.route('/api/login', type='http', auth='none', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        try:
            # Obtener el cuerpo de la solicitud POST
            data = json.loads(request.httprequest.data)

            # Obtener el correo y la contraseña desde el cuerpo de la solicitud
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return request.make_response(
                    json.dumps({'error': 'Faltan datos requeridos.'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Intentar autenticar al usuario
            uid = request.session.authenticate(request.env.cr.dbname, email, password)

            if uid:
                user = request.env['res.users'].sudo().browse(uid)
                   # Obtener todos los grupos (roles) del usuario
                roles = user.groups_id.mapped('name')  # Extraer los nombres de los grupos a los que pertenece el usuario
                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'uid': uid,
                        'user_name': user.name,
                        'roles': roles,  # Devolver una lista con los roles del usuario
                    }),
                    headers={'Content-Type': 'application/json'}
                )
            else:
                return request.make_response(
                    json.dumps({'error': 'Login failed'}),
                    headers={'Content-Type': 'application/json'}
                )

        except Exception as e:
            _logger.error(f"Error al iniciar sesión: {str(e)}")
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
    @http.route('/api/comunicados', type='http', auth='public', methods=['GET'], csrf=False)
    def get_comunicados(self, rol=None, usuario_id=None, curso=None, nivel=None, paralelo=None, **kwargs):
        try:
            # Obtener el usuario actual
            user = request.env['res.users'].browse(int(usuario_id)) if usuario_id else request.env.user

            domain = []

            # Si se pasa rol, agregar al dominio
            if rol:
                rol_group = request.env['res.groups'].sudo().search([('name', '=', rol)], limit=1)
                domain.append(('destinatario_ids', 'in', rol_group.id))

            # Agregar curso, nivel y paralelo al dominio si están especificados
            if curso:
                domain.append(('curso_id.name', '=', curso))
            if nivel:
                domain.append(('nivel_id.name', '=', nivel))
            if paralelo:
                domain.append(('paralelo_id.name', '=', paralelo))

            # Buscar los comunicados según el dominio
            comunicados = request.env['agenda.comunicado'].sudo().search(domain)

            # Filtrar comunicados no leídos por el usuario actual
            comunicados_no_leidos = comunicados.filtered(lambda c: user not in c.leido_ids)

            # Marcar como leídos los comunicados no leídos
            for comunicado in comunicados_no_leidos:
                comunicado.leido_ids = [(4, user.id)]  # Añadir usuario a leido_ids

            # Preparar datos para enviar a Flutter, incluyendo el estado de lectura
            comunicados_data = [{
                'id': comunicado.id,
                'name': comunicado.name,
                'descripcion_comunicado': comunicado.descripcion_comunicado,
                'fecha': comunicado.fecha_creacion.isoformat() if comunicado.fecha_creacion else None,  # Convertir a formato ISO
                
                'remitente': {
                    'name': comunicado.remitente_id.name,
                } if comunicado.remitente_id else None,
                'leido': user in comunicado.leido_ids  # Verificar si el usuario ha leído el comunicado
            } for comunicado in comunicados]

            # Enviar la respuesta en formato JSON
            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'comunicados': comunicados_data,
                    'no_leidos': len(comunicados_no_leidos)
                }),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            _logger.error(f"Error al obtener comunicados: {str(e)}")
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
    @http.route('/api/comunicados/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_comunicado(self, **kwargs):
        """
        API para crear un nuevo comunicado.
        """
        try:
            # Obtener datos de entrada
            name = kwargs.get('name')
            descripcion_comunicado = kwargs.get('descripcion_comunicado')
            destinatario_name = kwargs.get('destinatario_name')
            curso_name = kwargs.get('curso_id')
            nivel_name = kwargs.get('nivel_id')
            paralelo_name = kwargs.get('paralelo_id')
            fecha_envio = kwargs.get('fecha_envio')
            enviar_notificacion = kwargs.get('enviar_notificacion', True)
            uid = kwargs.get('uid')  # Obtener el UID del usuario como parámetro

            # Validación de campos requeridos
            if not name or not descripcion_comunicado:
                return {'status': 'error', 'message': 'El nombre y la descripción son obligatorios'}

            # Verificar que se haya pasado un uid
            if not uid:
                return {'status': 'error', 'message': 'El UID del usuario es obligatorio'}

            # Buscar el grupo correspondiente al nombre del destinatario
            destinatario_group = request.env['res.groups'].sudo().search([('name', '=', destinatario_name)], limit=1)
            if not destinatario_group:
                return {'status': 'error', 'message': f'El rol "{destinatario_name}" no existe'}

            # Buscar curso, nivel y paralelo
            curso = request.env['agenda.curso'].sudo().search([('name', '=', curso_name)], limit=1)
            nivel = request.env['agenda.nivel'].sudo().search([('name', '=', nivel_name)], limit=1)
            paralelo = request.env['agenda.paralelo'].sudo().search([('name', '=', paralelo_name)], limit=1)

            # Buscar el usuario por su UID
            user = request.env['res.users'].sudo().browse(uid)
            if not user.exists():
                return {'status': 'error', 'message': 'El usuario no existe'}

            # Crear el comunicado con los IDs correspondientes
            comunicado = request.env['agenda.comunicado'].sudo().create({
                'name': name,
                'descripcion_comunicado': descripcion_comunicado,
                'destinatario_ids': [(6, 0, [destinatario_group.id])],  # Asignar el ID del grupo destinatario
                'curso_id': curso.id if curso else None,
                'nivel_id': nivel.id if nivel else None,
                'paralelo_id': paralelo.id if paralelo else None,
                'fecha_envio': fecha_envio,
                'remitente_id': uid,  # Almacenar el UID del remitente
                'enviar_notificacion': enviar_notificacion,
            })

            # Devolver respuesta de éxito
            return {
                'status': 'success',
                'message': 'Comunicado creado exitosamente',
                'comunicado_id': comunicado.id
            }

        except Exception as e:
            _logger.error(f"Error al crear comunicado: {str(e)}")
            return {
                'status': 'error',
                'message': f'Error al crear comunicado: {str(e)}'
            }





