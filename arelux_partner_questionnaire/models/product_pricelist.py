# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),
            ('both', 'Ambos'),        
        ],
        size=15, 
        string='Tipo de actividad', 
        default='todocesped'
    )
    
    ar_qt_customer_type = fields.Selection(
        [
            ('all', 'Todos'),
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),        
        ], 
        string='Tipo de cliente',
    )
    state_ids = fields.Many2many(
        comodel_name='res.country.state', 
        string='Provincias',
    )