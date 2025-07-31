from odoo import models, fields, api

class Address(models.Model):
    _name = 'provider.address'
    _description = 'Provider Address'

    province_id = fields.Many2one(
        'res.country.state',
        string='Province'
    )
    district_id = fields.Many2one(
        'res.country.district',
        string='District'
    )
    ward_id = fields.Many2one(
        'res.country.ward',
        string='Ward',
    )
    street = fields.Char(string='Street', required=True)
    full_address = fields.Char(
        string='Full Address',
        compute='_compute_full_address',
        store=True
    )
    provider_ids = fields.Many2many(
        'provider.provider',
        string='Providers',
        help='Providers associated with this address'
    )

    @api.depends('street', 'ward_id', 'district_id', 'province_id')
    def _compute_full_address(self):
        for record in self:
            address_parts = [
                record.street or '',
                record.ward_id.name or '',
                record.district_id.name or '',
                record.province_id.name or ''
            ]
            record.full_address = ', '.join(part for part in address_parts if part)