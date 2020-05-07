# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerTodocespedPrContactForm(models.Model):
    _name = 'res.partner.todocesped.pr.contact.form'
    _description = 'Res Partner Todocesped Pr Contact Form'

    name = fields.Char(
        string="Nombre"
    )
    
class ResPartnerTodocespedPrValuationThing(models.Model):
    _name = 'res.partner.todocesped.pr.valuation.thing'
    _description = 'Res Partner Todocesped Pr Valuation Thing'

    name = fields.Char(
        string="Nombre"
    )                                                 