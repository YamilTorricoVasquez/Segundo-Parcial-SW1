from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Profesor(models.Model):
    _name = 'agenda.profesor'
    _description = 'Profesor'

    name = fields.Char(string='Nombre completo', required=True)
    ci = fields.Char(string='Cédula de identidad', required=True, size=7)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Teléfono', size=8)
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento', required=True)

    # Relación Many2many con el modelo intermedio
    cursos_niveles_ids = fields.Many2many('agenda.curso.nivel', string='Cursos asignados')

    # Relación Many2one con res.users para asociar la cuenta de usuario
    user_id = fields.Many2one('res.users', string='Cuenta de usuario')

    @api.model
    def create(self, vals):
        profesor = super(Profesor, self).create(vals)

        # Creación de cuenta y asignación de grupo para el profesor
        if profesor.email:
            password = profesor.ci  # Usar el CI como contraseña
            user_vals = {
                'name': profesor.name,
                'login': profesor.email,
                'email': profesor.email,
                'phone': profesor.phone,
                'password': password,
            }
            user = self.env['res.users'].create(user_vals)

            # Asignación de grupo específico para el profesor
            profesor_group = self.env.ref('agenda.group_profesor')  # Cambia esto por el nombre correcto del grupo de profesores
            if profesor_group:
                user.groups_id = [(4, profesor_group.id)]
            profesor.user_id = user.id

        return profesor

    def write(self, vals):
        # Verificar si se está actualizando el CI o email del profesor
        if 'ci' in vals or 'email' in vals or 'name' in vals:
            if 'ci' in vals:
                new_ci = vals.get('ci')
                _logger.info(f"Nuevo CI del profesor detectado: {new_ci}")
            if 'email' in vals:
                new_email = vals.get('email')
                _logger.info(f"Nuevo email del profesor detectado: {new_email}")
            if 'name' in vals:
                new_name = vals.get('name')
                _logger.info(f"Nuevo nombre del profesor detectado: {new_name}")

            # Actualizar la información de usuario del profesor
            if self.user_id:
                update_vals = {}
                if 'ci' in vals:
                    update_vals['password'] = new_ci  # Actualizar contraseña al nuevo CI
                if 'email' in vals:
                    update_vals['login'] = new_email
                    update_vals['email'] = new_email
                if 'name' in vals:  # Actualizar el nombre del usuario
                    update_vals['name'] = new_name
                self.user_id.write(update_vals)
            else:
                _logger.warning(f"No se encontró usuario asociado para el profesor {self.name}")

        # Llamar al método write original para actualizar el resto de los campos en el modelo
        return super(Profesor, self).write(vals)
