# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
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