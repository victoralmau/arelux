# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import http
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class AreluxContactFormSubmissionController(http.Controller):

    @http.route(['/arelux_contact_form_submission/action_run'], type='http', auth='public', methods=['GET'], website=True)
    def arelux_contact_form_submission_action_run(self, **post):
        _logger.info('arelux_contact_form_submission_action_run (controller)')
        request.env['contact.form.submission'].sudo().cron_sqs_contact_form_submission()
        return request.render('website.404')