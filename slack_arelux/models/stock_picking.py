# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_send_account_invoice_out_refund(self):
        res = super(StockPicking, self).action_send_account_invoice_out_refund()
        for item in self:
            item.action_send_account_invoice_out_refund_create_message_slack()
        return res

    @api.multi
    def action_send_account_invoice_out_refund_create_message_slack(self):
        self.ensure_one()
        if self.out_refund_invoice_id:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url_item = "%s/web?#id=%s&view_type=form&model=account.invoice" % (
                base_url,
                self.out_refund_invoice_id.id
            )
            attachments = [
                {
                    "title":
                        _('The refund invoice has been created automatically'),
                    "text": self.out_refund_invoice_id.number,
                    "color": "#36a64f",
                    "fallback": _('View invoice %s %s') % (
                        self.out_refund_invoice_id.number,
                        url_item
                    ),
                    "actions": [
                        {
                            "type": "button",
                            "text": _('View invoice %s') %
                                    self.out_refund_invoice_id.number,
                            "url": url_item
                        }
                    ],
                    "fields": [
                        {
                            "title": _('Customer'),
                            "value": self.out_refund_invoice_id.partner_id.name,
                            'short': True,
                        },
                        {
                            "title": _('Origin'),
                            "value": self.out_refund_invoice_id.origin,
                            'short': True,
                        }
                    ],
                }
            ]
            vals = {
                'attachments': attachments,
                'model': 'account.invoice',
                'res_id': self.out_refund_invoice_id.id,
                'channel': self.env['ir.config_parameter'].sudo().get_param(
                    'slack_log_contabilidad_channel'
                ),
            }
            self.env['slack.message'].sudo().create(vals)
