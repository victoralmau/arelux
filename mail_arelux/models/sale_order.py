# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.one
    def write(self, vals):
        return_object = super(SaleOrder, self).write(vals)
        # check_message_follower_ids
        self.remove_mail_follower_ids()
        # return
        return return_object

    @api.one
    def remove_mail_follower_ids(self):
        if self.user_id:
            for message_follower_id in self.message_follower_ids:
                if message_follower_id.partner_id.user_ids:
                    for user_id in message_follower_id.partner_id.user_ids:
                        if user_id.id != self.user_id.id or user_id.id == 1:
                            message_follower_id.sudo().unlink()