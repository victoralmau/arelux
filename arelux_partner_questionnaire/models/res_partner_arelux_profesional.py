# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class ResPartnerAreluxProfesionalContactForm(models.Model):
    _name = 'res.partner.arelux.profesional.contact.form'
    _description = 'Res Partner Arelux Profesional Contact Form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerAreluxProfesionalValuationThing(models.Model):
    _name = 'res.partner.arelux.profesional.valuation.thing'
    _description = 'Res Partner Arelux Profesional Valuation Thing'

    name = fields.Char(
        string="Nombre"
    )                                                 