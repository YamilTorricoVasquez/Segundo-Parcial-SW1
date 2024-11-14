from odoo import models, fields, api


class Nivel(models.Model):
    _name = 'agenda.nivel'
    _description = 'Nivel'

    name = fields.Char(string='Nivel', required=True)
   
    _sql_constraints = [
        ('name_nivel_unique', 'UNIQUE(name)', 'Solo puede existir un solo nivel.')
    ]
