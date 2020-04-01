# -*- coding: utf-8 -*-
from openerp import api, models, fields
from dateutil.relativedelta import relativedelta
from datetime import datetime

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