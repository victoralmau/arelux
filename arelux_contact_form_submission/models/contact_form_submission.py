# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

import logging
_logger = logging.getLogger(__name__)

import requests, json
from dateutil.relativedelta import relativedelta
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

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
        string='Telefono'
    )
    mobile = fields.Char(
        string='Movil'
    )
    m2 = fields.Integer(
        string='m2'
    )
    description = fields.Text(
        string='Description'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Usuario'
    )
    lang = fields.Selection(
        selection=[
            ('es_ES', 'es_ES'),
            ('en_US', 'en_US')
        ],
        string='Idioma',
        default='es_ES'
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Pais'
    )
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='Provincia'
    )
    ar_qt_todocesped_pr_type_surface = fields.Many2one(
        comodel_name='res.partner.type.surface',
        domain=[('filter_company', 'in', ('all', 'todocesped')),
                ('filter_ar_qt_customer_type', 'in', ('all', 'particular'))],
        string='TC - Tipo de superficie',
    )
    category_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria'
    )
    ar_qt_customer_type = fields.Selection(
        [
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),
        ],
        size=15,
        string='Tipo de cliente',
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
        string='Tipo de actividad',
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
        string='Date Deadline'
    )
    date_action = fields.Integer(
        string='Date action'
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
    next_activity_id = fields.Many2one(
        comodel_name='crm.activity',
        string='Next Activity Id'
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
    #final
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner Id'
    )
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead Id'
    )

    @api.one
    def tracking_session_addProperties(self):
        if self.lead_id.id>0:
            if self.tracking_profile_uuid!=False and self.tracking_session_uuid!=False:
                headers = {
                    'Content-type': 'application/json',
                    'origin': 'erp.arelux.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
                }
                data = {
                    "profile_uuid": str(self.tracking_profile_uuid),
                    "properties": {"lead_id": self.lead_id.id}
                }
                url = 'https://tr.oniad.com/api/session/' + str(self.tracking_session_uuid) + '/addProperties'
                response = requests.post(url, data=json.dumps(data), headers=headers)
                return response.status_code

    @api.one
    def operations_item(self):
        #country_id
        if self.country_id.id==0:
            self.country_id = 69#Spain
        #date_deadline
        if self.date_deadline==0:
            self.date_deadline = 90
        #team_id
        if self.user_id.id>0:
            if self.user_id.sale_team_id.id>0:
                self.team_id = self.user_id.sale_team_id.id#Force team_id user (correct)
        #operations
        self.operations_item_partner_id()
        self.operations_item_lead_id()
        self.operations_item_extra()

    @api.one
    def operations_item_partner_id(self):
        #partner_id
        if self.partner_id.id==0:
            #search
            if self.phone == False and self.mobile == False:
                res_partner_ids = self.env['res.partner'].search([('email', '=', str(self.email)),('active', '=', True),('supplier', '=', False)])
                if len(res_partner_ids)>0:
                    self.partner_id = res_partner_ids[0].id
            elif self.phone != False:
                res_partner_ids = self.env['res.partner'].search([('email', '=', str(self.email)),('phone', '=', str(self.phone)),('active', '=', True),('supplier', '=', False)])
                if len(res_partner_ids) > 0:
                    self.partner_id = res_partner_ids[0].id
            elif self.mobile != False:
                res_partner_ids = self.env['res.partner'].search([('email', '=', str(self.email)),('mobile', '=', str(self.mobile)),('active', '=', True),('supplier', '=', False)])
                if len(res_partner_ids) > 0:
                    self.partner_id = res_partner_ids[0].id
            #create
            if self.partner_id.id==0:
                #vals
                res_partner_vals = {
                    'lang': str(self.lang),
                    'name': str(self.name),
                    'email': str(self.email),
                    'ar_qt_activity_type': str(self.ar_qt_activity_type),
                    'ar_qt_customer_type': str(self.ar_qt_customer_type),
                    'ar_qt_todocesped_pf_install_artificial_grass': self.ar_qt_todocesped_pf_install_artificial_grass
                }
                #country_id
                if self.country_id.id>0:
                    res_partner_vals['country_id'] = self.country_id.id
                #state_id
                if self.state_id.id>0:
                    res_partner_vals['state_id'] = self.state_id.id
                #phone
                if self.phone!=False:
                    res_partner_vals['phone'] = str(self.phone)
                # mobile
                if self.mobile != False:
                    res_partner_vals['mobile'] = str(self.mobile)
                # user_id
                res_partner_vals['user_id'] = 0
                if self.user_id.id>0:
                    res_partner_vals['user_id'] = self.user_id.id
                #ar_qt_todocesped_pr_type_surface
                if self.ar_qt_todocesped_pr_type_surface.id>0:
                    #res_partner_vals['ar_qt_todocesped_pr_type_surface'] = [{'id': self.ar_qt_todocesped_pr_type_surface.id}]
                     res_partner_vals['ar_qt_todocesped_pr_type_surface'] = [(4, self.ar_qt_todocesped_pr_type_surface.id)]
                    #category_id
                if self.category_id.id>0:
                    #res_partner_vals['category_id'] = [{'id': self.category_id.id}]
                    res_partner_vals['category_id'] = [(4, self.category_id.id)]
                #ar_qt_todocesped_contact_form
                if self.ar_qt_todocesped_contact_form.id>0:
                    #res_partner_vals['ar_qt_todocesped_contact_form'] = [{'id': self.ar_qt_todocesped_contact_form.id}]
                    res_partner_vals['ar_qt_todocesped_contact_form'] = [(4, self.ar_qt_todocesped_contact_form.id)]
                #tracking_profile_uuid
                if self.tracking_profile_uuid!=False:
                    res_partner_vals['tracking_profile_uuid'] = str(self.tracking_profile_uuid)
                # tracking_cookie_uuid
                if self.tracking_cookie_uuid != False:
                    res_partner_vals['tracking_cookie_uuid'] = str(self.tracking_cookie_uuid)
                # tracking_user_uuid
                if self.tracking_user_uuid != False:
                    res_partner_vals['tracking_user_uuid'] = str(self.tracking_user_uuid)
                # tracking_session_uuid
                if self.tracking_session_uuid != False:
                    res_partner_vals['tracking_session_uuid'] = str(self.tracking_session_uuid)
                #create_real
                if self.user_id.id>0:
                    res_partner_obj = self.env['res.partner'].sudo(self.user_id.id).create(res_partner_vals)
                else:
                    res_partner_obj = self.env['res.partner'].sudo(self.create_uid.id).create(res_partner_vals)
                #update
                self.partner_id = res_partner_obj.id
                #tr_oniad
                if self.partner_id.id>0:
                    self.partner_id.tracking_user_identify()

    @api.one
    def operations_item_lead_id(self):
        current_date = datetime.today()
        # lead_id
        if self.lead_id.id == 0 and self.partner_id.id > 0:
            # search
            crm_lead_ids = self.env['crm.lead'].search(
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
            if len(crm_lead_ids) > 0:
                self.lead_id = crm_lead_ids[0].id
                # update_description
                if self.description != False:
                    if self.lead_id.description!=False:
                        self.lead_id.description += "\n\n" + str(current_date.strftime("%Y-%m-%d %H:%I:%S")) + "\n" + str(self.description)
                    else:
                        self.lead_id.description = str(self.description)
            # create
            if self.lead_id.id == 0:
                # vals
                crm_lead_vals = {
                    'name': '',
                    'email_from': str(self.partner_id.email),
                    'active': True,
                    'probability': 10,
                    'type': 'opportunity',
                    'ar_qt_customer_type': str(self.partner_id.ar_qt_customer_type)
                }
                # name
                if self.m2>0:
                    crm_lead_vals['name'] = str(self.m2)+' '
                if self.state_id.id>0:
                    crm_lead_vals['name'] += str(self.state_id.name) + ' '
                # add_name
                crm_lead_vals['name'] += str(self.partner_id.name) + ' '
                # description
                if self.description!=False:
                    crm_lead_vals['description'] = str(self.description)
                # phone
                if self.partner_id.phone!=False:
                    crm_lead_vals['phone'] = str(self.partner_id.phone)
                # mobile
                if self.partner_id.mobile!=False:
                    crm_lead_vals['mobile'] = str(self.partner_id.mobile)
                # state_id
                if self.state_id.id>0:
                    crm_lead_vals['state_id'] = self.state_id.id
                #user_id
                crm_lead_vals['user_id'] = 0
                if self.user_id.id>0:
                    crm_lead_vals['user_id'] = self.user_id.id
                #team_id
                if self.team_id.id>0:
                    crm_lead_vals['team_id'] = self.team_id.id
                #medium_id
                if self.medium_id.id>0:
                    crm_lead_vals['medium_id'] = self.medium_id.id
                #source_id
                if self.source_id.id>0:
                    crm_lead_vals['source_id'] = self.source_id.id
                #utm_website_id
                if self.utm_website_id.id>0:
                    crm_lead_vals['utm_website_id'] = self.utm_website_id.id
                # odoo_ar_qt_activity_type
                crm_lead_vals['ar_qt_activity_type'] = str(self.partner_id.ar_qt_activity_type)
                # date_deadline
                if self.date_deadline>0:
                    date_deadline = current_date + relativedelta(days=self.date_deadline)
                    crm_lead_vals['date_deadline'] = str(date_deadline.strftime("%Y-%m-%d %H:%I:%S"))
                # lead_m2
                if self.m2>0:
                    crm_lead_vals['lead_m2'] = self.m2
                #tracking_profile_uuid
                if self.tracking_profile_uuid!=False:
                    crm_lead_vals['tracking_profile_uuid'] = str(self.tracking_profile_uuid)
                #tracking_cookie_uuid
                if self.tracking_cookie_uuid!=False:
                    crm_lead_vals['tracking_cookie_uuid'] = str(self.tracking_cookie_uuid)
                #tracking_user_uuid
                if self.tracking_user_uuid!=False:
                    crm_lead_vals['tracking_user_uuid'] = str(self.tracking_user_uuid)
                #tracking_session_uuid
                if self.tracking_session_uuid!=False:
                    crm_lead_vals['tracking_session_uuid'] = str(self.tracking_session_uuid)
                # create_real
                crm_lead_obj = self.env['crm.lead'].sudo(self.create_uid.id).create(crm_lead_vals)
                self.lead_id = crm_lead_obj.id
                # mail_followers_check (remove=True, add=False)
                self.mail_followers_check('crm.lead', self.lead_id.id, False, True)
                #partner_id (fix)
                self.lead_id.partner_id = self.partner_id.id
                #tr_oniad
                if self.lead_id.id>0:
                    self.lead_id.tracking_session_addProperties()

    @api.one
    def mail_followers_check(self, model, res_id, check_remove=True, check_add=True):
        mail_follower_extra_need_create = False
        if check_add==True:
            mail_follower_extra_need_create = True
        #search
        mail_followers_ids = self.env['mail.followers'].search([('res_model', '=', str(model)), ('res_id', '=', str(res_id))])
        if len(mail_followers_ids) > 0:
            for mail_followers_id in mail_followers_ids:
                is_super_admin = False
                if self.create_uid.id == 1 and mail_followers_id.partner_id.id == self.create_uid.partner_id.id:
                    is_super_admin = True
                #check_remove
                if check_remove==True:
                    if is_super_admin==True:
                        mail_followers_id.unlink()
                    else:
                        if mail_followers_id.partner_id.id == self.create_uid.partner_id.id:  # remove create webservice user follower
                            mail_followers_id.unlink()
                        elif mail_followers_id.partner_id.id == self.partner_id.id:
                            if check_add == True:
                                mail_follower_extra_need_create = False
        #mail_follower_extra_need_create
        if mail_follower_extra_need_create == True:
            mail_followers_vals = {
                'res_model': str(model),
                'res_id': str(res_id),
                'partner_id': self.partner_id.id,
                'subtype_ids': [(4, [1])]
            }
            mail_followers_obj = self.env['mail.followers'].sudo().create(mail_followers_vals)

    @api.one
    def operations_item_extra(self):
        # operations_welcome_email_lead_id
        if self.lead_id.id > 0:
            need_send_mail = True
            if self.source_id.id>0:
                if self.source_id.id==7:
                    need_send_mail = False
            #need_send_mail
            if need_send_mail==True:
                template_id = 0
                if self.utm_website_id.id>0:
                    if self.utm_website_id.mail_template_id.id>0:
                        template_id = self.utm_website_id.mail_template_id.id
                # fix profesional
                if self.ar_qt_activity_type == 'todocesped' and self.ar_qt_customer_type == 'profesional':
                    template_id = 135
                #fix
                if template_id==0:
                    template_id = 94
                #send_mail
                self.send_mail(template_id)
                # mail_followers_check (remove=True, add=False)
                self.mail_followers_check('crm.lead', self.lead_id.id, True, False)
        # operations sale_oders
        if self.lead_id.id > 0:
            if self.ar_qt_activity_type == 'todocesped' and self.ar_qt_customer_type == 'particular' and self.m2 > 0:
                self.create_sale_order(2)#presupuesto_muestras
                self.create_sale_order(3)#presupuesto_extra

    @api.one
    def send_mail(self, template_id):
        if self.lead_id.id>0:
            # create
            if self.user_id.id>0:
                mail_compose_message_obj = self.env['mail.compose.message'].sudo(self.user_id.id).create({})
            else:
                mail_compose_message_obj = self.env['mail.compose.message'].sudo(self.create_uid.id).create({})
            #onchange_template_id
            return_onchange_template_id = mail_compose_message_obj.onchange_template_id(template_id, 'comment', 'crm.lead', self.lead_id.id)
            # update
            if 'value' in return_onchange_template_id:
                mail_compose_message_obj.composition_mode = 'comment'
                mail_compose_message_obj.model = 'crm.lead'
                mail_compose_message_obj.res_id = self.lead_id.id
                mail_compose_message_obj.template_id = template_id
                mail_compose_message_obj.body = return_onchange_template_id['value']['body']
                mail_compose_message_obj.subject = return_onchange_template_id['value']['subject']
                mail_compose_message_obj.record_name = return_onchange_template_id['value']['subject']
                # email_from
                if 'email_from' in return_onchange_template_id['value']:
                    mail_compose_message_obj.email_from = return_onchange_template_id['value']['email_from']
                # reply_to
                if 'reply_to' in return_onchange_template_id['value']:
                    mail_compose_message_obj.reply_to = return_onchange_template_id['value']['reply_to']
                # action
                mail_compose_message_obj.send_mail_action()
    @api.one
    def create_sale_order(self, id):
        sale_order_template_ids = self.env['sale.order.template'].search([('id', '=', id)])
        if len(sale_order_template_ids)>0:
            sale_order_template_id = sale_order_template_ids[0]
            #vals
            sale_order_vals = {
                'partner_id': self.lead_id.partner_id.id,
                'medium_id': self.lead_id.medium_id.id,
                'source_id': self.lead_id.source_id.id,
                'utm_website_id': self.lead_id.utm_website_id.id,
                'partner_invoice_id': self.lead_id.partner_id.id,
                'partner_shipping_id': self.lead_id.partner_id.id,
                'sale_order_template_id': sale_order_template_id.id,
                'opportunity_id': self.lead_id.id,
                'team_id': self.lead_id.team_id.id,
                'ar_qt_activity_type': str(self.lead_id.ar_qt_activity_type),
                'ar_qt_customer_type': str(self.lead_id.ar_qt_customer_type),
                'carrier_id': sale_order_template_id.delivery_carrier_id.id,
                'require_payment': sale_order_template_id.require_payment,
                'state': 'draft'
            }
            # fix user_id
            sale_order_vals['user_id'] = 0
            if self.lead_id.user_id.id>0:
                sale_order_vals['user_id'] = self.lead_id.user_id.id
            #tracking_profile_uuid
            if self.lead_id.tracking_profile_uuid!=False:
                sale_order_vals['tracking_profile_uuid'] = str(self.lead_id.tracking_profile_uuid)
            # tracking_cookie_uuid
            if self.lead_id.tracking_cookie_uuid != False:
                sale_order_vals['tracking_cookie_uuid'] = str(self.lead_id.tracking_cookie_uuid)
            # tracking_user_uuid
            if self.lead_id.tracking_user_uuid != False:
                sale_order_vals['tracking_user_uuid'] = str(self.lead_id.tracking_user_uuid)
            # tracking_session_uuid
            if self.lead_id.tracking_session_uuid != False:
                sale_order_vals['tracking_session_uuid'] = str(self.lead_id.tracking_session_uuid)
            # sale_order_template_line_ids
            if len(sale_order_template_id.sale_order_template_line_ids) > 0:
                sale_order_vals['order_line'] = []
                for sale_order_template_line_id in sale_order_template_id.sale_order_template_line_ids:
                    data_sale_order_line = {
                        'name': str(sale_order_template_line_id.name),
                        'product_id': sale_order_template_line_id.product_id.id,
                        'product_uom': sale_order_template_line_id.product_uom_id.id,
                        'product_uom_qty': sale_order_template_line_id.product_uom_qty,
                        'discount': sale_order_template_line_id.discount,
                    }
                    # fix
                    if sale_order_template_id.id == 3:  # Pto especial, cambiamos cosas
                        data_sale_order_line['product_uom_qty'] = self.m2
                        # product_id
                        if sale_order_template_line_id.product_id.id == 73:  # Articulo extra
                            data_sale_order_line['product_uom_qty'] = 1
                        elif sale_order_template_line_id.product_id.id == 63:  # Banda autoadhesiva
                            data_sale_order_line['product_uom_qty'] = 1
                            if self.m2 > 40:
                                data_sale_order_line['product_uom_qty'] = int((self.m2 / 40))
                        elif sale_order_template_line_id.product_id.id == 71:  # Clavos
                            data_sale_order_line['product_uom_qty'] = 1
                            if self.m2 > 50:
                                data_sale_order_line['product_uom_qty'] = int((self.m2 / 50))
                    # append
                    sale_order_vals['order_line'].append((0, 0, data_sale_order_line))
            # sale_order_template_option_ids
            if len(sale_order_template_id.sale_order_template_option_ids) > 0:
                sale_order_vals['options'] = []
                for sale_order_template_option_id in sale_order_template_id.sale_order_template_option_ids:
                    data_sale_order_option = {
                        'name': str(sale_order_template_option_id.name),
                        'product_id': sale_order_template_option_id.product_id.id,
                        'discount': sale_order_template_option_id.discount,
                        'price_unit': sale_order_template_option_id.price_unit,
                        'uom_id': sale_order_template_option_id.uom_id.id,
                        'quantity': sale_order_template_option_id.quantity,
                    }
                    #append
                    sale_order_vals['options'].append((0, 0, data_sale_order_option))
            # create
            if self.lead_id.user_id.id > 0:
                sale_order_obj = self.env['sale.order'].sudo(self.lead_id.user_id.id).create(sale_order_vals)
            else:
                sale_order_obj = self.env['sale.order'].sudo(self.create_uid.id).create(sale_order_vals)
            # mail_followers_check (remove=True, add=True)
            self.mail_followers_check('sale.order', sale_order_obj.id, True, True)
            #return
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
        _logger.info('cron_sqs_contact_form_submission')

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
                    fields_need_check = ['name', 'email', 'odoo_ar_qt_activity_type', 'odoo_ar_qt_activity_type']
                    for field_need_check in fields_need_check:
                        if field_need_check not in message_body:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = 'No existe el campo ' + str(field_need_check)
                    # operations
                    if result_message['statusCode'] == 200:
                        #params
                        contact_form_submission_vals = {}
                        #params_need_check_str
                        params_need_check_str = ['name', 'email', 'description', 'odoo_lang', 'phone', 'mobile', 'odoo_ar_qt_activity_type', 'odoo_ar_qt_activity_type', 'tracking_profile_uuid', 'tracking_cookie_uuid', 'tracking_user_uuid', 'tracking_session_uuid']
                        for param_need_check_str in params_need_check_str:
                            if param_need_check_str in message_body:
                                if message_body[param_need_check_str] != '':
                                    # replace+assign
                                    key_val = str(param_need_check_str.replace('odoo_', ''))
                                    contact_form_submission_vals[key_val] = str(message_body[param_need_check_str])
                        # params_need_check_int
                        params_need_check_int = ['m2', 'odoo_country_id', 'odoo_state_id', 'odoo_user_id', 'odoo_ar_qt_todocesped_pr_type_surface', 'odoo_partner_category_id', 'odoo_ar_qt_todocesped_contact_form', 'odoo_team_id', 'odoo_medium_id', 'odoo_source_id', 'odoo_utm_website_id', 'odoo_date_deadline', 'odoo_next_activity_id', 'date_action']
                        for param_need_check_int in params_need_check_int:
                            if param_need_check_int in message_body:
                                if message_body[param_need_check_int] > 0:
                                    #replace+assign
                                    key_val = str(param_need_check_int.replace('odoo_', ''))
                                    contact_form_submission_vals[key_val] = int(message_body[param_need_check_int])
                        #params_need_check_not_format (bool)
                        params_need_check_not_format = ['ar_qt_todocesped_pf_install_artificial_grass']
                        for param_need_check_not_format in params_need_check_not_format:
                            if param_need_check_not_format in message_body:
                                # replace+assign
                                key_val = str(param_need_check_not_format.replace('odoo_', ''))
                                contact_form_submission_vals[key_val] = message_body[param_need_check_not_format]                                                                                
                        #replace
                        if 'partner_category_id' in contact_form_submission_vals:
                            contact_form_submission_vals['category_id'] = contact_form_submission_vals['partner_category_id']
                            del contact_form_submission_vals['partner_category_id']
                        #ar_qt_todocesped_pr_type_surface (check imposible)
                        if 'ar_qt_todocesped_pr_type_surface' in contact_form_submission_vals:
                            res_partner_type_surface_ids = self.env['res.partner.type.surface'].search([('id', '=', int(contact_form_submission_vals['ar_qt_todocesped_pr_type_surface']))])
                            if len(res_partner_type_surface_ids)==0:
                                del contact_form_submission_vals['ar_qt_todocesped_pr_type_surface']
                        #category_id (check imposible)
                        if 'category_id' in contact_form_submission_vals:
                            res_partner_category_ids = self.env['res.partner.category'].search([('id', '=', int(contact_form_submission_vals['category_id']))])
                            if len(res_partner_category_ids)==0:
                                del contact_form_submission_vals['category_id']
                        #ar_qt_todocesped_contact_form (check imposible)
                        if 'ar_qt_todocesped_contact_form' in contact_form_submission_vals:
                            res_partner_contact_form_ids = self.env['res.partner.contact.form'].search([('id', '=', int(contact_form_submission_vals['ar_qt_todocesped_contact_form']))])
                            if len(res_partner_contact_form_ids)==0:
                                del contact_form_submission_vals['category_id']                                                            
                        # final_operations
                        result_message['data'] = contact_form_submission_vals
                        _logger.info(result_message)
                        # create-write
                        if result_message['statusCode'] == 200:  # error, data not exists
                            contact_form_submission_obj = self.env['contact.form.submission'].sudo(6).create(contact_form_submission_vals)
                            _logger.info(contact_form_submission_obj)
                        # remove_message
                        if result_message['statusCode'] == 200:
                            response_delete_message = sqs.delete_message(
                                QueueUrl=sqs_url,
                                ReceiptHandle=message['ReceiptHandle']
                            )
