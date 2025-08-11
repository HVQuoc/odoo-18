from odoo import http
from odoo.http import request
import logging
import json
from .base_api import BaseAPIController

_logger = logging.getLogger(__name__)

class BrandAPIController(BaseAPIController):
    """Brand API Controller with GET and POST endpoints"""

    @http.route('/api/sale_man/brands', type='http', auth='public', method=['GET'], csrf=False)
    def get_brands(self, **kwargs):
        try:
            brands = request.env['sale_man.brand'].sudo().search([])
            fields = ['id', 'name_vi', 'name_en', 'code', 'status']
            return self._get_list_response(brands, fields)
        except Exception as e:
            _logger.error(f"Error fetching brands: {str(e)}")
            return self._create_error_response(str(e), 500)

    @http.route('/api/sale_man/brands/create', type='http', auth='public', method=['POST'], csrf=False)
    def create_brand_http(self, **kwargs):
        try:
            # Authenticate user using API key
            user, auth_error = self._authenticate_user()
            if not user:
                return self._create_error_response(auth_error, 401)
            
            # Parse form data (multipart/form-data)
            name_vi = request.httprequest.form.get('name_vi')
            name_en = request.httprequest.form.get('name_en')
            status = request.httprequest.form.get('status', 'active')
            image_file = request.httprequest.files.get('image')
            
            # Validate required fields
            if not name_vi:
                return self._create_error_response('name_vi is required', 400)
            
            # Validate status value
            if status not in ['active', 'inactive']:
                return self._create_error_response('status must be either "active" or "inactive"', 400)
            
            # Prepare values for creation
            vals = {
                'name_vi': name_vi,
                'status': status
            }
            if name_en:
                vals['name_en'] = name_en
            
            # Handle image upload
            if image_file:
                import base64
                image_data = image_file.read()
                vals['image'] = base64.b64encode(image_data)
            
            # Create the brand (sequence will automatically generate the code)
            brand = request.env['sale_man.brand'].sudo().create(vals)
            
            # Return success response with created brand data
            response_data = {
                'id': brand.id,
                'name_vi': brand.name_vi,
                'name_en': brand.name_en,
                'code': brand.code,
                'status': brand.status
            }
            
            return self._create_success_response(response_data, 'Brand created successfully', 201)
            
        except Exception as e:
            _logger.error(f"Error creating brand: {str(e)}")
            return self._create_error_response(str(e), 500)

    @http.route('/api/sale_man/brands/update', type='http', auth='public', method=['POST'], csrf=False)
    def update_brand_http(self, **kwargs):
        try:
            # Authenticate user using API key
            user, auth_error = self._authenticate_user()
            if not user:
                return self._create_error_response(auth_error, 401)

            # Parse form data
            brand_id = request.httprequest.form.get('id')
            if not brand_id:
                return self._create_error_response('Brand id is required', 400)

            brand = request.env['sale_man.brand'].sudo().browse(int(brand_id))
            if not brand.exists():
                return self._create_error_response('Brand not found', 404)

            # Parse optional fields for partial update
            name_vi = request.httprequest.form.get('name_vi')
            name_en = request.httprequest.form.get('name_en')
            status = request.httprequest.form.get('status')
            image_file = request.httprequest.files.get('image')

            vals = {}
            if name_vi:
                vals['name_vi'] = name_vi
            if name_en:
                vals['name_en'] = name_en
            if status:
                if status not in ['active', 'inactive']:
                    return self._create_error_response('status must be either "active" or "inactive"', 400)
                vals['status'] = status
            if image_file:
                import base64
                image_data = image_file.read()
                vals['image'] = base64.b64encode(image_data)

            if not vals:
                return self._create_error_response('No valid data provided for update', 400)

            brand.sudo().write(vals)

            response_data = {
                'id': brand.id,
                'name_vi': brand.name_vi,
                'name_en': brand.name_en,
                'code': brand.code,
                'status': brand.status
            }
            return self._create_success_response(response_data, 'Brand updated successfully', 200)
        except Exception as e:
            _logger.error(f"Error updating brand: {str(e)}")
            return self._create_error_response(str(e), 500)
