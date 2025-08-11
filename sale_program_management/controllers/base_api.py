from odoo import http
from odoo.http import request
import logging
import json
from odoo.addons.base.models.res_users import API_KEY_SIZE, KEY_CRYPT_CONTEXT, INDEX_SIZE

_logger = logging.getLogger(__name__)

class BaseAPIController(http.Controller):
    """Base API Controller with reusable authentication and sequence management"""
    
    def _authenticate_user(self):
        """Authenticate user using API key from Authorization header"""
        try:
            # Get Authorization header
            auth_header = request.httprequest.headers.get('Authorization', '')
            _logger.info(f"Auth header received: {auth_header}")
            
            if not auth_header.startswith('Bearer '):
                return None, "Invalid authorization header format. Use 'Bearer YOUR_API_KEY'"
            
            # Extract API key
            api_key = auth_header.replace('Bearer ', '')
            _logger.info(f"Extracted API key length: {len(api_key)}")
            _logger.info(f"API key starts with: {api_key[:8] if len(api_key) >= 8 else 'too short'}")
            
            if not api_key:
                return None, "API key is required"
            
            # Use Odoo's built-in API key system with proper hashing
            try:
                # Get the index part of the API key (first 8 characters)
                if len(api_key) < INDEX_SIZE:
                    return None, "Invalid API key format"

                key_index = api_key[:INDEX_SIZE]
                _logger.info(f"Looking for API keys with index: {key_index}")

                # Use raw SQL to find API key records with matching index
                request.env.cr.execute("""
                    SELECT user_id, key
                    FROM res_users_apikeys INNER JOIN res_users u ON (u.id = user_id)
                    WHERE
                        u.active and index = %s
                        AND (
                            expiration_date IS NULL OR
                            expiration_date >= now() at time zone 'utc'
                        )
                """, [key_index])

                api_key_records = request.env.cr.fetchall()
                _logger.info(f"Found {len(api_key_records)} API key records with matching index")

                # Check each record to find the one with matching hash
                for user_id, stored_hash in api_key_records:
                    try:
                        _logger.info(f"Checking API key for user ID: {user_id}")
                        # Verify the API key against the stored hash
                        if KEY_CRYPT_CONTEXT.verify(api_key, stored_hash):
                            user = request.env['res.users'].sudo().browse(user_id)
                            _logger.info(f"Authentication successful for user: {user.name}")
                            return user, None
                        else:
                            _logger.info(f"Hash verification failed for user {user_id}")
                    except Exception as verify_error:
                        _logger.debug(f"API key verification failed for user {user_id}: {str(verify_error)}")
                        continue

                _logger.warning("No matching API key found after checking all records")
                return None, "Invalid API key"

            except Exception as auth_error:
                _logger.error(f"API key authentication error: {str(auth_error)}")
                return None, "Invalid API key"
            
        except Exception as e:
            _logger.error(f"Authentication error: {str(e)}")
            return None, "Authentication failed"

    def _update_sequence(self, model_name, sequence_code, code_prefix, table_name):
        """Generic sequence update method"""
        try:
            # Get current sequence
            sequence = request.env['ir.sequence'].sudo().search([('code', '=', sequence_code)])
            if not sequence:
                return
            
            # Use SQL to find the highest number efficiently
            request.env.cr.execute(f"""
                SELECT MAX(CAST(SUBSTRING(code FROM {len(code_prefix) + 1}) AS INTEGER))
                FROM {table_name} 
                WHERE code LIKE '{code_prefix}%' AND code ~ '^{code_prefix}[0-9]+$'
            """)
            
            result = request.env.cr.fetchone()
            max_number = result[0] if result[0] else 0
            
            # Only update if sequence is behind the current max
            if max_number > 0 and sequence.number_next <= max_number:
                sequence.write({'number_next': max_number + 1})
                _logger.info(f"Updated {model_name} sequence from {sequence.number_next} to {max_number + 1}")
            else:
                _logger.debug(f"{model_name} sequence already up to date: current={sequence.number_next}, max={max_number}")
                
        except Exception as e:
            _logger.error(f"Error updating {model_name} sequence: {str(e)}")

    def _parse_request_data(self, kwargs):
        """Parse request data from JSON body or kwargs"""
        request_data = request.httprequest.data.decode('utf-8')
        _logger.info(f"HTTP request data: {request_data}")
        _logger.info(f"HTTP kwargs: {kwargs}")
        
        if request_data:
            try:
                data = json.loads(request_data)
                _logger.info(f"Parsed JSON data: {data}")
                return data
            except json.JSONDecodeError as e:
                _logger.error(f"JSON decode error: {e}")
                return kwargs
        else:
            return kwargs

    def _create_success_response(self, data, message="Created successfully", status=201):
        """Create a standardized success response"""
        return http.Response(
            json.dumps({
                'status': 'success',
                'message': message,
                'data': data
            }),
            content_type='application/json',
            status=status
        )

    def _create_error_response(self, message, status=400):
        """Create a standardized error response"""
        return http.Response(
            json.dumps({'status': 'error', 'message': message}),
            content_type='application/json',
            status=status
        )

    def _get_list_response(self, records, fields):
        """Create a standardized list response with relational fields converted to IDs"""
        result = []
        for record in records:
            item = {}
            for field in fields:
                if hasattr(record, field):
                    value = getattr(record, field)
                    # If the value is a many2one/many2many record, convert to its id (or list of ids)
                    if hasattr(value, 'id'):
                        # For many2one, value is a recordset; return id if exists, or None
                        item[field] = value.id if value else None
                    elif isinstance(value, (list, tuple)):
                        # In case it's a recordset of many2many fields (list of records), return list of ids
                        item[field] = [rec.id for rec in value] if value else []
                    else:
                        item[field] = value
            result.append(item)
        
        return http.Response(
            json.dumps({'status': 'success', 'data': result}),
            content_type='application/json',
            status=200
        )

    @http.route('/api/sale_man/test-auth', type='http', auth='public', method=['GET'], csrf=False)
    def test_auth(self, **kwargs):
        """Test endpoint to debug API key authentication"""
        try:
            # Get Authorization header
            auth_header = request.httprequest.headers.get('Authorization', '')
            
            debug_info = {
                'auth_header': auth_header,
                'all_headers': dict(request.httprequest.headers),
                'api_keys_in_db': []
            }
            
            # Get all API keys from database for debugging using raw SQL
            request.env.cr.execute("""
                SELECT id, name, user_id, index, scope, expiration_date
                FROM res_users_apikeys
                ORDER BY id
            """)

            api_keys_data = request.env.cr.fetchall()
            for key_data in api_keys_data:
                key_id, name, user_id, index, scope, expiration_date = key_data
                user = request.env['res.users'].sudo().browse(user_id)
                debug_info['api_keys_in_db'].append({
                    'id': key_id,
                    'name': name,
                    'index': index,
                    'user_id': user.name,
                    'user_active': user.active,
                    'has_sales_manager': user.has_group('sales_team.group_sale_manager'),
                    'scope': scope,
                    'expiration_date': expiration_date.isoformat() if expiration_date else None
                })
            
            return http.Response(
                json.dumps(debug_info, indent=2),
                content_type='application/json',
                status=200
            )
        except Exception as e:
            return http.Response(
                json.dumps({'error': str(e)}),
                content_type='application/json',
                status=500
            )