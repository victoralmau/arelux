# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Res Arelux",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base"
    ],
    "external_dependencies": {
        "python": [
            "validate_email"
        ],
    },
    "data": [
        "data/ir_cron.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True
}
