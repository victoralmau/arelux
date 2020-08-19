# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, fields
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    opportunity_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Opportunity',
        domain="[('type', '=', 'opportunity')]"
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
        string='Email',
        related='partner_id.email',
        store=False,
        readonly=True
    )
    partner_id_phone = fields.Char(
        string='Telefono',
        related='partner_id.phone',
        store=False,
        readonly=True
    )
    partner_id_mobile = fields.Char(
        string='Movil',
        related='partner_id.mobile',
        store=False,
        readonly=True
    )
    partner_id_state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='Provincia',
        related='partner_id.state_id',
        store=False,
        readonly=True
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
                if self.opportunity_id.user_id \
                        and self.opportunity_id.user_id.id != self.user_id.id:
                    self.user_id = self.opportunity_id.user_id.id
                # team_id
                if self.opportunity_id.team_id \
                        and self.opportunity_id.team_id.id != self.team_id.id:
                    self.team_id = self.opportunity_id.team_id.id

    @api.model
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        if res.user_id.id and res.partner_id.user_id.id\
                and self.user_id.id != res.partner_id.user_id.id:
            res.user_id = res.partner_id.user_id.id

        if res.user_id.id == 6:
            res.user_id = 0

        res.fix_copy_custom_field_opportunity_id()
        return res

    @api.multi
    def write(self, vals):
        # date_order_management
        if vals.get('state') == 'sent' and 'date_order_management' not in vals:
            vals['date_order_management'] = fields.datetime.now()

        res = super(SaleOrder, self).write(vals)
        if self.user_id.id:
            for message_follower_id in self.message_follower_ids:
                if message_follower_id.partner_id.user_ids:
                    for user_id in message_follower_id.partner_id.user_ids:
                        if user_id.id != self.user_id.id:
                            message_follower_id.sudo().unlink()

        return res

    @api.multi
    @api.onchange('user_id')
    def change_user_id(self):
        for item in self:
            if item.user_id:
                if item.user_id.sale_team_id:
                    item.team_id = item.user_id.sale_team_id.id

    @api.multi
    @api.onchange('sale_order_template_id')
    def change_sale_order_template_id(self):
        for item in self:
            if item.sale_order_template_id:
                if item.sale_order_template_id.delivery_carrier_id:
                    item.carrier_id = item.sale_order_template_id.delivery_carrier_id
                else:
                    item.carrier_id = False
