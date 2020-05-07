#-*- coding: utf-8 -*-
from odoo import models, fields

class SageDelegacion(models.Model):
    _name = 'sage.delegacion'
    _description = 'Sage Delegacion'
    
    name = fields.Char('Nombre', required=True)
    code = fields.Char('Codigo', required=True)    
    sage_territorio_id = fields.Many2one(comodel_name='sage.territorio', ondelete='restrict')
    sage_zona_id = fields.Many2one(comodel_name='sage.zona', ondelete='restrict')