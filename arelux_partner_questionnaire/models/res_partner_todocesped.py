# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, models, fields
_logger = logging.getLogger(__name__)


class ResPartnerTodocesped(models.Model):
    _inherit = 'res.partner'

    # General
    ar_qt_todocesped_interest_product_1 = fields.Many2one(
        comodel_name='product.template',
        domain=[
            ('sale_ok', '=', True),
            ('product_brand_id', '=', 5)
        ],
        string='TC - Modelos que más le interesan',
    )
    ar_qt_todocesped_interest_product_2 = fields.Many2one(
        comodel_name='product.template',
        domain=[
            ('sale_ok', '=', True),
            ('product_brand_id', '=', 5)
        ],
    )
    ar_qt_todocesped_interest_product_3 = fields.Many2one(
        comodel_name='product.template',
        domain=[
            ('sale_ok', '=', True),
            ('product_brand_id', '=', 5)
        ],
    )
    ar_qt_todocesped_interest_product_4 = fields.Many2one(
        comodel_name='product.template',
        domain=[
            ('sale_ok', '=', True),
            ('product_brand_id', '=', 5)]
        ,
    )
    ar_qt_todocesped_interest_product_all = fields.Boolean(
        string="TC - Modelos que más le interesan - Todos"
    )

    @api.multi
    @api.onchange('ar_qt_todocesped_interest_product_all')
    def change_ar_qt_todocesped_interest_product_all(self):
        for item in self:
            item.ar_qt_todocesped_interest_product_1 = 0
            item.ar_qt_todocesped_interest_product_2 = 0
            item.ar_qt_todocesped_interest_product_3 = 0
            item.ar_qt_todocesped_interest_product_4 = 0
            item.ar_qt_todocesped_interest_products_not_yet = False

    ar_qt_todocesped_interest_products_not_yet = fields.Boolean(
        string="TC - Modelos que más le interesan - Todavia no lo tiene claro"
    )

    @api.multi
    @api.onchange('ar_qt_todocesped_interest_products_not_yet')
    def change_ar_qt_todocesped_interest_products_not_yet(self):
        for item in self:
            item.ar_qt_todocesped_interest_product_1 = 0
            item.ar_qt_todocesped_interest_product_2 = 0
            item.ar_qt_todocesped_interest_product_3 = 0
            item.ar_qt_todocesped_interest_product_4 = 0
            item.ar_qt_todocesped_interest_product_all = False

    ar_qt_todocesped_contact_form = fields.Many2many(
        comodel_name='res.partner.contact.form',
        string='TC - Formas de contacto / Colectivo',
    )
    ar_qt_todocesped_contact_form_other = fields.Char(
        string='TC - Formas de contacto / Colectivo - Otro',
        size=35
    )
    ar_qt_todocesped_contact_form_other_show = fields.Boolean(
        store=False
    )
    ar_qt_todocesped_is_recommendation = fields.Boolean(
        string="TC - Viene recomendado"
    )
    ar_qt_todocesped_recommendation_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='TC - Quién nos recomendó',
    )
    # Particular
    # 1
    ar_qt_todocesped_pr_where_install = fields.Selection(
        [
            ('garden', 'Jardin (planta baja)'),
            ('terrace', 'Terraza'),
            ('penhouse', 'Atico (ultima planta)'),
            ('inside', 'Interior'),
            ('deal', 'Negocio'),
            ('urbanization', 'Urbanizacion'),
            ('event', 'Evento/Feria'),
            ('other', 'Otro'),
        ],
        size=15,
        string='TC - Dónde lo instala',
        copy=False,
        index=True
    )

    @api.multi
    @api.onchange('ar_qt_todocesped_pr_where_install')
    def change_ar_qt_todocesped_pr_where_install(self):
        for item in self:
            if item.ar_qt_todocesped_pr_where_install == "garden":
                item.ar_qt_todocesped_pr_type_surface = [1]
            elif item.ar_qt_todocesped_pr_where_install == "terrace":
                item.ar_qt_todocesped_pr_type_surface = [3]
            elif item.ar_qt_todocesped_pr_where_install == "penhouse":
                item.ar_qt_todocesped_pr_type_surface = [3]
            elif item.ar_qt_todocesped_pr_where_install == "event":
                item.ar_qt_todocesped_pr_type_surface = [2]

    ar_qt_todocesped_pr_where_install_other = fields.Char(
        string='TC - Dónde lo instala - Otro',
        size=35
    )
    # 1b
    ar_qt_todocesped_pr_budget_instalation = fields.Boolean(
        string="TC - Quiere presupuesto de instalación"
    )
    # 2
    ar_qt_todocesped_pr_type_surface = fields.Many2many(
        comodel_name='res.partner.type.surface',
        domain=[
            ('filter_company', 'in', ('all', 'todocesped')),
            ('filter_ar_qt_customer_type', 'in', ('all', 'particular'))
        ],
        string='TC - Tipo de superficie',
    )

    @api.multi
    @api.onchange('ar_qt_todocesped_pr_type_surface')
    def change_ar_qt_todocesped_pr_type_surface(self):
        for item in self:
            item._compute_ar_qt_todocesped_pr_type_surface_other_show()

    ar_qt_todocesped_pr_type_surface_other = fields.Char(
        string='TC - Tipo de superficie - Otro',
        size=35
    )
    ar_qt_todocesped_pr_type_surface_other_show = fields.Boolean(
        compute='_compute_ar_qt_todocesped_pr_type_surface_other_show',
        store=False
    )

    @api.multi
    def _compute_ar_qt_todocesped_pr_type_surface_other_show(self):
        for item in self:
            item.ar_qt_todocesped_pr_type_surface_other_show = False
            for item2 in item.ar_qt_todocesped_pr_type_surface:
                if item2.other:
                    item.ar_qt_todocesped_pr_type_surface_other_show = True

    # 3
    ar_qt_todocesped_pr_specific_segment = fields.Many2many(
        comodel_name='res.partner.specific.segment',
        domain=[
            ('filter_company', 'in', ('all', 'todocesped')),
            ('filter_ar_qt_customer_type', 'in', ('all', 'particular'))
        ],
        string='TC - Segmento específico',
    )

    @api.multi
    @api.onchange('ar_qt_todocesped_pr_specific_segment')
    def change_ar_qt_todocesped_pr_specific_segment(self):
        for item in self:
            item._compute_ar_qt_todocesped_pr_specific_segment_other_show()

    ar_qt_todocesped_pr_specific_segment_other = fields.Char(
        string='TC - Segmento específico - Otro',
        size=35
    )
    ar_qt_todocesped_pr_specific_segment_other_show = fields.Boolean(
        compute='_compute_ar_qt_todocesped_pr_specific_segment_other_show',
        store=False
    )

    @api.multi
    def _compute_ar_qt_todocesped_pr_specific_segment_other_show(self):
        for item in self:
            item.ar_qt_todocesped_pr_specific_segment_other_show = False
            for item2 in item.ar_qt_todocesped_pr_specific_segment:
                if item2.other:
                    item.ar_qt_todocesped_pr_specific_segment_other_show = True

    # 4
    ar_qt_todocesped_pr_why_install_it = fields.Many2many(
        comodel_name='res.partner.reason.install',
        domain=[
            ('filter_company', 'in', ('all', 'todocesped')),
            ('filter_ar_qt_customer_type', 'in', ('all', 'particular'))
        ],
        string='TC - Por qué lo instala',
    )

    @api.multi
    @api.onchange('ar_qt_todocesped_pr_why_install_it')
    def change_ar_qt_todocesped_pr_why_install_it(self):
        for item in self:
            item._compute_ar_qt_todocesped_pr_why_install_it_other_show()

    ar_qt_todocesped_pr_why_install_it_other = fields.Char(
        string='TC - Por qué lo instala - Otro',
        size=35
    )
    ar_qt_todocesped_pr_why_install_it_other_show = fields.Boolean(
        compute='_compute_ar_qt_todocesped_pr_why_install_it_other_show',
        store=False
    )

    @api.multi
    def _compute_ar_qt_todocesped_pr_why_install_it_other_show(self):
        for item in self:
            item.ar_qt_todocesped_pr_why_install_it_other_show = False
            for item2 in item.ar_qt_todocesped_pr_why_install_it:
                if item2.other:
                    item.ar_qt_todocesped_pr_why_install_it_other_show = True

    # 5
    ar_qt_todocesped_pr_who_values_more = fields.Many2many(
        comodel_name='res.partner.valuation.thing',
        domain=[
            ('filter_company', 'in', ('all', 'todocesped')),
            ('filter_ar_qt_customer_type', 'in', ('all', 'particular'))
        ],
        string='TC - Quién valora más',
    )
    ar_qt_todocesped_pr_who_values_more_other = fields.Char(
        string='TC - Quién valora más - Otro',
        size=35
    )
    ar_qt_todocesped_pr_who_values_more_other_show = fields.Boolean(
        compute='_compute_ar_qt_todocesped_pr_who_values_more_other_show',
        store=False
    )

    @api.multi
    def _compute_ar_qt_todocesped_pr_who_values_more_other_show(self):
        for item in self:
            item.ar_qt_todocesped_pr_who_values_more_other_show = False
            for item2 in item.ar_qt_todocesped_pr_who_values_more:
                if item2.other:
                    item.ar_qt_todocesped_pr_who_values_more_other_show = True

    @api.multi
    @api.onchange('ar_qt_todocesped_pr_who_values_more')
    def change_ar_qt_todocesped_pr_who_values_more(self):
        for item in self:
            item._compute_ar_qt_todocesped_pr_who_values_more_other_show()

    # Profesional
    # 1
    ar_qt_todocesped_pf_customer_type = fields.Selection(
        [
            ('warehouse_construction', 'Almacen de construccion'),
            ('architect', 'Arquitecto'),
            ('construction', 'Constructora / Promotora'),
            ('decorator', 'Decorador / Paisajista'),
            ('gardener', 'Jardinero'),
            ('multiservice', 'Multiservicio'),
            ('event_planner', 'Organizador de eventos'),
            ('pool', 'Piscinas'),
            ('nursery', 'Vivero'),
            ('other', 'Otro'),
        ],
        size=35,
        string='TC - Tipo de cliente',
        copy=False,
        index=True
    )
    ar_qt_todocesped_pf_customer_type_other = fields.Char(
        string='TC - Tipo de cliente - Otro',
        size=35
    )
    # 2
    ar_qt_todocesped_pf_install_artificial_grass = fields.Boolean(
        string="TC - Instala el cesped artificial"
    )
    # 3
    ar_qt_todocesped_pf_type_customers_sale = fields.Many2many(
        comodel_name='res.partner.type.customer.sale',
        domain=[
            ('filter_company', 'in', ('all', 'todocesped')),
            ('filter_ar_qt_customer_type', 'in', ('all', 'profesional'))
        ],
        string='TC  A qué tipo de clientes vende nuestro cesped',
    )
    # 4
    ar_qt_todocesped_pf_stock_capacity = fields.Many2many(
        comodel_name='res.partner.stock.capacity',
        domain=[
            ('filter_company', 'in', ('all', 'todocesped')),
            ('filter_ar_qt_customer_type', 'in', ('all', 'profesional'))
        ],
        string='TC - Tiene capacidad de stockar',
    )
    # 5
    ar_qt_todocesped_pf_valuation_thing = fields.Many2many(
        comodel_name='res.partner.valuation.thing',
        domain=[
            ('filter_company', 'in', ('all', 'todocesped')),
            ('filter_ar_qt_customer_type', 'in', ('all', 'profesional'))
        ],
        string='TC - Que valora más ',
    )

    @api.multi
    @api.onchange('ar_qt_todocesped_pf_valuation_thing')
    def change_ar_qt_todocesped_pf_valuation_thing(self):
        for item in self:
            item._compute_ar_qt_todocesped_pf_valuation_thing_other_show()

    ar_qt_todocesped_pf_valuation_thing_other = fields.Char(
        string='TC - Qué valora más - Otro',
        size=35
    )
    ar_qt_todocesped_pf_valuation_thing_other_show = fields.Boolean(
        compute='_compute_ar_qt_todocesped_pf_valuation_thing_other_show',
        store=False
    )

    @api.multi
    def _compute_ar_qt_todocesped_pf_valuation_thing_other_show(self):
        for item in self:
            item.ar_qt_todocesped_pf_valuation_thing_other_show = False
            for item2 in item.ar_qt_todocesped_pf_valuation_thing:
                if item2.other:
                    item.ar_qt_todocesped_pf_valuation_thing_other_show = True
