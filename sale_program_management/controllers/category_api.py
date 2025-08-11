from odoo import http
from odoo.http import request
import logging
import base64
import json
from .base_api import BaseAPIController

_logger = logging.getLogger(__name__)

class CategoryAPIController(BaseAPIController):
    """Category API Controller with GET and POST endpoints"""

    @http.route('/api/sale_man/categories', type='http', auth='public', method=['GET'], csrf=False)
    def get_categories(self, **kwargs):
        try:
            categories = request.env['sale_man.category'].sudo().search([])
            result = []
            for cat in categories:
                result.append({
                    'id': cat.id,
                    'name_vi': cat.name_vi,
                    'name_en': cat.name_en,
                    'code': cat.code,
                    'status': cat.status,
                    'parent': {
                        'id': cat.parent_id.id,
                        'name_vi': cat.parent_id.name_vi,
                        'name_en': cat.parent_id.name_en,
                        'code': cat.parent_id.code,
                        'status': cat.parent_id.status,
                    } if cat.parent_id else None,
                    'children': [
                        {
                            'id': child.id,
                            'name_vi': child.name_vi,
                            'name_en': child.name_en,
                            'code': child.code,
                            'status': child.status,
                        } for child in cat.child_ids
                    ]
                })
            return self._create_success_response(result, 'Categories fetched successfully', 200)
        except Exception as e:
            _logger.error(f"Error fetching categories: {str(e)}")
            return self._create_error_response(str(e), 500)

    @http.route('/api/sale_man/categories/create', type='http', auth='public', method=['POST'], csrf=False)
    def create_category_http(self, **kwargs):
        try:
            # Authenticate user using API key
            user, auth_error = self._authenticate_user()
            if not user:
                return self._create_error_response(auth_error, 401)
            
            # Parse form data (multipart/form-data)
            name_vi = request.httprequest.form.get('name_vi')
            name_en = request.httprequest.form.get('name_en')
            status = request.httprequest.form.get('status', 'active')
            parent_id = request.httprequest.form.get('parent_id')
            image_file = request.httprequest.files.get('image')
            
            # Validate required fields
            if not name_vi or not name_en:
                return self._create_error_response('name_vi and name_en are required', 400)

            # Validate status value
            if status not in ['active', 'inactive']:
                return self._create_error_response('status must be either "active" or "inactive"', 400)
            
            # Prepare values for creation
            vals = {
                'name_vi': name_vi,
                'name_en': name_en,
                'status': status
            }
            if parent_id:
                vals['parent_id'] = int(parent_id)
            if image_file:
                vals['image'] = base64.b64encode(image_file.read())

            # Create the category (sequence will automatically generate the code)
            category = request.env['sale_man.category'].sudo().create(vals)
            
            # Return success response with created category data
            response_data = {
                'id': category.id,
                'name_vi': category.name_vi,
                'name_en': category.name_en,
                'code': category.code,
                'status': category.status,
                'parent_id': category.parent_id.id if category.parent_id else None
            }
            
            return self._create_success_response(response_data, 'Category created successfully', 201)
            
        except Exception as e:
            _logger.error(f"Error creating category: {str(e)}")
            return self._create_error_response(str(e), 500)

    @http.route('/api/sale_man/categories/update', type='http', auth='public', method=['POST'], csrf=False)
    def update_category_http(self, **kwargs):
        try:
            # Authenticate user using API key
            user, auth_error = self._authenticate_user()
            if not user:
                return self._create_error_response(auth_error, 401)

            category_id = request.httprequest.form.get('id')
            if not category_id:
                return self._create_error_response('Category id is required', 400)

            category = request.env['sale_man.category'].sudo().browse(int(category_id))
            if not category.exists():
                return self._create_error_response('Category not found', 404)

            vals = {}
            name_vi = request.httprequest.form.get('name_vi')
            if name_vi:
                vals['name_vi'] = name_vi
            name_en = request.httprequest.form.get('name_en')
            if name_en:
                vals['name_en'] = name_en
            status = request.httprequest.form.get('status')
            if status:
                if status not in ['active', 'inactive']:
                    return self._create_error_response('status must be either "active" or "inactive"', 400)
                vals['status'] = status
            parent_id = request.httprequest.form.get('parent_id')
            if parent_id:
                vals['parent_id'] = int(parent_id)
            image_file = request.httprequest.files.get('image')
            if image_file:
                vals['image'] = base64.b64encode(image_file.read())

            if not vals:
                return self._create_error_response('No valid data provided for update', 400)

            category.sudo().write(vals)
            response_data = {
                'id': category.id,
                'name_vi': category.name_vi,
                'name_en': category.name_en,
                'code': category.code,
                'status': category.status,
                'parent_id': category.parent_id.id if category.parent_id else None
            }
            return self._create_success_response(response_data, 'Category updated successfully', 200)
        except Exception as e:
            _logger.error(f"Error updating category: {str(e)}")
            return self._create_error_response(str(e), 500)
