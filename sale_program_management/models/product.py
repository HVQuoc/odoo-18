from odoo import models, fields, api
import logging
from odoo.exceptions import ValidationError
import io
import base64
import xlsxwriter

_logger = logging.getLogger(__name__)

class Product(models.Model):
    _name = 'sale_man.product'
    _description = 'Product'
    _rec_name = 'display_name'

    name_vi = fields.Char(string="Vietnamese Name", required=True)
    name_en = fields.Char(string="English Name", required=True)
    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='/')
    image = fields.Image(string="Image")
    list_price = fields.Float(string="Sale Price", default=0.0, required=True)
    cost = fields.Float(string="Cost", default=0.0, required=True)
    quantity = fields.Integer(string="Quantity", default=0, required=True)
    display_name = fields.Char(string="Display Name", compute='_compute_display_name', store=False)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string="Status", default='active')
    brand_id = fields.Many2one('sale_man.brand', string="Brand", required=True)
    category_id = fields.Many2one('sale_man.category', string="Category", domain="[('status', '=', 'active')]")

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('sale_man.product') or '/'
            _logger.info('Generated code: %s', vals['code'])
        return super(Product, self).create(vals)

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationError("Available quantity cannot be negative.")

    @api.depends('name_vi', 'name_en')
    def _compute_display_name(self):
        lang = self.env.context.get('lang', 'en_US')
        for record in self:
            if lang.startswith('vi'):
                record.display_name = record.name_vi or record.name_en or ''
            else:
                record.display_name = record.name_en or record.name_vi or ''

    def action_export_excel(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Products')

        # Define custom formats
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#4CAF50',
            'align': 'center',
            'valign': 'vcenter'
        })

        # Define the header titles
        headers = ['Name (VI)', 'Name (EN)', 'Code', 'Sale Price', 'Cost', 'Quantity', 'Status']

        # Write the header row
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        # Write the data rows
        row_num = 1
        for product in self.search([]):
            worksheet.write(row_num, 0, product.name_vi)
            worksheet.write(row_num, 1, product.name_en)
            worksheet.write(row_num, 2, product.code)
            worksheet.write(row_num, 3, product.list_price)
            worksheet.write(row_num, 4, product.cost)
            worksheet.write(row_num, 5, product.quantity)
            worksheet.write(row_num, 6, product.status)
            row_num += 1

        workbook.close()
        output.seek(0)

        file_content = base64.b64encode(output.read())
        filename = "Physical_Gift_Orders_%s.xlsx" % fields.Datetime.now().strftime("%Y%m%d_%H%M%S")

        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": file_content,
            "res_model": "physical.gift.order",
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=1",
            "target": "self",
        }