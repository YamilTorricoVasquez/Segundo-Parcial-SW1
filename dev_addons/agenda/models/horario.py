from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Horario(models.Model):
    _name = 'agenda.horario'
    _description = 'Horario'

    materia_id = fields.Many2one('agenda.materia', string='Materia', required=True)
    dia = fields.Selection([
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo')
    ], string='Día', required=True)

    HORA_OPTIONS = [(str(i), f"{i}:00") for i in range(8, 22)]  # Horas de 8 AM a 9 PM
    
    hora_inicio = fields.Selection(HORA_OPTIONS, string='Hora de Inicio', required=True)
    hora_fin = fields.Selection(HORA_OPTIONS, string='Hora de Fin', required=True)

    @api.constrains('materia_id', 'dia', 'hora_inicio', 'hora_fin')
    def _check_unique_horario(self):
        for record in self:
            # Buscar si ya existe otro horario con la misma materia, día y horario
            existing_horario = self.search([
                ('id', '!=', record.id),  # Excluir el registro actual
                ('materia_id', '=', record.materia_id.id),
                ('dia', '=', record.dia),
                ('hora_inicio', '=', record.hora_inicio),
                ('hora_fin', '=', record.hora_fin)
            ])
            if existing_horario:
                raise ValidationError('Ya existe un horario para esta materia en el mismo día y horas.')

    @api.constrains('hora_inicio', 'hora_fin')
    def _check_hora_fin_mayor_inicio(self):
        for record in self:
            if int(record.hora_fin) <= int(record.hora_inicio):
                raise ValidationError('La hora de fin debe ser mayor que la hora de inicio.')
