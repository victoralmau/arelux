# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerQualificationProduct(models.Model):
    _name = 'res.partner.qualification.product'
    _description = 'Res Partner Qualification Product'
    _order = "position asc"

    name = fields.Char(
        string="Nombre"
    )
    filter_company = fields.Selection(
        [
            ('all', 'Todas'),
            ('todocesped', 'Todocesped'),
            ('evert', 'Evert'),
            ('arelux', 'Arelux'),        
        ], 
        string='Empresa', 
        default='all'
    )
    filter_ar_qt_customer_type = fields.Selection(
        [
            ('all', 'Todas'),
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),        
        ], 
        string='Tipo cliente', 
        default='particular'
    )
    position = fields.Integer(
        string="Posicion"
    ) 
    other = fields.Boolean(
        string="Otro"
    )