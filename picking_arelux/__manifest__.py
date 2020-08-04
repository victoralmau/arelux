# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Picking Arelux",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "ont_base_picking",  # https://github.com/OdooNodrizaTech/ont
        "delivery",
        "sale",
        "stock",
        "account",
        "shipping_expedition",  # https://github.com/OdooNodrizaTech/stock
        "sale_stock"
    ],
    "data": [
        "data/ir_cron.xml",
        "views/delivery_carrier_view.xml",
        "views/stock_quant_view.xml",
        "views/stock_inventory_line_view.xml",
        "views/stock_move_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_production_lot_view.xml",
        "views/stock_return_picking_view.xml",
        "views/stock_scrap_view.xml",
    ],
    'installable': True
}
