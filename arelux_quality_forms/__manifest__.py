# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Arelux Quality Forms",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "mail"
    ],
    "data": [
        "security/security.xml",
        "data/quality_team.xml",
        "data/waste_remove_product.xml",
        "data/maintenance_installation_need_check_data.xml",
        "data/ir_cron.xml",
        "views/fire_drill_view.xml",
        "views/fire_drill_decision_view.xml",
        "views/quality_team_view.xml",
        "views/maintenance_installation_view.xml",
        "views/maintenance_installation_need_check_view.xml",
        "views/waste_remove_view.xml",
        "views/waste_remove_detail_view.xml",
        "views/waste_remove_product_view.xml",
        "views/menu_view.xml",
        "wizard/maintenance_installation.xml",
        "wizard/waste_remove.xml",
        "report/report_maintenance_installation_items.xml",
        "report/report_waste_remove_items.xml",
    ],
    "installable": True
}
