# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    installer_id = fields.Many2one(
        comodel_name='res.partner',         
        string='Instalador',
        domain="[('installer', '=', True)]"
    )                                                                           