from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'sale_man.order'
    _description = 'Order'

    order_time = fields.Datetime(string="Order Time", default=fields.Datetime.now, required=True)
    receiver_tel = fields.Char(string="Receiver Telephone")
    voucher_code = fields.Char(string="Voucher Code")
    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='/')
    order_status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string="Order Status", default='draft', required=True)
    tracking_number = fields.Char(string="Tracking Number")
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ], string="Payment Status", default='pending')
    transaction_code = fields.Char(string="Transaction Code")
    error_content = fields.Text(string="Error Content", default="/")
    program = fields.Many2one('sale_man.program', string="Program")
    transportation_company = fields.Many2one('sale_man.trans_co', string="Transportation Company")
    order_line_ids = fields.One2many('sale_man.order_line', 'order_id', string="Order Lines")
    total_amount = fields.Float(string="Total Value", compute="_compute_total_amount", store=True)

    @api.depends('order_line_ids.price_subtotal')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.price_subtotal for line in record.order_line_ids)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique!')
    ]

    def _validate_order_lines(self):
        """Validate that each order line's quantity does not exceed the product's available quantity."""
        for order in self:
            for line in order.order_line_ids:
                if not line.product_id:
                    continue  # Skip lines without a product
                if line.quantity > line.product_id.quantity:
                    raise ValidationError(
                        f"The quantity ({line.quantity}) for product '{line.product_id.name_vi}' "
                        f"exceeds the available quantity ({line.product_id.quantity})."
                    )

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('sale_man.order') or '/'
        # Create the order and validate order lines
        order = super(Order, self).create(vals)
        order._validate_order_lines()
        return order

    def write(self, vals):
        # Update the order and validate order lines
        res = super(Order, self).write(vals)
        self._validate_order_lines()
        return res

