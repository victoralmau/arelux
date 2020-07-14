# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.multi
    def send_mail(self, auto_commit=False):
        if self._context.get('default_model') == 'sale.order' and self._context.get('default_res_id') and self._context.get('mark_so_as_sent'):
            order = self.env['sale.order'].browse([self._context['default_res_id']])
            #date_order_send_mail
            if order.date_order_send_mail==False:
                order.date_order_send_mail = fields.datetime.now()
        #send_mail                
        return super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)
