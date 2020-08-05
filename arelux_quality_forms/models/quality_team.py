# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QualityTeam(models.Model):
    _name = 'quality.team'
    _description = 'Quality Team'

    name = fields.Char(
        string='Name'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User'
    )
