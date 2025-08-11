from odoo import models, fields

class Company(models.Model):
    _name = 'sale_man.company'
    _description = 'Company'

    name = fields.Char(string='Company Name', required=True)
    address = fields.Char(string='Address')
    phone = fields.Char(string='Phone')
    tax_code = fields.Char(string='Tax ID')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')