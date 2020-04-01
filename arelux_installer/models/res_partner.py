# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerSage(models.Model):
    _inherit = 'res.partner'
           
    installer = fields.Boolean(
        string="Instalador"
    )                                       