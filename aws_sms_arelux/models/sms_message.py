# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SmsMessage(models.Model):
    _inherit = 'sms.message'

    @api.multi
    def action_send_real(self):
        self.ensure_one()
        # override sender
        if self.model_id and self.res_id:
            model_item_ids = self.env[self.model_id.model].sudo().search(
                [
                    ('id', '=', self.res_id)
                ]
            )
            if model_item_ids:
                model_item_id = model_item_ids[0]
                if 'ar_qt_activity_type' in model_item_id:
                    if model_item_id['ar_qt_activity_type'] == 'todocesped':
                        self.sender = 'Todocesped'
                    elif model_item_id['ar_qt_activity_type'] == 'arelux':
                        self.sender = 'Arelux'
        # return
        return super(SmsMessage, self).action_send_real()
