# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Survey Arelux",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "ont_base_survey",
        "survey_extra_crm",
        "crm",
        "crm_claim",
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