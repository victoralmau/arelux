# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class PhoneCallLog(models.Model):
    _inherit = 'phone.call.log'

    @api.model
    def operations_item(self):
        res = super(PhoneCallLog, self).operations_item()
        if self.lead_id:
            if not self.lead_id.is_revision:
                if self.lead_id.ar_qt_activity_type == 'todocesped':
                    if self.lead_id.ar_qt_customer_type == 'particular':
                        expedition_ids = self.env['shipping.expedition'].search(
                            [
                                ('lead_id', '=', self.lead_id.id),
                                ('state', '=', 'delivered')
                            ]
                        )
                        if expedition_ids:
                            expedition_id = expedition_ids[0]
                            # last phone_call (max 1 minute)
                            phone_call_log_ids = self.env['phone.call.log'].search(
                                [
                                    ('lead_id', '=', self.lead_id.id),
                                    ('type', 'in', (1, 2)),
                                    ('duration', '>=', 0.3)
                                ],
                                order="date desc"
                            )
                            if phone_call_log_ids:
                                phone_call_log_id = phone_call_log_ids[0]
                                # difference hours
                                diff = datetime.strptime(
                                    str(expedition_id.date),
                                    '%Y-%m-%d'
                                ) - datetime.strptime(
                                    str(phone_call_log_id.date),
                                    '%Y-%m-%d %H:%M:%S'
                                )
                                diffInHours = diff.total_seconds() / 3600
                                if diffInHours >= 24:
                                    # update is_revision
                                    self.lead_id.is_revision = True
        return res
