from odoo import models, fields, api

class Usuario(models.Model):
    _inherit = 'res.users'

    # Campo para indicar si el usuario está activo
    active = fields.Boolean(string="Activo", default=True)

    @api.model
    def action_inhabilitar(self):
        for usuario in self:
            usuario.active = False
        return False

    @api.model
    def action_habilitar(self):
        for usuario in self:
            usuario.active = True
        return True

    @api.model
    def crear_usuario(self, vals):
        nuevo_usuario = self.create(vals)
        return nuevo_usuario

    @api.model
    def editar_usuario(self, user_id, vals):
        usuario = self.browse(user_id)
        if usuario:
            usuario.write(vals)
        return usuario

    @api.model
    def eliminar_usuario(self, user_id):
        # Esta función ahora está deshabilitada para no eliminar usuarios
        raise Exception("No se puede eliminar el usuario, solo se puede inhabilitar.")
