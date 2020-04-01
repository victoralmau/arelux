# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerTodocespedParticularContactForm(models.Model):
    _name = 'res.partner.todocesped.particular.contact.form'

    name = fields.Char(
        string="Nombre"
    )
    
class ResPartnerTodocespedParticularValuationThing(models.Model):
    _name = 'res.partner.todocesped.particular.valuation.thing'

    name = fields.Char(
        string="Nombre"
    )                                                 