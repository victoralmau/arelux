# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'
    
    prod_lot_id_ref = fields.Char( 
        string='Referencia interna',
        compute='_compute_prod_lot_id_ref',
        store=False
    )
    
    @api.multi
    def _compute_prod_lot_id_ref(self):
        for item in self:
            item.prod_lot_id_ref = item.prod_lot_id.ref
