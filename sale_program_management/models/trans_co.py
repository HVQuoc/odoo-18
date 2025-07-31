from odoo import models, fields

class TransCo(models.Model):
    _name = 'sale_man.trans_co'
    _description = 'Transportation Company'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    api_link = fields.Char(string="API link")
    token = fields.Char(string="Token")
    private_key = fields.Char(string="Private key")
    login_user = fields.Char(string="Login User")
    login_password = fields.Char(string="Login Password")
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string="Status", default='active')