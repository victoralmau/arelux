# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class WasteRemoveDetail(models.Model):
    _name = 'waste.remove.detail'
    _description = 'Waste Remove Detail'        

    waste_remove_id = fields.Many2one(
        comodel_name='waste.remove',
        string='Retirada'
    )
    waste_remove_product_id = fields.Many2one(
        comodel_name='waste.remove.product',
        string='Producto'
    )
    quantity = fields.Integer(        
        string='Cantidad'
    )                                                        