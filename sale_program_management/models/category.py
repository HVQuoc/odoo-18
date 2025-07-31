from odoo import models, fields, api

class Category(models.Model):
    _name = 'sale_man.category'
    _description = 'Category'
    _rec_name = 'name_en'

    name_vi = fields.Char(required=True)
    name_en = fields.Char(required=True)
    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='/')
    image = fields.Image()

    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string="Status", default='active')

    parent_id = fields.Many2one('sale_man.category', string="Parent Category")
    child_ids = fields.One2many('sale_man.category', 'parent_id', string="Subcategories")
    product_ids = fields.Many2many(
        'sale_man.product',
        'sale_man_category_product_rel',
        'category_id',
        'product_id',
        string="Products"
    )

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('sale_man.category') or '/'
        return super().create(vals)

    def name_get(self):
        """Display name_vi in the many2many_tags widget."""
        result = []
        for record in self:
            result.append((record.id, record.name_vi))
        return result