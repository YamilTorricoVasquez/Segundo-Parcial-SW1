from odoo import models, fields

class Asistencia(models.Model):
    _name = 'agenda.asistencia'
    _description = 'Registro de Asistencia'

    estudiante_id = fields.Many2one('agenda.estudiante', string='Estudiante', required=True)
    profesor_id = fields.Many2one('agenda.profesor', string='Profesor', required=True)  # Agregar este campo
    curso_id = fields.Many2one('agenda.curso', string='Curso', required=True)
    nivel_id = fields.Many2one('agenda.nivel', string='Nivel', required=True)
    estado = fields.Selection([('presente', 'Presente'), ('ausente', 'Ausente')], string='Estado', required=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.today, required=True)  # Se establece la fecha por defecto
