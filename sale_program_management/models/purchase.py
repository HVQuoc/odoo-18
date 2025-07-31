from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Purchase(models.Model):
    _name = 'sale_man.purchase'
    _description = 'Purchase'

    purchase_date = fields.Datetime(string="Purchase Date", default=fields.Datetime.now, required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', required=True)
    vat = fields.Float(string="VAT", digits=(10, 2), required=True)
    total_quantity = fields.Integer(string="Total Quantity", compute='_compute_total_quantity', store=True)
    total_amount = fields.Float(string="Total Value", compute="_compute_total_amount", store=True)
    total_return = fields.Integer(string="Total Return", compute='_compute_total_return', store=True)
    total_remain = fields.Float(string="Total Remain", compute='_compute_total_remain', store=True)

    purchase_line_ids = fields.One2many('sale_man.purchase_line', 'purchase_id', string="Purchase Lines")
    provider = fields.Many2one('sale_man.provider', string="Provider")
    program = fields.Many2one('sale_man.program', string="Program")

    @api.depends('purchase_line_ids.price_subtotal')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.price_subtotal for line in record.purchase_line_ids)

    @api.depends('purchase_line_ids.quantity')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity = sum(line.quantity for line in record.purchase_line_ids)

    @api.depends('purchase_line_ids.return_count')
    def _compute_total_return(self):
        for record in self:
            record.total_return = sum(line.return_count for line in record.purchase_line_ids)

    @api.depends('total_quantity', 'total_return')
    def _compute_total_remain(self):
        for record in self:
            record.total_remain = record.total_quantity - record.total_return

