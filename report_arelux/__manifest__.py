# -*- coding: utf-8 -*-
{
    'name': 'Report Arelux',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'website', 'sale', 'account', 'arelux_partner_questionnaire', 'delivery', 'purchase'],
    'data': [
        'views/external_layout_header.xml',
        'views/external_layout_footer.xml',
        'views/report_saleorder_document.xml',
        'views/report_delivery_document.xml',
        'views/report_purchaseorder_document.xml',
        'views/report_invoice_document.xml',
    ],
    'installable': True,
    'auto_install': False,    
}