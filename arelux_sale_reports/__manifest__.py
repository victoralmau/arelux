# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Arelux Sale Reports',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['sale', 'arelux_partner_questionnaire'],
    'data': [
        'data/ir_cron.xml',
        'data/ir_configparameter_data.xml',
        'data/arelux_sale_report_type.xml',
        'data/arelux_sale_report_template.xml',
        'data/arelux_sale_report_template_line.xml',        
        'views/arelux_sale_report_view.xml',                
        'security/ir.model.access.csv',
        'report/arelux_sale_report.xml',
    ],
    'installable': True,
    'auto_install': False,    
}