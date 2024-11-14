from odoo import models, fields, api


class Materia(models.Model):
    _name = 'agenda.materia'
    _description = 'Materia'

    name = fields.Char(string='Nombre de la materia', required=True)
   
    _sql_constraints = [
        ('name_curso_unique', 'UNIQUE(name)', 'No puede duplicar el nombre del curso.')
    ]
