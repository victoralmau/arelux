# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model
    def define_account_invoice_line_header_info_commission(self):
        res = super(
            AccountInvoiceLine, self
        ).define_account_invoice_line_header_info_commission()
        res['ar_qt_activity_type'] = _('Activity type')
        return res

    @api.multi
    def define_account_invoice_line_info_commission(self):
        res = super(
            AccountInvoiceLine, self
        ).define_account_invoice_line_info_commission()
        for item in self:
            item['ar_qt_activity_type'] = item.invoice_id.ar_qt_activity_type
        return res
