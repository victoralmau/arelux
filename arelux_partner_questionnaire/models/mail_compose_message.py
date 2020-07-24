# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'
                    
    @api.one
    @api.depends('model', 'res_id')        
    def _get_ar_qt_activity_type(self):                    
        if self.model and self.res_id:
            model_item = self.env[self.model].search([('id', '=', self.res_id)])[0]
            if 'ar_qt_activity_type' in model_item:
                self.ar_qt_activity_type = model_item.ar_qt_activity_type
                
    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),                    
        ],
        compute='_get_ar_qt_activity_type',
        size=15, 
        string='Tipo de actividad'
    )                             