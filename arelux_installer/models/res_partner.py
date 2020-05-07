# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerSage(models.Model):
    _inherit = 'res.partner'
           
    installer = fields.Boolean(
        string="Instalador"
    )                                       