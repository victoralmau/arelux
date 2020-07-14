# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class SaleQuoteTemplate(models.Model):
    _inherit = 'sale.quote.template'
    
    delivery_carrier_id = fields.Many2one(
        comodel_name='delivery.carrier', 
        string='Metodo de envio',
    )