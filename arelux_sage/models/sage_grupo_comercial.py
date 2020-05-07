#-*- coding: utf-8 -*-
from odoo import models, fields

class SageGrupoComercial(models.Model):
    _name = 'sage.grupo.comercial'
    _description = 'Sage Grupo Comercial'
    
    name = fields.Char('Nombre', required=True)
    sage_delegacion_id = fields.Many2one(comodel_name='sage.delegacion', ondelete='restrict')
    employee_id = fields.Many2one(comodel_name='hr.employee', ondelete='restrict')    