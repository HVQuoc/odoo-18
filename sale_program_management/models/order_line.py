from odoo import models, fields, api

class OrderLine(models.Model):
    _name = 'sale_man.order_line'
    _description = 'Order Line'

    order_id = fields.Many2one('sale_man.order', string="Order", required=True, ondelete='cascade')
    product_id = fields.Many2one('sale_man.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", default=1.0, required=True)
    price_unit = fields.Float(string="Unit Price", required=True)
    price_subtotal = fields.Float(string="Subtotal", compute="_compute_price_subtotal", store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Fetch the product's list price when product_id changes."""
        if self.product_id:
            self.price_unit = self.product_id.list_price