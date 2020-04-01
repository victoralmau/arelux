# -*- coding: utf-8 -*-
from openerp import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'
                    
    @api.one
    @api.depends('model', 'res_id')        
    def _get_ar_qt_activity_type(self):                    
        if self.model!=False and self.res_id!=False and self.res_id>0:         
            model_item = self.env[self.model].search([('id', '=', self.res_id)])[0]            
            if 'ar_qt_activity_type' in model_item:
                self.ar_qt_activity_type = model_item.ar_qt_activity_type
                
    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),                    
        ],
        compute='_get_ar_qt_activity_type',
        size=15, 
        string='Tipo de actividad'
    )                             