from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PurchaseLine(models.Model):
    _name = 'sale_man.purchase_line'
    _description = 'Purchase Line'

    purchase_id = fields.Many2one('sale_man.purchase', string="Purchase", required=True, ondelete='cascade')
    product_id = fields.Many2one('sale_man.product', string="Product", required=True, domain="[('status', '=', 'active')]")
    quantity = fields.Integer(string="Quantity", default=0, required=True)
    return_count = fields.Integer(string="Return Count", default=0, required=True)
    price_unit = fields.Float(string="Unit Price", required=True)
    price_subtotal = fields.Float(string="Subtotal", compute="_compute_price_subtotal", store=True)

    @api.depends('quantity', 'price_unit', 'return_count')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = (line.quantity - line.return_count) * line.price_unit if line.quantity >= line.return_count else 0.0

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Fetch the product's list price when product_id changes."""
        if self.product_id:
            self.price_unit = self.product_id.list_price

    @api.constrains('return_count', 'quantity')
    def _check_return_count(self):
        for line in self:
            if line.return_count > line.quantity:
                raise ValidationError("Return count cannot exceed quantity.")