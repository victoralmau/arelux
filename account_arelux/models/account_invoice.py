# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    hide_fiscal_position_description = fields.Boolean(
        string='Hide fiscal position message',
        default=False
    )
    # override date
    date = fields.Date(
        string='Date',
        copy=False,
        help="Leave empty to use the invoice date",
        track_visibility='always',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )

    @api.model
    def create(self, values):
        obj = super(AccountInvoice, self).create(values)
        # Fix payment_mode_id
        if obj.payment_mode_id:
            if obj.payment_mode_id.payment_method_id.mandate_required:
                if obj.partner_id.bank_ids:
                    for bank_id in obj.partner_id.bank_ids:
                        if bank_id.mandate_ids:
                            for mandate_id in bank_id.mandate_ids:
                                if mandate_id.state == 'valid':
                                    obj.mandate_id = mandate_id.id

        partner_ids_exclude = [
            self.env.ref('base.res_partner_1').id,
            self.env.ref('base.res_partner_2').id,
            self.env.ref('base.res_partner_12').id
        ]
        if obj.partner_id.id not in partner_ids_exclude:
            obj.check_message_follower_ids()
        return obj

    @api.multi
    def write(self, vals):
        # write
        return_object = super(AccountInvoice, self).write(vals)
        # check_message_follower_ids
        partner_ids_exclude = [
            self.env.ref('base.res_partner_1').id,
            self.env.ref('base.res_partner_2').id,
            self.env.ref('base.res_partner_12').id
        ]
        for item in self:
            if item.partner_id.id not in partner_ids_exclude:
                item.check_message_follower_ids()
        # return
        return return_object

    @api.multi
    def check_message_follower_ids(self):
        partner_ids_exclude = [
            self.env.ref('base.res_partner_1').id,
            self.env.ref('base.res_partner_2').id,
            self.env.ref('base.res_partner_12').id
        ]
        for item in self:
            if item.partner_id.id not in partner_ids_exclude:
                if item.user_id.id:
                    for message_follower_id in item.message_follower_ids:
                        if message_follower_id.partner_id.user_ids:
                            for user_id in message_follower_id.partner_id.user_ids:
                                if user_id.id == item.user_id.id or user_id.id == 1:
                                    message_follower_id.sudo().unlink()

    @api.multi
    def action_send_account_invoice_create_message_slack(self):
        return True

    @api.multi
    def action_send_account_invoice_out_refund_create_message_slack(self):
        return True
