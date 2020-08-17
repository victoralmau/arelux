# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ReportMaintenanceInstallationItems(models.AbstractModel):
    _name = 'report.arelux_quality_forms.maintenance_installation_items'
    _description = 'Report Arelux quality forms maintenance installation items'

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
        }
        return self.env['report'].render(
            'arelux_quality_forms.maintenance_installation_items',
            docargs
        )
