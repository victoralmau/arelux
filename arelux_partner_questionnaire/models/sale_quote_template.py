# -*- coding: utf-8 -*-
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class SaleQuoteTemplate(models.Model):
    _inherit = 'sale.quote.template'
    
    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),
            ('both', 'Ambos'),                    
        ],
        size=15, 
        string='Tipo de actividad'
    )                                                                                                                                                                    