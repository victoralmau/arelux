# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AreluxSaleReportLineSaleOrder(models.Model):
    _name = 'arelux.sale.report.line.sale.order'
    _description = 'Arelux Sale Report Line Sale Order'    
        
    arelux_sale_report_line_id = fields.Many2one(
        comodel_name='arelux.sale.report.line',
        string='Arelux Sale Report Line'
    )
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order'
    )    