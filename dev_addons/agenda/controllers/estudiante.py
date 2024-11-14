from odoo import http
from odoo.http import request
import logging
import json
from datetime import datetime
# Definir el logger
_logger = logging.getLogger(__name__)

class EstudianteController(http.Controller):

    
    @http.route('/api/estudiante/info/<string:email>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_estudiante_informacion(self, email, **kwargs):
        try:
            # Buscar al estudiante por su CI
            estudiante = request.env['agenda.estudiante'].sudo().search([('email', '=', email)], limit=1)
            if not estudiante:
                return request.make_response(
                    json.dumps({'error': 'Estudiante no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )
            
            _logger.info(f"Estudiante encontrado: {estudiante.name}")

            # Preparar la información del estudiante y su curso
            get_estudiante_informacion = {
                'nombre': estudiante.name,
                'ci': estudiante.ci,
               # 'email': estudiante.email,
                #'telefono': estudiante.phone,
                'curso': estudiante.curso_id.name if estudiante.curso_id else None,
                'nivel': estudiante.nivel_id.name if estudiante.nivel_id else None,
                'paralelo': estudiante.paralelo_id.name if estudiante.paralelo_id else None,
                #'tutor': estudiante.tutor_id,
                #'ci_tutor': estudiante.ci_tutor,
                # Convertir el campo 'gestion' a cadena
               # 'gestion': estudiante.gestion.strftime('%Y-%m-%d') if estudiante.gestion else None
            }

            # Retornar la información del estudiante
            return request.make_response(
                json.dumps(get_estudiante_informacion),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            _logger.error(f"Error al procesar la solicitud: {str(e)}")
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
    @http.route('/api/estudiante/informacion/<string:email_tutor>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_estudiante_info(self, email_tutor, **kwargs):
        try:
            # Buscar al estudiante por su CI
            estudiante = request.env['agenda.estudiante'].sudo().search([('email_tutor', '=', email_tutor)], limit=1)
            if not estudiante:
                return request.make_response(
                    json.dumps({'error': 'Estudiante no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )
            
            _logger.info(f"Estudiante encontrado: {estudiante.name}")

            # Preparar la información del estudiante y su curso
            get_estudiante_info = {
                #'nombre': estudiante.name,
                'ci': estudiante.ci,
               # 'email': estudiante.email,
                #'telefono': estudiante.phone,
                #'curso': estudiante.curso_id.name if estudiante.curso_id else None,
                #'nivel': estudiante.nivel_id.name if estudiante.nivel_id else None,
                #'paralelo': estudiante.paralelo_id.name if estudiante.paralelo_id else None,
                #'tutor': estudiante.tutor_id,
                #'ci_tutor': estudiante.ci_tutor,
                # Convertir el campo 'gestion' a cadena
               # 'gestion': estudiante.gestion.strftime('%Y-%m-%d') if estudiante.gestion else None
            }

            # Retornar la información del estudiante
            return request.make_response(
                json.dumps(get_estudiante_info),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            _logger.error(f"Error al procesar la solicitud: {str(e)}")
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
            
    @http.route('/api/estudiante/asistencia', type='http', auth='public', methods=['POST'], csrf=False)
    def registrar_asistencia(self, **kwargs):
        try:
            # Obtener el cuerpo de la solicitud POST
            data = json.loads(request.httprequest.data)

            # Obtener el CI del estudiante, el estado de asistencia y el CI del profesor desde el cuerpo de la solicitud
            ci_estudiante = data.get('ci')
            estado_asistencia = data.get('estado')  # 'Presente' o 'Ausente'
            ci_profesor = data.get('ci_profesor')  # CI del profesor que toma la asistencia

            if not ci_estudiante or not estado_asistencia or not ci_profesor:
                return request.make_response(
                    json.dumps({'error': 'Faltan datos requeridos.'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Buscar al estudiante por su CI
            estudiante = request.env['agenda.estudiante'].sudo().search([('ci', '=', ci_estudiante)], limit=1)
            if not estudiante:
                return request.make_response(
                    json.dumps({'error': 'Estudiante no encontrado.'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Buscar al profesor por su CI
            profesor = request.env['agenda.profesor'].sudo().search([('ci', '=', ci_profesor)], limit=1)
            if not profesor:
                return request.make_response(
                    json.dumps({'error': 'Profesor no encontrado.'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Obtener curso y nivel asignados al estudiante
            curso_id = estudiante.curso_id.id
            nivel_id = estudiante.nivel_id.id

            if not curso_id or not nivel_id:
                return request.make_response(
                    json.dumps({'error': 'El estudiante no está asignado a un curso o nivel.'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Obtener la fecha actual
            fecha_actual = datetime.now().date()

            # Verificar si ya existe un registro de asistencia para hoy por ese profesor
            asistencia_existente = request.env['agenda.asistencia'].sudo().search([
                ('estudiante_id', '=', estudiante.id),
                ('curso_id', '=', curso_id),
                ('nivel_id', '=', nivel_id),
                ('profesor_id', '=', profesor.id),  # Verifica por el profesor que registra
                ('fecha', '=', fecha_actual)
            ], limit=1)

            if asistencia_existente:
                return request.make_response(
                    json.dumps({'error': 'La asistencia ya ha sido registrada para hoy por este profesor.'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Crear un registro de asistencia
            request.env['agenda.asistencia'].sudo().create({
                'estudiante_id': estudiante.id,
                'curso_id': curso_id,
                'nivel_id': nivel_id,
                'profesor_id': profesor.id,  # Relacionar la asistencia con el profesor
                'estado': estado_asistencia,
                'fecha': fecha_actual
            })

            return request.make_response(
                json.dumps({'success': 'Asistencia registrada correctamente.'}),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            _logger.error(f"Error al registrar asistencia: {str(e)}")
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
    @http.route('/api/estudiante/notas/<string:ci>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_notas_estudiante(self, ci, **kwargs):
        try:
            # Buscar al estudiante por su CI
            estudiante = request.env['agenda.estudiante'].sudo().search([('ci', '=', ci)], limit=1)
            if not estudiante:
                return request.make_response(
                    json.dumps({'error': 'Estudiante no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )

            _logger.info(f"Estudiante encontrado: {estudiante.name}")

            # Obtener todas las notas del estudiante
            notas = request.env['agenda.boletin'].sudo().search([('estudiante_id', '=', estudiante.id)])
            if not notas:
                return request.make_response(
                    json.dumps({'error': 'No se encontraron notas para el estudiante'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Preparar los datos de las notas en formato JSON
            notas_info = {}
            for nota in notas:
                trimestre = nota.trimestre_id.name if nota.trimestre_id else 'Desconocido'
                nota_data = {
                    'curso': nota.curso_id.name if nota.curso_id else None,
                    'nivel': nota.nivel_id.name if nota.nivel_id else None,
                    'paralelo': nota.paralelo_id.name if nota.paralelo_id else None,
                    'materia': nota.materia_id.name if nota.materia_id else None,
                    'nota': nota.nota,
                    'fecha_entrega': nota.fecha_id.strftime('%Y-%m-%d') if nota.fecha_id else None
                }

                # Agrupar notas por trimestre
                if trimestre not in notas_info:
                    notas_info[trimestre] = []
                notas_info[trimestre].append(nota_data)

            # Retornar la información de las notas
            return request.make_response(
                json.dumps({'notas': notas_info}),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            _logger.error(f"Error al procesar la solicitud: {str(e)}")
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
    @http.route('/api/estudiante/horario/<string:nombre_curso>/<string:nombre_nivel>/<string:nombre_paralelo>', 
                type='http', auth='public', methods=['GET'], csrf=False)
    def get_horario_by_curso_nivel(self, nombre_curso, nombre_nivel, nombre_paralelo, **kwargs):
        try:
            # Buscar el curso por su nombre
            curso = request.env['agenda.curso'].sudo().search([('name', '=', nombre_curso)], limit=1)
            if not curso:
                return request.make_response(
                    json.dumps({'error': 'Curso no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Buscar el nivel por su nombre
            nivel = request.env['agenda.nivel'].sudo().search([('name', '=', nombre_nivel)], limit=1)
            if not nivel:
                return request.make_response(
                    json.dumps({'error': 'Nivel no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Buscar el paralelo por su nombre
            paralelo = request.env['agenda.paralelo'].sudo().search([('name', '=', nombre_paralelo)], limit=1)
            if not paralelo:
                return request.make_response(
                    json.dumps({'error': 'Paralelo no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )

            _logger.info(f"Curso encontrado: {curso.name}, Nivel encontrado: {nivel.name}, Paralelo encontrado: {paralelo.name}")

            # Obtener el horario relacionado
            curso_nivel = request.env['agenda.curso.nivel'].sudo().search([
                ('curso_id', '=', curso.name),
                ('nivel_id', '=', nivel.name),
                ('paralelo_id', '=', paralelo.name)
            ], limit=1)

            if not curso_nivel:
                return request.make_response(
                    json.dumps({'error': 'No se encontró la relación entre curso, nivel y paralelo'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Obtener horarios
            horarios = curso_nivel.horario_id

            # Recopilar la información de los horarios
            horarios_info = []
            for horario in horarios:
                horarios_info.append({
                    'dia':horario.dia,
                    'materia_id': horario.materia_id.name,
                    'hora_inicio': horario.hora_inicio,
                    'hora_fin': horario.hora_fin,
                })

            # Retornar la lista de horarios
            return request.make_response(
                json.dumps(horarios_info),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            _logger.error(f"Error al procesar la solicitud: {str(e)}")
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )