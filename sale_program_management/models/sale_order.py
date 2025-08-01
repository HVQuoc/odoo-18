from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

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

    @api.model
    def create(self, vals):
        if not vals.get('po_number'):
            vals['po_number'] = self.env['ir.sequence'].next_by_code('sale_man.sale_order') or '/'
        return super(SaleOrder, self).create(vals)