# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Arelux Partner Questionnaire",
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
        "product",
        "stock",
        "web",
        "shipping_expedition",  # https://github.com/OdooNodrizaTech/stock
        "sale_stock"
    ],
    "data": [
        "views/crm_lead_view.xml",
        "views/crm_team_view.xml",
        "views/product_pricelist_view.xml",
        "data/res_partner_contact_form.xml",
        "data/res_partner_qualification_product.xml",
        "data/res_partner_reason_buy.xml",
        "data/res_partner_reason_install.xml",
        "data/res_partner_specific_segment.xml",
        "data/res_partner_stock_capacity.xml",
        "data/res_partner_type_customer_sale.xml",
        "data/res_partner_type_surface.xml",
        "data/res_partner_valuation_thing.xml",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
        "views/sale_order_template_view.xml",
        "views/shipping_expedition_view.xml",
        "views/stock_picking_view.xml",
        "views/account_invoice_view.xml",
        "views/mail_template_view.xml",
        "views/mail_compose_message_view.xml",
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True
}
