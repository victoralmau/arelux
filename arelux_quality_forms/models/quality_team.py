# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class QualityTeam(models.Model):
    _name = 'quality.team'
    _description = 'Quality Team'

    name = fields.Char(
        string='Nombre'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsable'
    )