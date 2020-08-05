# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, fields, _
from odoo.exceptions import Warning as UserError
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

    @api.model
    def cron_action_generate_ar_qt_todocesped_pf_customer_type(self):
        self.env.cr.execute("UPDATE crm_lead "
                            "SET ar_qt_todocesped_pf_customer_type = ("
                            "SELECT rp.ar_qt_todocesped_pf_customer_type "
                            "FROM res_partner AS rp "
                            "WHERE rp.id = crm_lead.partner_id) "
                            "WHERE crm_lead.partner_id IN ("
                            "SELECT rp.id FROM res_partner AS rp "
                            "WHERE rp.customer = True AND rp.active = True "
                            "AND rp.type = 'contact' "
                            "AND rp.ar_qt_activity_type = 'todocesped' "
                            "AND rp.ar_qt_customer_type = 'profesional')")

    @api.onchange('partner_id')
    def change_partner_id(self):
        return_item = super(CrmLead, self)._onchange_partner_id()
        # operations
        if self._origin.id == 0 and self.partner_id:
            # ar_qt_activity_type
            if self.partner_id.ar_qt_activity_type:
                self.ar_qt_activity_type = 'todocesped'
                # check both
                if self.partner_id.ar_qt_activity_type != 'both':
                    self.ar_qt_activity_type = self.partner_id.ar_qt_activity_type
            # ar_qt_customer_type
            if self.partner_id.ar_qt_customer_type:
                self.ar_qt_customer_type = self.partner_id.ar_qt_customer_type
        # return
        return return_item

    @api.onchange('user_id')
    def change_user_id(self):
        return_item = super(CrmLead, self)._onchange_user_id()
        # operations
        if self._origin and self.user_id:
            self.fix_copy_custom_field_sale_orders(True)
            # partner_id
            if self.partner_id.id:
                # ar_qt_activity_type
                if not self.partner_id.ar_qt_activity_type:
                    self.partner_id.ar_qt_activity_type = self.ar_qt_activity_type
                # ar_qt_customer_type
                if not self.partner_id.ar_qt_customer_type:
                    self.partner_id.ar_qt_customer_type = self.ar_qt_customer_type
        # return
        return return_item

    @api.multi
    def fix_copy_custom_field_sale_orders(self, update_user_id=True):
        self.ensure_one()
        order_ids = self.env['sale.order'].search(
            [
                ('opportunity_id', '=', self.id)
            ]
        )
        if order_ids:
            for order_id in order_ids:
                # update sqls prevent mail.message
                if order_id.state in ['draft', 'sent']:
                    if self.user_id and update_user_id:
                        sql = "UPDATE sale_order SET user_id = %s WHERE id = %s" % (
                            self.user_id.id,
                            order_id.id
                        )
                        self.env.cr.execute(sql)

                    if self.team_id:
                        sql = "UPDATE sale_order SET team_id = %s WHERE id = %s" % (
                            self.team_id.id,
                            order_id.id
                        )
                        self.env.cr.execute(sql)
                # ar_qt_activity_type
                if self.ar_qt_activity_type:
                    if self.ar_qt_activity_type != 'both':
                        order_id.ar_qt_activity_type = self.ar_qt_activity_type
                    else:
                        order_id.ar_qt_activity_type = 'todocesped'
                # ar_qt_customer_type
                if self.ar_qt_customer_type:
                    order_id.ar_qt_customer_type = self.ar_qt_customer_type

    @api.model
    def create(self, values):
        allow_create = True
        # ar_qt_activity_type
        if 'ar_qt_activity_type' not in values:
            values['ar_qt_activity_type'] = 'todocesped'
        # ar_qt_customer_type
        if 'ar_qt_customer_type' not in values:
            values['ar_qt_customer_type'] = 'particular'
        # prevent duplicate
        if 'partner_id' in values:
            if values['partner_id']:
                sale_quote_template_obj = self.env['crm.lead'].search(
                    [
                        ('active', '=', True),
                        ('partner_id', '=', values['partner_id']),
                        ('ar_qt_activity_type', '=', values['ar_qt_activity_type']),
                        ('ar_qt_customer_type', '=', values['ar_qt_customer_type']),
                        ('probability', '<', 100),
                    ]
                )
                if sale_quote_template_obj:
                    allow_create = False
                    raise UserError(
                        _("No se puede crear otro flujo para el mismo contacto,"
                          " tipo de actividad y tipo de cliente si ya existe "
                          "uno abierto")
                    )
        # operations
        if allow_create:
            return_object = super(CrmLead, self).create(values)
            # fix change team_id
            if self.user_id:
                team_ids = self.env['crm.team'].search(
                    [
                        ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                    ]
                )
                if team_ids:
                    team_modify = False
                    for team_id in team_ids:
                        if team_id.ar_qt_customer_type \
                                and team_id.ar_qt_customer_type == \
                                self.ar_qt_customer_type:
                            self.team_id = team_id.id
                            team_modify = True
                        else:
                            if not team_modify:
                                self.team_id = team_id.id
            # return
            return return_object

    @api.multi
    def write(self, vals):
        allow_write = True
        if self.id > 0:
            # check imposible team_id
            if 'team_id' in vals:
                team_obj = self.env['crm.team'].browse(vals['team_id'])
                # ar_qt_activity_type
                ar_qt_activity_type_check = self.ar_qt_activity_type
                if 'ar_qt_activity_type' in vals:
                    ar_qt_activity_type_check = vals['ar_qt_activity_type']
                # ar_qt_customer_type
                ar_qt_customer_type_check = self.ar_qt_customer_type
                if 'ar_qt_customer_type' in vals:
                    ar_qt_customer_type_check = vals['ar_qt_customer_type']
                # ar_qt_activity_type
                if team_obj.ar_qt_activity_type \
                        and team_obj.ar_qt_activity_type != ar_qt_activity_type_check:
                    allow_write = False
                    raise UserError(
                        _("No puedes cambiar el equipo de ventas a uno que "
                          "no corresponde de este tipo de actividad")
                    )
                elif team_obj.ar_qt_activity_type \
                        and team_obj.ar_qt_customer_type \
                        and team_obj.ar_qt_customer_type != ar_qt_customer_type_check:
                    allow_write = False
                    raise UserError(
                        _("No puedes cambiar el equipo de ventas a uno que "
                          "no corresponde de este tipo de cliente")
                    )
        # allow_write
        if allow_write:
            return_object = super(CrmLead, self).write(vals)
            self.fix_copy_custom_field_sale_orders(True)
            # return
            return return_object
