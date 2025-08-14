from odoo import models, fields

class ProductReportExcel(models.TransientModel):
    _name = 'sale_man.product.report.excel'
    _description = 'Product Excel Report'

    excel_file = fields.Binary('Excel File')
    file_name = fields.Char('Filename', size=256)