from odoo import models, fields, api

class PurchaseLine(models.Model):
    _name = 'sale_man.purchase_line'
    _description = 'Purchase Line'

    purchase_id = fields.Many2one('sale_man.purchase', string="Purchase", required=True, ondelete='cascade')
    product_id = fields.Many2one('sale_man.product', string="Product", required=True)
    quantity = fields.Integer(string="Quantity", default=0, required=True)
    return_count = fields.Integer(string="Quantity", default=0, required=True)
    cost = fields.Float(string="Cost", required=True)
    price_unit = fields.Float(string="Unit Price", required=True)
    price_subtotal = fields.Float(string="Subtotal", compute="_compute_price_subtotal", store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = (line.quantity - line.return_count) * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Fetch the product's list price when product_id changes."""
        if self.product_id:
            self.price_unit = self.product_id.list_price

    @api.constrains('status')
    def _update_product_quantity(self):
        for record in self:
            if record.status == 'received' and record._origin.status != 'received':
                for line in record.purchase_line_ids:
                    if line.quantity > line.return_count:
                        line.product_id.quantity += (line.quantity - line.return_count)
            elif record._origin.status == 'received' and record.status != 'received':
                for line in record.purchase_line_ids:
                    if line.quantity > line.return_count:
                        new_quantity = line.product_id.quantity - (line.quantity - line.return_count)
                        if new_quantity < 0:
                            raise ValidationError(f"Cannot reduce quantity of {line.product_id.name} below 0.")
                        line.product_id.quantity = new_quantity