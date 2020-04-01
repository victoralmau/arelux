# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
import json

import logging
_logger = logging.getLogger(__name__)

class AreluxSaleReportLineUser(models.Model):
    _name = 'arelux.sale.report.line.user'
    _description = 'Arelux Sale Report Line User'    
        
    arelux_sale_report_line_id = fields.Many2one(
        comodel_name='arelux.sale.report.line',
        string='Arelux Sale Report Line'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User Id'
    )
    count = fields.Integer(
        string='Count'
    )
    percent = fields.Float(
        string='Percent'
    )
    amount_untaxed = fields.Float(
        string='Amount Untaxed'
    )