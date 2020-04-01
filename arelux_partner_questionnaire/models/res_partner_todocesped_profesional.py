# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerTodocespedProfesionalContactForm(models.Model):
    _name = 'res.partner.todocesped.profesional.contact.form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerTodocespedProfesionalValuationThing(models.Model):
    _name = 'res.partner.todocesped.profesional.valuation.thing'

    name = fields.Char(
        string="Nombre"
    )                                                 