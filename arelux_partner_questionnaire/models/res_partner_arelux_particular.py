# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerAreluxParticularContactForm(models.Model):
    _name = 'res.partner.arelux.particular.contact.form'
    _description = 'Res Partner Arelux Particular Contact Form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerAreluxParticularValuationThing(models.Model):
    _name = 'res.partner.arelux.particular.valuation.thing'
    _description = 'Res Partner Arelux Particular Valuation Thing'

    name = fields.Char(
        string="Nombre"
    )                                                 