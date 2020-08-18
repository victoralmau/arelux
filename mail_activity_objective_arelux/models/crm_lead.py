# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, models, fields, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    activities_count = fields.Integer(
        compute='_compute_activities_count',
        string="Actividades (count)",
    )
    crm_activity_ids = fields.One2many(
        'crm.activity.report',
        'lead_id',
        string='Actividades'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency id',
        default=lambda self: self.env.user.company_id.currency_id
    )
    partner_id_total_sale_order = fields.Integer(
        string='Nº Pedidos (cliente)',
        related='partner_id.total_sale_order',
        store=False,
        readonly=True
    )
    total_sale_order = fields.Integer(
        string="Nº Pedidos (oport)",
        help="Nº pedidos > 300€ de ese cliente (Flujo)",
        default=0,
        readonly=True
    )
    total_sale_order_last_30_days = fields.Integer(
        string="Nº pedidos 30 dias",
        help="Nº pedidos (>300€) de los ultimos 30 dias",
        default=0,
        readonly=True
    )
    total_sale_order_last_90_days = fields.Integer(
        string="Nº pedidos 90 dias",
        help="Nº pedidos (>300€) de los ultimos 90 dias",
        default=0,
        readonly=True
    )
    total_sale_order_last_12_months = fields.Integer(
        string="Nº pedidos 12 meses",
        help="Nº pedidos (>300€) de los ultimos 12 meses",
        default=0,
        readonly=True
    )
    partner_id_account_invoice_amount_untaxed_total = fields.Monetary(
        string='Facturación (cliente)',
        related='partner_id.account_invoice_amount_untaxed_total',
        store=False,
        readonly=True
    )
    account_invoice_amount_untaxed_total = fields.Monetary(
        string="Facturación (oport)",
        help="Historico de facturacion (BI) de ese cliente (Flujo)",
        readonly=True
    )
    days_from_last_sale_order = fields.Integer(
        string="Dias desde pto",
        help="Nº de dias desde el ultimo presupuesto enviado",
        default=0,
        readonly=True
    )
    date_from_last_sale_order = fields.Date(
        string="Fecha desde pto",
        readonly=True
    )
    days_from_last_message = fields.Integer(
        string="Dias desde contacto",
        help="Nº de dias desde el ultimo contacto (Generalmente "
             "mensaje enviado como remitente el comercial)",
        default=0,
        readonly=True
    )
    date_from_last_message = fields.Date(
        string="Fecha desde contacto",
        readonly=True
    )

    @api.multi
    @api.depends('crm_activity_ids')
    def _compute_activities_count(self):
        for item in self:
            item.activities_count = len(item.crm_activity_ids)

    @api.model
    def cron_odoo_crm_lead_fields_generate(self):
        self._cr.execute("""
            UPDATE crm_lead SET (total_sale_order, total_sale_order_last_30_days,
            total_sale_order_last_90_days, total_sale_order_last_12_months,
            date_from_last_sale_order) = (
            SELECT clr.total_sale_order, total_sale_order_last_30_days,
            total_sale_order_last_90_days, total_sale_order_last_12_months,
            last_date_order_management
            FROM crm_lead_report AS clr
            WHERE clr.lead_id = crm_lead.id
            )
            WHERE crm_lead.id IN (
            SELECT clr2.lead_id
            FROM crm_lead_report AS clr2
            LEFT JOIN crm_lead AS cl ON clr2.lead_id = cl.id
            WHERE (
            (cl.total_sale_order <> clr2.total_sale_order)
            OR (cl.total_sale_order_last_30_days <> clr2.total_sale_order_last_30_days)
            OR (cl.total_sale_order_last_90_days <> clr2.total_sale_order_last_90_days)
            OR (cl.total_sale_order_last_12_months  <>
            clr2.total_sale_order_last_12_months)
            OR (cl.date_from_last_sale_order IS NOT NULL
            AND cl.date_from_last_sale_order <> clr2.last_date_order_management)
            OR (cl.date_from_last_sale_order IS NULL
            AND clr2.last_date_order_management IS NOT NULL))
            LIMIT 1000
            )
        """)
        self._cr.execute("""
            UPDATE crm_lead SET (account_invoice_amount_untaxed_total) = (
            SELECT ROUND((clair.amount_untaxed_total_out_invoice-
            clair.amount_untaxed_total_out_refund)::numeric,2)::float
            FROM crm_lead_account_invoice_report AS clair
            WHERE clair.lead_id = crm_lead.id
            )
            WHERE crm_lead.id IN (
            SELECT clair2.lead_id
            FROM crm_lead_account_invoice_report AS clair2
            LEFT JOIN crm_lead AS cl ON clair2.lead_id = cl.id
            WHERE (clair2.amount_untaxed_total_out_invoice IS NOT NULL
            OR clair2.amount_untaxed_total_out_refund IS NOT NULL)
            AND (
            (
            cl.account_invoice_amount_untaxed_total IS NOT NULL
            AND (ROUND((clair2.amount_untaxed_total_out_invoice-
            clair2.amount_untaxed_total_out_refund)::numeric,2)::float <>
            cl.account_invoice_amount_untaxed_total))
            OR cl.account_invoice_amount_untaxed_total IS NULL
            )
            LIMIT 1000
            )
        """)
        self._cr.execute("""
        SELECT clmmr2.lead_id, clmmr2.date
        FROM crm_lead_mail_message_report AS clmmr2
        LEFT JOIN crm_lead AS cl ON clmmr2.lead_id = cl.id
        WHERE (
        (cl.date_from_last_message IS NOT NULL
        AND clmmr2.date  <> cl.date_from_last_message)
        OR (cl.date_from_last_message IS NULL
        AND clmmr2.date IS NOT NULL))
        AND clmmr2.lead_id > 0
        LIMIT 1000
        """)
        items = self._cr.fetchall()
        if len(items) > 0:
            for item in items:
                lead_ids = self.env['crm.lead'].search(
                    [
                        ('id', '=', item[0])
                    ]
                )
                if lead_ids:
                    lead_id = lead_ids[0]
                    lead_id.date_from_last_message = item[1]

        self._cr.execute("""
            UPDATE crm_lead SET (mobile, phone) = (
            SELECT rp.mobile, rp.phone
            FROM res_partner AS rp
            WHERE crm_lead.partner_id = rp.id
            )
            WHERE crm_lead.id IN (
            SELECT cl.id
            FROM crm_lead AS cl
            LEFT JOIN res_partner AS rp ON cl.partner_id = rp.id
            WHERE cl.partner_id IS NOT NULL
            AND (rp.mobile IS NOT NULL OR rp.phone IS NOT NULL)
            AND (
            (rp.mobile IS NOT NULL AND cl.mobile IS NULL)
            OR (rp.mobile IS NOT NULL AND cl.mobile IS NOT NULL
            AND rp.mobile <> cl.mobile)
            OR (rp.phone IS NOT NULL AND cl.phone IS NULL)
            OR (rp.phone IS NOT NULL AND cl.phone IS NOT NULL AND rp.phone <> cl.phone)
            )
            LIMIT 1000
            )
        """)

    @api.model
    def cron_odoo_crm_lead_fields_generate_days(self):
        self._cr.execute("""
            UPDATE crm_lead SET (days_from_last_sale_order) = (
            SELECT(NOW()::date - cl.date_from_last_sale_order)
            FROM crm_lead AS cl
            WHERE cl.id = crm_lead.id)
            WHERE crm_lead.date_from_last_sale_order IS NOT NULL
        """)
        self._cr.execute("""
            UPDATE crm_lead SET (days_from_last_message) = (
            SELECT(NOW()::date - cl.date_from_last_message)
            FROM crm_lead AS cl
            WHERE cl.id = crm_lead.id)
            WHERE crm_lead.date_from_last_message IS NOT NULL
        """)

    @api.model
    def cron_odoo_crm_lead_change_empty_next_activity_objective_id(self):
        _logger.info('cron_odoo_crm_lead_change_empty_next_activity_objective_id')
        self.cron_odoo_crm_lead_change_empty_next_activity_objective_id_todocesped()
        self.cron_odoo_crm_lead_change_empty_next_activity_objective_id_arelux()

    @api.model
    def cron_odoo_crm_lead_change_empty_next_activity_objective_id_todocesped(self):
        # ar_qt_todocesped_pf_customer_type=False
        crm_lead_ids = self.env['crm.lead'].search(
            [
                ('next_activity_objective_id.objective_type', '=', 'activation'),
                ('partner_id.ar_qt_activity_type', 'in', ('todocesped', 'both')),
                ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                ('partner_id.ar_qt_todocesped_pf_customer_type', '=', False),
                ('partner_id.total_sale_order', '=', 0),
                ('type', '=', 'opportunity'),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100)
            ]
        )
        # operations
        if crm_lead_ids:
            for crm_lead_id in crm_lead_ids:
                crm_lead_id.next_activity_objective_id = False
        # ar_qt_todocesped_pf_customer_type=other
        crm_lead_ids = self.env['crm.lead'].search(
            [
                ('next_activity_objective_id.objective_type', '=', 'activation'),
                ('partner_id.ar_qt_activity_type', 'in', ('todocesped', 'both')),
                ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                ('partner_id.ar_qt_todocesped_pf_customer_type', '=', 'other'),
                ('partner_id.total_sale_order', '=', 0),
                ('type', '=', 'opportunity'),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100)
            ]
        )
        # operations
        if crm_lead_ids:
            for crm_lead_id in crm_lead_ids:
                crm_lead_id.next_activity_objective_id = False

    @api.model
    def cron_odoo_crm_lead_change_empty_next_activity_objective_id_arelux(self):
        # ar_qt_arelux_pf_customer_type=False
        crm_lead_ids = self.env['crm.lead'].search(
            [
                ('next_activity_objective_id.objective_type', '=', 'activation'),
                ('partner_id.ar_qt_activity_type', '=', 'arelux'),
                ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                ('partner_id.ar_qt_arelux_pf_customer_type', '=', False),
                ('partner_id.total_sale_order', '=', 0),
                ('type', '=', 'opportunity'),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100)
            ]
        )
        # operations
        if crm_lead_ids:
            for crm_lead_id in crm_lead_ids:
                crm_lead_id.next_activity_objective_id = False
        # ar_qt_arelux_pf_customer_type=other
        crm_lead_ids = self.env['crm.lead'].search(
            [
                ('next_activity_objective_id.objective_type', '=', 'activation'),
                ('partner_id.ar_qt_activity_type', '=', 'arelux'),
                ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                ('partner_id.ar_qt_arelux_pf_customer_type', '=', 'other'),
                ('partner_id.total_sale_order', '=', 0),
                ('type', '=', 'opportunity'),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100)
            ]
        )
        # operations
        if crm_lead_ids:
            for crm_lead_id in crm_lead_ids:
                crm_lead_id.next_activity_objective_id = False

    @api.model
    def cron_odoo_crm_lead_change_seguimiento(self):
        self.cron_odoo_crm_lead_change_seguimiento_todocesped()
        self.cron_odoo_crm_lead_change_seguimiento_arelux()

    @api.model
    def cron_odoo_crm_lead_change_seguimiento_todocesped(self):
        # search
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        current_date_month = current_date.strftime("%m")
        if current_date_month in ['03', '04', '05', '06', '07', '08']:
            crm_lead_ids = self.env['crm.lead'].search(
                [
                    (
                        'next_activity_objective_id.objective_type',
                        'not in',
                        ('reserved', 'review', 'closing', 'tracking')
                    ),
                    ('partner_id.ar_qt_activity_type', 'in', ('todocesped', 'both')),
                    ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                    ('partner_id.total_sale_order_last_30_days', '>', 0),
                    ('type', '=', 'opportunity'),
                    ('active', '=', True),
                    ('probability', '>', 0),
                    ('probability', '<', 100)
                ]
            )
        else:
            crm_lead_ids = self.env['crm.lead'].search(
                [
                    (
                        'next_activity_objective_id.objective_type',
                        'not in',
                        ('reserved', 'review', 'closing', 'tracking')
                    ),
                    ('partner_id.ar_qt_activity_type', 'in', ('todocesped', 'both')),
                    ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                    ('partner_id.total_sale_order_last_90_days', '>', 0),
                    ('type', '=', 'opportunity'),
                    ('active', '=', True),
                    ('probability', '>', 0),
                    ('probability', '<', 100)
                ]
            )
        # tracking
        objective_ids = self.env['crm.activity.objective'].search(
            [
                ('objective_type', '=', 'tracking')
            ]
        )
        if objective_ids:
            # operations
            if crm_lead_ids:
                for crm_lead_id in crm_lead_ids:
                    crm_lead_id.next_activity_objective_id = objective_ids[0].id

    @api.model
    def cron_odoo_crm_lead_change_seguimiento_arelux(self):
        # search
        crm_lead_ids = self.env['crm.lead'].search(
            [
                (
                    'next_activity_objective_id.objective_type',
                    'not in',
                    ('reserved', 'review', 'closing', 'tracking')
                ),
                ('partner_id.ar_qt_activity_type', '=', 'arelux'),
                ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                ('partner_id.total_sale_order_last_90_days', '>', 0),
                ('type', '=', 'opportunity'),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100)
            ]
        )
        # tracking
        objective_ids = self.env['crm.activity.objective'].search(
            [
                ('objective_type', '=', 'tracking')
            ]
        )
        if objective_ids:
            # operations
            if crm_lead_ids:
                for crm_lead_id in crm_lead_ids:
                    crm_lead_id.next_activity_objective_id = objective_ids[0].id

    @api.model
    def cron_odoo_crm_lead_change_dormidos(self):
        self.cron_odoo_crm_lead_change_dormidos_todocesped()
        self.cron_odoo_crm_lead_change_dormidos_arelux()

    @api.model
    def cron_odoo_crm_lead_change_dormidos_todocesped(self):
        # search
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        current_date_month = current_date.strftime("%m")
        if current_date_month in ['03', '04', '05', '06', '07', '08']:
            crm_lead_ids = self.env['crm.lead'].search(
                [
                    (
                        'next_activity_objective_id.objective_type',
                        'not in',
                        ('reserved', 'review', 'closing', 'wake')
                    ),
                    ('partner_id.ar_qt_activity_type', 'in', ('todocesped', 'both')),
                    ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                    ('partner_id.total_sale_order_last_30_days', '=', 0),
                    ('partner_id.total_sale_order', '>', 0),
                    ('type', '=', 'opportunity'),
                    ('active', '=', True),
                    ('probability', '>', 0),
                    ('probability', '<', 100)
                ]
            )
        else:
            crm_lead_ids = self.env['crm.lead'].search(
                [
                    (
                        'next_activity_objective_id.objective_type',
                        'not in',
                        ('reserved', 'review', 'closing', 'wake')
                    ),
                    ('partner_id.ar_qt_activity_type', 'in', ('todocesped', 'both')),
                    ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                    ('partner_id.total_sale_order_last_90_days', '=', 0),
                    ('partner_id.total_sale_order', '>', 0),
                    ('type', '=', 'opportunity'),
                    ('active', '=', True),
                    ('probability', '>', 0),
                    ('probability', '<', 100)
                ]
            )
        # wake
        objective_ids = self.env['crm.activity.objective'].search(
            [
                ('objective_type', '=', 'wake')
            ]
        )
        if objective_ids:
            # operations
            if crm_lead_ids:
                for crm_lead_id in crm_lead_ids:
                    crm_lead_id.next_activity_objective_id = objective_ids[0].id

    @api.model
    def cron_odoo_crm_lead_change_dormidos_arelux(self):
        # search
        crm_lead_ids = self.env['crm.lead'].search(
            [
                (
                    'next_activity_objective_id.objective_type',
                    'not in',
                    ('reserved', 'review', 'closing', 'wake')
                ),
                ('partner_id.ar_qt_activity_type', '=', 'arelux'),
                ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                ('partner_id.total_sale_order_last_90_days', '=', 0),
                ('partner_id.total_sale_order', '>', 0),
                ('type', '=', 'opportunity'),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100)
            ]
        )
        # wake
        objective_ids = self.env['crm.activity.objective'].search(
            [
                ('objective_type', '=', 'wake')
            ]
        )
        if objective_ids:
            # operations
            if crm_lead_ids:
                for crm_lead_id in crm_lead_ids:
                    crm_lead_id.next_activity_objective_id = objective_ids[0].id

    @api.model
    def action_boton_pedir_dormido(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        current_date + relativedelta(hours=2)
        response = {
            'errors': True,
            'error': _("No tienes flujos de objetivo Despertar sin "
                       "siguiente actividad para poder asignarte")
        }
        lead_ids = self.env['crm.lead'].search(
            [
                ('next_activity_objective_id.objective_type', '=', 'wake'),
                ('user_id', '=', self._uid),
                ('date_action', '=', False),
                ('type', '=', 'opportunity'),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100)
            ]
        )
        if lead_ids:
            lead_id = False
            # criterio_1
            lead_ids2 = self.env['crm.lead'].search(
                [
                    ('id', 'in', lead_ids.ids),
                    ('partner_id.total_sale_order_last_12_months', '>', 2)
                ],
                order='total_sale_order_last_12_months desc'
            )
            if lead_ids2:
                lead_id = lead_ids2[0]
            # criterio_2
            if not lead_id:
                # criterio_2 (Todocesped)
                lead_ids2 = self.env['crm.lead'].search(
                    [
                        ('id', 'in', lead_ids.ids),
                        (
                            'partner_id.ar_qt_activity_type',
                            'in',
                            ('todocesped', 'both')
                        ),
                        ('partner_id.total_sale_order_last_12_months', '>', 0),
                        (
                            'ar_qt_todocesped_pf_customer_type',
                            'in',
                            (
                                'gardener', 'pool', 'multiservice',
                                'warehouse_construction', 'nursery'
                            )
                        )
                    ],
                    order='total_sale_order_last_12_months desc'
                )
                if lead_ids2:
                    lead_id = lead_ids2[0]
                # criterio_2 (Arelux)
                lead_ids2 = self.env['crm.lead'].search(
                    [
                        ('id', 'in', lead_ids.ids),
                        ('partner_id.ar_qt_activity_type', '=', 'arelux'),
                        ('partner_id.total_sale_order_last_12_months', '>', 0),
                    ],
                    order='total_sale_order_last_12_months desc'
                )
                if lead_ids2:
                    lead_id = lead_ids2[0]
            # criterio_3
            if not lead_id:
                # criterio_3 (Todocesped)
                lead_ids2 = self.env['crm.lead'].search(
                    [
                        ('id', 'in', lead_ids.ids),
                        (
                            'partner_id.ar_qt_activity_type',
                            'in',
                            ('todocesped', 'both')
                        ),
                        ('partner_id.total_sale_order_last_12_months', '>', 0),
                        (
                            'ar_qt_todocesped_pf_customer_type',
                            'in',
                            ('construction', 'architect', 'decorator', 'event_planner')
                        )
                    ],
                    order='total_sale_order_last_12_months desc'
                )
                if lead_ids2:
                    lead_id = lead_ids2[0]
                # criterio_3 (Arelux)
                lead_ids2 = self.env['crm.lead'].search(
                    [
                        ('id', 'in', lead_ids.ids),
                        ('partner_id.ar_qt_activity_type', '=', 'arelux'),
                        ('partner_id.total_sale_order_last_12_months', '>', 0),
                    ],
                    order='total_sale_order_last_12_months desc'
                )
                if lead_ids2:
                    lead_id = lead_ids2[0]
            # other
            if not lead_id:
                lead_ids2 = self.env['crm.lead'].search(
                    [
                        ('id', 'in', lead_ids.ids)
                    ]
                )
                if lead_ids2:
                    lead_id = lead_ids2[0]
            # operations
            if lead_id:
                lead_id.date_action = current_date.strftime("%Y-%m-%d %H:%M:%S")
                response['errors'] = False
            else:
                response['error'] = \
                    _("No tienes flujos de objetivo Despertar sin siguiente "
                      "actividad para poder asignarte")
        # return
        return response

    @api.model
    def cron_odoo_crm_lead_change_inactivos(self):
        self.cron_odoo_crm_lead_change_inactivos_todocesped()
        self.cron_odoo_crm_lead_change_inactivos_arelux()

    @api.model
    def cron_odoo_crm_lead_change_inactivos_todocesped(self):
        _logger.info('cron_odoo_crm_lead_change_inactivos_todocesped')
        # search
        lead_ids = self.env['crm.lead'].search(
            [
                (
                    'next_activity_objective_id.objective_type',
                    'not in',
                    ('reserved', 'review', 'closing', 'activation')
                ),
                (
                    'partner_id.ar_qt_activity_type',
                    'in',
                    ('todocesped', 'both')
                ),
                ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                ('partner_id.ar_qt_todocesped_pf_customer_type', '!=', False),
                ('partner_id.ar_qt_todocesped_pf_customer_type', '!=', 'other'),
                ('partner_id.total_sale_order', '=', 0),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100)
            ]
        )
        # activation
        objective_ids = self.env['crm.activity.objective'].search(
            [
                ('objective_type', '=', 'activation')
            ]
        )
        if objective_ids:
            if lead_ids:
                for lead_id in lead_ids:
                    lead_id.next_activity_objective_id = objective_ids[0].id

    @api.model
    def cron_odoo_crm_lead_change_inactivos_arelux(self):
        # search
        lead_ids = self.env['crm.lead'].search(
            [
                (
                    'next_activity_objective_id.objective_type',
                    'not in',
                    ('reserved', 'review', 'closing', 'activation')
                ),
                ('partner_id.ar_qt_activity_type', '=', 'arelux'),
                ('partner_id.ar_qt_customer_type', '=', 'profesional'),
                ('partner_id.ar_qt_arelux_pf_customer_type', '!=', False),
                ('partner_id.ar_qt_arelux_pf_customer_type', '!=', 'other'),
                ('partner_id.total_sale_order', '=', 0),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100)
            ]
        )
        # activation
        objective_ids = self.env['crm.activity.objective'].search(
            [
                ('objective_type', '=', 'activation')
            ]
        )
        if objective_ids:
            if lead_ids:
                for lead_id in lead_ids:
                    lead_id.next_activity_objective_id = objective_ids[0].id

    @api.model
    def action_boton_pedir_activo(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        current_date + relativedelta(hours=2)
        response = {
            'errors': True,
            'error': _("No tienes flujos de objetivo Activar sin "
                       "siguiente actividad para poder asignarte")
        }
        lead_ids = self.env['crm.lead'].search(
            [
                ('next_activity_objective_id.objective_type', '=', 'activation'),
                ('user_id', '=', self._uid),
                ('date_action', '=', False),
                ('type', '=', 'opportunity'),
                ('active', '=', True),
                ('probability', '>', 0),
                ('probability', '<', 100)
            ]
        )
        if lead_ids:
            lead_id = False
            # criterio_1 (Todocesped)
            lead_ids2 = self.env['crm.lead'].search(
                [
                    ('id', 'in', lead_ids.ids),
                    ('partner_id.ar_qt_activity_type', 'in', ('todocesped', 'both')),
                    ('partner_id.total_sale_order_last_12_months', '>', 0),
                    ('partner_id.ar_qt_todocesped_pf_customer_type', '=', 'other')
                ],
                order='total_sale_order_last_12_months desc'
            )
            if lead_ids2:
                lead_id = lead_ids2[0]
            # criterio_1 (Arelux)
            lead_ids2 = self.env['crm.lead'].search(
                [
                    ('id', 'in', lead_ids.ids),
                    ('partner_id.ar_qt_activity_type', '=', 'arelux'),
                    ('partner_id.total_sale_order_last_12_months', '>', 0),
                    ('partner_id.ar_qt_arelux_pf_customer_type', '=', 'other')
                ],
                order='total_sale_order_last_12_months desc'
            )
            if lead_ids2:
                lead_id = lead_ids2[0]
            # criterio_2 (Todocesped + Arelux)
            if not lead_id:
                lead_ids2 = self.env['crm.lead'].search(
                    [
                        ('id', 'in', lead_ids.ids),
                        ('partner_id.total_sale_order', '>', 0),
                        ('account_invoice_amount_untaxed_total', '>', 2000)
                    ],
                    order='create_date asc'
                )
                if lead_ids2:
                    lead_id = lead_ids2[0]
            # criterio_3 (Todocesped + Arelux)
            if not lead_id:
                lead_ids2 = self.env['crm.lead'].search(
                    [
                        ('id', 'in', lead_ids.ids),
                        ('account_invoice_amount_untaxed_total', '>', 0)
                    ],
                    order='create_date asc'
                )
                if lead_ids2:
                    lead_id = lead_ids2[0]
            # other
            if not lead_id:
                lead_ids2 = self.env['crm.lead'].search(
                    [
                        ('id', 'in', lead_ids.ids)
                    ]
                )
                if lead_ids2:
                    lead_id = lead_ids2[0]
            # operations
            if lead_id:
                lead_id.date_action = current_date.strftime("%Y-%m-%d %H:%M:%S")
                response['errors'] = False
            else:
                response['error'] = \
                    _("No tienes flujos de objetivo Activar sin siguiente "
                      "actividad para poder asignarte")
        # return
        return response
