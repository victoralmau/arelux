# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerAreluxProfesionalContactForm(models.Model):
    _name = 'res.partner.arelux.profesional.contact.form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerAreluxProfesionalValuationThing(models.Model):
    _name = 'res.partner.arelux.profesional.valuation.thing'

    name = fields.Char(
        string="Nombre"
    )                                                 