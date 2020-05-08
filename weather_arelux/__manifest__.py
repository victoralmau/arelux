# -*- coding: utf-8 -*-
{
    'name': 'Weather Arelux',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'base_location'],
    'data': [
        'data/ir_cron.xml',
        'views/res_city_zip.xml',
    ],
    'installable': True,
    'auto_install': False,    
}