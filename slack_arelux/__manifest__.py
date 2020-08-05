# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Slack Arelux",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "sale",
        "account",
        "delivery",
        "slack",  # https://github.com/OdooNodrizaTech/slack
        "picking_arelux",
        "arelux_partner_questionnaire"
    ],
    "data": [
        "data/slack_data.xml",
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True
}
