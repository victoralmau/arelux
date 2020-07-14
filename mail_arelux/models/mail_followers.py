# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class MailFollowers(models.Model):
    _inherit = 'mail.followers'

    @api.model
    def create(self, values):
        need_return = True                                               
        return_val = super(MailFollowers, self).create(values)
        
        if return_val.partner_id.user_ids!=False:
            user_id_check = 0
            for user_id in return_val.partner_id.user_ids:
                user_id_check = user_id.id 
            #operations                
            if return_val.res_model=='sale.order':  
                res_model_ids = self.env[return_val.res_model].search([('id', '=', return_val.res_id)])
                for res_model_id in res_model_ids:
                    if res_model_id.user_id.id!=False:
                        if return_val.partner_id.user_ids!=False:
                            if user_id_check!=res_model_id.user_id.id:
                                return_val.unlink()
                                need_return = False
                                    
            elif return_val.res_model=='account.invoice':
                res_model_ids = self.env[return_val.res_model].search([('id', '=', return_val.res_id)])
                for res_model_id in res_model_ids:
                    if res_model_id.user_id.id!=False:
                        if return_val.partner_id.user_ids!=False:
                            if user_id_check==res_model_id.user_id.id:
                                return_val.unlink()
                                need_return = False                            
        #need_return
        if need_return==True:                                
            return return_val