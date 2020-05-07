# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerTodocespedProfesionalContactForm(models.Model):
    _name = 'res.partner.todocesped.profesional.contact.form'
    _description = 'Res Partner Todocesped Profesional Contact Form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerTodocespedProfesionalValuationThing(models.Model):
    _name = 'res.partner.todocesped.profesional.valuation.thing'
    _description = 'Res Partner Todocesped Profesional Valuation Thing'

    name = fields.Char(
        string="Nombre"
    )                                                 