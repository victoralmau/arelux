# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

from dateutil.relativedelta import relativedelta
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class AreluxSaleReportTemplate(models.Model):
    _name = 'arelux.sale.report.template'
    _description = 'Arelux Sale Report Template'
    _inherit = ['mail.thread']    
        
    name = fields.Char(        
        string='Nombre'
    )
    active = fields.Boolean(
        default=True,        
        string='Activo'
    )    
    custom_type = fields.Selection(
        selection=[
            ('daily','Diario'),
            ('weekly','Semanal'),
            ('monthly','Mensual'),
            ('annual','Anual')                                                                           
        ],
        string='Custom Type',
        default='daily'
    )
    show_in_table_format = fields.Boolean(
        default=False,
        string='Show in table format'
    )
    order_by = fields.Char(        
        string='Order by',
        default='user_name'
    )
    order_way = fields.Selection(
        selection=[
            ('asc','ASC'),
            ('desc','DESC')                                                                           
        ],
        string='Order way',
        default='asc'
    )
    report_template_line = fields.One2many('arelux.sale.report.template.line', 'arelux_sale_report_template_id', string='Report Template Lines', copy=True)
    
    @api.model    
    def cron_generate_automatic_arelux_sale_report(self):
        current_date = datetime.today()
        
        arelux_sale_report_template_ids = self.env['arelux.sale.report.template'].search([('active', '=', True)])
        if len(arelux_sale_report_template_ids)>0:
            for arelux_sale_report_template_id in arelux_sale_report_template_ids:
                if arelux_sale_report_template_id.custom_type=='daily':
                    start_date = current_date + relativedelta(days=1)
                    end_date = start_date
                elif arelux_sale_report_template_id.custom_type=='weekly':
                    start_date = current_date + relativedelta(days=-7)
                    end_date = start_date + relativedelta(days=6)                
                elif arelux_sale_report_template_id.custom_type=='monthly':
                    start_date = datetime(current_date.year, current_date.month, 1) + relativedelta(months=-1)
                    end_date = start_date + relativedelta(months=1, days=-1)
                elif arelux_sale_report_template_id.custom_type=='annual':
                    start_date = datetime(current_date.year, 1, 1) + relativedelta(years=-1)
                    end_date = datetime(start_date.year, 12, 31)
                    
                arelux_sale_report_ids = self.env['arelux.sale.report'].search(
                    [
                        ('arelux_sale_report_template_id', '=', arelux_sale_report_template_id.id),
                        ('date_from', '=', start_date.strftime("%Y-%m-%d")),
                        ('date_to', '=', end_date.strftime("%Y-%m-%d"))
                    ]
                )
                if len(arelux_sale_report_ids)==0:
                    arelux_sale_report_vals = {
                        'name': arelux_sale_report_template_id.name,
                        'arelux_sale_report_template_id': arelux_sale_report_template_id.id,
                        'date_from': start_date.strftime("%Y-%m-%d"),
                        'date_to': end_date.strftime("%Y-%m-%d"),
                        'show_in_table_format': arelux_sale_report_template_id.show_in_table_format,
                        'state': 'new',
                        'order_by': arelux_sale_report_template_id.order_by,
                        'order_way': arelux_sale_report_template_id.order_way                                                                       
                    }
                    arelux_sale_report_obj = self.env['arelux.sale.report'].sudo().create(arelux_sale_report_vals)
                    #lines
                    for report_template_line in arelux_sale_report_template_id.report_template_line:
                        arelux_sale_report_line_vals = {
                            'arelux_sale_report_id': arelux_sale_report_obj.id,
                            'arelux_sale_report_type_id': report_template_line.arelux_sale_report_type_id.id,
                            'position': report_template_line.position,
                            'ar_qt_activity_type': report_template_line.ar_qt_activity_type,
                            'ar_qt_customer_type': report_template_line.ar_qt_customer_type,
                            'crm_team_id': report_template_line.crm_team_id.id,
                            'group_by_user': report_template_line.group_by_user,
                            'show_in_table_format': report_template_line.show_in_table_format                                                                                                                                                           
                        }
                        arelux_sale_report_line_obj = self.env['arelux.sale.report.line'].sudo().create(arelux_sale_report_line_vals)
                    #mail_followers
                    mail_follower_ids = self.env['mail.followers'].search(
                        [
                            ('res_model', '=', self._name),
                            ('res_id', '=', arelux_sale_report_template_id.id)
                        ]
                    )
                    if len(mail_follower_ids)>0:
                        for mail_follower_id in mail_follower_ids:                            
                            mail_followers_vals = {
                                'res_id': arelux_sale_report_obj.id,
                                'res_model': 'arelux.sale.report',
                                'partner_id': mail_follower_id.partner_id.id,
                                'subtype_ids': [(6, 0, [1])],
                            }
                            
                            mail_follower_ids_item = self.env['mail.followers'].search(
                                [
                                    ('res_model', '=', mail_followers_vals['res_model']),
                                    ('res_id', '=', mail_followers_vals['res_id']),
                                    ('partner_id', '=', mail_followers_vals['partner_id'])
                                ]
                            )
                            if len(mail_follower_ids_item)==0:#Prevent exist
                                mail_followers_obj = self.env['mail.followers'].create(mail_followers_vals)
                            else:
                                if mail_followers_vals['partner_id']==3:
                                    mail_follower_id_item = mail_follower_ids_item[0]
                                    mail_follower_id_item.unlink()
                                    
                    #fix generate_value_lines
                    arelux_sale_report_obj.change_state_to_generate()
                    #auto_send_mail_item
                    arelux_sale_report_obj.action_send_mail()