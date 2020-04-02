# -*- coding: utf-8 -*-
{
    'name': 'Arelux Contact Form Submission',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'website_quote', 'utm_websites', 'tr_oniad', 'arelux_partner_questionnaire', 'delivery'],
    'data': [
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'views/contact_form_submission_view.xml',
    ],
    'installable': True,
    'auto_install': False,    
}