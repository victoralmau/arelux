# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

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