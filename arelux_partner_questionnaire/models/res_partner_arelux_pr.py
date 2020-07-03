# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerAreluxPrContactForm(models.Model):
    _name = 'res.partner.arelux.pr.contact.form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerAreluxPrValuationThing(models.Model):
    _name = 'res.partner.arelux.pr.valuation.thing'

    name = fields.Char(
        string="Nombre"
    )                                                 