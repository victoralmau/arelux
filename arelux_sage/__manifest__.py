# -*- coding: utf-8 -*-
{
    'name': 'Arelux Sage',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale'],
    'data': [
        'views/sage_actividad_view.xml',
        'views/sage_subactividad_view.xml',
        'views/sage_sector_view.xml',
        'views/sage_categoria_cliente_view.xml',  
        'views/sage_tipo_cliente_view.xml',
        'views/sage_colectivo_view.xml',
        'views/sage_zona_view.xml',
        'views/sage_delegacion_view.xml',
        'views/sage_territorio_view.xml',
        'views/sage_grupo_comercial_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,    
}