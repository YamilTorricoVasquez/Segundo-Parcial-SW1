from odoo import models, fields, api


class Curso(models.Model):
    _name = 'agenda.curso'
    _description = 'Curso'

    name = fields.Char(string='Nombre del curso', required=True)
   
    _sql_constraints = [
        ('name_curso_unique', 'UNIQUE(name)', 'No puede duplicar el nombre del curso.')
    ]
