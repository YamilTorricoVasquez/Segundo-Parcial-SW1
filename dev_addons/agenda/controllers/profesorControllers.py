from odoo import http
from odoo.http import request
import logging
import json

# Definir el logger
_logger = logging.getLogger(__name__)

class ProfesorController(http.Controller):

    @http.route('/api/profesor/informacion/<string:email>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_profesor_info(self, email, **kwargs):
        try:
            # Buscar al profesor por su email
            profesor = request.env['agenda.profesor'].sudo().search([('email', '=', email)], limit=1)
            if not profesor:
                return request.make_response(
                    json.dumps({'error': 'Profesor no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )
            
            _logger.info(f"Profesor encontrado: {profesor.name}")

            # Preparar la información del profesor
            profesor_info = {
                'nombre': profesor.name,
                'ci': profesor.ci,
                'email': profesor.email,
                'telefono': profesor.phone,
                'fecha_nacimiento': profesor.fecha_nacimiento.strftime('%Y-%m-%d') if profesor.fecha_nacimiento else None,
            }

            # Retornar la información del profesor
            return request.make_response(
                json.dumps(profesor_info),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            _logger.error(f"Error al procesar la solicitud: {str(e)}")
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
            #trae informacion de los cursos asignados a cada profesor
    @http.route('/api/profesor/cursos/horario/<string:email>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_profesor_materias_horario(self, email, **kwargs):
        try:
            # Buscar al profesor por su email
            profesor = request.env['agenda.profesor'].sudo().search([('email', '=', email)], limit=1)
            if not profesor:
                return request.make_response(
                    json.dumps({'error': 'Profesor no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )

            _logger.info(f"Profesor encontrado: {profesor.name}")

            # Preparar la información de las materias asignadas
            materias_asignadas = []
            for curso_nivel in profesor.cursos_niveles_ids:
                curso = curso_nivel.curso_id  # Acceder al curso relacionado
                nivel = curso_nivel.nivel_id
                paralelo = curso_nivel.paralelo_id
                
                # Recorrer los horarios asignados a la materia
                horarios = []
                for horario in curso_nivel.horario_id:  # Aquí accedes a los horarios asignados
                      # Acceder a la materia asociada al horario
                    materia = horario.materia_id  # Obtener la materia asociada al horario
                    horarios.append({
                        'dia': horario.dia,
                        'materia': materia.name if materia else 'No asignada',  # Mostrar el nombre de la materia
                        'hora_inicio': horario.hora_inicio,
                        'hora_fin': horario.hora_fin,
                        
                        # Si tienes un campo de profesor relacionado, puedes agregarlo también
                       # 'profesor': horario.materia_id.profesor_id.name if horario.materia_id.profesor_id else 'No asignado'
                    })

                # Añadir la información de la materia y los horarios
                materias_asignadas.append({
                    'curso': curso.name,
                    'nivel': nivel.name,
                    'paralelo': paralelo.name,
                    'horarios': horarios  # Añadir lista de horarios
                })

            # Retornar la información de las materias
            return request.make_response(
                json.dumps({'cursos_asignados': materias_asignadas}),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            _logger.error(f"Error al procesar la solicitud: {str(e)}")
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
    @http.route('/api/profesor/cursos/<string:email>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_profesor_materias(self, email, **kwargs):
        try:
            # Buscar al profesor por su email
            profesor = request.env['agenda.profesor'].sudo().search([('email', '=', email)], limit=1)
            if not profesor:
                return request.make_response(
                    json.dumps({'error': 'Profesor no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )

            _logger.info(f"Profesor encontrado: {profesor.name}")

            # Preparar la información de las materias asignadas
            materias_asignadas = []
            for curso_nivel in profesor.cursos_niveles_ids:
                curso = curso_nivel.curso_id  # Acceder al curso relacionado
                nivel = curso_nivel.nivel_id
                paralelo = curso_nivel.paralelo_id
                
                # Recorrer los horarios asignados a la materia
                horarios = []
                for horario in curso_nivel.horario_id:  # Aquí accedes a los horarios asignados
                      # Acceder a la materia asociada al horario
                    materia = horario.materia_id  # Obtener la materia asociada al horario
                    horarios.append({
                        'dia': horario.dia,
                        'materia': materia.name if materia else 'No asignada',  # Mostrar el nombre de la materia
                        'hora_inicio': horario.hora_inicio,
                        'hora_fin': horario.hora_fin,
                        
                        # Si tienes un campo de profesor relacionado, puedes agregarlo también
                       # 'profesor': horario.materia_id.profesor_id.name if horario.materia_id.profesor_id else 'No asignado'
                    })

                # Añadir la información de la materia y los horarios
                materias_asignadas.append({
                    'curso': curso.name,
                    'nivel': nivel.name,
                    'paralelo': paralelo.name
                })

            # Retornar la información de las materias
            return request.make_response(
                json.dumps({'cursos_asignados': materias_asignadas}),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            _logger.error(f"Error al procesar la solicitud: {str(e)}")
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
    
    #api para traer lista de estudiantes
    @http.route('/api/profesor/estudiantes/<string:nombre_curso>/<string:nombre_nivel>/<string:nombre_paralelo>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_estudiantes_by_curso_nivel(self, nombre_curso, nombre_nivel,nombre_paralelo, **kwargs):
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
            if not nivel:
                return request.make_response(
                    json.dumps({'error': 'Nivel no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )
            _logger.info(f"Curso encontrado: {curso.name}, Nivel encontrado: {nivel.name}")

            # Preparar la lista de estudiantes
            estudiantes_info = []

            # Buscar estudiantes por curso , nivel y paralelo
            estudiantes = request.env['agenda.estudiante'].sudo().search([
                ('curso_id', '=', curso.id),
                ('nivel_id', '=', nivel.id),  # Asegúrate de que tu modelo 'agenda.estudiante' tenga el campo 'nivel_id'
                ('paralelo_id', '=', paralelo.id)  # Asegúrate de que tu modelo 'agenda.estudiante' tenga el campo 'paralelo_id'
                
            ])

            # Recopilar la información de los estudiantes
            for est in estudiantes:
                estudiantes_info.append({'nombre': est.name, 'ci': est.ci})

            # Retornar la lista de estudiantes
            return request.make_response(
                json.dumps(estudiantes_info),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            _logger.error(f"Error al procesar la solicitud: {str(e)}")
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )

@http.route('/api/profesor/asistencia', type='http', auth='public', methods=['POST'], csrf=False)
def registrar_asistencia(self, **kwargs):
    try:
        # Obtener el CI del estudiante y el estado de asistencia
        ci_estudiante = kwargs.get('ci')
        estado_asistencia = kwargs.get('estado')  # 'Presente' o 'Ausente'

        if not ci_estudiante or not estado_asistencia:
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

        # Obtener curso y nivel asignados al estudiante
        curso_id = estudiante.curso_id.id
        nivel_id = estudiante.nivel_id.id

        if not curso_id or not nivel_id:
            return request.make_response(
                json.dumps({'error': 'El estudiante no está asignado a un curso o nivel.'}),
                headers={'Content-Type': 'application/json'}
            )

        # Crear un registro de asistencia
        request.env['agenda.asistencia'].sudo().create({
            'estudiante_id': estudiante.id,
            'curso_id': curso_id,
            'nivel_id': nivel_id,
            'estado': estado_asistencia,
            # La fecha se establecerá automáticamente al crear el registro
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

