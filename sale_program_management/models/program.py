from odoo import models, fields, api

class Program(models.Model):
    _name = 'sale_man.program'
    _description: 'Program'

    name_vi = fields.Char(string='Name', required=True)
    name_en = fields.Char(string='Name', required=True)

    company_id = fields.Many2one('sale_man.company', string='Company', required=True)
    creator_id = fields.Many2one('res.users', string='Creator', default=lambda self: self.env.user, required=True)

    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='/')

    category_ids = fields.Many2many(
        'sale_man.category',
        'sale_man_program_category_rel',  # relation table name
        'program_id',  # this model’s FK
        'category_id',  # target model’s FK
        string='Gift Categories'
    )

    product_ids = fields.Many2many(
        'sale_man.product',
        'sale_man_program_product_rel',
        'program_id',
        'product_id',
        string='Gifts'
    )

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('sale_man.program') or '/'
        vals['creator_id'] = self.env.uid  # Gán user hiện tại làm creator
        return super().create(vals)