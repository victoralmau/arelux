# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime


class AreluxSaleReportTemplate(models.Model):
    _name = 'arelux.sale.report.template'
    _description = 'Arelux Sale Report Template'
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Nombre'
    )
    active = fields.Boolean(
        default=True,
        string='Activo'
    )
    custom_type = fields.Selection(
        selection=[
            ('daily', 'Diario'),
            ('weekly', 'Semanal'),
            ('monthly', 'Mensual'),
            ('annual', 'Anual')
        ],
        string='Custom Type',
        default='daily'
    )
    show_in_table_format = fields.Boolean(
        default=False,
        string='Show in table format'
    )
    order_by = fields.Char(
        string='Order by',
        default='user_name'
    )
    order_way = fields.Selection(
        selection=[
            ('asc', 'ASC'),
            ('desc', 'DESC')
        ],
        string='Order way',
        default='asc'
    )
    report_template_line = fields.One2many(
        'arelux.sale.report.template.line',
        'arelux_sale_report_template_id',
        string='Report Template Lines',
        copy=True
    )

    @api.model
    def cron_generate_automatic_arelux_sale_report(self):
        current_date = datetime.today()
        template_ids = self.env['arelux.sale.report.template'].search(
            [
                ('active', '=', True)
            ]
        )
        if template_ids:
            for template_id in template_ids:
                if template_id.custom_type == 'daily':
                    start_date = current_date + relativedelta(days=1)
                    end_date = start_date
                elif template_id.custom_type == 'weekly':
                    start_date = current_date + relativedelta(days=-7)
                    end_date = start_date + relativedelta(days=6)
                elif template_id.custom_type == 'monthly':
                    start_date = datetime(
                        current_date.year,
                        current_date.month,
                        1
                    ) + relativedelta(months=-1)
                    end_date = start_date + relativedelta(months=1, days=-1)
                elif template_id.custom_type == 'annual':
                    start_date = datetime(
                        current_date.year,
                        1,
                        1
                    ) + relativedelta(years=-1)
                    end_date = datetime(
                        start_date.year,
                        12,
                        31
                    )

                report_ids = self.env['arelux.sale.report'].search(
                    [
                        ('arelux_sale_report_template_id', '=', template_id.id),
                        ('date_from', '=', start_date.strftime("%Y-%m-%d")),
                        ('date_to', '=', end_date.strftime("%Y-%m-%d"))
                    ]
                )
                if len(report_ids) == 0:
                    vals = {
                        'name': template_id.name,
                        'arelux_sale_report_template_id': template_id.id,
                        'date_from': start_date.strftime("%Y-%m-%d"),
                        'date_to': end_date.strftime("%Y-%m-%d"),
                        'show_in_table_format': template_id.show_in_table_format,
                        'state': 'new',
                        'order_by': template_id.order_by,
                        'order_way': template_id.order_way
                    }
                    report_obj = self.env['arelux.sale.report'].sudo().create(vals)
                    # lines
                    for line_id in template_id.report_template_line:
                        line_vals = {
                            'arelux_sale_report_id': report_obj.id,
                            'arelux_sale_report_type_id':
                                line_id.arelux_sale_report_type_id.id,
                            'position': line_id.position,
                            'ar_qt_activity_type': line_id.ar_qt_activity_type,
                            'ar_qt_customer_type': line_id.ar_qt_customer_type,
                            'crm_team_id': line_id.crm_team_id.id,
                            'group_by_user': line_id.group_by_user,
                            'show_in_table_format': line_id.show_in_table_format
                        }
                        self.env['arelux.sale.report.line'].sudo().create(line_vals)
                    # mail_followers
                    follower_ids = self.env['mail.followers'].search(
                        [
                            ('res_model', '=', self._name),
                            ('res_id', '=', template_id.id)
                        ]
                    )
                    if follower_ids:
                        for follower_id in follower_ids:
                            vals = {
                                'res_id': report_obj.id,
                                'res_model': 'arelux.sale.report',
                                'partner_id': follower_id.partner_id.id,
                                'subtype_ids': [(6, 0, [1])],
                            }
                            follower_ids_item = self.env['mail.followers'].search(
                                [
                                    ('res_model', '=', vals['res_model']),
                                    ('res_id', '=', vals['res_id']),
                                    ('partner_id', '=', vals['partner_id'])
                                ]
                            )
                            if len(follower_ids_item) == 0:
                                self.env['mail.followers'].create(vals)
                            else:
                                if vals['partner_id'] == 3:
                                    follower_ids_item = follower_ids_item[0]
                                    follower_ids_item.unlink()
                    # fix generate_value_lines
                    report_obj.change_state_to_generate()
                    # auto_send_mail_item
                    report_obj.action_send_mail()
