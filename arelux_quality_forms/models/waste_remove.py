# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WasteRemove(models.Model):
    _name = 'waste.remove'
    _description = 'Waste Remove'

    date = fields.Date(
        string='Fecha'
    )
    retired_by = fields.Many2one(
        comodel_name='res.users',
        string='Retirado por'
    )
    sign_by = fields.Many2one(
        comodel_name='res.users',
        string='Firmado por'
    )
    destination = fields.Selection(
        selection=[
            ('container', 'Contenedor'),
            ('clean_point', 'Punto limpio')
        ],
        string='Destino'
    )
    waste_remove_detail_ids = fields.One2many(
        'waste.remove.detail',
        'waste_remove_id',
        string='Detalles'
    )
