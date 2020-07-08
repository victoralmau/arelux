# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
import operator

import logging
_logger = logging.getLogger(__name__)

class AreluxSaleReport(models.Model):
    _name = 'arelux.sale.report'
    _description = 'Arelux Sale Report'
    _inherit = ['mail.thread']    
    
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id
    )        
    name = fields.Char(        
        string='Nombre'
    )
    date_from = fields.Date(        
        string='Fecha desde'
    )
    date_to = fields.Date(        
        string='Fecha hasta'
    )
    date_from_filter = fields.Datetime(        
        string='Fecha desde filtro'
    )
    date_to_filter = fields.Datetime(        
        string='Fecha hasta filtro'
    )
    arelux_sale_report_template_id = fields.Many2one(
        comodel_name='arelux.sale.report.template',
        string='Arelux Sale Report Template'
    )
    ir_attachment_id = fields.Many2one(
        comodel_name='ir.attachment',
        string='Adjunto'
    )
    state = fields.Selection(
        selection=[
            ('new','Nuevo'),
            ('generate','Generado'),
            ('sent','Enviado')                                                                           
        ],
        string='Estado',
        default='new'
    )    
    show_in_table_format = fields.Boolean(
        default=False,
        string='Show in table format'
    )
    order_by = fields.Char(        
        string='Order by',
        default='user_name'
    )
    order_way = fields.Char(        
        string='Order way',
        default='asc'
    )
    order_way = fields.Selection(
        selection=[
            ('asc','ASC'),
            ('desc','DESC')                                                                           
        ],
        string='Order way',
        default='asc'
    )
    report_line = fields.One2many('arelux.sale.report.line', 'arelux_sale_report_id', string='Report Lines', copy=True)    
     
    def action_generate_ir_report(self, context=None):
        self.ensure_one()
        self.change_state_to_generate()
            
        context = dict(context or {}, active_ids=self._ids, active_model=self._name)
        
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'arelux_sale_reports.arelux_sale_report_pdf_template',
            'context': context            
        }
    
    @api.one   
    def get_table_info_metrics(self):
        metrics_info = {}                        
        for report_line_item in self.report_line:
            if report_line_item.show_in_table_format==True:
                #report_line_item._get_line_info()
                if report_line_item.position not in metrics_info:
                    metrics_info[report_line_item.position] = {
                        'position': report_line_item.position,
                        'name': report_line_item.arelux_sale_report_type_id.name,
                        'response_result_value': report_line_item.response_result_value,
                        'custom_type': report_line_item.arelux_sale_report_type_id.custom_type                                                     
                    }                                        
        #metrics_info_sort
        metrics_info_sorted = []
        for metrics_info_key in metrics_info:
            metric_info = metrics_info[metrics_info_key]
            metrics_info_sorted.append(metric_info)
                                
        return metrics_info_sorted            
        
    @api.one   
    def get_table_info(self):        
        metrics_info = {}        
        table_info = {}
        for report_line_item in self.report_line:
            if report_line_item.show_in_table_format==True:
                #report_line_item._get_line_info()                
                for user_line in report_line_item.user_line:
                    if user_line.user_id.id not in table_info:
                        table_info[user_line.user_id.id] = {
                            'id': user_line.user_id.id,
                            'user_name': user_line.user_id.name,
                            'metrics': [],
                            'metrics_add': []
                        }                    
                    #Fix metric
                    if report_line_item.position not in metrics_info:
                        metrics_info[report_line_item.position] = {
                            'position': report_line_item.position,
                            'name': report_line_item.arelux_sale_report_type_id.name,
                            'response_result_value': report_line_item.response_result_value,
                            'custom_type': report_line_item.arelux_sale_report_type_id.custom_type,                            
                        }
                    #value_user
                    if report_line_item.response_result_value=='count':
                        value_user = user_line.count
                    elif report_line_item.response_result_value=='percent':
                        value_user = user_line.percent
                    else:
                        value_user = user_line.amount_untaxed                    
                    #metrics append
                    table_info[user_line.user_id.id]['metrics'].append({
                        'position': report_line_item.position,
                        'name': report_line_item.arelux_sale_report_type_id.name,
                        'response_result_value': report_line_item.response_result_value,
                        'custom_type': report_line_item.arelux_sale_report_type_id.custom_type,
                        'value': value_user
                    })
                    #metrics_add
                    table_info[user_line.user_id.id]['metrics_add'].append(report_line_item.position) 
        #fix fill all users
        for table_info_key in table_info:
            table_info_item = table_info[table_info_key]
                        
            for metric_info_key in metrics_info:
                metric_info = metrics_info[metric_info_key]            
                
                if metric_info['position'] not in table_info_item['metrics_add']:
                    table_info[table_info_key]['metrics'].append({
                        'position': metric_info['position'],                        
                        'name': metric_info['name'],
                        'response_result_value': metric_info['response_result_value'],
                        'custom_type': metric_info['custom_type'],
                        'value': 0
                    })
                    
            #sort_metrics
            table_info[table_info_key]['metrics'] = sorted(table_info[table_info_key]['metrics'], key=operator.itemgetter('position'))                                                            
        #sort_all
        table_info_sorted = []
        for table_info_key in table_info:
            table_info_item = table_info[table_info_key]
            if self.order_by!='user_name':
                for metric in table_info_item['metrics']:
                    if metric['custom_type']==self.order_by:
                        table_info_item[self.order_by] = metric['value']
                        
            table_info_sorted.append(table_info_item)        
        
        if self.order_way=='asc':
            table_info = sorted(table_info_sorted, key=operator.itemgetter(self.order_by))
        else:
            table_info = sorted(table_info_sorted, key=operator.itemgetter(self.order_by), reverse=True)                                                                     

        return table_info
        
    @api.one   
    def get_table_info_total(self):
        metrics_info = {}
        for report_line_item in self.report_line:
            if report_line_item.show_in_table_format==True:
                #report_line_item._get_line_info()
                if report_line_item.arelux_sale_report_type_id.custom_type not in metrics_info:
                    metrics_info[report_line_item.arelux_sale_report_type_id.custom_type] = {
                        'position': report_line_item.position,
                        'name': report_line_item.arelux_sale_report_type_id.name,
                        'response_result_value': report_line_item.response_result_value,
                        'custom_type': report_line_item.arelux_sale_report_type_id.custom_type,
                        'value': 0                            
                    }
                    for user_line in report_line_item.user_line:
                        #value_user
                        if report_line_item.response_result_value=='count':
                            value_user = user_line.count
                        else:
                            value_user = user_line.amount_untaxed
                            
                        metrics_info[report_line_item.arelux_sale_report_type_id.custom_type]['value'] += value_user
        
        #fix percents
        for report_line_item in self.report_line:
            if report_line_item.show_in_table_format==True and report_line_item.group_by_user==True and report_line_item.response_type=='percent':
                if report_line_item.arelux_sale_report_type_id.custom_type=='ratio_muestras':                    
                    numerador = metrics_info['sale_order_done_muestras']['value']
                    denominador = metrics_info['sale_order_sent_count']['value']                                                                                                    
                elif report_line_item.arelux_sale_report_type_id.custom_type=='ratio_calidad':
                    numerador = metrics_info['sale_order_done_count']['value']
                    denominador = metrics_info['sale_order_sent_count']['value']                
                #percent_item
                percent_item = 0
                if numerador>0 and denominador>0:
                    percent_item = (float(numerador)/float(denominador))*100              
                    percent_item = "{0:.2f}".format(percent_item)
                    
                metrics_info[report_line_item.arelux_sale_report_type_id.custom_type]['value'] = percent_item                                                               
        #metrics_info_sort
        metrics_info_sorted = []
        for metrics_info_key in metrics_info:
            metric_info = metrics_info[metrics_info_key]
            metrics_info_sorted.append(metric_info)
            
        metrics_info_sorted = sorted(metrics_info_sorted, key=operator.itemgetter('position'))            
                                
        return metrics_info_sorted                        
    
    @api.one
    def change_state_to_generate(self):
        if self.state=='new':
            self.date_from_filter = datetime.strptime(self.date_from+' 00:00:00', '%Y-%m-%d %H:%M:%S') + relativedelta(hours=-2)            
            self.date_to_filter = datetime.strptime(self.date_to+' 23:59:59', '%Y-%m-%d %H:%M:%S') + relativedelta(hours=-2)
        
            for report_line_item in self.report_line:
                report_line_item._get_line_info()
            
            self.state = 'generate'
            #Fix percents
            for report_line_item in self.report_line:
                if report_line_item.response_type=='percent' and report_line_item.group_by_user==True:
                    user_ids = []
                    ratio_muestras_by_user_id = []
                    
                    numerador_by_user_id = {}
                    denominador_by_user_id = {}
                    
                    if report_line_item.arelux_sale_report_type_id.custom_type=='ratio_muestras':                                                
                        #numerador
                        arelux_sale_report_line_ids = self.env['arelux.sale.report.line'].search([('arelux_sale_report_id', '=', self.id),('arelux_sale_report_type_id.custom_type', '=', 'sale_order_done_muestras')])
                        if len(arelux_sale_report_line_ids)>0:
                            arelux_sale_report_line_id = arelux_sale_report_line_ids[0]
                            for user_line in arelux_sale_report_line_id.user_line:
                                numerador_by_user_id[user_line.user_id.id] = user_line.count
                        #denominador
                        arelux_sale_report_line_ids = self.env['arelux.sale.report.line'].search([('arelux_sale_report_id', '=', self.id),('arelux_sale_report_type_id.custom_type', '=', 'sale_order_sent_count')])
                        if len(arelux_sale_report_line_ids)>0:
                            arelux_sale_report_line_id = arelux_sale_report_line_ids[0]
                            for user_line in arelux_sale_report_line_id.user_line:
                                denominador_by_user_id[user_line.user_id.id] = user_line.count                                                                        
                        
                    elif report_line_item.arelux_sale_report_type_id.custom_type=='ratio_calidad':                        
                        #numerador
                        arelux_sale_report_line_ids = self.env['arelux.sale.report.line'].search([('arelux_sale_report_id', '=', self.id),('arelux_sale_report_type_id.custom_type', '=', 'sale_order_done_count')])
                        if len(arelux_sale_report_line_ids)>0:
                            arelux_sale_report_line_id = arelux_sale_report_line_ids[0]
                            for user_line in arelux_sale_report_line_id.user_line:
                                numerador_by_user_id[user_line.user_id.id] = user_line.count                                
                        #denominador
                        arelux_sale_report_line_ids = self.env['arelux.sale.report.line'].search([('arelux_sale_report_id', '=', self.id),('arelux_sale_report_type_id.custom_type', '=', 'sale_order_sent_count')])
                        if len(arelux_sale_report_line_ids)>0:
                            arelux_sale_report_line_id = arelux_sale_report_line_ids[0]
                            for user_line in arelux_sale_report_line_id.user_line:
                                denominador_by_user_id[user_line.user_id.id] = user_line.count                                                                                        
                    #operations
                    for numerador_by_user_id_real in numerador_by_user_id:
                        if numerador_by_user_id_real not in user_ids:
                            user_ids.append(numerador_by_user_id_real)
                            
                    for denominador_by_user_id_real in denominador_by_user_id:
                        if denominador_by_user_id_real not in user_ids:
                            user_ids.append(denominador_by_user_id_real)
                    #save
                    #remove_all_previously
                    report_line_item.remove_all_user_line()                                
                    #calculate
                    for user_id in user_ids:
                        numerador_user_line = 0
                        if user_id in numerador_by_user_id:
                            numerador_user_line = numerador_by_user_id[user_id]
                            
                        denominador_user_line = 0
                        if user_id in denominador_by_user_id:
                            denominador_user_line = denominador_by_user_id[user_id]
                            
                        percent_item = 0
                        if numerador_user_line>0 and denominador_user_line>0:
                            percent_item = (float(numerador_user_line)/float(denominador_user_line))*100  
            
                        percent_item = "{0:.2f}".format(percent_item)
                        #add_report_line_user
                        arelux_sale_report_line_user_vals = {
                            'arelux_sale_report_line_id': report_line_item.id,
                            'user_id': user_id,
                            'percent': percent_item                                                                       
                        }
                        arelux_sale_report_line_user_obj = self.env['arelux.sale.report.line.user'].sudo().create(arelux_sale_report_line_user_vals)                             
    
    @api.one 
    def auto_send_mail_item(self):
        if self.state=='generate':
            arelux_sale_report_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('arelux_sale_report_mail_template_id'))
            if arelux_sale_report_mail_template_id>0:                                                       
                mail_template_item = self.env['mail.template'].search([('id', '=', arelux_sale_report_mail_template_id)])[0]
                                                        
                mail_compose_message_vals = {                    
                    'record_name': self.name,                                                                                                                                                                                           
                }
                mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo().create(mail_compose_message_vals)
                return_onchange_template_id = mail_compose_message_obj.onchange_template_id(mail_template_item.id, 'comment', self._name, self.id)
                                
                mail_compose_message_obj.update({
                    #'author_id': account_invoice_auto_send_mail_author_id,
                    'template_id': mail_template_item.id,                    
                    'composition_mode': 'comment',                    
                    'model': self._name,
                    'res_id': self.id,
                    'body': return_onchange_template_id['value']['body'],
                    'subject': return_onchange_template_id['value']['subject'],
                    'email_from': return_onchange_template_id['value']['email_from'],
                    'attachment_ids': return_onchange_template_id['value']['attachment_ids'],                    
                    'record_name': self.name,
                    'no_auto_thread': False,                     
                })                                                   
                mail_compose_message_obj.send_mail_action()
                
                self.state = 'sent'        
    
    @api.one
    def action_cancel_report(self):
        if self.state!="sent":
            self.state = 'new'                                
            
    @api.one
    def action_send_mail(self):
        self.auto_send_mail_item()            
    
        return True                                       