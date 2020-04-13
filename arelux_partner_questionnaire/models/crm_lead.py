# -*- coding: utf-8 -*-
from openerp import api, models, fields
from openerp.exceptions import Warning
from dateutil.relativedelta import relativedelta
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    ar_qt_customer_type = fields.Selection(
        [
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),        
        ],        
        string='Tipo de cliente',
    )
    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),                    
        ],
        size=15, 
        string='Tipo de actividad'
    )
    ar_qt_todocesped_pf_customer_type = fields.Selection(        
        [
            ('warehouse_construction', 'Almacen de construccion'),
            ('architect', 'Arquitecto'),
            ('construction', 'Constructora / Promotora'),
            ('decorator', 'Decorador / Paisajista'),
            ('gardener', 'Jardinero'),
            ('multiservice', 'Multiservicio'),
            ('event_planner', 'Organizador de eventos'),
            ('pool', 'Piscinas'),
            ('nursery', 'Vivero'),
            ('other', 'Otro'),
        ], 
        string='Tipo de cliente (Prof)',
        readonly=True,
    )
    
    @api.multi    
    def cron_action_generate_ar_qt_todocesped_pf_customer_type(self, cr=None, uid=False, context=None):
        self.env.cr.execute("UPDATE crm_lead SET ar_qt_todocesped_pf_customer_type = (SELECT rp.ar_qt_todocesped_pf_customer_type FROM res_partner AS rp WHERE rp.id = crm_lead.partner_id) WHERE crm_lead.partner_id IN (SELECT rp.id FROM res_partner AS rp WHERE rp.customer = True AND rp.active = True AND rp.type = 'contact' AND rp.ar_qt_activity_type = 'todocesped' AND rp.ar_qt_customer_type = 'profesional')")
    
    @api.onchange('partner_id')
    def change_partner_id(self):
        return_item = super(CrmLead, self).change_partner_id()
        #operations
        if self._origin.id==0 and self.partner_id.id>0:
            #ar_qt_activity_type
            if self.partner_id.ar_qt_activity_type!=False:
                self.ar_qt_activity_type = 'todocesped'
                #check both
                if self.partner_id.ar_qt_activity_type!='both':
                    self.ar_qt_activity_type = self.partner_id.ar_qt_activity_type
            #ar_qt_customer_type                
            if self.partner_id.ar_qt_customer_type!=False:
                self.ar_qt_customer_type = self.partner_id.ar_qt_customer_type
        #return
        return return_item                         
                    
    @api.onchange('user_id')
    def change_user_id(self):
        return_item = super(CrmLead, self)._onchange_user_id()
        #operations
        if self._origin.id>0 and self.user_id.id>0:
            self.fix_copy_custom_field_sale_orders(True)
            #partner_id
            if self.partner_id.id!=False:
                #ar_qt_activity_type
                if self.partner_id.ar_qt_activity_type==False:
                    self.partner_id.ar_qt_activity_type = self.ar_qt_activity_type
                #ar_qt_customer_type
                if self.partner_id.ar_qt_customer_type==False:
                    self.partner_id.ar_qt_customer_type = self.ar_qt_customer_type
        #return
        return return_item
        
    @api.one
    def fix_copy_custom_field_sale_orders(self, update_user_id=True):                    
        sale_order_ids = self.env['sale.order'].search([('opportunity_id', '=', self.id)])
        if sale_order_ids!=False:
            for sale_order in sale_order_ids:
                if sale_order.id>0:
                    #update sqls prevent mail.message
                    if sale_order.state=='draft' or sale_order.state=='sent':
                        if self.user_id.id>0 and update_user_id==True:
                            self.env.cr.execute("UPDATE sale_order SET user_id = "+str(self.user_id.id)+" WHERE id = "+str(sale_order.id))
                        
                        if self.team_id.id>0:                   
                            self.env.cr.execute("UPDATE sale_order SET team_id = "+str(self.team_id.id)+" WHERE id = "+str(sale_order.id))
                    #ar_qt_activity_type
                    if self.ar_qt_activity_type!=False:
                        if self.ar_qt_activity_type!='both':
                            sale_order.ar_qt_activity_type = self.ar_qt_activity_type
                        else:
                            sale_order.ar_qt_activity_type = 'todocesped'                                                                      
                    #ar_qt_customer_type
                    if self.ar_qt_customer_type!=False:
                        sale_order.ar_qt_customer_type = self.ar_qt_customer_type
                        
    @api.model
    def create(self, values):
        allow_create = True
        #ar_qt_activity_type
        if 'ar_qt_activity_type' not in values:
            values['ar_qt_activity_type'] = 'todocesped'
        #ar_qt_customer_type
        if 'ar_qt_customer_type' not in values:
            values['ar_qt_customer_type'] = 'particular'                                    
        #prevent duplicate
        if 'partner_id' in values:
            if values['partner_id']!=False:        
                sale_quote_template_obj = self.env['crm.lead'].search(
                    [
                        ('active', '=', True),
                        ('partner_id', '=', values['partner_id']),                
                        ('ar_qt_activity_type', '=', values['ar_qt_activity_type']),
                        ('ar_qt_customer_type', '=', values['ar_qt_customer_type']),
                        ('probability', '<', 100),                
                    ]
                )
                if len(sale_quote_template_obj)>0:
                    allow_create = False
                    raise Warning("No se puede crear otro flujo para el mismo contacto, tipo de actividad y tipo de cliente si ya existe uno abierto")
        #operations
        if allow_create==True:    
            return_object = super(CrmLead, self).create(values)
            #fix change team_id
            if self.user_id.id>0:
                crm_team_ids = self.env['crm.team'].search([('ar_qt_activity_type', '=', self.ar_qt_activity_type)])
                if crm_team_ids!=False:
                    team_modify = False
                    for crm_team_id in crm_team_ids:                                                    
                        if crm_team_id.ar_qt_customer_type!=False and crm_team_id.ar_qt_customer_type==self.ar_qt_customer_type:
                            self.team_id = crm_team_id.id
                            team_modify = True
                        else:
                            if team_modify==False:
                                self.team_id = crm_team_id.id                                                                                                               
            #return
            return return_object                                            
    
    @api.multi
    def write(self, vals):                              
        allow_write = True
        if self.id>0:
            #check imposible team_id
            if 'team_id' in vals:
                team_id_obj = self.env['crm.team'].browse(vals['team_id'])
                
                ar_qt_activity_type_check = self.ar_qt_activity_type
                if 'ar_qt_activity_type' in vals:
                    ar_qt_activity_type_check = vals['ar_qt_activity_type']
                
                ar_qt_customer_type_check = self.ar_qt_customer_type
                if 'ar_qt_customer_type' in vals:
                    ar_qt_customer_type_check = vals['ar_qt_customer_type']
                
                if team_id_obj.ar_qt_activity_type!=False and team_id_obj.ar_qt_activity_type!=ar_qt_activity_type_check:
                    allow_write = False
                    raise Warning("No puedes cambiar el equipo de ventas a uno que no corresponde de este tipo de actividad")
                elif team_id_obj.ar_qt_activity_type!=False and team_id_obj.ar_qt_customer_type!=False and team_id_obj.ar_qt_customer_type!=ar_qt_customer_type_check:
                    allow_write = False
                    raise Warning("No puedes cambiar el equipo de ventas a uno que no corresponde de este tipo de cliente")
        #allow_write
        if allow_write==True:                                      
            return_object = super(CrmLead, self).write(vals)
            self.fix_copy_custom_field_sale_orders(True)                                                                                                                            
            #return                                                                                
            return return_object                                        