# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
import operator
_logger = logging.getLogger(__name__)


class AreluxSaleReport(models.Model):
    _name = 'arelux.sale.report'
    _description = 'Arelux Sale Report'
    _inherit = ['mail.thread']

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id
    )
    name = fields.Char(
        string='Nombre'
    )
    date_from = fields.Date(
        string='Fecha desde'
    )
    date_to = fields.Date(
        string='Fecha hasta'
    )
    date_from_filter = fields.Datetime(
        string='Fecha desde filtro'
    )
    date_to_filter = fields.Datetime(
        string='Fecha hasta filtro'
    )
    arelux_sale_report_template_id = fields.Many2one(
        comodel_name='arelux.sale.report.template',
        string='Arelux Sale Report Template'
    )
    ir_attachment_id = fields.Many2one(
        comodel_name='ir.attachment',
        string='Adjunto'
    )
    state = fields.Selection(
        selection=[
            ('new', 'Nuevo'),
            ('generate', 'Generado'),
            ('sent', 'Enviado')
        ],
        string='Estado',
        default='new'
    )
    show_in_table_format = fields.Boolean(
        default=False,
        string='Show in table format'
    )
    order_by = fields.Char(
        string='Order by',
        default='user_name'
    )
    order_way = fields.Char(
        string='Order way',
        default='asc'
    )
    order_way = fields.Selection(
        selection=[
            ('asc', 'ASC'),
            ('desc', 'DESC')
        ],
        string='Order way',
        default='asc'
    )
    report_line = fields.One2many(
        'arelux.sale.report.line',
        'arelux_sale_report_id',
        string='Report Lines',
        copy=True
    )

    def action_generate_ir_report(self, context=None):
        self.ensure_one()
        self.change_state_to_generate()

        context = dict(context or {}, active_ids=self._ids, active_model=self._name)

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'arelux_sale_reports.arelux_sale_report_pdf_template',
            'context': context
        }

    @api.one
    def get_table_info_metrics(self):
        metrics_info = {}
        for line in self.report_line:
            if line.show_in_table_format:
                # line._get_line_info()
                if line.position not in metrics_info:
                    metrics_info[line.position] = {
                        'position': line.position,
                        'name': line.arelux_sale_report_type_id.name,
                        'response_result_value': line.response_result_value,
                        'custom_type': line.arelux_sale_report_type_id.custom_type
                    }
        # metrics_info_sort
        metrics_info_sorted = []
        for metrics_info_key in metrics_info:
            metric_info = metrics_info[metrics_info_key]
            metrics_info_sorted.append(metric_info)

        return metrics_info_sorted

    @api.multi
    def get_table_info(self):
        self.ensure_one()
        metrics_info = {}
        table_info = {}
        for line in self.report_line:
            if line.show_in_table_format:
                # report_line_item._get_line_info()
                for user_line in line.user_line:
                    if user_line.user_id.id not in table_info:
                        table_info[user_line.user_id.id] = {
                            'id': user_line.user_id.id,
                            'user_name': user_line.user_id.name,
                            'metrics': [],
                            'metrics_add': []
                        }
                    # Fix metric
                    if line.position not in metrics_info:
                        metrics_info[line.position] = {
                            'position': line.position,
                            'name': line.arelux_sale_report_type_id.name,
                            'response_result_value': line.response_result_value,
                            'custom_type': line.arelux_sale_report_type_id.custom_type,
                        }
                    # value_user
                    if line.response_result_value == 'count':
                        value_user = user_line.count
                    elif line.response_result_value == 'percent':
                        value_user = user_line.percent
                    else:
                        value_user = user_line.amount_untaxed
                    # metrics append
                    table_info[user_line.user_id.id]['metrics'].append({
                        'position': line.position,
                        'name': line.arelux_sale_report_type_id.name,
                        'response_result_value': line.response_result_value,
                        'custom_type': line.arelux_sale_report_type_id.custom_type,
                        'value': value_user
                    })
                    # metrics_add
                    table_info[
                        user_line.user_id.id
                    ]['metrics_add'].append(line.position)
        # fix fill all users
        for table_info_key in table_info:
            table_info_item = table_info[table_info_key]

            for metric_info_key in metrics_info:
                metric_info = metrics_info[metric_info_key]

                if metric_info['position'] not in table_info_item['metrics_add']:
                    table_info[table_info_key]['metrics'].append({
                        'position': metric_info['position'],
                        'name': metric_info['name'],
                        'response_result_value': metric_info['response_result_value'],
                        'custom_type': metric_info['custom_type'],
                        'value': 0
                    })
            # sort_metrics
            table_info[table_info_key]['metrics'] = sorted(
                table_info[table_info_key]['metrics'],
                key=operator.itemgetter('position')
            )
        # sort_all
        table_info_sorted = []
        for table_info_key in table_info:
            table_info_item = table_info[table_info_key]
            if self.order_by != 'user_name':
                for metric in table_info_item['metrics']:
                    if metric['custom_type'] == self.order_by:
                        table_info_item[self.order_by] = metric['value']

            table_info_sorted.append(table_info_item)

        if self.order_way == 'asc':
            table_info = sorted(
                table_info_sorted,
                key=operator.itemgetter(self.order_by)
            )
        else:
            table_info = sorted(
                table_info_sorted,
                key=operator.itemgetter(self.order_by),
                reverse=True
            )

        return table_info

    @api.multi
    def get_table_info_total(self):
        self.ensure_one()
        metrics_info = {}
        for line in self.report_line:
            if line.show_in_table_format:
                # line._get_line_info()
                if line.arelux_sale_report_type_id.custom_type not in metrics_info:
                    metrics_info[line.arelux_sale_report_type_id.custom_type] = {
                        'position': line.position,
                        'name': line.arelux_sale_report_type_id.name,
                        'response_result_value': line.response_result_value,
                        'custom_type': line.arelux_sale_report_type_id.custom_type,
                        'value': 0
                    }
                    for user_line in line.user_line:
                        # value_user
                        if line.response_result_value == 'count':
                            value_user = user_line.count
                        else:
                            value_user = user_line.amount_untaxed

                        metrics_info[
                            line.arelux_sale_report_type_id.custom_type
                        ]['value'] += value_user
        # fix percents
        for line in self.report_line:
            if line.show_in_table_format \
                    and line.group_by_user \
                    and line.response_type == 'percent':
                if line.arelux_sale_report_type_id.custom_type == 'ratio_muestras':
                    numerador = metrics_info['sale_order_done_muestras']['value']
                    denominador = metrics_info['sale_order_sent_count']['value']
                elif line.arelux_sale_report_type_id.custom_type == 'ratio_calidad':
                    numerador = metrics_info['sale_order_done_count']['value']
                    denominador = metrics_info['sale_order_sent_count']['value']
                # percent_item
                percent_item = 0
                if numerador > 0 and denominador > 0:
                    percent_item = (float(numerador)/float(denominador))*100
                    percent_item = "{0:.2f}".format(percent_item)

                metrics_info[
                    line.arelux_sale_report_type_id.custom_type
                ]['value'] = percent_item
        # metrics_info_sort
        metrics_info_sorted = []
        for metrics_info_key in metrics_info:
            metric_info = metrics_info[metrics_info_key]
            metrics_info_sorted.append(metric_info)

        metrics_info_sorted = sorted(
            metrics_info_sorted,
            key=operator.itemgetter('position')
        )

        return metrics_info_sorted

    @api.multi
    def change_state_to_generate(self):
        self.ensure_one()
        if self.state == 'new':
            self.date_from_filter = datetime.strptime(
                '%s 00:00:00' % self.date_from,
                '%Y-%m-%d %H:%M:%S'
            ) + relativedelta(hours=-2)
            self.date_to_filter = datetime.strptime(
                '%s 23:59:59' % self.date_to,
                '%Y-%m-%d %H:%M:%S'
            ) + relativedelta(hours=-2)

            for line in self.report_line:
                line._get_line_info()

            self.state = 'generate'
            # Fix percents
            for line in self.report_line:
                if line.response_type == 'percent' and line.group_by_user:
                    user_ids = []
                    numerador_by_user_id = {}
                    denominador_by_user_id = {}
                    if line.arelux_sale_report_type_id.custom_type == 'ratio_muestras':
                        # numerador
                        line_ids = self.env['arelux.sale.report.line'].search(
                            [
                                ('arelux_sale_report_id', '=', self.id),
                                (
                                    'arelux_sale_report_type_id.custom_type',
                                    '=',
                                    'sale_order_done_muestras'
                                )
                            ]
                        )
                        if line_ids:
                            for user_line in line_ids[0].user_line:
                                numerador_by_user_id[
                                    user_line.user_id.id
                                ] = user_line.count
                        # denominador
                        line_ids = self.env['arelux.sale.report.line'].search(
                            [
                                ('arelux_sale_report_id', '=', self.id),
                                (
                                    'arelux_sale_report_type_id.custom_type',
                                    '=',
                                    'sale_order_sent_count'
                                )
                            ]
                        )
                        if line_ids:
                            for user_line in line_ids[0].user_line:
                                denominador_by_user_id[
                                    user_line.user_id.id
                                ] = user_line.count
                    elif line.arelux_sale_report_type_id.custom_type == 'ratio_calidad':
                        # numerador
                        line_ids = self.env['arelux.sale.report.line'].search(
                            [
                                ('arelux_sale_report_id', '=', self.id),
                                (
                                    'arelux_sale_report_type_id.custom_type',
                                    '=',
                                    'sale_order_done_count'
                                )
                            ]
                        )
                        if line_ids:
                            for user_line in line_ids[0].user_line:
                                numerador_by_user_id[
                                    user_line.user_id.id
                                ] = user_line.count
                        # denominador
                        line_ids = self.env['arelux.sale.report.line'].search(
                            [
                                ('arelux_sale_report_id', '=', self.id),
                                (
                                    'arelux_sale_report_type_id.custom_type',
                                    '=',
                                    'sale_order_sent_count'
                                )
                            ]
                        )
                        if line_ids:
                            for user_line in line_ids[0].user_line:
                                denominador_by_user_id[
                                    user_line.user_id.id
                                ] = user_line.count
                    # operations
                    for numerador_by_user_id_real in numerador_by_user_id:
                        if numerador_by_user_id_real not in user_ids:
                            user_ids.append(numerador_by_user_id_real)
                            
                    for denominador_by_user_id_real in denominador_by_user_id:
                        if denominador_by_user_id_real not in user_ids:
                            user_ids.append(denominador_by_user_id_real)
                    # save
                    # remove_all_previously
                    line.remove_all_user_line()
                    # calculate
                    for user_id in user_ids:
                        numerador = 0
                        if user_id in numerador_by_user_id:
                            numerador = numerador_by_user_id[user_id]
                            
                        denominador = 0
                        if user_id in denominador_by_user_id:
                            denominador = denominador_by_user_id[user_id]
                            
                        percent_item = 0
                        if numerador > 0 and denominador > 0:
                            percent_item = (float(numerador)/float(denominador))*100
            
                        percent_item = "{0:.2f}".format(percent_item)
                        # add_report_line_user
                        vals = {
                            'arelux_sale_report_line_id': line.id,
                            'user_id': user_id,
                            'percent': percent_item                                                                       
                        }
                        self.env['arelux.sale.report.line.user'].sudo().create(vals)
    
    @api.multi
    def auto_send_mail_item(self):
        self.ensure_one()
        if self.state == 'generate':
            template_id = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'arelux_sale_report_mail_template_id'
                )
            )
            if template_id > 0:
                mail_template_item = self.env['mail.template'].search(
                    [
                        ('id', '=', template_id)
                    ]
                )[0]
                vals = {
                    'record_name': self.name,                                                                                                                                                                                           
                }
                message_obj = self.env['mail.compose.message'].sudo().create(vals)
                res = message_obj.onchange_template_id(
                    mail_template_item.id,
                    'comment',
                    self._name,
                    self.id
                )
                message_obj.update({
                    'template_id': mail_template_item.id,                    
                    'composition_mode': 'comment',                    
                    'model': self._name,
                    'res_id': self.id,
                    'body': res['value']['body'],
                    'subject': res['value']['subject'],
                    'email_from': res['value']['email_from'],
                    'attachment_ids': res['value']['attachment_ids'],
                    'record_name': self.name,
                    'no_auto_thread': False,                     
                })                                                   
                message_obj.send_mail_action()
                self.state = 'sent'        
    
    @api.multi
    def action_cancel_report(self):
        for item in self:
            if item.state != "sent":
                item.state = 'new'
            
    @api.multi
    def action_send_mail(self):
        for item in self:
            item.auto_send_mail_item()
    
        return True
