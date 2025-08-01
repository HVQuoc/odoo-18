from odoo import fields, models, api

class CustomSaleOrder(models.Model):
    _inherit = ['sale.order']

    po_number = fields.Char(string="PO Number", required=True, copy=False, readonly=True, default='/')
    po_path = fields.Char(string="PO Path")

    print_legal = fields.Selection(
        selection=[
            ('dayone', 'Dayone'),
            ('standard', 'Standard'),
            ('none', 'None'),
        ],
        string='Print Legal',
        default='dayone'
    )

    order_type = fields.Selection(
        selection=[
            ('normal', 'Normal'),
            ('urgent', 'Urgent'),
            ('backorder', 'Backorder'),
        ],
        string='Order Type',
        default='normal',
        required=True
    )

    order_status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ],
        string='Order Status',
        default='draft',
        required=True
    )

    receiver_name = fields.Char(string="Receiver Name")
    receiver_email = fields.Char(string="Receiver Email")
    receiver_phone = fields.Char(string="Receiver Phone")

    delivery_code = fields.Char(string='Delivery Code', readonly=True)
    delivery_note = fields.Text(string='Delivery Note')

    street = fields.Char(string="Street")
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state', string='Province',
                               domain="[('country_id', '=', country_id)]")
    district_id = fields.Many2one(comodel_name='res.country.district', string='District',
                                  domain="[('state_id', '=', state_id)]")
    ward_id = fields.Many2one(comodel_name='res.country.ward', string='Ward',
                              domain="[('district_id', '=', district_id)]")

    @api.model
    def create(self, vals):
        if not vals.get('po_number'):
            vals['po_number'] = self.env['ir.sequence'].next_by_code('sale_man.sale_order') or '/'
        return super(CustomSaleOrder, self).create(vals)

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