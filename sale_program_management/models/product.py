from odoo import models, fields, api
import logging
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class Product(models.Model):
    _name = 'sale_man.product'
    _description = 'Product'
    _rec_name = 'display_name'

    name_vi = fields.Char(required=True)
    name_en = fields.Char(required=True)


    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='/')
    image = fields.Image()

    list_price = fields.Float(string="Sale Price", default=0.0, required=True)
    cost = fields.Float(string="Cost", default=0.0, required=True)
    quantity = fields.Integer(string="Quantity", default=0, required=True)
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=False)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string="Status", default='active')

    brand_id = fields.Many2one('sale_man.brand', required=True)
    category_id = fields.Many2one(
        'sale_man.category',
    )

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('sale_man.product') or '/'
            _logger.info('1')
            _logger.info(self.env['ir.sequence'].next_by_code('sale_man.product'))
        return super(Product, self).create(vals)

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationError("Available quantity cannot be negative.")

    @api.depends('name_vi', 'name_en')
    def _compute_display_name(self):
        lang = self.env.context.get('lang', 'en_US')  # Get user's language from context
        for record in self:
            if lang.startswith('vi'):  # Check if language is Vietnamese
                record.display_name = record.name_vi or record.name_en or ''
            else:  # Default to English or other languages
                record.display_name = record.name_en or record.name_vi or ''