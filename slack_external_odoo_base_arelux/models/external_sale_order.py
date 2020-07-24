# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, _


class ExternalSaleOrder(models.Model):
    _inherit = 'external.sale.order'
        
    @api.one    
    def action_sale_order_done_error_partner_id_without_vat(self):
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # attachments
        attachments = [
            {                    
                "title": _('Error creating external.sale.order'),
                "text": _('The order cannot be confirmed because the client does NOT have a CIF'),
                "color": "#ff0000",
                "fallback": _('View order %s/web?#id=%s&view_type=form&model=external.sale.order') % (
                    web_base_url,
                    self.id
                ),
                "actions": [
                    {
                        "type": "button",
                        "text": _('View order'),
                        "url": "%s/web?#id=%s&view_type=form&model=external.sale.order" & (
                            web_base_url,
                            self.id
                        )
                    }
                ],
                "fields": [
                    {
                        "title": _('Source'),
                        "value": self.external_source_id.name,
                        'short': True,
                    },                    
                    {
                        "title": _('External id'),
                        "value": self.external_id,
                        'short': True,
                    },                    
                ],                    
            }
        ]
        vals = {
            'attachments': attachments,
            'model': self._inherit,
            'res_id': self.id,
            'as_user': True,
            'channel': str(self.env['ir.config_parameter'].sudo().get_param('slack_arelux_log_channel'))                                                         
        }                        
        self.env['slack.message'].sudo().create(vals)
        
    @api.one    
    def action_sale_order_done_error_external_shipping_address_id_without_country_id(self):
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # attachments
        attachments = [
            {                    
                "title": _('Error creating external.sale.order'),
                "text": _('The order cannot be confirmed because the customers shipping address has NO mapped COUNTRY'),
                "color": "#ff0000",                                             
                "fallback": _('View order %s/web?#id=%s&view_type=form&model=external.sale.order') % (
                    web_base_url,
                    self.id
                ),
                "actions": [
                    {
                        "type": "button",
                        "text": _('View order'),
                        "url": "%s/web?#id=%s&view_type=form&model=external.sale.order" & (
                            web_base_url,
                            self.id
                        )
                    }
                ],
                "fields": [
                    {
                        "title": _('Source'),
                        "value": self.external_source_id.name,
                        'short': True,
                    },                    
                    {
                        "title": _('External Id'),
                        "value": self.external_id,
                        'short': True,
                    },                    
                ],                    
            }
        ]
        vals = {
            'attachments': attachments,
            'model': self._inherit,
            'res_id': self.id,
            'as_user': True,
            'channel': str(self.env['ir.config_parameter'].sudo().get_param('slack_arelux_log_channel'))                                                         
        }                        
        self.env['slack.message'].sudo().create(vals)
        
    @api.one    
    def action_sale_order_done_error_external_shipping_address_id_without_country_state_id(self):
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # attachments
        attachments = [
            {                    
                "title": _('Error creating external.sale.order'),
                "text": _('The order cannot be confirmed because the customers shipping address DOES NOT have a mapped STATE'),
                "color": "#ff0000",                                             
                "fallback": _('View order %s/web?#id=%s&view_type=form&model=external.sale.order') % (
                    web_base_url,
                    self.id
                ),
                "actions": [
                    {
                        "type": "button",
                        "text": _('View order'),
                        "url": "%s/web?#id=%s&view_type=form&model=external.sale.order" & (
                            web_base_url,
                            self.id
                        )
                    }
                ],
                "fields": [
                    {
                        "title": _('Source'),
                        "value": self.external_source_id.name,
                        'short': True,
                    },                    
                    {
                        "title": _('External Id'),
                        "value": self.external_id,
                        'short': True,
                    },                    
                ],                    
            }
        ]
        vals = {
            'attachments': attachments,
            'model': self._inherit,
            'res_id': self.id,
            'as_user': True,
            'channel': str(self.env['ir.config_parameter'].sudo().get_param('slack_arelux_log_channel'))                                                         
        }                        
        self.env['slack.message'].sudo().create(slack_message_vals)