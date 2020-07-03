# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import fields, models, api, _

import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.one    
    def action_send_account_invoice_out_refund(self):
        return_object = super(StockPicking, self).action_send_account_invoice_out_refund()
        #save_log
        automation_log_vals = {                    
            'model': 'account.invoice',
            'res_id': self.out_refund_invoice_id.id,
            'category': 'account_invoice',
            'action': 'create',                                                                                                                                                                                           
        }
        automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
        #return
        return return_object