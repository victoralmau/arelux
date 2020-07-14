# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    def action_invoice_open(self):
        return_action = super(AccountInvoice, self).action_invoice_open()
        # action_regenerate_commission_percent_lines
        self.remove_mail_follower_ids()
        # return
        return return_action

    @api.one
    def remove_mail_follower_ids(self):
        if self.user_id.id>0:
            for message_follower_id in self.message_follower_ids:
                if message_follower_id.partner_id.user_ids != False:
                    for user_id in message_follower_id.partner_id.user_ids:
                        if user_id.id!=self.user_id.id or user_id.id==1:
                            message_follower_id.sudo().unlink()