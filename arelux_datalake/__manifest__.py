# -*- coding: utf-8 -*-
{
    'name': 'Arelux Datalake',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'external_dependencies': {
        'python' : ['boto3'],
    },
    'depends': ['base'],
    'data': [
        'data/ir_cron.xml',
        'data/ir_configparameter_data.xml',                
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,    
}