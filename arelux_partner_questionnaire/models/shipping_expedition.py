# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class ShippingExpedition(models.Model):
    _inherit = 'shipping.expedition'
        
    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),                  
        ],
        size=15, 
        string='Tipo de actividad'
    )
    ar_qt_customer_type = fields.Selection(
        [
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),        
        ],        
        string='Tipo de cliente',
    )
    
    @api.model
    def create(self, vals):
        return_shipping_expedition = super(ShippingExpedition, self).create(vals)
        
        return_shipping_expedition.ar_qt_activity_type = 'todocesped'
        return_shipping_expedition.ar_qt_customer_type = 'particular'
        
        if return_shipping_expedition.picking_id.id>0:
            if return_shipping_expedition.picking_id.ar_qt_activity_type!=False:
                if return_shipping_expedition.picking_id.ar_qt_activity_type!='both':
                    return_shipping_expedition.ar_qt_activity_type = return_shipping_expedition.picking_id.ar_qt_activity_type
                    
            if return_shipping_expedition.picking_id.ar_qt_customer_type!=False:
                return_shipping_expedition.ar_qt_customer_type = return_shipping_expedition.picking_id.ar_qt_customer_type
                                                        
        return return_shipping_expedition                                                                           