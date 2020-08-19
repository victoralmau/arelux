# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        return_action = super(AccountInvoice, self).action_invoice_open()
        # action_regenerate_commission_percent_lines
        for item in self:
            item.remove_mail_follower_ids()
        # return
        return return_action

    @api.multi
    def remove_mail_follower_ids(self):
        partner_ids_exclude = [
            self.env.ref('base.res_partner_1').id,
            self.env.ref('base.res_partner_2').id,
            self.env.ref('base.res_partner_12').id
        ]
        for item in self:
            if item.partner_id.id not in partner_ids_exclude:
                if item.user_id:
                    for message_follower_id in item.message_follower_ids:
                        if message_follower_id.partner_id.user_ids:
                            for user_id in message_follower_id.partner_id.user_ids:
                                if user_id.id != item.user_id.id or user_id.id == 1:
                                    message_follower_id.sudo().unlink()
