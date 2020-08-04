# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, fields, models, tools, _
import requests
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime
import boto3
_logger = logging.getLogger(__name__)


class ContactFormSubmission(models.Model):
    _name = 'contact.form.submission'
    _description = 'Contact Form Submission'
    _order = 'create_date desc'

    name = fields.Char(
        string='Name'
    )
    email = fields.Char(
        string='Email'
    )
    phone = fields.Char(
        string='Phone'
    )
    mobile = fields.Char(
        string='Mobile'
    )
    m2 = fields.Integer(
        string='m2'
    )
    description = fields.Text(
        string='Description'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User'
    )
    lang = fields.Selection(
        selection=[
            ('es_ES', 'es_ES'),
            ('en_US', 'en_US')
        ],
        string='Lang',
        default='es_ES'
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country'
    )
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State'
    )
    ar_qt_todocesped_pr_type_surface = fields.Many2one(
        comodel_name='res.partner.type.surface',
        domain=[
            ('filter_company', 'in', ('all', 'todocesped')),
            ('filter_ar_qt_customer_type', 'in', ('all', 'particular'))
        ],
        string='TC - Tipo de superficie',
    )
    category_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Category'
    )
    ar_qt_customer_type = fields.Selection(
        [
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),
        ],
        size=15,
        string='Customer type',
        default='particular'
    )
    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),
            ('both', 'Ambos'),
        ],
        size=15,
        string='Activity type',
        default='todocesped'
    )
    ar_qt_todocesped_contact_form = fields.Many2one(
        comodel_name='res.partner.contact.form',
        string='TC - Formas de contacto / Colectivo',
    )
    ar_qt_todocesped_pf_install_artificial_grass = fields.Boolean(
        string="TC - Instala el cesped artificial"
    )
    date_deadline = fields.Integer(
        string='Deadline date'
    )
    mail_activity_type_id = fields.Many2one(
        comodel_name='mail.activity.type',
        string='Next activity',
        domain=[('res_model_id.model', '=', 'crm.lead')]
    )
    mail_activity_date_deadline = fields.Integer(
        string='Activity date deadline'
    )
    medium_id = fields.Many2one(
        comodel_name='utm.medium',
        string='Medium id'
    )
    source_id = fields.Many2one(
        comodel_name='utm.source',
        string='Source id'
    )
    utm_website_id = fields.Many2one(
        comodel_name='utm.website',
        string='Website id'
    )
    team_id = fields.Many2one(
        comodel_name='crm.team',
        string='Team Id'
    )
    tracking_profile_uuid = fields.Char(
        string='Tracking Profile Uuid'
    )
    tracking_cookie_uuid = fields.Char(
        string='Tracking Cookie Uuid'
    )
    tracking_user_uuid = fields.Char(
        string='Tracking User Uuid'
    )
    tracking_session_uuid = fields.Char(
        string='Tracking Session Uuid'
    )
    sessionAdGroupCF7 = fields.Char(
        string='sessionAdGroupCF7'
    )
    sessionAdSetCF7 = fields.Char(
        string='sessionAdSetCF7'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner Id'
    )
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead Id'
    )

    @api.multi
    def tracking_session_addProperties(self):
        self.ensure_one()
        if self.lead_id:
            if self.tracking_profile_uuid and self.tracking_session_uuid:
                headers = {
                    'Content-type': 'application/json',
                    'origin': 'erp.arelux.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; '
                                  'rv:68.0) Gecko/20100101 Firefox/68.0'
                }
                data = {
                    "profile_uuid": str(self.tracking_profile_uuid),
                    "properties": {"lead_id": self.lead_id.id}
                }
                url = 'https://tr.oniad.com/api/session/%s/addProperties' % \
                      self.tracking_session_uuid
                response = requests.post(
                    url,
                    data=json.dumps(data),
                    headers=headers
                )
                return response.status_code

    @api.multi
    def operations_item(self):
        for item in self:
            # country_id
            if item.country_id.id == 0:
                item.country_id = 69
            # date_deadline
            if item.date_deadline == 0:
                item.date_deadline = 90
            # team_id
            if item.user_id:
                if item.user_id.sale_team_id:
                    item.team_id = item.user_id.sale_team_id.id
            # operations
            item.operations_item_partner_id()
            item.operations_item_lead_id()
            item.operations_item_extra()

    @api.multi
    def operations_item_partner_id(self):
        self.ensure_one()
        # partner_id
        if self.partner_id.id == 0:
            # search
            if not self.phone and not self.mobile:
                partner_ids = self.env['res.partner'].search(
                    [
                        ('email', '=', str(self.email)),
                        ('active', '=', True),
                        ('supplier', '=', False)
                    ]
                )
                if partner_ids:
                    self.partner_id = partner_ids[0].id
            elif not self.phone :
                partner_ids = self.env['res.partner'].search(
                    [
                        ('email', '=', str(self.email)),
                        ('phone', '=', str(self.phone)),
                        ('active', '=', True),
                        ('supplier', '=', False)
                    ]
                )
                if partner_ids:
                    self.partner_id = partner_ids[0].id
            elif not self.mobile:
                partner_ids = self.env['res.partner'].search(
                    [
                        ('email', '=', str(self.email)),
                        ('mobile', '=', str(self.mobile)),
                        ('active', '=', True),
                        ('supplier', '=', False)
                    ]
                )
                if partner_ids:
                    self.partner_id = partner_ids[0].id
            # create
            if self.partner_id.id == 0:
                # vals
                vals = {
                    'lang': str(self.lang),
                    'name': str(self.name),
                    'email': str(self.email),
                    'ar_qt_activity_type': str(self.ar_qt_activity_type),
                    'ar_qt_customer_type': str(self.ar_qt_customer_type),
                    'ar_qt_todocesped_pf_install_artificial_grass':
                        self.ar_qt_todocesped_pf_install_artificial_grass
                }
                # country_id
                if self.country_id:
                    vals['country_id'] = self.country_id.id
                # state_id
                if self.state_id:
                    vals['state_id'] = self.state_id.id
                # phone
                if self.phone:
                    vals['phone'] = str(self.phone)
                # mobile
                if self.mobile:
                    vals['mobile'] = str(self.mobile)
                # user_id
                vals['user_id'] = 0
                if self.user_id:
                    vals['user_id'] = self.user_id.id
                # ar_qt_todocesped_pr_type_surface
                if self.ar_qt_todocesped_pr_type_surface:
                    vals['ar_qt_todocesped_pr_type_surface'] = \
                        [(4, self.ar_qt_todocesped_pr_type_surface.id)]
                # category_id
                if self.category_id:
                    vals['category_id'] = [(4, self.category_id.id)]
                # ar_qt_todocesped_contact_form
                if self.ar_qt_todocesped_contact_form:
                    vals['ar_qt_todocesped_contact_form'] = \
                        [(4, self.ar_qt_todocesped_contact_form.id)]
                # tracking_profile_uuid
                if self.tracking_profile_uuid:
                    vals['tracking_profile_uuid'] = str(self.tracking_profile_uuid)
                # tracking_cookie_uuid
                if self.tracking_cookie_uuid:
                    vals['tracking_cookie_uuid'] = str(self.tracking_cookie_uuid)
                # tracking_user_uuid
                if self.tracking_user_uuid:
                    vals['tracking_user_uuid'] = str(self.tracking_user_uuid)
                # tracking_session_uuid
                if self.tracking_session_uuid:
                    vals['tracking_session_uuid'] = str(self.tracking_session_uuid)
                # create_real
                if self.user_id:
                    res_partner_obj = self.env['res.partner'].sudo(
                        self.user_id.id
                    ).create(vals)
                else:
                    res_partner_obj = self.env['res.partner'].sudo(
                        self.create_uid.id
                    ).create(vals)
                # update
                self.partner_id = res_partner_obj.id
                # tr_oniad
                if self.partner_id:
                    self.partner_id.tracking_user_identify()

    @api.multi
    def operations_item_lead_id(self):
        self.ensure_one()
        current_date = datetime.today()
        # lead_id
        if self.lead_id.id == 0 and self.partner_id:
            # search
            lead_ids = self.env['crm.lead'].search(
                [
                    ('partner_id', '=', self.partner_id.id),
                    ('active', '=', True),
                    ('type', '=', 'opportunity'),
                    ('ar_qt_activity_type', '=', str(self.ar_qt_activity_type)),
                    ('ar_qt_customer_type', '=', str(self.ar_qt_customer_type)),
                    ('probability', '>', 0),
                    ('probability', '<', 100)
                ]
            )
            if lead_ids:
                self.lead_id = lead_ids[0].id
                # update_description
                if self.description:
                    if self.lead_id.description:
                        self.lead_id.description = "%s\n\n %s \n %s" % (
                            self.lead_id.description,
                            current_date.strftime("%Y-%m-%d %H:%I:%S"),
                            self.description
                        )
                    else:
                        self.lead_id.description = str(self.description)
            # create
            if self.lead_id.id == 0:
                # vals
                vals = {
                    'name': '',
                    'email_from': str(self.partner_id.email),
                    'active': True,
                    'probability': 10,
                    'type': 'opportunity',
                    'ar_qt_customer_type': str(self.partner_id.ar_qt_customer_type)
                }
                # name
                if self.m2 > 0:
                    vals['name'] = str(self.m2)+' '
                # state_id
                if self.state_id:
                    vals['name'] = "%s %s " % (
                        vals['name'],
                        self.state_id.name
                    )
                # add_name
                vals['name'] = "%s %s " % (
                    vals['name'],
                    self.partner_id.name
                )
                # description
                if self.description:
                    vals['description'] = str(self.description)
                # phone
                if self.partner_id.phone:
                    vals['phone'] = str(self.partner_id.phone)
                # mobile
                if self.partner_id.mobile:
                    vals['mobile'] = str(self.partner_id.mobile)
                # state_id
                if self.state_id:
                    vals['state_id'] = self.state_id.id
                # user_id
                vals['user_id'] = 0
                if self.user_id:
                    vals['user_id'] = self.user_id.id
                # team_id
                if self.team_id:
                    vals['team_id'] = self.team_id.id
                # medium_id
                if self.medium_id:
                    vals['medium_id'] = self.medium_id.id
                # source_id
                if self.source_id:
                    vals['source_id'] = self.source_id.id
                # utm_website_id
                if self.utm_website_id:
                    vals['utm_website_id'] = self.utm_website_id.id
                # odoo_ar_qt_activity_type
                vals['ar_qt_activity_type'] = str(
                    self.partner_id.ar_qt_activity_type
                )
                # date_deadline
                if self.date_deadline > 0:
                    date_deadline = current_date + relativedelta(
                        days=self.date_deadline
                    )
                    vals['date_deadline'] = str(date_deadline.strftime(
                        "%Y-%m-%d %H:%I:%S"
                    ))
                # lead_m2
                if self.m2 > 0:
                    vals['lead_m2'] = self.m2
                # tracking_profile_uuid
                if self.tracking_profile_uuid:
                    vals['tracking_profile_uuid'] = str(
                        self.tracking_profile_uuid
                    )
                # tracking_cookie_uuid
                if self.tracking_cookie_uuid:
                    vals['tracking_cookie_uuid'] = str(
                        self.tracking_cookie_uuid
                    )
                # tracking_user_uuid
                if self.tracking_user_uuid:
                    vals['tracking_user_uuid'] = str(self.tracking_user_uuid)
                # tracking_session_uuid
                if self.tracking_session_uuid:
                    vals['tracking_session_uuid'] = str(
                        self.tracking_session_uuid
                    )
                # sessionAdGroupCF7
                if self.sessionAdGroupCF7:
                    vals['sessionAdGroupCF7'] = str(self.sessionAdGroupCF7)
                # sessionAdSetCF7
                if self.sessionAdSetCF7:
                    vals['sessionAdSetCF7'] = str(self.sessionAdSetCF7)
                # create_real
                crm_lead_obj = self.env['crm.lead'].sudo(
                    self.create_uid.id
                ).create(vals)
                self.lead_id = crm_lead_obj.id
                # operations
                if self.lead_id:
                    # mail_activity_type_id
                    if self.mail_activity_type_id and \
                            self.mail_activity_date_deadline > 0:
                        if self.lead_id.user_id:
                            date_deadline_new = current_date + relativedelta(
                                days=self.mail_activity_date_deadline
                            )
                            # search
                            activity_ids = self.env['mail.activity'].sudo().search(
                                [
                                    (
                                        'activity_type_id',
                                        '=',
                                        self.mail_activity_type_id.id
                                    ),
                                    (
                                        'date_deadline',
                                        '=',
                                        date_deadline_new.strftime(
                                            "%Y-%m-%d %H:%M:%S"
                                        )
                                    ),
                                    ('res_model_id.model', '=', 'crm.lead'),
                                    ('res_id', '=', self.lead_id.id)
                                ]
                            )
                            if len(activity_ids) == 0:
                                # search
                                ir_model_ids = self.env['ir.model'].sudo().search(
                                    [
                                        ('model', '=', 'crm.lead')
                                    ]
                                )
                                if ir_model_ids:
                                    ir_model_id = ir_model_ids[0]
                                    # create
                                    vals = {
                                        'activity_type_id':
                                            self.mail_activity_type_id.id,
                                        'date_deadline':
                                            date_deadline_new.strftime(
                                                "%Y-%m-%d %H:%M:%S"
                                            ),
                                        'user_id': self.lead_id.user_id.id,
                                        'res_model_id': ir_model_id.id,
                                        'res_id': self.lead_id.id
                                    }
                                    self.env['mail.activity'].sudo(
                                        self.create_uid.id
                                    ).create(vals)
                # mail_followers_check (remove=True, add=False)
                self.mail_followers_check('crm.lead', self.lead_id.id, False, True)
                # partner_id (fix)
                self.lead_id.partner_id = self.partner_id.id
                # tr_oniad
                if self.lead_id:
                    self.lead_id.tracking_session_addProperties()

    @api.multi
    def mail_followers_check(self, model, res_id, check_remove=True, check_add=True):
        self.ensure_one()
        mail_follower_extra_need_create = False
        if check_add:
            mail_follower_extra_need_create = True
        # search
        mail_followers_ids = self.env['mail.followers'].search(
            [
                ('res_model', '=', str(model)),
                ('res_id', '=', str(res_id))
            ]
        )
        if mail_followers_ids:
            for follower_id in mail_followers_ids:
                is_super_admin = False
                if self.create_uid.id == 1 \
                        and follower_id.partner_id.id == self.create_uid.partner_id.id:
                    is_super_admin = True
                # check_remove
                if check_remove:
                    if is_super_admin:
                        follower_id.unlink()
                    else:
                        if follower_id.partner_id.id == self.create_uid.partner_id.id:
                            follower_id.unlink()
                        elif follower_id.partner_id.id == self.partner_id.id:
                            if check_add:
                                mail_follower_extra_need_create = False
        # mail_follower_extra_need_create
        if mail_follower_extra_need_create:
            vals = {
                'res_model': str(model),
                'res_id': str(res_id),
                'partner_id': self.partner_id.id,
                'subtype_ids': [(4, [1])]
            }
            self.env['mail.followers'].sudo().create(vals)

    @api.multi
    def operations_item_extra(self):
        self.ensure_one()
        # operations_welcome_email_lead_id
        if self.lead_id:
            need_send_mail = True
            if self.source_id:
                if self.source_id.id == 7:
                    need_send_mail = False
            # need_send_mail
            if need_send_mail:
                template_id = 0
                if self.utm_website_id:
                    if self.utm_website_id.mail_template_id:
                        template_id = self.utm_website_id.mail_template_id.id
                # fix profesional
                if self.ar_qt_activity_type == 'todocesped' \
                        and self.ar_qt_customer_type == 'profesional':
                    template_id = 135
                # fix
                if template_id == 0:
                    template_id = 94
                # send_mail
                self.send_mail(template_id)
                # mail_followers_check (remove=True, add=False)
                self.mail_followers_check('crm.lead', self.lead_id.id, True, False)
        # operations sale_oders
        if self.lead_id:
            if self.ar_qt_activity_type == 'todocesped' \
                    and self.ar_qt_customer_type == 'particular' \
                    and self.m2 > 0:
                self.create_sale_order(2)
                self.create_sale_order(3)

    @api.multi
    def send_mail(self, template_id):
        self.ensure_one()
        if self.lead_id:
            # create
            if self.user_id:
                message_obj = self.env['mail.compose.message'].sudo(
                    self.user_id.id
                ).create({})
            else:
                message_obj = self.env['mail.compose.message'].sudo(
                    self.create_uid.id
                ).create({})
            # onchange_template_id
            res = message_obj.onchange_template_id(
                template_id,
                'comment',
                'crm.lead',
                self.lead_id.id
            )
            # update
            if 'value' in res:
                message_obj.composition_mode = 'comment'
                message_obj.model = 'crm.lead'
                message_obj.res_id = self.lead_id.id
                message_obj.template_id = template_id
                message_obj.body = res['value']['body']
                message_obj.subject = res['value']['subject']
                message_obj.record_name = res['value']['subject']
                # email_from
                if 'email_from' in res['value']:
                    message_obj.email_from = res['value']['email_from']
                # reply_to
                if 'reply_to' in res['value']:
                    message_obj.reply_to = res['value']['reply_to']
                # action
                message_obj.send_mail_action()

    @api.multi
    def create_sale_order(self, id):
        self.ensure_one()
        order_template_ids = self.env['sale.order.template'].search(
            [
                ('id', '=', id)
            ]
        )
        if order_template_ids:
            order_template_id = order_template_ids[0]
            # find previously
            order_ids = self.env['sale.order'].sudo().search(
                [
                    (
                        'ar_qt_activity_type',
                        '=',
                        str(self.lead_id.ar_qt_customer_type)
                    ),
                    (
                        'ar_qt_customer_type',
                        '=',
                        str(self.lead_id.ar_qt_customer_type)
                    ),
                    ('opportunity_id', '=', self.lead_id.id),
                    ('template_id', '=', order_template_id.id)
                ]
            )
            if len(order_ids) == 0:
                # vals
                vals = {
                    'partner_id': self.lead_id.partner_id.id,
                    'medium_id': self.lead_id.medium_id.id,
                    'source_id': self.lead_id.source_id.id,
                    'utm_website_id': self.lead_id.utm_website_id.id,
                    'partner_invoice_id': self.lead_id.partner_id.id,
                    'partner_shipping_id': self.lead_id.partner_id.id,
                    'sale_order_template_id': order_template_id.id,
                    'opportunity_id': self.lead_id.id,
                    'team_id': self.lead_id.team_id.id,
                    'ar_qt_activity_type':
                        str(self.lead_id.ar_qt_activity_type),
                    'ar_qt_customer_type':
                        str(self.lead_id.ar_qt_customer_type),
                    'carrier_id':
                        order_template_id.delivery_carrier_id.id,
                    'require_payment': order_template_id.require_payment,
                    'state': 'draft'
                }
                # fix user_id
                vals['user_id'] = 0
                if self.lead_id.user_id:
                    vals['user_id'] = self.lead_id.user_id.id
                # tracking_profile_uuid
                if self.lead_id.tracking_profile_uuid:
                    vals['tracking_profile_uuid'] = str(
                        self.lead_id.tracking_profile_uuid
                    )
                # tracking_cookie_uuid
                if self.lead_id.tracking_cookie_uuid:
                    vals['tracking_cookie_uuid'] = str(
                        self.lead_id.tracking_cookie_uuid
                    )
                # tracking_user_uuid
                if self.lead_id.tracking_user_uuid:
                    vals['tracking_user_uuid'] = str(
                        self.lead_id.tracking_user_uuid
                    )
                # tracking_session_uuid
                if self.lead_id.tracking_session_uuid:
                    vals['tracking_session_uuid'] = str(
                        self.lead_id.tracking_session_uuid
                    )
                # sale_order_template_line_ids
                if order_template_id.sale_order_template_line_ids:
                    sotl_ids = order_template_id.sale_order_template_line_ids
                    vals['order_line'] = []
                    for line_id in sotl_ids:
                        vals_line = {
                            'name': str(line_id.name),
                            'product_id': line_id.product_id.id,
                            'product_uom': line_id.product_uom_id.id,
                            'product_uom_qty': line_id.product_uom_qty,
                            'discount': line_id.discount,
                        }
                        # fix
                        if order_template_id.id == 3:
                            vals_line['product_uom_qty'] = self.m2
                            # product_id
                            if line_id.product_id.id in [70, 73]:
                                vals_line['product_uom_qty'] = 1
                            elif line_id.product_id.id == 63:
                                vals_line['product_uom_qty'] = 1
                                if self.m2 > 40:
                                    vals_line['product_uom_qty'] = int((self.m2 / 40))
                            elif line_id.product_id.id == 71:
                                vals_line['product_uom_qty'] = 1
                                if self.m2 > 50:
                                    vals_line['product_uom_qty'] = int((self.m2 / 50))
                        # append
                        vals['order_line'].append((0, 0, vals_line))
                # sale_order_template_option_ids
                if order_template_id.sale_order_template_option_ids:
                    soto_ids = order_template_id.sale_order_template_option_ids
                    vals['options'] = []
                    for option_id in soto_ids:
                        vals_option = {
                            'name': str(option_id.name),
                            'product_id': option_id.product_id.id,
                            'discount': option_id.discount,
                            'price_unit': option_id.price_unit,
                            'uom_id': option_id.uom_id.id,
                            'quantity': option_id.quantity,
                        }
                        # append
                        vals['options'].append((0, 0, vals_option))
                # create
                if self.lead_id.user_id:
                    sale_order_obj = self.env['sale.order'].sudo(
                        self.lead_id.user_id.id
                    ).create(vals)
                else:
                    sale_order_obj = self.env['sale.order'].sudo(
                        self.create_uid.id
                    ).create(vals)
                # mail_followers_check (remove=True, add=True)
                self.mail_followers_check(
                    'sale.order',
                    sale_order_obj.id,
                    True,
                    True
                )
                # return
                return sale_order_obj

    @api.model
    def create(self, values):
        return_item = super(ContactFormSubmission, self).create(values)
        # operations
        return_item.operations_item()
        # return
        return return_item

    @api.model
    def cron_sqs_contact_form_submission(self):
        sqs_url = tools.config.get('sqs_contact_form_submission_url')
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
        # boto3
        sqs = boto3.client(
            'sqs',
            region_name=AWS_SMS_REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        # Receive message from SQS queue
        total_messages = 10
        while total_messages > 0:
            response = sqs.receive_message(
                QueueUrl=sqs_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10,
                MessageAttributeNames=['All']
            )
            if 'Messages' in response:
                total_messages = len(response['Messages'])
            else:
                total_messages = 0
            # continue
            if 'Messages' in response:
                for message in response['Messages']:
                    # message_body
                    message_body = json.loads(message['Body'])
                    # fix message
                    if 'Message' in message_body:
                        message_body = json.loads(message_body['Message'])
                    # result_message
                    result_message = {
                        'statusCode': 200,
                        'return_body': 'OK',
                        'message': message_body
                    }
                    # fields_need_check
                    fields_need_check = [
                        'name', 'email', 'odoo_ar_qt_activity_type',
                        'odoo_ar_qt_activity_type'
                    ]
                    for fnc in fields_need_check:
                        if fnc not in message_body:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = \
                                _('No existe el campo %s') % fnc
                    # operations
                    if result_message['statusCode'] == 200:
                        # params
                        vals = {}
                        # params_need_check_str
                        params_need_check_str = [
                            'name', 'email', 'description', 'odoo_lang', 'phone',
                            'mobile', 'odoo_ar_qt_activity_type',
                            'odoo_ar_qt_activity_type', 'tracking_profile_uuid',
                            'tracking_cookie_uuid', 'tracking_user_uuid',
                            'tracking_session_uuid', 'sessionAdGroupCF7',
                            'sessionAdSetCF7'
                        ]
                        for pnd in params_need_check_str:
                            if pnd in message_body:
                                if message_body[pnd] != '':
                                    # replace+assign
                                    key_val = str(pnd.replace('odoo_', ''))
                                    vals[key_val] = str(message_body[pnd])
                        # params_need_check_int
                        params_need_check_int = [
                            'm2', 'odoo_country_id', 'odoo_state_id',
                            'odoo_user_id', 'odoo_ar_qt_todocesped_pr_type_surface',
                            'odoo_partner_category_id',
                            'odoo_ar_qt_todocesped_contact_form', 'odoo_team_id',
                            'odoo_medium_id', 'odoo_source_id', 'odoo_utm_website_id',
                            'odoo_date_deadline', 'odoo_next_activity_id',
                            'date_action'
                        ]
                        for pnd in params_need_check_int:
                            if pnd in message_body:
                                if message_body[pnd] > 0:
                                    # replace+assign
                                    key_val = str(pnd.replace('odoo_', ''))
                                    vals[key_val] = int(message_body[pnd])
                        # params_need_check_not_format (bool)
                        params_need_check_not_format = [
                            'ar_qt_todocesped_pf_install_artificial_grass'
                        ]
                        for pnd in params_need_check_not_format:
                            if pnd in message_body:
                                # replace+assign
                                key_val = str(pnd.replace('odoo_', ''))
                                vals[key_val] = message_body[pnd]
                        # replace
                        if 'partner_category_id' in vals:
                            vals['category_id'] = vals['partner_category_id']
                            del vals['partner_category_id']
                        # ar_qt_todocesped_pr_type_surface (check imposible)
                        if 'ar_qt_todocesped_pr_type_surface' in vals:
                            ids = self.env['res.partner.type.surface'].search(
                                [
                                    (
                                        'id',
                                        '=',
                                        int(vals['ar_qt_todocesped_pr_type_surface'])
                                    )
                                ]
                            )
                            if len(ids) == 0:
                                del vals['ar_qt_todocesped_pr_type_surface']
                        # category_id (check imposible)
                        if 'category_id' in vals:
                            ids = self.env['res.partner.category'].search(
                                [
                                    ('id', '=', int(vals['category_id']))
                                ]
                            )
                            if len(ids) == 0:
                                del vals['category_id']
                        # ar_qt_todocesped_contact_form (check imposible)
                        if 'ar_qt_todocesped_contact_form' in vals:
                            ids = self.env['res.partner.contact.form'].search(
                                [
                                    (
                                        'id',
                                        '=',
                                        int(vals['ar_qt_todocesped_contact_form']))
                                ]
                            )
                            if len(ids) == 0:
                                del vals['category_id']
                        # final_operations
                        result_message['data'] = vals
                        _logger.info(result_message)
                        # create-write
                        if result_message['statusCode'] == 200:
                            self.env['contact.form.submission'].sudo(6).create(vals)
                        # remove_message
                        if result_message['statusCode'] == 200:
                            sqs.delete_message(
                                QueueUrl=sqs_url,
                                ReceiptHandle=message['ReceiptHandle']
                            )
