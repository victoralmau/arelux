# -*- coding: utf-8 -*-
from openerp import api, models, fields
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