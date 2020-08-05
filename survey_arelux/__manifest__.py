# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Survey Arelux",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "ont_base_survey",  # https://github.com/OdooNodrizaTech/ont
        "survey_extra_crm",  # https://github.com/OdooNodrizaTech/survey
        "crm",
        "crm_claim",  # https://github.com/OdooNodrizaTech/crm
        "sale",
        "survey",
        "arelux_partner_questionnaire"
    ],
    "data": [
        "views/survey_user_input_view.xml",
        "views/survey_survey_view.xml",
    ],
    "installable": True
}
