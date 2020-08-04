# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Arelux Automation",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "crm",
        "mail",
        "sale",
        "stock",
        "aws_sms",  # https://github.com/OdooNodrizaTech/sms
        "sale_order_link_tracker",  # https://github.com/OdooNodrizaTech/sale
        "sale_stock",
        "automation_log"  # https://github.com/OdooNodrizaTech/automation_log
    ],
    "data": [
        "data/ir_configparameter_data.xml",
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
        "views/arelux_automation_process_view.xml",
    ],
    "installable": True
}
