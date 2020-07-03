# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime
import json
import operator

import logging
_logger = logging.getLogger(__name__)

class AreluxSaleReportLine(models.Model):
    _name = 'arelux.sale.report.line'
    _description = 'Arelux Sale Report Line'
    _order = "position asc"    
        
    arelux_sale_report_id = fields.Many2one(
        comodel_name='arelux.sale.report',
        string='Arelux Sale Report'
    )
    arelux_sale_report_type_id = fields.Many2one(
        comodel_name='arelux.sale.report.type',
        string='Arelux Sale Report Type'
    )
    position = fields.Integer(
        string='Posicion'
    )                                       
    ar_qt_activity_type = fields.Selection(
        selection=[
            ('none','Ninguno'), 
            ('arelux','Arelux'), 
            ('todocesped','Todocesped'),
            ('evert','Evert')                         
        ],
        string='Tipo de actividad',
        default='none'
    )
    ar_qt_customer_type = fields.Selection(
        selection=[
            ('none','Ninguno'), 
            ('particular','Particular'), 
            ('profesional','Profesional')                         
        ],
        string='Tipo de cliente',
        default='none'
    )
    crm_team_id = fields.Many2one(
        comodel_name='crm.team',
        string='Equipo de ventas'
    )
    response_type = fields.Text(
        string='Response type'
    )
    response_result_value = fields.Text(
        string='Response result value'
    )
    group_by_user = fields.Boolean(
        default=False,
        string='Group by user'
    )
    show_in_table_format = fields.Boolean(
        default=False,
        string='Show in table format'
    )    
    user_line = fields.One2many('arelux.sale.report.line.user', 'arelux_sale_report_line_id', string='User Lines', copy=True)
    sale_order_line = fields.One2many('arelux.sale.report.line.sale.order', 'arelux_sale_report_line_id', string='Sale Order Lines', copy=True)    
    
    @api.one
    def remove_all_user_line(self):
        arelux_sale_report_line_user_ids = self.env['arelux.sale.report.line.user'].search([('arelux_sale_report_line_id', '=', self.id)])            
        if len(arelux_sale_report_line_user_ids)>0:
            for arelux_sale_report_line_user_id in arelux_sale_report_line_user_ids:
                arelux_sale_report_line_user_id.unlink()
                
    @api.one
    def remove_all_sale_order_line(self):
        arelux_sale_report_line_sale_order_ids = self.env['arelux.sale.report.line.sale.order'].search([('arelux_sale_report_line_id', '=', self.id)])            
        if len(arelux_sale_report_line_sale_order_ids)>0:
            for arelux_sale_report_line_sale_order_id in arelux_sale_report_line_sale_order_ids:
                arelux_sale_report_line_sale_order_id.unlink()                        
    
    @api.one
    def _get_line_info_real(self, custom_type):
        return_values = {
            'response_type': '',
            'response_result_value': ''
        }
        
        if custom_type=='sale_order_done_amount_untaxed':            
            search_filters = [
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '>', 0),
                ('claim', '=', False),
                ('confirmation_date', '>=', self.arelux_sale_report_id.date_from_filter),
                ('confirmation_date', '<=', self.arelux_sale_report_id.date_to_filter)
            ]
            #ar_qt_activity_type
            if self.ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', self.ar_qt_activity_type))
            #ar_qt_customer_type
            if self.ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', self.ar_qt_customer_type))
            #sale_team_id
            if self.crm_team_id.id>0:
                search_filters.append(('sale_team_id', '=', self.crm_team_id.id))
            
            sale_order_ids = self.env['sale.order'].search(search_filters)
            
            if self.group_by_user==False:
                return_values['response_type'] = 'sum'
                amount_untaxed = sum(sale_order_ids.mapped('amount_untaxed'))                                
                return_values['response_result_value'] = amount_untaxed
                return_values['amount_untaxed'] = amount_untaxed
            else:
                return_values['response_type'] = 'list_by_user_id'                        
            
                res_users = {}
                if len(sale_order_ids)>0:
                    for sale_order_id in sale_order_ids:
                        #fix if need create
                        user_id = int(sale_order_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'amount_untaxed': 0
                            }
                        
                            if user_id>0:
                                res_users[user_id]['name'] = sale_order_id.user_id.name                                
                        #sum
                        res_users[user_id]['amount_untaxed'] += sale_order_id.amount_untaxed
                #fix response_result_value
                return_values['response_result_value'] = 'amount_untaxed'                                 
                return_values['amount_untaxed'] = sum(sale_order_ids.mapped('amount_untaxed'))                    
                #remove_all
                self.remove_all_user_line()                                               
                #creates
                if len(sale_order_ids)>0:
                    for res_user_id, res_user in res_users.items():
                        arelux_sale_report_line_user_vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'amount_untaxed': res_user['amount_untaxed']                                                                       
                        }
                        arelux_sale_report_line_user_obj = self.env['arelux.sale.report.line.user'].sudo().create(arelux_sale_report_line_user_vals)
        
        elif custom_type=='sale_order_done_count':                                            
            search_filters = [
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '>', 0),
                ('claim', '=', False),
                ('confirmation_date', '>=', self.arelux_sale_report_id.date_from_filter),
                ('confirmation_date', '<=', self.arelux_sale_report_id.date_to_filter)
            ]
            #ar_qt_activity_type
            if self.ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', self.ar_qt_activity_type))
            #ar_qt_customer_type
            if self.ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', self.ar_qt_customer_type))
            #sale_team_id
            if self.crm_team_id.id>0:
                search_filters.append(('sale_team_id', '=', self.crm_team_id.id))
            
            sale_order_ids = self.env['sale.order'].search(search_filters)
            
            if self.group_by_user==False:
                return_values['response_type'] = 'count'                                
                return_values['response_result_value'] = len(sale_order_ids)
                return_values['count'] = len(sale_order_ids)
            else:
                return_values['response_type'] = 'list_by_user_id'                        
            
                res_users = {}
                if len(sale_order_ids)>0:
                    for sale_order_id in sale_order_ids:
                        #fix if need create
                        user_id = int(sale_order_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'count': 0
                            }
                            
                            if user_id>0:
                                res_users[user_id]['name'] = sale_order_id.user_id.name
                        #sum
                        res_users[user_id]['count'] += 1
                #fix response_result_value                    
                return_values['response_result_value'] = 'count'
                return_values['count'] = len(sale_order_ids)
                #remove_all
                self.remove_all_user_line()                                               
                #creates
                if len(sale_order_ids)>0:
                    for res_user_id, res_user in res_users.items():
                        arelux_sale_report_line_user_vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'count': res_user['count']                                                                       
                        }
                        arelux_sale_report_line_user_obj = self.env['arelux.sale.report.line.user'].sudo().create(arelux_sale_report_line_user_vals)                                    
    
        elif custom_type=='sale_order_ticket_medio':            
            search_filters = [
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '>', 0),
                ('claim', '=', False),
                ('confirmation_date', '>=', self.arelux_sale_report_id.date_from_filter),
                ('confirmation_date', '<=', self.arelux_sale_report_id.date_to_filter)
            ]
            #ar_qt_activity_type
            if self.ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', self.ar_qt_activity_type))
            #ar_qt_customer_type
            if self.ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', self.ar_qt_customer_type))
            #sale_team_id
            if self.crm_team_id.id>0:
                search_filters.append(('sale_team_id', '=', self.crm_team_id.id))
            
            sale_order_ids = self.env['sale.order'].search(search_filters)
            
            if self.group_by_user==False:
                return_values['response_type'] = 'sum'
            
                amount_untaxed = sum(sale_order_ids.mapped('amount_untaxed'))
                
                ticket_medio = 0
                if len(sale_order_ids)>0:
                    ticket_medio = (amount_untaxed/len(sale_order_ids))
                
                ticket_medio = "{0:.2f}".format(ticket_medio)
                                        
                return_values['response_result_value'] = ticket_medio
                return_values['ticket_medio'] = ticket_medio
            else:
                return_values['response_type'] = 'list_by_user_id'                        
            
                res_users = {}
                if len(sale_order_ids)>0:
                    for sale_order_id in sale_order_ids:
                        #fix if need create
                        user_id = int(sale_order_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'count': 0,
                                'amount_untaxed': 0
                            }
                            
                            if user_id>0:
                                res_users[user_id]['name'] = sale_order_id.user_id.name
                        #sum
                        res_users[user_id]['count'] += 1
                        res_users[user_id]['amount_untaxed'] += sale_order_id.amount_untaxed
                #fix response_result_value                                   
                return_values['response_result_value'] = 'amount_untaxed'
                
                amount_untaxed = sum(sale_order_ids.mapped('amount_untaxed'))
                
                ticket_medio = 0
                if len(sale_order_ids)>0:
                    ticket_medio = (amount_untaxed/len(sale_order_ids))
                
                ticket_medio = "{0:.2f}".format(ticket_medio)                                        
                return_values['ticket_medio'] = ticket_medio
                #remove_all
                self.remove_all_user_line()                                               
                #creates
                if len(sale_order_ids)>0:
                    for res_user_id, res_user in res_users.items():
                        arelux_sale_report_line_user_vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'amount_untaxed': 0                                                                       
                        }
                        
                        if res_user['count']>0:
                            arelux_sale_report_line_user_vals['amount_untaxed'] = (res_user['amount_untaxed']/res_user['count'])
                        
                        arelux_sale_report_line_user_obj = self.env['arelux.sale.report.line.user'].sudo().create(arelux_sale_report_line_user_vals)
                            
        elif custom_type=='sale_order_sent_count':            
            search_filters = [
                ('date_order_management', '!=', False),
                ('amount_untaxed', '>', 0),
                ('opportunity_id', '!=', False),
                ('claim', '=', False),
                ('date_order_management', '>=', self.arelux_sale_report_id.date_from_filter),
                ('date_order_management', '<=', self.arelux_sale_report_id.date_to_filter)
            ]
            #ar_qt_activity_type
            if self.ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', self.ar_qt_activity_type))
            #ar_qt_customer_type
            if self.ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', self.ar_qt_customer_type))
            #sale_team_id
            if self.crm_team_id.id>0:
                search_filters.append(('sale_team_id', '=', self.crm_team_id.id))
            
            sale_order_ids = self.env['sale.order'].search(search_filters)
            
            if self.group_by_user==False:
                return_values['response_type'] = 'count'            
                return_values['response_result_value'] = len(sale_order_ids)
                return_values['count'] = len(sale_order_ids)
            else:
                return_values['response_type'] = 'list_by_user_id'                        
            
                res_users = {}
                if len(sale_order_ids)>0:
                    for sale_order_id in sale_order_ids:
                        #fix if need create
                        user_id = int(sale_order_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'count': 0
                            }
                            
                            if user_id>0:
                                res_users[user_id]['name'] = sale_order_id.user_id.name
                        #sum
                        res_users[user_id]['count'] += 1
                #fix response_result_value                    
                return_values['response_result_value'] = 'count'
                return_values['count'] = len(sale_order_ids)
                #remove_all
                self.remove_all_user_line()                                               
                #creates
                if len(sale_order_ids)>0:
                    for res_user_id, res_user in res_users.items():
                        arelux_sale_report_line_user_vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'count': res_user['count']                                                                       
                        }
                        arelux_sale_report_line_user_obj = self.env['arelux.sale.report.line.user'].sudo().create(arelux_sale_report_line_user_vals)
        
        elif custom_type=='sale_order_done_muestras':            
            search_filters = [
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '=', 0),
                ('claim', '=', False),
                ('carrier_id', '!=', False),
                ('carrier_id.carrier_type', '=', 'nacex'),
                ('confirmation_date', '>=', self.arelux_sale_report_id.date_from_filter),
                ('confirmation_date', '<=', self.arelux_sale_report_id.date_to_filter)
            ]
            #ar_qt_activity_type
            if self.ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', self.ar_qt_activity_type))
            #ar_qt_customer_type
            if self.ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', self.ar_qt_customer_type))
            #sale_team_id
            if self.crm_team_id.id>0:
                search_filters.append(('sale_team_id', '=', self.crm_team_id.id))
            
            sale_order_ids = self.env['sale.order'].search(search_filters)
            
            if self.group_by_user==False:
                return_values['response_type'] = 'count'            
                return_values['response_result_value'] = len(sale_order_ids)
                return_values['count'] = len(sale_order_ids)
            else:
                return_values['response_type'] = 'list_by_user_id'                        
            
                res_users = {}
                if len(sale_order_ids)>0:
                    for sale_order_id in sale_order_ids:
                        #fix if need create
                        user_id = int(sale_order_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'count': 0
                            }
                            
                            if user_id>0:
                                res_users[user_id]['name'] = sale_order_id.user_id.name
                        #sum
                        res_users[user_id]['count'] += 1
                #fix response_result_value                    
                return_values['response_result_value'] = 'count'
                return_values['count'] = len(sale_order_ids)
                #remove_all
                self.remove_all_user_line()                                               
                #creates
                if len(sale_order_ids)>0:
                    for res_user_id, res_user in res_users.items():
                        arelux_sale_report_line_user_vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'count': res_user['count']                                                                       
                        }
                        arelux_sale_report_line_user_obj = self.env['arelux.sale.report.line.user'].sudo().create(arelux_sale_report_line_user_vals)
        
        elif custom_type=='res_partner_potencial_count':
            return_values['response_type'] = 'list_by_user_id'            
            
            search_filters = [
                ('type', '=', 'contact'),
                ('active', '=', True),
                ('create_uid', '!=', 1),
                ('create_date', '>=', self.arelux_sale_report_id.date_from_filter),
                ('create_date', '<=', self.arelux_sale_report_id.date_to_filter)
            ]
            #ar_qt_activity_type
            if self.ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', self.ar_qt_activity_type))
            #ar_qt_customer_type
            if self.ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', self.ar_qt_customer_type))            
            
            res_users = {}
            res_partner_ids = self.env['res.partner'].search(search_filters)
            if len(res_partner_ids)>0:
                for res_partner_id in res_partner_ids:
                    #fix if need create
                    user_id = int(res_partner_id.create_uid.id)
                    if user_id not in res_users:
                        res_users[user_id] = {
                            'id': user_id,
                            'name': 'Sin comercial',
                            'total': 0
                        }
                        
                        if user_id>0:
                            res_users[user_id]['name'] = res_partner_id.create_uid.name
                    #sum
                    res_users[user_id]['total'] += 1
            #fix response_result_value
            return_values['response_result_value'] = 'count'                
            #remove_all
            self.remove_all_user_line()                                               
            #creates
            if len(res_partner_ids)>0:
                for res_user_id, res_user in res_users.items():
                    arelux_sale_report_line_user_vals = {
                        'arelux_sale_report_line_id': self.id,
                        'user_id': res_user['id'],
                        'count': res_user['total']                                                                       
                    }
                    arelux_sale_report_line_user_obj = self.env['arelux.sale.report.line.user'].sudo().create(arelux_sale_report_line_user_vals)
                    
        elif custom_type=='cartera_actual_activa_count':                                    
            search_filters = [
                ('type', '=', 'contact'),
                ('active', '=', True),
                ('user_id', '!=', False),
                ('sale_order_amount_untaxed_year_now', '>', 0),
                ('create_date', '>=', self.arelux_sale_report_id.date_from_filter),
                ('create_date', '<=', self.arelux_sale_report_id.date_to_filter)
            ]
            #ar_qt_activity_type
            if self.ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', self.ar_qt_activity_type))
            #ar_qt_customer_type
            if self.ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', self.ar_qt_customer_type))            
            
            res_partner_ids = self.env['res.partner'].search(search_filters)
            
            if self.group_by_user==False:
                return_values['response_type'] = 'count'                        
                return_values['response_result_value'] = len(res_partner_ids)
                return_values['count'] = len(res_partner_ids)
            else:
                return_values['response_type'] = 'list_by_user_id'                        
            
                res_users = {}
                if len(res_partner_ids)>0:
                    for res_partner_id in res_partner_ids:
                        #fix if need create
                        user_id = int(res_partner_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'count': 0
                            }
                            
                            if user_id>0:
                                res_users[user_id]['name'] = res_partner_id.user_id.name
                        #sum
                        res_users[user_id]['count'] += 1
                #fix response_result_value                    
                return_values['response_result_value'] = 'count'
                return_values['count'] = len(res_partner_ids)
                #remove_all
                self.remove_all_user_line()                                               
                #creates
                if len(res_partner_ids)>0:
                    for res_user_id, res_user in res_users.items():
                        arelux_sale_report_line_user_vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'count': res_user['count']                                                                       
                        }
                        arelux_sale_report_line_user_obj = self.env['arelux.sale.report.line.user'].sudo().create(arelux_sale_report_line_user_vals)
        
        elif custom_type=='cartera_actual_count':                        
            search_filters = [
                ('type', '=', 'contact'),
                ('active', '=', True),
                ('user_id', '!=', False),
                ('create_date', '>=', self.arelux_sale_report_id.date_from_filter),
                ('create_date', '<=', self.arelux_sale_report_id.date_to_filter)
            ]
            #ar_qt_activity_type
            if self.ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', self.ar_qt_activity_type))
            #ar_qt_customer_type
            if self.ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', self.ar_qt_customer_type))            
            
            res_partner_ids = self.env['res.partner'].search(search_filters)
            
            if self.group_by_user==False:
                return_values['response_type'] = 'count'
                return_values['response_result_value'] = len(res_partner_ids)
                return_values['count'] = len(res_partner_ids)
            else:
                return_values['response_type'] = 'list_by_user_id'
                res_users = {}            
                if len(res_partner_ids)>0:
                    for res_partner_id in res_partner_ids:
                        #fix if need create
                        user_id = int(res_partner_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'total': 0
                            }
                            
                            if user_id>0:
                                res_users[user_id]['name'] = res_partner_id.user_id.name
                        #sum
                        res_users[user_id]['total'] += 1
                #fix response_result_value
                return_values['response_result_value'] = 'count'
                return_values['count'] = len(res_partner_ids)                    
                #remove_all
                self.remove_all_user_line()                                               
                #creates
                if len(res_partner_ids)>0:
                    for res_user_id, res_user in res_users.items():
                        arelux_sale_report_line_user_vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'count': res_user['total']                                                                       
                        }
                        arelux_sale_report_line_user_obj = self.env['arelux.sale.report.line.user'].sudo().create(arelux_sale_report_line_user_vals)
        
        elif custom_type=='nuevos_clientes_con_ventas':
            return_values['response_type'] = 'list_sale_orders'
            #partner_ids with sale_orders < date_from
            res_partner_ids = []
            search_filters = [
                ('state', 'in', ('sale', 'done')),
                ('claim', '=', False),
                ('amount_untaxed', '>', 0),
                ('confirmation_date', '<', self.arelux_sale_report_id.date_from_filter),
            ]
            #ar_qt_activity_type
            if self.ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', self.ar_qt_activity_type))
            #ar_qt_customer_type
            if self.ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', self.ar_qt_customer_type))
                
            sale_order_ids = self.env['sale.order'].search(search_filters)            
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:
                    if sale_order_id.partner_id.id not in res_partner_ids:
                        res_partner_ids.append(sale_order_id.partner_id.id)                
            #sale_orders with filters and partner_id not in                                        
            search_filters = [
                ('state', 'in', ('sale', 'done')),
                ('claim', '=', False),
                ('amount_untaxed', '>', 0),
                ('partner_id', 'not in', res_partner_ids),
                ('confirmation_date', '>=', self.arelux_sale_report_id.date_from_filter),
                ('confirmation_date', '<=', self.arelux_sale_report_id.date_to_filter)
            ]
            #ar_qt_activity_type
            if self.ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', self.ar_qt_activity_type))
            #ar_qt_customer_type
            if self.ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', self.ar_qt_customer_type))
                
            sale_order_ids = self.env['sale.order'].search(search_filters)
            #sort_custom
            sale_order_ids2 = []
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:
                    sale_order_ids2.append({
                        'id': sale_order_id.id,
                        'user_name': sale_order_id.user_id.name
                    })
                sale_order_ids = sorted(sale_order_ids2, key=operator.itemgetter('user_name'))
            #remove_all
            self.remove_all_sale_order_line()
            #creates
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:
                    arelux_sale_report_line_sale_order_vals = {
                        'arelux_sale_report_line_id': self.id,
                        'sale_order_id': sale_order_id['id']                                                                
                    }
                    arelux_sale_report_line_sale_order_obj = self.env['arelux.sale.report.line.sale.order'].sudo().create(arelux_sale_report_line_sale_order_vals)                                                                                                                                                                                                                                  
        
        return return_values
    
    @api.one
    def _get_line_info(self):        
        if self.arelux_sale_report_type_id.id>0:
            
            if self.arelux_sale_report_type_id.custom_type=='ratio_muestras':            
                if self.group_by_user==False:
                    return_values_sale_order_done_muestras = self._get_line_info_real('sale_order_done_muestras')[0]
                    return_values_sale_order_sent_count = self._get_line_info_real('sale_order_sent_count')[0]
                    
                    self.response_type = 'percent'
                    ratio_muestras = 0                
                    
                    if return_values_sale_order_done_muestras['count']>0 and return_values_sale_order_sent_count['count']>0:
                        ratio_muestras = (float(return_values_sale_order_done_muestras['count'])/float(return_values_sale_order_sent_count['count']))*100  
                    
                    ratio_muestras = "{0:.2f}".format(ratio_muestras)
                    
                    self.response_result_value = ratio_muestras
                else:
                    self.response_type = 'percent'
                    self.response_result_value = 'percent'
            
            elif self.arelux_sale_report_type_id.custom_type=='ratio_calidad':
                if self.group_by_user==False:
                    self.response_type = 'percent'
                    
                    return_values_sale_order_done_count = self._get_line_info_real('sale_order_done_count')[0]
                    return_values_sale_order_sent_count = self._get_line_info_real('sale_order_sent_count')[0]
                    
                    ratio_calidad = 0
                    
                    if return_values_sale_order_done_count['count']>0 and return_values_sale_order_sent_count['count']>0:
                        ratio_calidad = (float(return_values_sale_order_done_count['count'])/float(return_values_sale_order_sent_count['count']))*100
                    
                    ratio_calidad = "{0:.2f}".format(ratio_calidad)
                    
                    self.response_result_value = ratio_calidad
                else:
                    self.response_type = 'percent'
                    self.response_result_value = 'percent'
                    
            elif self.arelux_sale_report_type_id.custom_type=='line_break':
                self.response_type = 'line_break'                                           
            else:
                return_values = self._get_line_info_real(self.arelux_sale_report_type_id.custom_type)[0]
            
                self.response_type = return_values['response_type']
                self.response_result_value = return_values['response_result_value']
                                                                                                       
        #_logger.info(response)                        
        #return response                                                    