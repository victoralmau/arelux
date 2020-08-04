# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields, _
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
                
    @api.multi
    def write(self, vals):
        allow_write = True
        # check_dni
        if self.type == 'contact' and self.parent_id.id == 0:
            if 'vat' in vals:
                if vals['vat']:
                    vals['vat'] = vals['vat'].strip().replace(' ', '').upper()
                
                    if self.country_id and self.country_id.code == 'ES':
                        if '-' in vals['vat']:
                            allow_write = False
                            raise Warning(_('The NIF does not allow the character -'))
                    
                    if allow_write:
                        if self.supplier:
                            partner_ids = self.env['res.partner'].search(
                                [
                                    ('id', 'not in', (1, str(self.id))),
                                    ('type', '=', 'contact'),
                                    ('parent_id', '=', False),
                                    ('supplier', '=', True),
                                    ('vat', '=', vals['vat']) 
                                 ]
                            )
                        else:
                            partner_ids = self.env['res.partner'].search(
                                [
                                    ('id', 'not in', (1, str(self.id))),
                                    ('type', '=', 'contact'),
                                    ('parent_id', '=', False),
                                    ('supplier', '=', False),
                                    ('vat', '=', vals['vat']) 
                                 ]
                            )
                        
                        if partner_ids:
                            allow_write = False
                            raise Warning(
                                _('The NIF already exists for another contact')
                            )
        # check_email
        if allow_write:
            if 'email' in vals:
                if vals['email'] != '':
                    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', vals['email'])
                    if match == None:
                        allow_write = False
                        raise ValidationError(_('Email incorrect'))
        # return
        if allow_write:
            return super(ResPartner, self).write(vals)
    
    @api.model    
    def cron_res_partners_fix_customer(self):            
        self.env.cr.execute("UPDATE res_partner SET customer = True WHERE id IN (SELECT rp.id FROM res_partner AS rp WHERE rp.id > 1 AND rp.type = 'contact' AND rp.active = True AND rp.customer = False AND ((SELECT COUNT(cl.id) FROM crm_lead AS cl WHERE cl.type = 'opportunity' AND cl.partner_id = rp.id) > 0 OR (SELECT COUNT(so.id) FROM sale_order AS so WHERE so.partner_id = rp.id) > 0))")