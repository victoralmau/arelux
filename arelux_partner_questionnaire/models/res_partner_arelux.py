# -*- coding: utf-8 -*-
from openerp import api, models, fields

import logging

_logger = logging.getLogger(__name__)

class ResPartnerArelux(models.Model):
    _inherit = 'res.partner'
    
    '''General'''
    ar_qt_arelux_interest_product_1 = fields.Many2one(
        comodel_name='product.template', 
        domain=[('sale_ok', '=', True),('product_brand_id','=', 1)],
        string='AR - Productos relacionados que le podrían encajar',
    )
    ar_qt_arelux_interest_product_2 = fields.Many2one(
        comodel_name='product.template',
        domain=[('sale_ok', '=', True),('product_brand_id','=', 1)], 
    )
    ar_qt_arelux_interest_product_3 = fields.Many2one(
        comodel_name='product.template',
        domain=[('sale_ok', '=', True),('product_brand_id','=', 1)],
    )
    ar_qt_arelux_interest_product_4 = fields.Many2one(
        comodel_name='product.template',
        domain=[('sale_ok', '=', True),('product_brand_id','=', 1)],
    )
    ar_qt_arelux_interest_product_all = fields.Boolean(
        string="AR - Productos relacionados que le podrían encajar - Todos"
    )    
    @api.onchange('ar_qt_arelux_interest_product_all')
    def change_ar_qt_arelux_interest_product_all(self):
        self.ar_qt_arelux_interest_product_1 = 0
        self.ar_qt_arelux_interest_product_2 = 0
        self.ar_qt_arelux_interest_product_3 = 0
        self.ar_qt_arelux_interest_product_4 = 0
        self.ar_qt_arelux_interest_product_not_yet = False        
    
    ar_qt_arelux_interest_product_not_yet = fields.Boolean(
        string="AR - Productos relacionados que le podrían encajar - Todavía no lo tiene claro"
    )
    @api.onchange('ar_qt_arelux_interest_product_not_yet')
    def change_ar_qt_arelux_interest_product_not_yet(self):
        self.ar_qt_arelux_interest_product_1 = 0
        self.ar_qt_arelux_interest_product_2 = 0
        self.ar_qt_arelux_interest_product_3 = 0
        self.ar_qt_arelux_interest_product_4 = 0
        self.ar_qt_arelux_interest_product_all = False
    
    ar_qt_arelux_valuation_thing = fields.Many2many(
        comodel_name='res.partner.valuation.thing',         
        string='AR - Qué valora más',
    )            
    ar_qt_arelux_valuation_thing_other = fields.Char(
        string='AR - Otro',
        size=35
    )
    ar_qt_arelux_valuation_thing_other_show = fields.Boolean(
        store=False
    )            
    ar_qt_arelux_contact_form = fields.Many2many(
        comodel_name='res.partner.contact.form', 
        string='AR - Formas de contacto / Colectivo',
    )     
    ar_qt_arelux_contact_form_other = fields.Char(
        string='AR - Formas de contacto / Colectivo - Otro',
        size=35
    )
    ar_qt_arelux_contact_form_other_show = fields.Boolean(
        store=False
    )    
                        
    ar_qt_arelux_is_recommendation = fields.Boolean(
        string="AR - Viene recomendado"
    )    
    ar_qt_arelux_recommendation_partner_id = fields.Many2one(
        comodel_name='res.partner', 
        string='AR - Quién nos recomendó',
    )                    
    '''Particular'''
    ''''1'''
    ar_qt_arelux_pr_ql_product = fields.Many2many(
        comodel_name='res.partner.qualification.product', 
        string='AR - Clasificación segun producto',
    )
    
    @api.onchange('ar_qt_arelux_pr_ql_product')
    def change_ar_qt_arelux_pr_ql_product(self):
        self._get_ar_qt_arelux_pr_ql_product_waterproofing_show()
        self._get_ar_qt_arelux_pr_ql_product_thermal_paints_show()
        self._get_ar_qt_arelux_pr_ql_product_reflective_insulators_show()
        self._get_ar_qt_arelux_pr_ql_product_surface_treatment_show()
        self._get_ar_qt_arelux_pr_ql_product_other_show()
            
    '''1-Impermeabilizantes'''
    ar_qt_arelux_pr_ql_product_waterproofing = fields.Selection(
        [
            ('leaks', 'Filtraciones'),
            ('other', 'Otro'),
        ], 
        size=15,
        string='AR - Impermeabilizantes - Por qué?', 
        copy=False, 
        index=True
    ) 
    
    ar_qt_arelux_pr_ql_product_waterproofing_show = fields.Boolean(
        compute='_get_ar_qt_arelux_pr_ql_product_waterproofing_show',
        store=False
    )
    
    @api.one        
    def _get_ar_qt_arelux_pr_ql_product_waterproofing_show(self):
        for partner_obj in self:          
            partner_obj.ar_qt_arelux_pr_ql_product_waterproofing_show = False
            for item in partner_obj.ar_qt_arelux_pr_ql_product:
                if item.id==1:
                    partner_obj.ar_qt_arelux_pr_ql_product_waterproofing_show = True
       
    ar_qt_arelux_pr_ql_product_waterproofing_other = fields.Char(
        string='AR - Impermeabilizantes - Otro',
        size=35
    )                    
    '''1-Pinturas termincas'''
    ar_qt_arelux_pr_ql_product_thermal_paints = fields.Selection(
        [
            ('saving', 'Ahorro (Reducir uso de calefaccion y aire acondicionado)'),
            ('insulation_little_space', 'Aislante que ocupa poco espacio'),
            ('thermal_insulation', 'Aislante termico'),
            ('humidity', 'Humedades por condesacion'),
            ('mold', 'Moho'),
            ('cold wall', 'Pared fria'),
            ('other', 'Otro'),
        ], 
        size=15,
        string='AR - Pinturas térmicas - Por qué pintura términa', 
        copy=False, 
        index=True
    )        
    ar_qt_arelux_pr_ql_product_thermal_paints_show = fields.Boolean(
        compute='_get_ar_qt_arelux_pr_ql_product_thermal_paints_show',
        store=False
    )
    
    @api.one        
    def _get_ar_qt_arelux_pr_ql_product_thermal_paints_show(self):
        for partner_obj in self:          
            partner_obj.ar_qt_arelux_pr_ql_product_thermal_paints_show = False
            for item in partner_obj.ar_qt_arelux_pr_ql_product:
                if item.id==2:
                    partner_obj.ar_qt_arelux_pr_ql_product_thermal_paints_show = True    
    
    ar_qt_arelux_pr_ql_product_thermal_paints_other = fields.Char(
        string='AR - Pinturas térmicas - Otro',
        size=35
    )
    '''1-Aislantes reflexivos'''
    ar_qt_arelux_pr_ql_product_reflective_insulators= fields.Selection(
        [
            ('insulation_little_space', 'Aislante que ocupa poco espacio'),
            ('thermal_insulation', 'Aislamiento termico'),
            ('acoustic_insulation', 'Aislamiento acustico'),
            ('vans_isolation', 'Aislamiento furgonetas'),
            ('floor_insulation', 'Aislamiento suelos'),
            ('other', 'Otro'),
        ], 
        size=15,
        string='AR - Aislantes reflexivos - Por qué aislantes', 
        copy=False, 
        index=True
    )
    ar_qt_arelux_pr_ql_product_reflective_insulators_show = fields.Boolean(
        compute='_get_ar_qt_arelux_pr_ql_product_reflective_insulators_show',
        store=False
    )
    
    @api.one        
    def _get_ar_qt_arelux_pr_ql_product_reflective_insulators_show(self):
        for partner_obj in self:          
            partner_obj.ar_qt_arelux_pr_ql_product_reflective_insulators_show = False
            for item in partner_obj.ar_qt_arelux_pr_ql_product:
                if item.id==3:
                    partner_obj.ar_qt_arelux_pr_ql_product_reflective_insulators_show = True    
        
    ar_qt_arelux_pr_ql_product_reflective_insulators_other = fields.Char(
        string='AR - Aislantes reflexivos - Otro',
        size=35
    )
    '''1-Tratamiento de superficies'''
    ar_qt_arelux_pr_ql_product_surface_treatment = fields.Selection(
        [
            ('parking', 'Garajes'),
            ('food_companies', 'Empresas alimentarias'),
            ('storage_rooms', 'Trasteros / pequenas zonas'),
            ('sports_areas', 'Zonas deportivas'),
            ('other', 'Otro'),
        ], 
        size=15,
        string='AR - Tratamiento de superficies - Dónde', 
        copy=False, 
        index=True
    )    
    ar_qt_arelux_pr_ql_product_surface_treatment_show = fields.Boolean(
        compute='_get_ar_qt_arelux_pr_ql_product_surface_treatment_show',
        store=False
    )
    
    @api.one        
    def _get_ar_qt_arelux_pr_ql_product_surface_treatment_show(self):
        for partner_obj in self:          
            partner_obj.ar_qt_arelux_pr_ql_product_surface_treatment_show = False
            for item in partner_obj.ar_qt_arelux_pr_ql_product:
                if item.id==4:
                    partner_obj.ar_qt_arelux_pr_ql_product_surface_treatment_show = True        
    
    ar_qt_arelux_pr_ql_product_surface_treatment_other = fields.Char(
        string='AR - Tratamiento de superficies - Otro',
        size=35
    )
    
            
    ar_qt_arelux_pr_ql_product_other_show = fields.Boolean(
        compute='_get_ar_qt_arelux_pr_ql_product_other_show',
        store=False
    )
    @api.one        
    def _get_ar_qt_arelux_pr_ql_product_other_show(self):
        for partner_obj in self:          
            partner_obj.ar_qt_arelux_pr_ql_product_other_show = False
            for item in partner_obj.ar_qt_arelux_pr_ql_product:
                if item.other==True:
                    partner_obj.ar_qt_arelux_pr_ql_product_other_show = True
                    
    ar_qt_arelux_pr_ql_product_other = fields.Char(
        string='AR - Otro',
        size=35
    )        
    '''1b'''
    ar_qt_arelux_pr_insall_the_same = fields.Boolean(
        string="AR - Lo aplica o instala ella/él mismo"
    )
    '''2'''
    ar_qt_arelux_pr_reason_buy = fields.Many2many(
        comodel_name='res.partner.reason.buy', 
        string='AR - Por qué lo compran',
    )    
    @api.onchange('ar_qt_arelux_pr_reason_buy')
    def change_ar_qt_arelux_pr_reason_buy(self):
        self._get_ar_qt_arelux_pr_reason_buy_other_show()
        
    ar_qt_arelux_pr_reason_buy_other = fields.Char(
        string='AR - Otro',
        size=35
    )
    ar_qt_arelux_pr_reason_buy_other_show = fields.Boolean(
        compute='_get_ar_qt_arelux_pr_reason_buy_other_show',
        store=False
    )
    
    @api.one        
    def _get_ar_qt_arelux_pr_reason_buy_other_show(self):
        for partner_obj in self:          
            partner_obj.ar_qt_arelux_pr_reason_buy_other_show = False
            for item in partner_obj.ar_qt_arelux_pr_reason_buy:
                if item.other==True:
                    partner_obj.ar_qt_arelux_pr_reason_buy_other_show = True
    
    ar_qt_arelux_pr_valuation_thing = fields.Many2many(
        comodel_name='res.partner.valuation.thing', 
        domain=[('filter_company', 'in', ('all', 'arelux')),('filter_ar_qt_customer_type', 'in', ('all', 'particular'))],
        string='AR - Que valora más',
    )
    @api.onchange('ar_qt_arelux_pr_valuation_thing')
    def change_ar_qt_arelux_pr_valuation_thing(self):        
        self.ar_qt_arelux_valuation_thing = self.ar_qt_arelux_pr_valuation_thing                        
        self._get_ar_qt_arelux_pr_valuation_thing_other_show()
                
    ar_qt_arelux_pr_valuation_thing_other = fields.Char(
        store=False
    )
    @api.onchange('ar_qt_arelux_pr_valuation_thing_other')
    def change_ar_qt_arelux_pr_valuation_thing_other(self):
        self.ar_qt_arelux_valuation_thing_other = self.ar_qt_arelux_pr_valuation_thing_other
    
    ar_qt_arelux_pr_valuation_thing_other_show = fields.Boolean(
        compute='_get_ar_qt_arelux_pr_valuation_thing_other_show',
        store=False
    )
    @api.one        
    def _get_ar_qt_arelux_pr_valuation_thing_other_show(self):
        for partner_obj in self:          
            partner_obj.ar_qt_arelux_pr_valuation_thing_other_show = False            
            for item in partner_obj.ar_qt_arelux_pr_valuation_thing:            
                if item.other==True:
                    partner_obj.ar_qt_arelux_pr_valuation_thing_other_show = True
                    partner_obj.ar_qt_arelux_valuation_thing_other_show = True                        
       
    '''7'''    
    '''Profesional'''      
    '''1'''
    ar_qt_arelux_pf_customer_type = fields.Selection(
        [
            ('warehouse_construction', 'Almacen de construccion / distribuidores'),
            ('architect', 'Arquitecto / Aparejador / Decorador'),
            ('construction', 'Constructora / Promotora'),
            ('energy_efficiency_company', 'Empresa de eficiencia energetica'),
            ('humidity_treatment_company', 'Empresa de tratamiento de humedades o filtraciones'),
            ('painter', 'Pintor'),
            ('reform', 'Reforma / Albanil'),
            ('companies_specialized_in_insulation', 'Empresas especializadas en aislamiento'),            
            ('other', 'Otros'),
        ], 
        size=30,
        string='AR - Tipo de cliente', 
        copy=False, 
        index=True
    )
    ar_qt_arelux_pf_customer_type_other = fields.Char(
        string='AR - Tipo de cliente - Otro',
        size=35
    )
    '''1.b'''
    ar_qt_arelux_pf_install = fields.Boolean(
        string="AR - Hacen ellos la aplicación?"
    )
    '''2'''
    ar_qt_arelux_pf_type_customers_sale = fields.Many2many(
        comodel_name='res.partner.type.customer.sale', 
        string='AR - A que tipo de clientes vende nuestros productos',
    )
    '''3'''
    ar_qt_arelux_pf_stock_capacity = fields.Many2many(
        comodel_name='res.partner.stock.capacity', 
        string='AR - Tiene capacidad de stockar',
    )
    ar_qt_arelux_pf_valuation_thing= fields.Many2many(
        comodel_name='res.partner.valuation.thing', 
        domain=[('filter_company', 'in', ('all', 'arelux')),('filter_ar_qt_customer_type', 'in', ('all', 'profesional'))]
    )
    @api.onchange('ar_qt_arelux_pf_valuation_thing')
    def change_ar_qt_arelux_pf_valuation_thing(self):
        self.ar_qt_arelux_valuation_thing = self.ar_qt_arelux_pf_valuation_thing        
        self._get_ar_qt_arelux_pf_valuation_thing_other_show()
                
    ar_qt_arelux_pf_valuation_thing_other = fields.Char(
        store=False
    )
    @api.onchange('ar_qt_arelux_pf_valuation_thing_other')
    def change_ar_qt_arelux_pf_valuation_thing_other(self):
        self.ar_qt_arelux_valuation_thing_other = self.ar_qt_arelux_pf_valuation_thing_other
    
    ar_qt_arelux_pf_valuation_thing_other_show = fields.Boolean(
        compute='_get_ar_qt_arelux_pf_valuation_thing_other_show',
        store=False
    )
    @api.one        
    def _get_ar_qt_arelux_pf_valuation_thing_other_show(self):
        for partner_obj in self:          
            partner_obj.ar_qt_arelux_pf_valuation_thing_other_show = False
            for item in partner_obj.ar_qt_arelux_pf_valuation_thing:
                if item.other==True:
                    partner_obj.ar_qt_arelux_pf_valuation_thing_other_show = True
                    partner_obj.ar_qt_arelux_valuation_thing_other_show = True            
             
    '''7'''                                                                    