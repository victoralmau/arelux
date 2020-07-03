# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class WasteRemoveProduct(models.Model):
    _name = 'waste.remove.product'
    _description = 'Waste Remove Product'        

    name = fields.Char(        
        string='Nombre'
    )
    uom = fields.Char(        
        string='Unidad de medida'
    )                                                    