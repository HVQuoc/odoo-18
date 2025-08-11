from odoo import models, fields, api

class AddressMixin(models.AbstractModel):
    _name = 'sale_man.address_mixin'
    _description = 'Address Mixin'
    _abstract = True

    street = fields.Char(string="Street")
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state', string='Province',
                               domain="[('country_id', '=', country_id)]")
    district_id = fields.Many2one(comodel_name='res.country.district', string='District',
                                  domain="[('state_id', '=', state_id)]")
    ward_id = fields.Many2one(comodel_name='res.country.ward', string='Ward',
                              domain="[('district_id', '=', district_id)]")

    @api.onchange('country_id')
    def _onchange_country_id(self):
        """Reset all address subfields when country_id changes."""
        if self.country_id and self.state_id and self.state_id.country_id != self.country_id:
            self.state_id = False
            self.district_id = False
            self.ward_id = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        """Reset district, ward, and street when state_id changes."""
        if self.state_id and self.district_id and self.district_id.state_id != self.state_id:
            self.ward_id = False
            self.street = False

    @api.onchange('district_id')
    def _onchange_district(self):
        """Reset ward and street when district changes."""
        if self.district_id and self.ward_id and self.ward_id.district_id != self.district_id:
            self.ward_id = False