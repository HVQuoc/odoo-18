from odoo import models, fields, api

class Product(models.Model):
    _name = 'product_program.product'
    _description = 'Product'

    name = fields.Char(required=True)
    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='/')
    image = fields.Image()
    brand_id = fields.Many2one('product_program.brand', required=True)
    price = fields.Float()

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('product_program.brand') or '/'
        return super().create(vals)
