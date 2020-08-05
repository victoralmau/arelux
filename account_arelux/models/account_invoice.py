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
        # Override the original create function for the res.partner model
        if 'origin' in values and values['origin']:
            order_ids = self.env['sale.order'].search(
                [
                    ('name', '=', values['origin'])
                ]
            )
            if order_ids:
                for order_id in order_ids:
                    if order_id.payment_mode_id:
                        values['payment_mode_id'] = order_id.payment_mode_id.id

                        if order_id.payment_mode_id.payment_method_id.mandate_required:
                            if order_id.partner_id.bank_ids:
                                for bank_id in order_id.partner_id.bank_ids:
                                    if bank_id.mandate_ids:
                                        for mandate_id in bank_id.mandate_ids:
                                            if mandate_id.state == 'valid':
                                                values['mandate_id'] = mandate_id.id
        # create
        return_object = super(AccountInvoice, self).create(values)
        self.check_message_follower_ids()
        return return_object

    @api.multi
    def write(self, vals):
        # write
        return_object = super(AccountInvoice, self).write(vals)
        # check_message_follower_ids
        self.check_message_follower_ids()
        # return
        return return_object

    @api.multi
    def check_message_follower_ids(self):
        for item in self:
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
