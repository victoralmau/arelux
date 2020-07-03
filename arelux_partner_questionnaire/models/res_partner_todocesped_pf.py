# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerTodocespedPfContactForm(models.Model):
    _name = 'res.partner.todocesped.pf.contact.form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerTodocespedPfValuationThing(models.Model):
    _name = 'res.partner.todocesped.pf.valuation.thing'

    name = fields.Char(
        string="Nombre"
    )                                                 