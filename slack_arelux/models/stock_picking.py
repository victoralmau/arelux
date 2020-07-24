# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.one    
    def action_send_account_invoice_out_refund(self):
        return_object = super(StockPicking, self).action_send_account_invoice_out_refund()
        self.action_send_account_invoice_out_refund_create_message_slack()
        return return_object
    
    @api.one    
    def action_send_account_invoice_out_refund_create_message_slack(self):
        if self.out_refund_invoice_id:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                                                            
            attachments = [
                {                    
                    "title": _('The refund invoice has been created automatically'),
                    "text": self.out_refund_invoice_id.number,                        
                    "color": "#36a64f",
                    "fallback": _('View invoice %s %s/web?#id=%s&view_type=form&model=account.invoice') % (
                        self.out_refund_invoice_id.number,
                        web_base_url,
                        self.out_refund_invoice_id.id
                    ),
                    "actions": [
                        {
                            "type": "button",
                            "text": _('View invoice %s') % self.out_refund_invoice_id.number,
                            "url": "%s/web?#id=%s&view_type=form&model=account.invoice" % (
                                web_base_url,
                                self.out_refund_invoice_id.id
                            )
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
                'channel': self.env['ir.config_parameter'].sudo().get_param('slack_log_contabilidad_channel'),                                                         
            }                        
            self.env['slack.message'].sudo().create(vals)