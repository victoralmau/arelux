# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerAreluxPfContactForm(models.Model):
    _name = 'res.partner.arelux.pf.contact.form'
    _description = 'Res Partner Arelux Pf Contact Form'

    name = fields.Char(
        string="Nombre"
    )

class ResPartnerAreluxPfValuationThing(models.Model):
    _name = 'res.partner.arelux.pf.valuation.thing'
    _description = 'Res Partner Arelux Pf Valuation Thing'

    name = fields.Char(
        string="Nombre"
    )
