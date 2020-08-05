# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mail Activity Objective Arelux",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "mail_activity_objective",  # https://github.com/OdooNodrizaTech/mail
        "crm_claim",  # https://github.com/OdooNodrizaTech/crm
        "sale_arelux"
    ],
    "data": [
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
        "views/crm_lead_view.xml",
    ],
    "installable": True
}
