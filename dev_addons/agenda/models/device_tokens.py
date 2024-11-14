from odoo import models, fields, api

class DeviceToken(models.Model):
    _name = 'device.token'
    _description = 'Token de Dispositivo'

    user_id = fields.Many2one('res.users', string='Usuario', required=True)
    token = fields.Char(string='Token del Dispositivo', required=True)
