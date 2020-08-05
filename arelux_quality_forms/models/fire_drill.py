# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FireDrill(models.Model):
    _name = 'fire.drill'
    _description = 'Fire Drill'

    date = fields.Date(
        string='Date'
    )
    emergency_type = fields.Selection(
        selection=[
            ('general', 'General'),
            ('partial', 'Parcial')
        ],
        string='Tipo de emergencia'
    )
    drill = fields.Boolean(
        string='Simulacro'
    )
    description = fields.Text(
        string='Descripcion'
    )
    teams_must_act = fields.Text(
        string='Equipos deben actuar'
    )
    internal_communications = fields.Text(
        string='Comunicaciones internas'
    )
    description_causes = fields.Text(
        string='Descripcion de las causas'
    )
    description_consequences = fields.Text(
        string='Descripcion de las consecuencias'
    )
    general_description_intervention_performed = fields.Text(
        string='Descripcion general de la intervencion realizada'
    )
    fire_drill_decision_ids = fields.One2many(
        'fire.drill.decision',
        'fire_drill_id',
        string='Decisiones'
    )
