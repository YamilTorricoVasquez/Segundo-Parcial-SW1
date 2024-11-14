from odoo import models, fields, api

class Comunicado(models.Model):
    _name = 'agenda.comunicado'
    _description = 'Comunicado'

    name = fields.Char(string='Título del comunicado', required=True)
    descripcion_comunicado = fields.Text(string='Descripción del comunicado', required=True)
    
    destinatario_ids = fields.Many2many(
        'res.groups', 
        string='Roles Destinatarios',
        help='Roles a los que se enviará este comunicado'
    )
      # Nuevos campos para curso, nivel y paralelo
    curso_id = fields.Many2one('agenda.curso', string='Curso')
    nivel_id = fields.Many2one('agenda.nivel', string='Nivel')
    paralelo_id = fields.Many2one('agenda.paralelo', string='Paralelo')
    fecha_creacion = fields.Datetime(string='Fecha de Creación', default=fields.Datetime.now)
    fecha_envio = fields.Datetime(string='Fecha de Envío')
    
    archivo_adjunto = fields.Binary(string='Archivo Adjunto')
    
    remitente_id = fields.Many2one('res.users', string='Remitente', default=lambda self: self.env.user)
    
    # En el modelo agenda.comunicado
    leido_ids = fields.Many2many(
        'res.users',
        string='Usuarios que leyeron',
        help='Usuarios que han leído el comunicado'
    )

  
  
    enviar_notificacion = fields.Boolean(string='Enviar Notificación', default=True)

    _sql_constraints = [
        ('name_comunicado_unique', 'UNIQUE(name)', 'No puede duplicar el nombre del comunicado.')
    ]

    
