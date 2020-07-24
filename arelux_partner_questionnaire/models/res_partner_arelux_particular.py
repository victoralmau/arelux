# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerAreluxParticularContactForm(models.Model):
    _name = 'res.partner.arelux.particular.contact.form'
    _description = 'Res Partner Arelux Particular Contact Form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerAreluxParticularValuationThing(models.Model):
    _name = 'res.partner.arelux.particular.valuation.thing'
    _description = 'Res Partner Arelux Particular Valuation Thing'

    name = fields.Char(
        string="Nombre"
    )                                                 