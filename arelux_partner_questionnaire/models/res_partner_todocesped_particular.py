# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerTodocespedParticularContactForm(models.Model):
    _name = 'res.partner.todocesped.particular.contact.form'

    name = fields.Char(
        string="Nombre"
    )
    
class ResPartnerTodocespedParticularValuationThing(models.Model):
    _name = 'res.partner.todocesped.particular.valuation.thing'

    name = fields.Char(
        string="Nombre"
    )                                                 