# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerReasonBuy(models.Model):
    _name = 'res.partner.reason.buy'
    _order = "position asc"

    name = fields.Char(
        string="Nombre"
    )
    filter_company = fields.Selection(
        [
            ('all', 'Todas'),
            ('todocesped', 'Todocesped'),
            ('evert', 'Evert'),
            ('arelux', 'Arelux'),        
        ], 
        string='Empresa', 
        default='all'
    )
    filter_ar_qt_customer_type = fields.Selection(
        [
            ('all', 'Todas'),
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),        
        ], 
        string='Empresa', 
        default='particular'
    )
    position = fields.Integer(
        string="Posicion"
    )
    other = fields.Boolean(
        string="Otro"
    )