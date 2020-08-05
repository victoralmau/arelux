# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, fields, models
import operator
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
            ('none', 'Ninguno'),
            ('arelux', 'Arelux'),
            ('todocesped', 'Todocesped'),
            ('evert', 'Evert')
        ],
        string='Tipo de actividad',
        default='none'
    )
    ar_qt_customer_type = fields.Selection(
        selection=[
            ('none', 'Ninguno'),
            ('particular', 'Particular'),
            ('profesional', 'Profesional')
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
    user_line = fields.One2many(
        'arelux.sale.report.line.user',
        'arelux_sale_report_line_id',
        string='User Lines',
        copy=True
    )
    sale_order_line = fields.One2many(
        'arelux.sale.report.line.sale.order',
        'arelux_sale_report_line_id',
        string='Sale Order Lines',
        copy=True
    )

    @api.multi
    def remove_all_user_line(self):
        for item in self:
            line_user_ids = self.env['arelux.sale.report.line.user'].search(
                [
                    ('arelux_sale_report_line_id', '=', item.id)
                ]
            )
            if line_user_ids:
                for line_user_id in line_user_ids:
                    line_user_id.unlink()

    @api.multi
    def remove_all_sale_order_line(self):
        for item in self:
            order_ids = self.env['arelux.sale.report.line.sale.order'].search(
                [
                    ('arelux_sale_report_line_id', '=', item.id)
                ]
            )
            if order_ids:
                for order_id in order_ids:
                    order_id.unlink()

    @api.multi
    def _get_line_info_real(self, custom_type):
        self.ensure_one()
        return_values = {
            'response_type': '',
            'response_result_value': ''
        }
        if custom_type == 'sale_order_done_amount_untaxed':
            filters = [
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '>', 0),
                ('claim', '=', False),
                (
                    'confirmation_date',
                    '>=',
                    self.arelux_sale_report_id.date_from_filter
                ),
                (
                    'confirmation_date',
                    '<=',
                    self.arelux_sale_report_id.date_to_filter
                )
            ]
            # ar_qt_activity_type
            if self.ar_qt_activity_type != 'none':
                filters.append(
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                )
            # ar_qt_customer_type
            if self.ar_qt_customer_type != 'none':
                filters.append(
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type)
                )
            # sale_team_id
            if self.crm_team_id:
                filters.append(
                    ('sale_team_id', '=', self.crm_team_id.id)
                )

            order_ids = self.env['sale.order'].search(filters)

            if not self.group_by_user:
                return_values['response_type'] = 'sum'
                amount_untaxed = sum(order_ids.mapped('amount_untaxed'))
                return_values['response_result_value'] = amount_untaxed
                return_values['amount_untaxed'] = amount_untaxed
            else:
                return_values['response_type'] = 'list_by_user_id'

                res_users = {}
                if order_ids:
                    for order_id in order_ids:
                        # fix if need create
                        user_id = int(order_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'amount_untaxed': 0
                            }
                            if user_id > 0:
                                res_users[user_id]['name'] = order_id.user_id.name
                        # sum
                        res_users[user_id]['amount_untaxed'] += order_id.amount_untaxed
                # fix response_result_value
                return_values['response_result_value'] = 'amount_untaxed'
                return_values['amount_untaxed'] = \
                    sum(order_ids.mapped('amount_untaxed'))
                # remove_all
                self.remove_all_user_line()
                # creates
                if order_ids:
                    for res_user_id, res_user in res_users.items():
                        vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'amount_untaxed': res_user['amount_untaxed']
                        }
                        self.env['arelux.sale.report.line.user'].sudo().create(vals)

        elif custom_type == 'sale_order_done_count':
            filters = [
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '>', 0),
                ('claim', '=', False),
                (
                    'confirmation_date',
                    '>=',
                    self.arelux_sale_report_id.date_from_filter
                ),
                (
                    'confirmation_date',
                    '<=',
                    self.arelux_sale_report_id.date_to_filter
                )
            ]
            # ar_qt_activity_type
            if self.ar_qt_activity_type != 'none':
                filters.append(
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                )
            # ar_qt_customer_type
            if self.ar_qt_customer_type != 'none':
                filters.append(
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type)
                )
            # sale_team_id
            if self.crm_team_id:
                filters.append(
                    ('sale_team_id', '=', self.crm_team_id.id)
                )

            order_ids = self.env['sale.order'].search(filters)

            if not self.group_by_user:
                return_values['response_type'] = 'count'
                return_values['response_result_value'] = len(order_ids)
                return_values['count'] = len(order_ids)
            else:
                return_values['response_type'] = 'list_by_user_id'

                res_users = {}
                if order_ids:
                    for order_id in order_ids:
                        # fix if need create
                        user_id = int(order_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'count': 0
                            }
                            if user_id > 0:
                                res_users[user_id]['name'] = order_id.user_id.name
                        # sum
                        res_users[user_id]['count'] += 1
                # fix response_result_value
                return_values['response_result_value'] = 'count'
                return_values['count'] = len(order_ids)
                # remove_all
                self.remove_all_user_line()
                # creates
                if order_ids:
                    for res_user_id, res_user in res_users.items():
                        vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'count': res_user['count']
                        }
                        self.env['arelux.sale.report.line.user'].sudo().create(vals)

        elif custom_type == 'sale_order_ticket_medio':
            filters = [
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '>', 0),
                ('claim', '=', False),
                (
                    'confirmation_date',
                    '>=',
                    self.arelux_sale_report_id.date_from_filter
                ),
                (
                    'confirmation_date',
                    '<=',
                    self.arelux_sale_report_id.date_to_filter
                )
            ]
            # ar_qt_activity_type
            if self.ar_qt_activity_type != 'none':
                filters.append(
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                )
            # ar_qt_customer_type
            if self.ar_qt_customer_type != 'none':
                filters.append(
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type)
                )
            # sale_team_id
            if self.crm_team_id:
                filters.append(
                    ('sale_team_id', '=', self.crm_team_id.id)
                )

            order_ids = self.env['sale.order'].search(filters)

            if not self.group_by_user:
                return_values['response_type'] = 'sum'
                amount_untaxed = sum(order_ids.mapped('amount_untaxed'))

                ticket_medio = 0
                if order_ids:
                    ticket_medio = (amount_untaxed/len(order_ids))

                ticket_medio = "{0:.2f}".format(ticket_medio)
                return_values['response_result_value'] = ticket_medio
                return_values['ticket_medio'] = ticket_medio
            else:
                return_values['response_type'] = 'list_by_user_id'

                res_users = {}
                if order_ids:
                    for order_id in order_ids:
                        # fix if need create
                        user_id = int(order_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'count': 0,
                                'amount_untaxed': 0
                            }
                            if user_id > 0:
                                res_users[user_id]['name'] = order_id.user_id.name
                        # sum
                        res_users[user_id]['count'] += 1
                        res_users[user_id]['amount_untaxed'] += order_id.amount_untaxed
                # fix response_result_value
                return_values['response_result_value'] = 'amount_untaxed'
                amount_untaxed = sum(order_ids.mapped('amount_untaxed'))

                ticket_medio = 0
                if order_ids:
                    ticket_medio = (amount_untaxed/len(order_ids))

                ticket_medio = "{0:.2f}".format(ticket_medio)
                return_values['ticket_medio'] = ticket_medio
                # remove_all
                self.remove_all_user_line()
                # creates
                if order_ids:
                    for res_user_id, res_user in res_users.items():
                        vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'amount_untaxed': 0
                        }
                        if res_user['count'] > 0:
                            vals['amount_untaxed'] = \
                                (res_user['amount_untaxed']/res_user['count'])

                        self.env['arelux.sale.report.line.user'].sudo().create(vals)

        elif custom_type == 'sale_order_sent_count':
            filters = [
                ('date_order_management', '!=', False),
                ('amount_untaxed', '>', 0),
                ('opportunity_id', '!=', False),
                ('claim', '=', False),
                (
                    'date_order_management',
                    '>=',
                    self.arelux_sale_report_id.date_from_filter
                ),
                (
                    'date_order_management',
                    '<=',
                    self.arelux_sale_report_id.date_to_filter
                )
            ]
            # ar_qt_activity_type
            if self.ar_qt_activity_type != 'none':
                filters.append(
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                )
            # ar_qt_customer_type
            if self.ar_qt_customer_type != 'none':
                filters.append(
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type)
                )
            # sale_team_id
            if self.crm_team_id:
                filters.append(
                    ('sale_team_id', '=', self.crm_team_id.id)
                )

            order_ids = self.env['sale.order'].search(filters)

            if not self.group_by_user:
                return_values['response_type'] = 'count'
                return_values['response_result_value'] = len(order_ids)
                return_values['count'] = len(order_ids)
            else:
                return_values['response_type'] = 'list_by_user_id'

                res_users = {}
                if order_ids:
                    for order_id in order_ids:
                        # fix if need create
                        user_id = int(order_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'count': 0
                            }
                            if user_id > 0:
                                res_users[user_id]['name'] = order_id.user_id.name
                        # sum
                        res_users[user_id]['count'] += 1
                # fix response_result_value
                return_values['response_result_value'] = 'count'
                return_values['count'] = len(order_ids)
                # remove_all
                self.remove_all_user_line()
                # creates
                if order_ids:
                    for res_user_id, res_user in res_users.items():
                        vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'count': res_user['count']
                        }
                        self.env['arelux.sale.report.line.user'].sudo().create(vals)

        elif custom_type == 'sale_order_done_muestras':
            filters = [
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '=', 0),
                ('claim', '=', False),
                ('carrier_id', '!=', False),
                ('carrier_id.carrier_type', '=', 'nacex'),
                (
                    'confirmation_date',
                    '>=',
                    self.arelux_sale_report_id.date_from_filter
                ),
                (
                    'confirmation_date',
                    '<=',
                    self.arelux_sale_report_id.date_to_filter
                )
            ]
            # ar_qt_activity_type
            if self.ar_qt_activity_type != 'none':
                filters.append(
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                )
            # ar_qt_customer_type
            if self.ar_qt_customer_type != 'none':
                filters.append(
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type)
                )
            # sale_team_id
            if self.crm_team_id:
                filters.append(
                    ('sale_team_id', '=', self.crm_team_id.id)
                )

            order_ids = self.env['sale.order'].search(filters)

            if not self.group_by_user:
                return_values['response_type'] = 'count'
                return_values['response_result_value'] = len(order_ids)
                return_values['count'] = len(order_ids)
            else:
                return_values['response_type'] = 'list_by_user_id'

                res_users = {}
                if order_ids:
                    for order_id in order_ids:
                        # fix if need create
                        user_id = int(order_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'count': 0
                            }
                            if user_id > 0:
                                res_users[user_id]['name'] = order_id.user_id.name
                        # sum
                        res_users[user_id]['count'] += 1
                # fix response_result_value
                return_values['response_result_value'] = 'count'
                return_values['count'] = len(order_ids)
                # remove_all
                self.remove_all_user_line()
                # creates
                if order_ids:
                    for res_user_id, res_user in res_users.items():
                        vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'count': res_user['count']
                        }
                        self.env['arelux.sale.report.line.user'].sudo().create(vals)

        elif custom_type == 'res_partner_potencial_count':
            return_values['response_type'] = 'list_by_user_id'
            filters = [
                ('type', '=', 'contact'),
                ('active', '=', True),
                ('create_uid', '!=', 1),
                (
                    'create_date',
                    '>=',
                    self.arelux_sale_report_id.date_from_filter
                ),
                (
                    'create_date',
                    '<=',
                    self.arelux_sale_report_id.date_to_filter
                )
            ]
            # ar_qt_activity_type
            if self.ar_qt_activity_type != 'none':
                filters.append(
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                )
            # ar_qt_customer_type
            if self.ar_qt_customer_type != 'none':
                filters.append(
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type)
                )

            res_users = {}
            partner_ids = self.env['res.partner'].search(filters)
            if partner_ids:
                for partner_id in partner_ids:
                    # fix if need create
                    user_id = int(partner_id.create_uid.id)
                    if user_id not in res_users:
                        res_users[user_id] = {
                            'id': user_id,
                            'name': 'Sin comercial',
                            'total': 0
                        }
                        if user_id > 0:
                            res_users[user_id]['name'] = partner_id.create_uid.name
                    # sum
                    res_users[user_id]['total'] += 1
            # fix response_result_value
            return_values['response_result_value'] = 'count'
            # remove_all
            self.remove_all_user_line()
            # creates
            if partner_ids:
                for res_user_id, res_user in res_users.items():
                    vals = {
                        'arelux_sale_report_line_id': self.id,
                        'user_id': res_user['id'],
                        'count': res_user['total']
                    }
                    self.env['arelux.sale.report.line.user'].sudo().create(vals)

        elif custom_type == 'cartera_actual_activa_count':
            filters = [
                ('type', '=', 'contact'),
                ('active', '=', True),
                ('user_id', '!=', False),
                ('sale_order_amount_untaxed_year_now', '>', 0),
                (
                    'create_date',
                    '>=',
                    self.arelux_sale_report_id.date_from_filter
                ),
                (
                    'create_date',
                    '<=',
                    self.arelux_sale_report_id.date_to_filter
                )
            ]
            # ar_qt_activity_type
            if self.ar_qt_activity_type != 'none':
                filters.append(
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                )
            # ar_qt_customer_type
            if self.ar_qt_customer_type != 'none':
                filters.append(
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type)
                )

            partner_ids = self.env['res.partner'].search(filters)

            if not self.group_by_user:
                return_values['response_type'] = 'count'
                return_values['response_result_value'] = len(partner_ids)
                return_values['count'] = len(partner_ids)
            else:
                return_values['response_type'] = 'list_by_user_id'

                res_users = {}
                if partner_ids:
                    for partner_id in partner_ids:
                        # fix if need create
                        user_id = int(partner_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'count': 0
                            }
                            if user_id > 0:
                                res_users[user_id]['name'] = partner_id.user_id.name
                        # sum
                        res_users[user_id]['count'] += 1
                # fix response_result_value
                return_values['response_result_value'] = 'count'
                return_values['count'] = len(partner_ids)
                # remove_all
                self.remove_all_user_line()
                # creates
                if partner_ids:
                    for res_user_id, res_user in res_users.items():
                        vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'count': res_user['count']
                        }
                        self.env['arelux.sale.report.line.user'].sudo().create(vals)

        elif custom_type == 'cartera_actual_count':
            filters = [
                ('type', '=', 'contact'),
                ('active', '=', True),
                ('user_id', '!=', False),
                (
                    'create_date',
                    '>=',
                    self.arelux_sale_report_id.date_from_filter
                ),
                (
                    'create_date',
                    '<=',
                    self.arelux_sale_report_id.date_to_filter
                )
            ]
            # ar_qt_activity_type
            if self.ar_qt_activity_type != 'none':
                filters.append(
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                )
            # ar_qt_customer_type
            if self.ar_qt_customer_type != 'none':
                filters.append(
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type)
                )

            partner_ids = self.env['res.partner'].search(filters)

            if not self.group_by_user:
                return_values['response_type'] = 'count'
                return_values['response_result_value'] = len(partner_ids)
                return_values['count'] = len(partner_ids)
            else:
                return_values['response_type'] = 'list_by_user_id'
                res_users = {}
                if partner_ids:
                    for partner_id in partner_ids:
                        # fix if need create
                        user_id = int(partner_id.user_id.id)
                        if user_id not in res_users:
                            res_users[user_id] = {
                                'id': user_id,
                                'name': 'Sin comercial',
                                'total': 0
                            }
                            if user_id > 0:
                                res_users[user_id]['name'] = partner_id.user_id.name
                        # sum
                        res_users[user_id]['total'] += 1
                # fix response_result_value
                return_values['response_result_value'] = 'count'
                return_values['count'] = len(partner_ids)
                # remove_all
                self.remove_all_user_line()
                # creates
                if partner_ids:
                    for res_user_id, res_user in res_users.items():
                        vals = {
                            'arelux_sale_report_line_id': self.id,
                            'user_id': res_user['id'],
                            'count': res_user['total']
                        }
                        self.env['arelux.sale.report.line.user'].sudo().create(vals)

        elif custom_type == 'nuevos_clientes_con_ventas':
            return_values['response_type'] = 'list_sale_orders'
            # partner_ids with sale_orders < date_from
            res_partner_ids = []
            filters = [
                ('state', 'in', ('sale', 'done')),
                ('claim', '=', False),
                ('amount_untaxed', '>', 0),
                (
                    'confirmation_date',
                    '<',
                    self.arelux_sale_report_id.date_from_filter
                ),
            ]
            # ar_qt_activity_type
            if self.ar_qt_activity_type != 'none':
                filters.append(
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                )
            # ar_qt_customer_type
            if self.ar_qt_customer_type != 'none':
                filters.append(
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type)
                )

            order_ids = self.env['sale.order'].search(filters)
            if order_ids:
                for order_id in order_ids:
                    if order_id.partner_id.id not in res_partner_ids:
                        res_partner_ids.append(order_id.partner_id.id)
            # sale_orders with filters and partner_id not in
            filters = [
                ('state', 'in', ('sale', 'done')),
                ('claim', '=', False),
                ('amount_untaxed', '>', 0),
                ('partner_id', 'not in', res_partner_ids),
                (
                    'confirmation_date',
                    '>=',
                    self.arelux_sale_report_id.date_from_filter
                ),
                (
                    'confirmation_date',
                    '<=',
                    self.arelux_sale_report_id.date_to_filter
                )
            ]
            # ar_qt_activity_type
            if self.ar_qt_activity_type != 'none':
                filters.append(
                    ('ar_qt_activity_type', '=', self.ar_qt_activity_type)
                )
            # ar_qt_customer_type
            if self.ar_qt_customer_type != 'none':
                filters.append(
                    ('ar_qt_customer_type', '=', self.ar_qt_customer_type)
                )

            order_ids = self.env['sale.order'].search(filters)
            # sort_custom
            order_ids2 = []
            if order_ids:
                for order_id in order_ids:
                    order_ids2.append({
                        'id': order_id.id,
                        'user_name': order_id.user_id.name
                    })
                order_ids = sorted(
                    order_ids2,
                    key=operator.itemgetter('user_name')
                )
            # remove_all
            self.remove_all_sale_order_line()
            # creates
            if order_ids:
                for order_id in order_ids:
                    vals = {
                        'arelux_sale_report_line_id': self.id,
                        'sale_order_id': order_id.id
                    }
                    self.env['arelux.sale.report.line.sale.order'].sudo().create(vals)

        return return_values

    @api.multi
    def _get_line_info(self):
        self.ensure_one()
        if self.arelux_sale_report_type_id:
            if self.arelux_sale_report_type_id.custom_type == 'ratio_muestras':
                if not self.group_by_user:
                    res_1 = self._get_line_info_real(
                        'sale_order_done_muestras'
                    )[0]
                    res_2 = self._get_line_info_real(
                        'sale_order_sent_count'
                    )[0]
                    self.response_type = 'percent'
                    ratio = 0
                    if res_1['count'] > 0 \
                            and res_2['count'] > 0:
                        ratio = (float(res_1['count'])/float(res_2['count']))*100

                    self.response_result_value = "{0:.2f}".format(ratio)
                else:
                    self.response_type = 'percent'
                    self.response_result_value = 'percent'

            elif self.arelux_sale_report_type_id.custom_type == 'ratio_calidad':
                if not self.group_by_user:
                    self.response_type = 'percent'
                    res_1 = self._get_line_info_real(
                        'sale_order_done_count'
                    )[0]
                    res_2 = self._get_line_info_real(
                        'sale_order_sent_count'
                    )[0]
                    ratio = 0
                    if res_1['count'] > 0 \
                            and res_2['count'] > 0:
                        ratio = (float(res_1['count'])/float(res_2['count']))*100

                    self.response_result_value = "{0:.2f}".format(ratio)
                else:
                    self.response_type = 'percent'
                    self.response_result_value = 'percent'

            elif self.arelux_sale_report_type_id.custom_type == 'line_break':
                self.response_type = 'line_break'
            else:
                res = self._get_line_info_real(
                    self.arelux_sale_report_type_id.custom_type
                )[0]
                self.response_type = res['response_type']
                self.response_result_value = res['response_result_value']
        # _logger.info(response)
        # return response
