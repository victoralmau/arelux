# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WasteRemoveDetail(models.Model):
    _name = 'waste.remove.detail'
    _description = 'Waste Remove Detail'        

    waste_remove_id = fields.Many2one(
        comodel_name='waste.remove',
        string='Retirada'
    )
    waste_remove_product_id = fields.Many2one(
        comodel_name='waste.remove.product',
        string='Producto'
    )
    quantity = fields.Integer(        
        string='Cantidad'
    )
