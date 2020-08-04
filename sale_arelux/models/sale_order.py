# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, fields
from odoo.exceptions import Warning
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    opportunity_id = fields.Many2one(
        comodel_name='crm.lead', 
        string='Opportunity', 
        domain="[('type', '=', 'opportunity')]", 
        required=True
    )
    show_total = fields.Boolean( 
        string='Mostrar total'
    )
    proforma = fields.Boolean( 
        string='Proforma'
    )        
    date_order_management = fields.Datetime(
        string='Fecha gestion', 
        readonly=True
    )
    date_order_send_mail = fields.Datetime(
        string='Fecha envio email', 
        readonly=True
    )        
    disable_autogenerate_create_invoice = fields.Boolean( 
        string='Desactivar auto facturar'
    )    
    partner_id_email = fields.Char(
        compute='_compute_partner_id_email',
        store=False,
        string='Email'
    )
    partner_id_phone = fields.Char(
        compute='_compute_partner_id_phone',
        store=False,
        string='Telefono'
    )
    partner_id_mobile = fields.Char(
        compute='_compute_partner_id_mobile',
        store=False,
        string='Movil'
    )
    partner_id_state_id = fields.Many2one(
        comodel_name='res.country.state',
        compute='_compute_partner_id_state_id',
        store=False,
        string='Provincia'
    )
    
    @api.onchange('partner_id')
    def onchange_partner_id_override(self):
        if self.partner_id:
            self.payment_mode_id = self.partner_id.customer_payment_mode_id.id or False
            # partner_shipping_id
            partner_ids = self.env['res.partner'].search(
                [
                    ('parent_id', '=', self.partner_id.id),
                    ('active', '=', True), 
                    ('type', '=', 'delivery')
                 ]
            )
            if len(partner_ids) > 1:
                self.partner_shipping_id = 0
            elif len(partner_ids) == 1:
                self.partner_shipping_id = partner_ids[0].id
    
    @api.model
    def fix_copy_custom_field_opportunity_id(self):
        if self.id > 0:
            if self.opportunity_id:
                # user_id
                if self.opportunity_id.user_id and self.opportunity_id.user_id.id != self.user_id.id:
                    self.user_id = self.opportunity_id.user_id.id
                # team_id
                if self.opportunity_id.team_id and self.opportunity_id.team_id.id != self.team_id.id:
                    self.team_id = self.opportunity_id.team_id.id                                                              
    
    @api.model
    def create(self, values):            
        res = super(SaleOrder, self).create(values)
        
        if res.user_id.id and res.partner_id.user_id.id and self.user_id.id != res.partner_id.user_id.id:
            res.user_id = return_val.partner_id.user_id.id
        
        if res.user_id.id == 6:
            res.user_id = 0
        
        res.fix_copy_custom_field_opportunity_id()
        return res
    
    @api.multi
    def write(self, vals):
        # date_order_management
        if vals.get('state')=='sent' and 'date_order_management' not in vals:
            vals['date_order_management'] = fields.datetime.now()                            
                                        
        return_object = super(SaleOrder, self).write(vals)
        if self.user_id.id:
            for message_follower_id in self.message_follower_ids:
                if message_follower_id.partner_id.user_ids:
                    for user_id in message_follower_id.partner_id.user_ids:
                        if user_id.id != self.user_id.id:
                            self.env.cr.execute("DELETE FROM  mail_followers WHERE id = "+str(message_follower_id.id))                            
                                                            
        return return_object                    
    
    @api.multi
    @api.depends('partner_id')
    def _compute_partner_id_state_id(self):
        for item in self:
            item.partner_id_state_id = item.partner_id.state_id.id
    
    @api.multi
    @api.depends('partner_id')
    def _compute_partner_id_email(self):
        for item in self:
            item.partner_id_email = item.partner_id.email
            
    @api.multi
    @api.depends('partner_id')
    def _compute_partner_id_phone(self):
        for item in self:
            item.partner_id_phone = item.partner_id.phone
            
    @api.multi
    @api.depends('partner_id')
    def _compute_partner_id_mobile(self):
        for item in self:
            item.partner_id_mobile = item.partner_id.mobile
    
    @api.multi
    @api.onchange('user_id')
    def change_user_id(self):
        for item in self:
            if item.user_id:
                if item.user_id.sale_team_id:
                    item.team_id = item.user_id.sale_team_id.id
                                                        
    @api.multi
    @api.onchange('template_id')
    def change_template_id(self):
        for item in self:
            if item.template_id:
                if item.template_id.delivery_carrier_id:
                    item.carrier_id = item.template_id.delivery_carrier_id
                else:
                    item.carrier_id = False