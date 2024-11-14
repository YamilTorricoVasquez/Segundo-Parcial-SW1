from odoo import models, fields, api, exceptions
import logging

_logger = logging.getLogger(__name__)

class Estudiante(models.Model):
    _name = 'agenda.estudiante'
    _description = 'Estudiante'

    name = fields.Char(string='Nombre completo', required=True)
    ci = fields.Char(string='Cedula de identidad', required=True, size=7)
    email = fields.Char(string='Email')
    email_tutor = fields.Char(string='Email del Tutor')
    phone = fields.Char(string='Teléfono', size=8)
    gestion = fields.Date(string='Año', required=True)
    curso_id = fields.Many2one('agenda.curso', string='Curso', required=True)
    nivel_id = fields.Many2one('agenda.nivel', string='Nivel', required=True)
    paralelo_id = fields.Many2one('agenda.paralelo', string='Paralelo', required=True)
    tutor_id = fields.Char(string='Nombre del tutor', required=True)
    ci_tutor = fields.Char(string='Cedula de identidad tutor', required=True, size=7)
    user_id = fields.Many2one('res.users', string='Cuenta de usuario del estudiante')
    tutor_user_id = fields.Many2one('res.users', string='Cuenta de usuario del tutor')

    @api.model
    def create(self, vals):
        estudiante = super(Estudiante, self).create(vals)

        # Creación de cuenta y asignación de grupo para el estudiante
        if estudiante.email:
            password = estudiante.ci
            user_vals = {
                'name': estudiante.name,
                'login': estudiante.email,
                'email': estudiante.email,
                'phone': estudiante.phone,
                'password': password,
            }
            user = self.env['res.users'].create(user_vals)
         

            # Asignación de grupo específico para el estudiante
            estudiante_group = self.env.ref('agenda.group_estudiante')  # Reemplaza 'agenda.group_estudiante' con el nombre del grupo adecuado para estudiantes
            if estudiante_group:
                user.groups_id = [(4, estudiante_group.id)]
            estudiante.user_id = user.id

        # Creación de cuenta y asignación de grupo para el tutor
        if estudiante.email_tutor and estudiante.ci_tutor:
            tutor_password = estudiante.ci_tutor
            tutor_user_vals = {
                'name': estudiante.tutor_id,
                'login': estudiante.email_tutor,
                'email': estudiante.email_tutor,
                'password': tutor_password,
            }

            # Verificación si el tutor ya tiene una cuenta
            existing_tutor_user = self.env['res.users'].sudo().search([('login', '=', estudiante.email_tutor)], limit=1)
            if not existing_tutor_user:
                tutor_user = self.env['res.users'].create(tutor_user_vals)
                  
                # Asignación de grupo específico para el tutor
                tutor_group = self.env.ref('agenda.group_padre')  # Reemplaza 'agenda.group_tutor' con el nombre del grupo adecuado para tutores
                if tutor_group:
                    tutor_user.groups_id = [(4, tutor_group.id)]
                estudiante.tutor_user_id = tutor_user.id
            else:
                _logger.info(f"El tutor {estudiante.tutor_id} ya tiene una cuenta de usuario con el email {estudiante.email_tutor}")

        return estudiante

    def write(self, vals):
        # Verificar si se está actualizando el CI o email del estudiante
        if 'ci' in vals or 'email' in vals or 'name' in vals:
            if 'ci' in vals:
                new_ci = vals.get('ci')
                _logger.info(f"Nuevo CI del estudiante detectado: {new_ci}")
            if 'email' in vals:
                new_email = vals.get('email')
                _logger.info(f"Nuevo email del estudiante detectado: {new_email}")
            if 'name' in vals:
                new_name = vals.get('name')
                _logger.info(f"Nuevo nombre del estudiante detectado: {new_name}")

            # Actualizar la información de usuario del estudiante
            if self.user_id:
                update_vals = {}
                if 'ci' in vals:
                    update_vals['password'] = new_ci  # Actualizar contraseña al nuevo CI
                if 'email' in vals:
                    update_vals['login'] = new_email
                    update_vals['email'] = new_email
                if 'name' in vals:  # Actualizamos el nombre del usuario
                    update_vals['name'] = new_name
                self.user_id.write(update_vals)
            else:
                _logger.warning(f"No se encontró usuario asociado para el estudiante {self.name}")

        # Verificar si se está actualizando el CI o email del tutor
        if 'ci_tutor' in vals or 'email_tutor' in vals or 'tutor_id' in vals:
            if 'ci_tutor' in vals:
                new_ci_tutor = vals.get('ci_tutor')
                _logger.info(f"Nuevo CI del tutor detectado: {new_ci_tutor}")
            if 'email_tutor' in vals:
                new_email_tutor = vals.get('email_tutor')
                _logger.info(f"Nuevo email del tutor detectado: {new_email_tutor}")
            if 'tutor_id' in vals:  # Utilizamos el valor de tutor_id directamente si existe
                new_name_tutor = vals.get('tutor_id', '')  # Suponiendo que el nombre del tutor se pasa aquí
                _logger.info(f"Nuevo nombre del tutor detectado: {new_name_tutor}")

            # Actualizar la información de usuario del tutor
            if self.tutor_user_id:
                tutor_update_vals = {}
                if 'ci_tutor' in vals:
                    tutor_update_vals['password'] = new_ci_tutor  # Actualizar contraseña al nuevo CI del tutor
                if 'email_tutor' in vals:
                    tutor_update_vals['login'] = new_email_tutor
                    tutor_update_vals['email'] = new_email_tutor
                if 'tutor_id' in vals:  # Actualizamos el nombre del usuario
                    tutor_update_vals['name'] = new_name_tutor
                self.tutor_user_id.write(tutor_update_vals)
            else:
                _logger.warning(f"No se encontró usuario asociado para el tutor {estudiante.tutor_id}")

        # Llamar al método write original para actualizar el resto de los campos en el modelo
        return super(Estudiante, self).write(vals)



