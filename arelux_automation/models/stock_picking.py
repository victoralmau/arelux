# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.multi
    def action_send_account_invoice_out_refund(self):
        self.ensure_one()
        res = super(StockPicking, self).action_send_account_invoice_out_refund()
        # save_log
        vals = {
            'model': 'account.invoice',
            'res_id': self.out_refund_invoice_id.id,
            'category': 'account_invoice',
            'action': 'create',                                                                                                                                                                                           
        }
        self.env['automation.log'].sudo().create(vals)
        # return
        return res
