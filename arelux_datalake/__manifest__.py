# -*- coding: utf-8 -*-
{
    'name': "Arelux Datalake",
    'summary': """Arelux Datalake""",    
    'author': "@victor.almau",
    'website': "http://www.arelux.com",
    'category': 'Test',
    'version': '1.2.1',
    'external_dependencies': {
        'python' : ['boto3'],
    },
    'depends': [
        'base'        
    ],
    'data': [
        'data/ir_cron.xml',
        'data/ir_configparameter_data.xml',                
        'security/ir.model.access.csv',                
    ],    
}