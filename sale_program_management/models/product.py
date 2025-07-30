from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class Product(models.Model):
    _name = 'sale_man.product'
    _description = 'Product'

    name_vi = fields.Char(required=True)
    name_en = fields.Char(required=True)


    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='/')
    image = fields.Image()

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
