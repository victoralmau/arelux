# -*- coding: utf-8 -*-
{
    'name': "Arelux Contact Form Submission",
    'summary': """Arelux Contact Form Submission""",
    'author': "@victor.almau",
    'website': "http://www.arelux.com",
    'category': 'Test',
    'version': '1.1.4',
    'depends': ['base', 'sale', 'website_quote', 'utm_websites', 'tracking_arelux', 'arelux_partner_questionnaire', 'delivery'],
    'data': [
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'views/contact_form_submission_view.xml',
    ],
}