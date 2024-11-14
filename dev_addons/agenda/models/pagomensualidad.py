from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class PagoMensualidad(models.Model):
    _name = 'agenda.mensualidad'
    _description = 'Pago de Mensualidad'

    # Campo identificador secuencial
    numero_pago = fields.Char(string='Número de Pago', readonly=True, copy=False, default='Nuevo')

    estudiante_id = fields.Many2one(
        'agenda.estudiante', 
        string='Estudiante', 
        required=True
    )
    curso_id = fields.Many2one('agenda.curso', string='Curso', related='estudiante_id.curso_id', readonly=True)
    nivel_id = fields.Many2one('agenda.nivel', string='Nivel', related='estudiante_id.nivel_id', readonly=True)
    paralelo_id = fields.Many2one('agenda.paralelo', string='Paralelo', related='estudiante_id.paralelo_id', readonly=True)

    ci_estudiante = fields.Char(string='Cédula de Identidad', related='estudiante_id.ci', readonly=True)
    mes = fields.Selection([
        ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), 
        ('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'),
        ('07', 'Julio'), ('08', 'Agosto'), ('09', 'Septiembre'),
        ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
    ], string='Mes', required=True)
    anio = fields.Integer(string='Año', required=True, default=date.today().year)
    monto = fields.Float(string='Monto', required=True)
    fecha_pago = fields.Date(string='Fecha de Pago', default=fields.Date.context_today, readonly=True)

    estado_pago = fields.Selection([
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado')
    ], string='Estado', default='pagado', readonly=True)

    _sql_constraints = [
        ('unique_pago_mensualidad', 
         'UNIQUE(estudiante_id, mes, anio, estado_pago)', 
         'Ya existe un pago de mensualidad para este estudiante en el mes y año seleccionados.')
    ]

    @api.constrains('monto')
    def _check_monto(self):
        for record in self:
            if record.monto <= 0:
                raise ValidationError("El monto debe ser mayor a cero.")

    @api.model
    def create(self, vals):
        # Asignar el número de pago secuencial
        if vals.get('numero_pago', 'Nuevo') == 'Nuevo':
            vals['numero_pago'] = self.env['ir.sequence'].next_by_code('agenda.mensualidad') or 'Nuevo'
        
        # Validación para asegurar que el monto y el estudiante existan
        if not vals.get('monto'):
            raise ValidationError("El monto es obligatorio.")
        if not vals.get('estudiante_id'):
            raise ValidationError("El estudiante es obligatorio.")
        
        # Validar duplicados antes de crear, excluyendo registros cancelados
        existing_pago = self.search([
            ('estudiante_id', '=', vals.get('estudiante_id')),
            ('mes', '=', vals.get('mes')),
            ('anio', '=', vals.get('anio')),
            ('estado_pago', '=', 'pagado')
        ])
        if existing_pago:
            raise ValidationError("Ya existe un pago para el estudiante en el mes y año seleccionados.")
        
        return super(PagoMensualidad, self).create(vals)

    def cancelar_pago(self):
        for record in self:
            if record.estado_pago == 'pagado':
                record.estado_pago = 'cancelado'
            else:
                raise ValidationError("El pago ya está cancelado.")

    def write(self, vals):
        # Evitar modificaciones en pagos ya realizados a menos que sea una cancelación
        if 'estado_pago' not in vals and self.estado_pago == 'pagado':
            raise ValidationError("No se puede modificar un pago ya realizado. Solo se permite cancelar el pago.")
        
        # Validar duplicados al editar
        estudiante_id = vals.get('estudiante_id') or self.estudiante_id.id
        mes = vals.get('mes') or self.mes
        anio = vals.get('anio') or self.anio
        estado_pago = vals.get('estado_pago') or self.estado_pago

        existing_pago = self.search([
            ('estudiante_id', '=', estudiante_id),
            ('mes', '=', mes),
            ('anio', '=', anio),
            ('estado_pago', '=', 'pagado'),
            ('id', '!=', self.id)
        ])
        if existing_pago:
            raise ValidationError("Ya existe un pago para el estudiante en el mes y año seleccionados.")
        
        return super(PagoMensualidad, self).write(vals)

    def unlink(self):
        # Evitar la eliminación de pagos
        raise ValidationError("No se permite eliminar un pago. Solo se puede cancelar.")
