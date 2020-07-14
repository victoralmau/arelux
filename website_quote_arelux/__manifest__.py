# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Website Quote Arelux',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'website_portal_sale'],
    'data': [
        'data/ir_configparameter_data.xml',
        'views/sale_order_view.xml',
        'views/website_quote.xml',
        'views/sale_quote_template.xml',
    ],
    'installable': True,
    'auto_install': False,    
}