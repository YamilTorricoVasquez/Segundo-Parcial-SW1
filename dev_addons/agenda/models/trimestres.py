from odoo import models, fields, api


class Trimestre(models.Model):
    _name = 'agenda.trimestre'
    _description = 'Nivel'

    name = fields.Char(string='Trimestre', required=True)
    fecha = fields.Date(string = 'Fecha de entrega', required=True)
    _sql_constraints = [
        ('name_nivel_unique', 'UNIQUE(name)', 'Solo puede existir un solo trimestre.')
    ]
