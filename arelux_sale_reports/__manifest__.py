# -*- coding: utf-8 -*-
{
    'name': "Arelux Sale Reports",
    'summary': """Arelux Sale Reports""",    
    'author': "@victor.almau",
    'website': "http://www.arelux.com",
    'category': 'Test',
    'version': '1.2.2',
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
}