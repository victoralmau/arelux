# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

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
            ('sale_order_done_amount_untaxed', 'Ventas (Base Imponible)'),
            ('sale_order_done_count', 'Ventas (Cuenta)'),
            ('sale_order_ticket_medio', 'Ventas (Ticket medio)'),
            ('sale_order_sent_count', 'Ptos realizados (Cuenta)'),
            ('sale_order_done_muestras', 'Muestras enviadas (Cuenta)'),
            ('ratio_muestras', 'Ratio muestras'),
            ('ratio_calidad', 'Ratio calidad'),
            ('res_partner_potencial_count', 'Contactos potenciales (Cuenta)'),
            ('cartera_actual_activa_count', 'Cartera Actual activa (Cuenta)'),
            ('cartera_actual_count', 'Cartera Actual (Cuenta)'),
            ('nuevos_clientes_con_ventas', 'Nuevos clientes con ventas'),
            ('line_break', 'Salto de linea'),
        ],
        string='Custom Type',
        default=''
    )
    group_by_user = fields.Boolean(
        default=False,
        string='Group by user'
    )

    @api.multi
    def get_info(self,
                 date_from,
                 date_to,
                 ar_qt_activity_type,
                 ar_qt_customer_type,
                 sale_team_id
                 ):
        self.ensure_one()
        if self.custom_type == 'sale_order_done_amount_untaxed':
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
            # ar_qt_activity_type
            if ar_qt_activity_type != 'none':
                search_filters.append(('ar_qt_activity_type', '=', ar_qt_activity_type))
            # ar_qt_customer_type
            if ar_qt_customer_type != 'none':
                search_filters.append(('ar_qt_customer_type', '=', ar_qt_customer_type))
            # sale_team_id
            if sale_team_id > 0:
                search_filters.append(('sale_team_id', '=', sale_team_id))

            sale_order_ids = self.env['sale.order'].search(search_filters)
            amount_untaxed = sum(sale_order_ids.mapped('amount_untaxed'))

            response['result_value'] = amount_untaxed
            response['result'] = amount_untaxed
            return response
        else:
            return {
                'type': 'sum',
                'result_value': '',
                'result': ''
            }

    @api.multi
    def _get_sale_order_done(self,
                             date_from,
                             date_to,
                             ar_qt_activity_type,
                             ar_qt_customer_type,
                             sale_team_id
                             ):
        self.ensure_one()
        search_filters = [
            ('state', 'in', ('sale', 'done')),
            ('amount_untaxed', '>', 0),
            ('confirmation_date', '>=', date_from),
            ('confirmation_date', '<=', date_to)
        ]
        # ar_qt_activity_type
        if ar_qt_activity_type != 'none':
            search_filters.append(('ar_qt_activity_type', '=', ar_qt_activity_type))
        # ar_qt_customer_type
        if ar_qt_customer_type != 'none':
            search_filters.append(('ar_qt_customer_type', '=', ar_qt_customer_type))
        # sale_team_id
        if sale_team_id > 0:
            search_filters.append(('sale_team_id', '=', sale_team_id))

        _logger.info(search_filters)
        ids = self.env['sale.order'].search(search_filters)
        _logger.info(ids)
        return ids

    @api.multi
    def _get_line_info_sale_order_done_amount_untaxed(self,
                                                      date_from,
                                                      date_to,
                                                      ar_qt_activity_type,
                                                      ar_qt_customer_type,
                                                      sale_team_id
                                                      ):
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
        # ar_qt_activity_type
        if ar_qt_activity_type != 'none':
            search_filters.append(('ar_qt_activity_type', '=', ar_qt_activity_type))
        # ar_qt_customer_type
        if ar_qt_customer_type != 'none':
            search_filters.append(('ar_qt_customer_type', '=', ar_qt_customer_type))
        # sale_team_id
        if sale_team_id > 0:
            search_filters.append(('sale_team_id', '=', sale_team_id))

        sale_order_ids = self.env['sale.order'].search(search_filters)
        amount_untaxed = sum(sale_order_ids.mapped('amount_untaxed'))
        response['result_value'] = amount_untaxed
        response['result'] = amount_untaxed
        return response
