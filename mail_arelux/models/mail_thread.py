# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.multi
    def _message_auto_subscribe_notify(self, partner_ids, template):
        not_notify = False
        for item in self:
            if item._name == 'sale.order':
                if item.opportunity_id and not item.opportunity_id.user_id.id:
                    not_notify = True
            elif item._name == 'account.invoice':
                not_notify = True
            if item._name == 'crm.lead' and item.ar_qt_activity_type == 'arelux':
                not_notify = True
            elif item._name == 'sale.order' and item.ar_qt_activity_type == 'arelux':
                not_notify = True

            if not not_notify:
                return super(MailThread, self)._message_auto_subscribe_notify(
                    partner_ids, template
                )
            else:
                return False
