from odoo import models, fields, api

class Category(models.Model):
    _name = 'product_program.category'
    _description = 'Product Category'

    name = fields.Char(required=True)
    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='/')
    image = fields.Image()
    parent_id = fields.Many2one('product_program.category', string="Parent Category")
    child_ids = fields.One2many('product_program.category', 'parent_id', string="Subcategories")

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('product_program.category') or '/'
        return super().create(vals)