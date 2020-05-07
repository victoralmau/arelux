# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerTodocespedPfContactForm(models.Model):
    _name = 'res.partner.todocesped.pf.contact.form'
    _description = 'Res Partner Todocesped Pf Contact Form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerTodocespedPfValuationThing(models.Model):
    _name = 'res.partner.todocesped.pf.valuation.thing'
    _description = 'Res Partner Todocesped Pf Valuation Thing'

    name = fields.Char(
        string="Nombre"
    )                                                 