# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WasteRemoveProduct(models.Model):
    _name = 'waste.remove.product'
    _description = 'Waste Remove Product'        

    name = fields.Char(        
        string='Nombre'
    )
    uom = fields.Char(        
        string='Unidad de medida'
    )
