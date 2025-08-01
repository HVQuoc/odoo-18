from odoo import models, fields, api

class Provider(models.Model):
    _name = 'sale_man.provider'
    _description = 'Provider'
    _rec_name = 'name_vi'
    _inherit = 'sale_man.address_mixin'

    name_vi = fields.Char(string="Vietnamese Name", required=True)
    name_en = fields.Char(string="English Name")
    short_name = fields.Char(string="Short Name")
    representative = fields.Char(string="Representative")
    stk = fields.Char(string="Bank Account Number")
    depot_code = fields.Char(string="Depot Code")
    mst = fields.Char(string="Tax Code")
    bank_name = fields.Char(string="Bank Name")
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string="Status", default='active')
