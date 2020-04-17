# -*- coding: utf-8 -*-
from openerp import api, models, fields
from dateutil.relativedelta import relativedelta
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
        
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
    
    @api.onchange('partner_shipping_id')
    def onchange_partner_shipping_id(self):
        if self.partner_id.id>0:
            if self.opportunity_id.id==0:
                self.ar_qt_activity_type = self.partner_id.ar_qt_activity_type
                self.ar_qt_customer_type = self.partner_id.ar_qt_customer_type
                
    @api.onchange('opportunity_id')
    def onchange_opportunity_id(self):
        if self.opportunity_id.id>0:
            self.ar_qt_activity_type = self.opportunity_id.ar_qt_activity_type
            self.ar_qt_customer_type = self.opportunity_id.ar_qt_customer_type                        
        
    @api.model
    def create(self, values):   
        return_val = super(SaleOrder, self).create(values)
        #operations
        if return_val.opportunity_id.id>0:
            #ar_qt_activity_type
            if return_val.ar_qt_activity_type==False:
                return_val.ar_qt_activity_type = return_val.opportunity_id.ar_qt_activity_type
            #ar_qt_customer_type
            if return_val.ar_qt_customer_type==False:
                return_val.ar_qt_customer_type = return_val.opportunity_id.ar_qt_customer_type
        #return
        return return_val
        
    @api.multi
    def write(self, vals):
        allow_write = True                        
        #fix validate template_id
        if 'template_id' in vals:
            if vals['template_id']!=False:
                template_id_check = vals['template_id']            
                sale_quote_template_obj = self.env['sale.quote.template'].browse(template_id_check)
                if sale_quote_template_obj.ar_qt_activity_type!=False:
                    if sale_quote_template_obj.ar_qt_activity_type!=self.ar_qt_activity_type:
                        allow_write = False
                        raise Warning("La plantilla de presupuesto no corresponde con el tipo de actividad")                    
        #allow_write                
        if allow_write==True:                        
            return_object = super(SaleOrder, self).write(vals)                        
            return return_object                                                                                               