# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerTodocespedPrContactForm(models.Model):
    _name = 'res.partner.todocesped.pr.contact.form'

    name = fields.Char(
        string="Nombre"
    )
    
class ResPartnerTodocespedPrValuationThing(models.Model):
    _name = 'res.partner.todocesped.pr.valuation.thing'

    name = fields.Char(
        string="Nombre"
    )                                                 