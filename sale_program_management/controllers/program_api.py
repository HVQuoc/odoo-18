from odoo import http
from odoo.http import request
import logging
from .base_api import BaseAPIController

_logger = logging.getLogger(__name__)

class ProgramAPIController(BaseAPIController):
    """Program API Controller with GET and POST endpoints"""

    @http.route('/api/sale_man/programs', type='http', auth='public', method=['GET'], csrf=False)
    def get_programs(self, **kwargs):
        try:
            programs = request.env['sale_man.program'].sudo().search([])
            result = []
            for program in programs:
                data = {
                    'id': program.id,
                    'name_vi': program.name_vi,
                    'name_en': program.name_en,
                    'code': program.code,
                    'status': program.status,
                    'company_id': program.company_id.id if program.company_id else None,
                    # Add detailed category information for each program
                    'categories': [
                        {
                            'id': category.id,
                            'name_vi': category.name_vi,
                            'name_en': category.name_en,
                        } for category in program.category_ids
                    ]
                }
                result.append(data)
            return self._create_success_response(result, 'Programs fetched successfully', 200)
        except Exception as e:
            _logger.error(f"Error fetching programs: {str(e)}")
            return self._create_error_response(str(e), 500)

    @http.route('/api/sale_man/programs/create', type='http', auth='public', method=['POST'], csrf=False)
    def create_program_http(self, **kwargs):
        try:
            # Authenticate user using API key
            user, auth_error = self._authenticate_user()
            if not user:
                return self._create_error_response(auth_error, 401)
            
            # Update sequence to continue from current highest number
            # self._update_sequence('program', 'sale_man.program', 'PRG', 'sale_man_program')
            
            # Parse request data
            data = self._parse_request_data(kwargs)
            
            # Validate required fields
            name_vi = data.get('name_vi')
            if not name_vi:
                return self._create_error_response('name_vi is required', 400)
            
            # Get optional fields
            name_en = data.get('name_en')
            company_id = data.get('company_id')
            status = data.get('status', 'active')
            
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
            if company_id:
                vals['company_id'] = int(company_id)
            
            # Create the program (sequence will automatically generate the code)
            program = request.env['sale_man.program'].sudo().create(vals)
            
            # Return success response with created program data
            response_data = {
                'id': program.id,
                'name_vi': program.name_vi,
                'name_en': program.name_en,
                'code': program.code,
                'status': program.status,
                'company_id': program.company_id.id if program.company_id else None
            }
            
            return self._create_success_response(response_data, 'Program created successfully', 201)
            
        except Exception as e:
            _logger.error(f"Error creating program: {str(e)}")
            return self._create_error_response(str(e), 500)

    @http.route('/api/sale_man/programs/update', type='http', auth='public', method=['POST'], csrf=False)
    def update_program_http(self, **kwargs):
        try:
            # Authenticate user using API key
            user, auth_error = self._authenticate_user()
            if not user:
                return self._create_error_response(auth_error, 401)

            # Parse request data
            data = self._parse_request_data(kwargs)
            program_id = data.get('id')
            if not program_id:
                return self._create_error_response('Program id is required', 400)

            program = request.env['sale_man.program'].sudo().browse(int(program_id))
            if not program.exists():
                return self._create_error_response('Program not found', 404)

            # Parse optional fields for partial update
            vals = {}
            if 'name_vi' in data:
                vals['name_vi'] = data.get('name_vi')
            if 'name_en' in data:
                vals['name_en'] = data.get('name_en')
            if 'status' in data:
                if data.get('status') not in ['active', 'inactive']:
                    return self._create_error_response('status must be either "active" or "inactive"', 400)
                vals['status'] = data.get('status')
            if 'company_id' in data:
                vals['company_id'] = int(data.get('company_id'))
            if 'start_date' in data:
                vals['start_date'] = data.get('start_date')
            if 'end_date' in data:
                vals['end_date'] = data.get('end_date')

            if not vals:
                return self._create_error_response('No valid data provided for update', 400)

            program.sudo().write(vals)

            response_data = {
                'id': program.id,
                'name_vi': program.name_vi,
                'name_en': program.name_en,
                'code': program.code,
                'status': program.status,
                'start_date': program.start_date.isoformat() if program.start_date else None,
                'end_date': program.end_date.isoformat() if program.end_date else None,
                'company_id': program.company_id.id if program.company_id else None
            }
            return self._create_success_response(response_data, 'Program updated successfully', 200)
        except Exception as e:
            _logger.error(f"Error updating program: {str(e)}")
            return self._create_error_response(str(e), 500)
