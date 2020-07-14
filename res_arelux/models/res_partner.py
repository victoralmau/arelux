# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields
from odoo.exceptions import Warning, ValidationError

import re

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    whatsapp = fields.Boolean( 
        string='Whatsapp'
    )            
    proposal_bring_a_friend = fields.Boolean( 
        string='Propuesta trae a un amigo'
    )                         
                
    @api.one
    def write(self, vals):
        allow_write = True
        #check_dni
        if self.type=='contact' and self.parent_id.id==0:
            if 'vat' in vals:
                if vals['vat']!=False:       
                    vals['vat'] = vals['vat'].strip().replace(' ', '').upper()#force to uppercase and remove spaces
                
                    if self.country_id.id > 0 and self.country_id.code=='ES':
                        if '-' in vals['vat']:
                            allow_write = False
                            raise Warning("El NIF no permite el caracter '-'") 
                    
                    if allow_write==True:                                
                        if self.supplier==True:
                            res_partner_ids = self.env['res.partner'].search(
                                [
                                    ('id', 'not in', (1, str(self.id))),
                                    ('type', '=', 'contact'),
                                    ('parent_id', '=', False),
                                    ('supplier', '=', True),
                                    ('vat', '=', vals['vat']) 
                                 ]
                            )
                        else:
                            res_partner_ids = self.env['res.partner'].search(
                                [
                                    ('id', 'not in', (1, str(self.id))),
                                    ('type', '=', 'contact'),
                                    ('parent_id', '=', False),
                                    ('supplier', '=', False),
                                    ('vat', '=', vals['vat']) 
                                 ]
                            )
                        
                        if len(res_partner_ids)>0:
                            allow_write = False
                            raise Warning("El NIF ya existe para otro contacto")                                                    
        #check_email
        if allow_write==True:
            if 'email' in vals:
                if vals['email']!='':
                    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', vals['email'])
                    if match == None:
                        allow_write = False
                        raise ValidationError('Email incorrecto')
        #return                             
        if allow_write==True:                        
            return super(ResPartner, self).write(vals)
    
    @api.model    
    def cron_res_partners_fix_customer(self):            
        self.env.cr.execute("UPDATE res_partner SET customer = True WHERE id IN (SELECT rp.id FROM res_partner AS rp WHERE rp.id > 1 AND rp.type = 'contact' AND rp.active = True AND rp.customer = False AND ((SELECT COUNT(cl.id) FROM crm_lead AS cl WHERE cl.type = 'opportunity' AND cl.partner_id = rp.id) > 0 OR (SELECT COUNT(so.id) FROM sale_order AS so WHERE so.partner_id = rp.id) > 0))")