from odoo import http
from odoo.http import request
import logging
from .base_api import BaseAPIController

_logger = logging.getLogger(__name__)

class ProductAPIController(BaseAPIController):
    """Product API Controller with GET and POST endpoints"""

    @http.route('/api/sale_man/products', type='http', auth='public', method=['GET'], csrf=False)
    def get_products(self, **kwargs):
        try:
            products = request.env['sale_man.product'].sudo().search([])
            result = []
            for product in products:
                item = {
                    'id': product.id,
                    'name_vi': product.name_vi,
                    'name_en': product.name_en,
                    'code': product.code,
                    'status': product.status,
                    # Return complete category details instead of just the ID.
                    'category': {
                        'id': product.category_id.id,
                        'name_vi': product.category_id.name_vi,
                        'name_en': product.category_id.name_en,
                        'code': product.category_id.code,
                        'status': product.category_id.status,
                    } if product.category_id else None,
                    # Return complete brand details.
                    'brand': {
                        'id': product.brand_id.id,
                        'name_vi': product.brand_id.name_vi,
                        'name_en': product.brand_id.name_en,
                        'code': product.brand_id.code,
                        'status': product.brand_id.status,
                    } if product.brand_id else None
                }
                result.append(item)

            return self._create_success_response(result, 'Products fetched successfully', 200)
        except Exception as e:
            _logger.error(f"Error fetching products: {str(e)}")
            return self._create_error_response(str(e), 500)

    @http.route('/api/sale_man/products/create', type='http', auth='public', method=['POST'], csrf=False)
    def create_product_http(self, **kwargs):
        try:
            # Authenticate user using API key
            user, auth_error = self._authenticate_user()
            if not user:
                return self._create_error_response(auth_error, 401)
            
            # Update sequence to continue from current highest number
            self._update_sequence('product', 'sale_man.product', 'PRD', 'sale_man_product')
            
            # Parse form data (multipart/form-data)
            name_vi = request.httprequest.form.get('name_vi')
            name_en = request.httprequest.form.get('name_en')
            category_id = request.httprequest.form.get('category_id')
            brand_id = request.httprequest.form.get('brand_id')
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
            if category_id:
                vals['category_id'] = int(category_id)
            if brand_id:
                vals['brand_id'] = int(brand_id)
            if image_file:
                import base64
                image_data = image_file.read()
                vals['image'] = base64.b64encode(image_data)
            
            # Create the product (sequence will automatically generate the code)
            product = request.env['sale_man.product'].sudo().create(vals)
            
            # Return success response with created product data
            response_data = {
                'id': product.id,
                'name_vi': product.name_vi,
                'name_en': product.name_en,
                'code': product.code,
                'status': product.status,
                'category_id': product.category_id.id if product.category_id else None,
                'brand_id': product.brand_id.id if product.brand_id else None
            }
            
            return self._create_success_response(response_data, 'Product created successfully', 201)
            
        except Exception as e:
            _logger.error(f"Error creating product: {str(e)}")
            return self._create_error_response(str(e), 500)

    @http.route('/api/sale_man/products/update', type='http', auth='public', method=['POST'], csrf=False)
    def update_product_http(self, **kwargs):
        try:
            # Authenticate user using API key
            user, auth_error = self._authenticate_user()
            if not user:
                return self._create_error_response(auth_error, 401)

            product_id = request.httprequest.form.get('id')
            if not product_id:
                return self._create_error_response('Product id is required', 400)

            product = request.env['sale_man.product'].sudo().browse(int(product_id))
            if not product.exists():
                return self._create_error_response('Product not found', 404)

            # Parse optional fields for partial update
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
            list_price = request.httprequest.form.get('list_price')
            if list_price:
                try:
                    vals['list_price'] = float(list_price)
                except ValueError:
                    return self._create_error_response('list_price must be a number', 400)
            cost = request.httprequest.form.get('cost')
            if cost:
                try:
                    vals['cost'] = float(cost)
                except ValueError:
                    return self._create_error_response('cost must be a number', 400)
            quantity = request.httprequest.form.get('quantity')
            if quantity:
                try:
                    vals['quantity'] = int(quantity)
                except ValueError:
                    return self._create_error_response('quantity must be an integer', 400)
            brand_id = request.httprequest.form.get('brand_id')
            if brand_id:
                vals['brand_id'] = int(brand_id)
            category_id = request.httprequest.form.get('category_id')
            if category_id:
                vals['category_id'] = int(category_id)
            image_file = request.httprequest.files.get('image')
            if image_file:
                import base64
                image_data = image_file.read()
                vals['image'] = base64.b64encode(image_data)

            if not vals:
                return self._create_error_response('No valid data provided for update', 400)

            product.sudo().write(vals)

            response_data = {
                'id': product.id,
                'name_vi': product.name_vi,
                'name_en': product.name_en,
                'code': product.code,
                'status': product.status,
                'list_price': product.list_price,
                'cost': product.cost,
                'quantity': product.quantity,
                'category': {
                    'id': product.category_id.id,
                    'name_vi': product.category_id.name_vi,
                    'name_en': product.category_id.name_en,
                    'code': product.category_id.code,
                    'status': product.category_id.status,
                } if product.category_id else None,
                'brand': {
                    'id': product.brand_id.id,
                    'name_vi': product.brand_id.name_vi,
                    'name_en': product.brand_id.name_en,
                    'code': product.brand_id.code,
                    'status': product.brand_id.status,
                } if product.brand_id else None,
            }
            return self._create_success_response(response_data, 'Product updated successfully', 200)
        except Exception as e:
            _logger.error(f"Error updating product: {str(e)}")
            return self._create_error_response(str(e), 500)
