from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CursoNivel(models.Model):
    _name = 'agenda.curso.nivel'
    _description = 'Relación entre Profesores, Cursos y Niveles'

    curso_id = fields.Many2one('agenda.curso', string='Curso', required=True)
    nivel_id = fields.Many2one('agenda.nivel', string='Nivel', required=True)
    paralelo_id = fields.Many2one('agenda.paralelo', string='Paralelo', required=True)

    # Relación Many2many con el modelo intermedio
   # materia_id = fields.Many2many('agenda.materia', string='Materias asignadas')
    horario_id = fields.Many2many('agenda.horario',string = 'horario asignado')
    _sql_constraints = [
        ('unique_curso_nivel_paralelo', 'UNIQUE(curso_id, nivel_id, paralelo_id)', 
         'La combinación de curso, nivel y paralelo ya existe.')
    ] 

    @api.model
    def create(self, vals):
        # Verifica si ya existe una combinación
        existing_record = self.search([
            ('curso_id', '=', vals.get('curso_id')),
            ('nivel_id', '=', vals.get('nivel_id')),
            ('paralelo_id', '=', vals.get('paralelo_id')),
        ], limit=1)

        if existing_record:
            raise ValidationError('La combinación de curso, nivel y paralelo ya existe.')

        return super(CursoNivel, self).create(vals)
