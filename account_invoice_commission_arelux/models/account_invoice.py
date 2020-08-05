# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_regenerate_commission_percent_lines(self):
        res = super(AccountInvoice, self).action_regenerate_commission_percent_lines()
        # override
        for item in self:
            for invoice_line_id in item.invoice_line_ids:
                if invoice_line_id.commission_percent > 0:
                    if item.ar_qt_activity_type == 'evert':
                        invoice_line_id.commission_percent = 1
        # return
        return res
