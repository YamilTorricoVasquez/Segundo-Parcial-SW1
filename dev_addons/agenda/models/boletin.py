from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Boletin(models.Model):
    _name = 'agenda.boletin'
    _description = 'Boletín de Calificaciones por Trimestre'

    curso_id = fields.Many2one('agenda.curso', string='Curso', required=True)
    nivel_id = fields.Many2one('agenda.nivel', string='Nivel', required=True)
    paralelo_id = fields.Many2one('agenda.paralelo', string='Paralelo', required=True)
    materia_id = fields.Many2one('agenda.materia', string='Materia', required=True)
    nota = fields.Integer(string = 'Nota', required = True)
    estudiante_id = fields.Many2one(
        'agenda.estudiante', 
        string='Estudiante', 
        required=True,
        domain="[('curso_id', '=', curso_id), ('nivel_id', '=', nivel_id), ('paralelo_id', '=', paralelo_id)]"
    )
    
    ci_estudiante = fields.Char(string='Cédula de Identidad', readonly=True)
    trimestre_id = fields.Many2one('agenda.trimestre', string='Trimestre', required=True)
    fecha_id = fields.Date(string='Fecha de Entrega', readonly=True)

    @api.onchange('trimestre_id')
    def _onchange_trimestre_id(self):
        if self.trimestre_id:
            self.fecha_id = self.trimestre_id.fecha
        else:
            self.fecha_id = False

    @api.onchange('estudiante_id')
    def _onchange_estudiante_id(self):
        if self.estudiante_id:
            self.ci_estudiante = self.estudiante_id.ci
        else:
            self.ci_estudiante = False

    def _check_duplicate_boletin(self, estudiante_id, materia_id, trimestre_id):
        # Verifica si ya existe un boletín para el mismo estudiante, materia y trimestre
        existing_boletin = self.search([
            ('estudiante_id', '=', estudiante_id),
            ('materia_id', '=', materia_id),
            ('trimestre_id', '=', trimestre_id)
        ])
        return existing_boletin
    @api.onchange('curso_id', 'nivel_id', 'paralelo_id')
    def _onchange_curso_nivel_paralelo(self):
        # Limpiar el campo estudiante_id cuando se cambie curso, nivel o paralelo
        self.estudiante_id = False
        # Actualizar el dominio del campo estudiante_id
        return {
            'domain': {
                'estudiante_id': [
                    ('curso_id', '=', self.curso_id.id),
                    ('nivel_id', '=', self.nivel_id.id),
                    ('paralelo_id', '=', self.paralelo_id.id)
                ]
            }
        }
    @api.model
    def create(self, vals):
        # Asigna el CI y la fecha antes de la validación
        if 'estudiante_id' in vals:
            estudiante = self.env['agenda.estudiante'].browse(vals['estudiante_id'])
            vals['ci_estudiante'] = estudiante.ci  # Asigna el CI del estudiante

        if 'trimestre_id' in vals:
            trimestre = self.env['agenda.trimestre'].browse(vals['trimestre_id'])
            vals['fecha_id'] = trimestre.fecha  # Asigna la fecha del trimestre

        # Validar que ci_estudiante y fecha_id estén presentes en los valores
        if not vals.get('ci_estudiante'):
            raise ValidationError("La Cédula de Identidad es obligatoria.")
        if not vals.get('fecha_id'):
            raise ValidationError("La Fecha de Entrega es obligatoria.")
        
        # Validar duplicados
        if self._check_duplicate_boletin(vals.get('estudiante_id'), vals.get('materia_id'), vals.get('trimestre_id')):
            raise ValidationError("Ya existe un boletín para el estudiante, materia y trimestre seleccionados.")

        return super(Boletin, self).create(vals)

    def write(self, vals):
        # Verificar si 'estudiante_id' está en los valores o si ya existe un estudiante asignado
        estudiante_id = vals.get('estudiante_id') or self.estudiante_id.id
        if estudiante_id:
            estudiante = self.env['agenda.estudiante'].browse(estudiante_id)
            vals['ci_estudiante'] = estudiante.ci  # Asegurarse de que el CI del estudiante esté asignado

        # Verificar si 'trimestre_id' está en los valores o si ya existe un trimestre asignado
        trimestre_id = vals.get('trimestre_id') or self.trimestre_id.id
        if trimestre_id:
            trimestre = self.env['agenda.trimestre'].browse(trimestre_id)
            vals['fecha_id'] = trimestre.fecha  # Asegurarse de que la fecha del trimestre esté asignada

        # Validar que ci_estudiante y fecha_id estén presentes en los valores
        if not vals.get('ci_estudiante'):
            raise ValidationError("La Cédula de Identidad es obligatoria.")
        if not vals.get('fecha_id'):
            raise ValidationError("La Fecha de Entrega es obligatoria.")

        # Validar duplicados
        if 'estudiante_id' in vals and 'materia_id' in vals and 'trimestre_id' in vals:
            if self._check_duplicate_boletin(vals.get('estudiante_id'), vals.get('materia_id'), vals.get('trimestre_id')):
                raise ValidationError("Ya existe un boletín para el estudiante, materia y trimestre seleccionados.")

        return super(Boletin, self).write(vals)


