# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
import json

import logging
_logger = logging.getLogger(__name__)

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