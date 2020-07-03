# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerAreluxPfContactForm(models.Model):
    _name = 'res.partner.arelux.pf.contact.form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerAreluxPfValuationThing(models.Model):
    _name = 'res.partner.arelux.pf.valuation.thing'

    name = fields.Char(
        string="Nombre"
    )                                                 