from odoo import http
from odoo.http import request
import json

class DeviceTokenController(http.Controller):

    @http.route('/api/device_tokens', type='json', auth='public', methods=['POST'])
    def get_device_tokens(self, **kwargs):
        # Obtener el ID del usuario de los parámetros JSON
        user_id = kwargs.get('user_id')
        
        # Verificar si se proporcionó el ID del usuario
        if not user_id:
            return {
                "status": "error",
                "message": "El ID del usuario es obligatorio."
            }
        
        # Buscar tokens en la base de datos
        tokens = request.env['device.token'].sudo().search([('user_id', '=', user_id)])
        
        # Verificar si existen tokens para el usuario
        if not tokens:
            return {
                "status": "error",
                "message": "No se encontraron tokens para el usuario proporcionado."
            }
        
        # Obtener los tokens en una lista
        token_list = [token.token for token in tokens]
        
        return {
            "status": "success",
            "tokens": token_list
        }
