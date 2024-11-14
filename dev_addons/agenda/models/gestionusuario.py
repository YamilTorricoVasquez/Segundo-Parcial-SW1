from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class GestionUsuario(models.Model):
    _name = 'agenda.gestion.usuario'
    _description = 'Gestión de Usuarios para Administrativos'

    name = fields.Char(string="Nombre", required=True)
    email = fields.Char(string="Correo Electrónico", required=True)
    phone = fields.Char(string="Teléfono")
    ci = fields.Char(string="CI", required=True)
    user_id = fields.Many2one('res.users', string="Usuario")

    # Campo para seleccionar el rol con todos los roles disponibles
    role_id = fields.Many2one(
        'res.groups', 
        string="Rol de Usuario", 
        required=True
    )

    @api.model
    def create_user_with_role(self, vals, role):
        """
        Crea un usuario y le asigna solo el grupo especificado, limpiando otros grupos.
        """
        user = self.env['res.users'].create(vals)
        # Quitar todos los grupos asignados automáticamente
        user.groups_id = [(5, 0)]
        # Asignar solo el grupo especificado
        if role:
            user.groups_id = [(4, role.id)]
            # Asignar permisos adicionales si el rol es 'Administrador'
        # Verificar si el rol es 'Administrador'
        if role.name == 'Administrador':
            # Obtener el grupo de creación de contactos
            contacto_group = self.env['res.groups'].sudo().search([('name', '=', 'Permisos de acceso')], limit=1)
            if contacto_group:
                # Asignar el rol de creación de contactos
                user.groups_id =  [(4, contacto_group.id)]
        return user

    @api.model
    def create(self, vals):
        record = super(GestionUsuario, self).create(vals)

        # Creación de usuario con el rol seleccionado
        if record.email:
            user_vals = {
                'name': record.name,
                'login': record.email,
                'email': record.email,
                'phone': record.phone,
                'password': record.ci,  # Usar el CI como contraseña
            }
            user = self.create_user_with_role(user_vals, record.role_id)
            record.user_id = user.id

        return record

    def write(self, vals):
        """
        Actualiza los datos del usuario asociado si se modifican ciertos campos.
        """
        if 'role_id' in vals:
            # Cambiar el rol del usuario si se ha actualizado
            if self.user_id:
                self.user_id.groups_id = [(5, 0)]  # Limpiar grupos existentes
                self.user_id.groups_id = [(4, vals['role_id'])]  # Asignar nuevo rol

        if 'ci' in vals or 'email' in vals or 'name' in vals:
            update_vals = {}
            if 'ci' in vals:
                update_vals['password'] = vals['ci']
            if 'email' in vals:
                update_vals['login'] = vals['email']
                update_vals['email'] = vals['email']
            if 'name' in vals:
                update_vals['name'] = vals['name']
            if self.user_id:
                self.user_id.write(update_vals)
            else:
                _logger.warning(f"No se encontró usuario asociado para {self.name}")

        return super(GestionUsuario, self).write(vals)
