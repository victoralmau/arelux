# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerTodocespedParticularContactForm(models.Model):
    _name = 'res.partner.todocesped.particular.contact.form'
    _description = 'Res Partner Todocesped Particular Contact Form'

    name = fields.Char(
        string="Nombre"
    )
    
class ResPartnerTodocespedParticularValuationThing(models.Model):
    _name = 'res.partner.todocesped.particular.valuation.thing'
    _description = 'Res Partner Todocesped Particular Valuation Thing'

    name = fields.Char(
        string="Nombre"
    )                                                 