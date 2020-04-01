# -*- coding: utf-8 -*-
from openerp import api, models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    installer_id = fields.Many2one(
        comodel_name='res.partner',         
        string='Instalador',
        domain="[('installer', '=', True)]"
    )                                                                           