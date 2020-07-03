# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class AreluxSaleReportType(models.Model):
    _name = 'arelux.sale.report.type'
    _description = 'Arelux Sale Report Type'    
    
    name = fields.Char(        
        string='Nombre'
    )
    custom_type = fields.Selection(
        selection=[
            ('sale_order_done_amount_untaxed','Ventas (Base Imponible)'),#Ventas � (Base imponible) 
            ('sale_order_done_count','Ventas (Cuenta)'),#Ventas pedidos (N� de pedidos)
            ('sale_order_ticket_medio','Ventas (Ticket medio)'),#Ticket medio (dividir los dos datos anteriores)
            ('sale_order_sent_count','Ptos realizados (Cuenta)'),#Presupuestos realizados (excluyendo los de muestras)
            ('sale_order_done_muestras','Muestras enviadas (Cuenta)'),#Muestras enviadas (presus de importe 0� confirmados en esa semana)
            ('ratio_muestras','Ratio muestras'),#Ratio muestras: (muestras enviadas/presupuestos realizados)
            ('ratio_calidad','Ratio calidad'),#Ratio de calidad: (pedidos confirmados/presupuestos realizados)
            ('res_partner_potencial_count','Contactos potenciales (Cuenta)'),#Nuevos pots (clientes nuevos creados por cada comercial, aqui tambi�n aparecer� como comercial el webservice que ser�n los que entren por formularios)
            ('cartera_actual_activa_count','Cartera Actual activa (Cuenta)'),#Cartera actual activa (N� clientes con alguna compra en 2019)
            ('cartera_actual_count','Cartera Actual (Cuenta)'),#Cartera actual (N� de clientes prof. de TC asignados a cada comercial)
            ('nuevos_clientes_con_ventas','Nuevos clientes con ventas'),#Nuevos clientes con ventas (clientes que han comprado la primera vez esa semana)
            ('line_break','Salto de linea'),#Salto de linea
        ],
        string='Custom Type',
        default=''
    )
    group_by_user = fields.Boolean(
        default=False,
        string='Group by user'
    )
    
    @api.one
    def get_info(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        if self.custom_type=='sale_order_done_amount_untaxed':
            response = {
                'type': 'sum',
                'result_value': '',
                'result': ''
            }
            search_filters = [
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '>', 0),
                ('confirmation_date', '>=', date_from),
                ('confirmation_date', '<=', date_to)
            ]
            #ar_qt_activity_type
            if ar_qt_activity_type!='none':
                search_filters.append(('ar_qt_activity_type', '=', ar_qt_activity_type))
            ##ar_qt_customer_type
            if ar_qt_customer_type!='none':
                search_filters.append(('ar_qt_customer_type', '=', ar_qt_customer_type))
            ##sale_team_id
            if sale_team_id>0:
                search_filters.append(('sale_team_id', '=', sale_team_id))
            
            sale_order_ids = self.env['sale.order'].search(search_filters)
            amount_untaxed = sum(sale_order_ids.mapped('amount_untaxed'))
                    
            response['result_value'] = amount_untaxed
            response['result'] = amount_untaxed
            return response
        
            #return self._get_line_info_sale_order_done_amount_untaxed(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)
        elif self.custom_type=='sale_order_done_count':
            return self._get_line_info_sale_order_done_count(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)
        elif self.custom_type=='sale_order_ticket_medio':
            return self._get_line_info_sale_order_ticket_medio(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)
        elif self.custom_type=='sale_order_sent_count':
            return self._get_line_info_sale_order_sent_count(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)
        elif self.custom_type=='sale_order_done_muestras':
            return self._get_line_info_sale_order_done_muestras(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)
        elif self.custom_type=='ratio_muestras':
            return self._get_line_info_ratio_muestras(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)
        elif self.custom_type=='ratio_calidad':
            return self._get_line_info_ratio_calidad(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)
        elif self.custom_type=='res_partner_potencial_count':
            return self._get_line_info_res_partner_potencial_count(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)
        elif self.custom_type=='cartera_actual_activa_count':
            return self._get_line_info_cartera_actual_activa_count(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)
        elif self.custom_type=='cartera_actual_count':
            return self._get_line_info_cartera_actual_count(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)
        elif self.custom_type=='nuevos_clientes_con_ventas':
            return self._get_line_info_nuevos_clientes_con_ventas(date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id)                                                                                                                                    
    
    @api.one
    def _get_sale_order_done(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        self.ensure_one()
        search_filters = [
            ('state', 'in', ('sale', 'done')),
            ('amount_untaxed', '>', 0),
            ('confirmation_date', '>=', date_from),
            ('confirmation_date', '<=', date_to)
        ]
        #ar_qt_activity_type
        if ar_qt_activity_type!='none':
            search_filters.append(('ar_qt_activity_type', '=', ar_qt_activity_type))
        ##ar_qt_customer_type
        if ar_qt_customer_type!='none':
            search_filters.append(('ar_qt_customer_type', '=', ar_qt_customer_type))
        ##sale_team_id
        if sale_team_id>0:
            search_filters.append(('sale_team_id', '=', sale_team_id))
        
        _logger.info(search_filters)
                
        ids = self.env['sale.order'].search(search_filters)
        _logger.info(ids)
        return ids
        
    @api.one
    def _get_line_info_sale_order_done_amount_untaxed(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        search_filters = [
            ('state', 'in', ('sale', 'done')),
            ('amount_untaxed', '>', 0),
            ('confirmation_date', '>=', date_from),
            ('confirmation_date', '<=', date_to)
        ]
        #ar_qt_activity_type
        if ar_qt_activity_type!='none':
            search_filters.append(('ar_qt_activity_type', '=', ar_qt_activity_type))
        ##ar_qt_customer_type
        if ar_qt_customer_type!='none':
            search_filters.append(('ar_qt_customer_type', '=', ar_qt_customer_type))
        ##sale_team_id
        if sale_team_id>0:
            search_filters.append(('sale_team_id', '=', sale_team_id))
        
        sale_order_ids = self.env['sale.order'].search(search_filters)
        amount_untaxed = sum(sale_order_ids.mapped('amount_untaxed'))
                
        response['result_value'] = amount_untaxed
        response['result'] = amount_untaxed        
        return response
    
    @api.one
    def _get_line_info_sale_order_done_count(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        return response
    
    @api.one
    def _get_line_info_sale_order_ticket_medio(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        return response
    
    @api.one
    def _get_line_info_sale_order_sent_count(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        return response
    
    @api.one
    def _get_line_info_sale_order_done_muestras(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        return response
    
    @api.one
    def _get_line_info_ratio_muestras(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        return response
    
    @api.one
    def _get_line_info_ratio_calidad(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        return response
    
    @api.one
    def _get_line_info_res_partner_potencial_count(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        return response
    
    @api.one
    def _get_line_info_cartera_actual_activa_count(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        return response
    
    @api.one
    def _get_line_info_cartera_actual_count(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        return response
    
    @api.one
    def _get_line_info_nuevos_clientes_con_ventas(self, date_from, date_to, ar_qt_activity_type, ar_qt_customer_type, sale_team_id):
        response = {
            'type': 'sum',
            'result_value': '',
            'result': ''
        }
        return response                