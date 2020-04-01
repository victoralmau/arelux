# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerAreluxParticularContactForm(models.Model):
    _name = 'res.partner.arelux.particular.contact.form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerAreluxParticularValuationThing(models.Model):
    _name = 'res.partner.arelux.particular.valuation.thing'

    name = fields.Char(
        string="Nombre"
    )                                                 