# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerTodocespedPrContactForm(models.Model):
    _name = 'res.partner.todocesped.pr.contact.form'
    _description = 'Res Partner Todocesped Pr Contact Form'

    name = fields.Char(
        string="Nombre"
    )


class ResPartnerTodocespedPrValuationThing(models.Model):
    _name = 'res.partner.todocesped.pr.valuation.thing'
    _description = 'Res Partner Todocesped Pr Valuation Thing'

    name = fields.Char(
        string="Nombre"
    )
