# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerAreluxPrContactForm(models.Model):
    _name = 'res.partner.arelux.pr.contact.form'
    _description = 'Res Partner Arelux Pr Contact Form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerAreluxPrValuationThing(models.Model):
    _name = 'res.partner.arelux.pr.valuation.thing'
    _description = 'Res Partner Arelux Pr Valuation Thing'

    name = fields.Char(
        string="Nombre"
    )                                                 