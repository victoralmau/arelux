# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def account_invoice_auto_send_mail_item_real(self, mail_template_id, author_id):
        self.ensure_one()
        # change mail_template_id
        if self.ar_qt_activity_type == 'arelux':
            template_id = self.journal_id.invoice_mail_template_id_arelux
        elif self.ar_qt_activity_type == 'todocesped':
            template_id = self.journal_id.invoice_mail_template_id_todocesped
        elif self.ar_qt_activity_type == 'evert':
            template_id = self.journal_id.invoice_mail_template_id_evert
        elif self.ar_qt_activity_type == 'both':
            template_id = self.journal_id.invoice_mail_template_id_both
        else:
            template_id = self.journal_id.invoice_mail_template_id_arelux
        # account_invoice_auto_send_mail_item_real
        return super(AccountInvoice, self).account_invoice_auto_send_mail_item_real(
            template_id,
            author_id
        )
