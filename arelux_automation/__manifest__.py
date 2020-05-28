# -*- coding: utf-8 -*-
{
    'name': 'Arelux Automation',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'crm', 'sale', 'stock', 'aws_sms', 'sale_order_link_tracker', 'automation_log'],
    'data': [
        'data/ir_configparameter_data.xml',
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'views/arelux_automation_process_view.xml',
    ],    
    'installable': True,
    'auto_install': False,    
}