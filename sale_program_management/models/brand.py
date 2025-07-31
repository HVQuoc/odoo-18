from odoo import models, fields, api

class Brand(models.Model):
    _name = 'sale_man.brand'
    _description = 'Brand'
    _rec_name = 'name_vi'

    name_vi = fields.Char(required=True)
    name_en = fields.Char()

    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='/')
    image = fields.Image()
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string="Status", default='active')


    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('sale_man.brand') or '/'
        return super().create(vals)
