from odoo import models, fields, api

class Paralelo(models.Model):
    _name = 'agenda.paralelo'
    _description = 'Paralelo'

    name = fields.Char(string='Paralelo', required=True,size=1)

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.name = self.name.upper()

    @api.model
    def create(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()  # Convertir a mayúsculas
        return super(Paralelo, self).create(vals)

    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()  # Convertir a mayúsculas
        return super(Paralelo, self).write(vals)

    _sql_constraints = [
        ('name_paralelo_unique', 'UNIQUE(name)', 'Solo puede existir un paralelo con ese nombre.')
    ]
