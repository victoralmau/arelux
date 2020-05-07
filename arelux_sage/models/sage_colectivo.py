#-*- coding: utf-8 -*-
from odoo import models, fields

class SageColectivo(models.Model):
    _name = 'sage.colectivo'
    _description = 'Sage Colectivo'
    
    name = fields.Char('Nombre', required=True)