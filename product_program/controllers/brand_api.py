from odoo import http
from odoo.http import request, Response
import logging
import json

_logger = logging.getLogger(__name__)

class BrandAPIController(http.Controller):
    @http.route('/api/brands', type='json', auth='public', methods=['GET'], csrf=False)
    def get_brands(self, **kwargs):
        try:
            brands = request.env['product_program.brand'].sudo().search([])
            result = [
                {
                    'id': brand.id,
                    'name': brand.name,
                    'code': brand.code,
                    'image': brand.image.decode('utf-8') if brand.image else None
                }
                for brand in brands
            ]
            return {'status': 'success', 'data': result}
        except Exception as e:
            _logger.error(f"Error fetching brands: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/brands', type='json', auth='public', methods=['POST'], csrf=False)
    def create_brand(self, **kwargs):
        try:
            data = kwargs
            name = data.get('name')
            code = data.get('code', '/')
            image = data.get('image')
            if not name:
                return {'status': 'error', 'message': 'Name is required'}
            vals = {'name': name}
            if code:
                vals['code'] = code
            if image:
                vals['image'] = image
            brand = request.env['product_program.brand'].sudo().create(vals)
            return {'status': 'success', 'id': brand.id}
        except Exception as e:
            _logger.error(f"Error creating brand: {str(e)}")
            return {'status': 'error', 'message': str(e)}