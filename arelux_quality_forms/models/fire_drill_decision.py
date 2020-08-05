# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FireDrillDecision(models.Model):
    _name = 'fire.drill.decision'
    _description = 'Fire Drill Decision'

    fire_drill_id = fields.Many2one(
        comodel_name='fire.drill',
        string='Simulacro'
    )
    responsible_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsable'
    )
    term_date = fields.Date(
        string='Plazo'
    )
    close_measurement = fields.Date(
        string='Cierre de la medida'
    )
