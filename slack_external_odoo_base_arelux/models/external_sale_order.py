# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, _


class ExternalSaleOrder(models.Model):
    _inherit = 'external.sale.order'
        
    @api.multi
    def action_sale_order_done_error_partner_id_without_vat(self):
        self.ensure_one()
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_item = "%s/web?#id=%s&view_type=form&model=external.sale.order" % (
            web_base_url,
            self.id
        )
        # attachments
        attachments = [
            {                    
                "title": _('Error creating external.sale.order'),
                "text": _('The order cannot be confirmed because the client does NOT have a CIF'),
                "color": "#ff0000",
                "fallback": _('View order %s') % url_item,
                "actions": [
                    {
                        "type": "button",
                        "text": _('View order'),
                        "url": url_item
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
            'channel': self.env['ir.config_parameter'].sudo().get_param(
                'slack_arelux_log_channel'
            )
        }                        
        self.env['slack.message'].sudo().create(vals)
        
    @api.multi
    def action_sale_order_done_error_external_shipping_address_id_without_country_id(self):
        self.ensure_one()
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_item = "%s/web?#id=%s&view_type=form&model=external.sale.order" % (
            web_base_url,
            self.id
        )
        # attachments
        attachments = [
            {                    
                "title": _('Error creating external.sale.order'),
                "text": _('The order cannot be confirmed because the customers shipping address has NO mapped COUNTRY'),
                "color": "#ff0000",                                             
                "fallback": _('View order %s') % url_item,
                "actions": [
                    {
                        "type": "button",
                        "text": _('View order'),
                        "url": url_item
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
            'channel': self.env['ir.config_parameter'].sudo().get_param(
                'slack_arelux_log_channel'
            )
        }                        
        self.env['slack.message'].sudo().create(vals)
        
    @api.multi
    def action_sale_order_done_error_external_shipping_address_id_without_country_state_id(self):
        self.ensure_one()
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_item = "%s/web?#id=%s&view_type=form&model=external.sale.order" % (
            web_base_url,
            self.id
        )
        # attachments
        attachments = [
            {                    
                "title": _('Error creating external.sale.order'),
                "text": _('The order cannot be confirmed because the customers shipping address DOES NOT have a mapped STATE'),
                "color": "#ff0000",                                             
                "fallback": _('View order %s') % url_item,
                "actions": [
                    {
                        "type": "button",
                        "text": _('View order'),
                        "url": url_item
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
            'channel': self.env['ir.config_parameter'].sudo().get_param(
                'slack_arelux_log_channel'
            )
        }                        
        self.env['slack.message'].sudo().create(vals)
