# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Arelux Contact Form Submission",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "sale",
        "utm_websites",  # https://github.com/OdooNodrizaTech/tools
        "tr_oniad",  # https://github.com/OdooNodrizaTech/tools
        "arelux_partner_questionnaire",
        "crm_arelux",
        "delivery",
        "mail",
        "mail_activity_datetime"  # https://github.com/OdooNodrizaTech/mail
    ],
    "external_dependencies": {
        "python": [
            "boto3"
        ],
    },
    "data": [
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
        "views/contact_form_submission_view.xml",
    ],
    "installable": True
}
