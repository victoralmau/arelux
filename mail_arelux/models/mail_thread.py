# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'
        
    @api.multi
    def _message_auto_subscribe_notify(self, partner_ids):
        not_notify = False
        
        for record in self:
            if record._name=='sale.order':
                if record.opportunity_id.id!=False and record.opportunity_id.user_id.id==False:#Fix leads 3 emails (lead + 2 sale.order)
                    not_notify = True
            elif record._name=='account.invoice':
                not_notify = True
                                                                                                                 
            if record._name=='crm.lead' and record.ar_qt_activity_type=='arelux':
                not_notify = True
            elif record._name=='sale.order' and record.ar_qt_activity_type=='arelux':
                not_notify = True
                                                                
            if not_notify==False:            
                return super(MailThread, self)._message_auto_subscribe_notify(partner_ids)
            else:
                return False