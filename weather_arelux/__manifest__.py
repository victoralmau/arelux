# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Weather Arelux',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [
        'data/ir_cron.xml',
        'views/res_better_zip.xml',
    ],
    'installable': True,
    'auto_install': False,    
}