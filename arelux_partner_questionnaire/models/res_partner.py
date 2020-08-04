# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from datetime import datetime
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'
        
    ar_qt_samples = fields.Date(
        compute='_ar_qt_samples',
        string='Muestras',
    )
    ar_qt_profession = fields.Char(
        string='Profesión',
        size=35
    )
    # ar_qt_questionnaire_todocesped_show
    ar_qt_questionnaire_todocesped_show = fields.Boolean(
        compute='_compute_ar_qt_questionnaire_todocesped_show',
        store=False,
    )
    
    @api.multi
    def _compute_ar_qt_questionnaire_todocesped_show(self):
        for item in self:
            item.ar_qt_questionnaire_todocesped_show = False
            if item.customer and (
                item.ar_qt_activity_type == 'todocesped'
                or item.ar_qt_activity_type == 'evert'
                or item.ar_qt_activity_type == 'both'
            ):
                item.ar_qt_questionnaire_todocesped_show = True
    
    # ar_qt_questionnaire_arelux_show
    ar_qt_questionnaire_arelux_show = fields.Boolean(
        compute='_compute_ar_qt_questionnaire_arelux_show',
        store=False,
    )
    
    @api.multi
    def _compute_ar_qt_questionnaire_arelux_show(self):
        for item in self:
            item.ar_qt_questionnaire_arelux_show = False
            if item.customer and item.ar_qt_activity_type == 'arelux':
                item.ar_qt_questionnaire_arelux_show = True
    
    ar_qt_customer_type = fields.Selection(
        [
            ('particular', 'Particular'),
            ('profesional', 'Profesional'),        
        ],
        size=15, 
        string='Tipo de cliente', 
        default='particular'
    )
    
    @api.onchange('ar_qt_customer_type')
    def change_ar_qt_customer_type(self):
        '''Todocesped'''                
        self.ar_qt_todocesped_interest_product_1 = 0        
        self.ar_qt_todocesped_interest_product_2 = 0                
        self.ar_qt_todocesped_interest_product_3 = 0                
        self.ar_qt_todocesped_interest_product_4 = 0                
        self.ar_qt_todocesped_interest_product_all = False                        
        self.ar_qt_todocesped_interest_products_not_yet = False        
        
        self.ar_qt_todocesped_contact_form = []                
        self.ar_qt_todocesped_contact_form_other = ''        
        
        self.ar_qt_todocesped_is_recommendation = False
        self.ar_qt_todocesped_recommendation_partner_id = 0        
        
        self.ar_qt_todocesped_pr_where_install = ''
        self.ar_qt_todocesped_pr_where_install_other = ''
        self.ar_qt_todocesped_pr_budget_instalation = False
        self.ar_qt_todocesped_pr_type_surface = []
        self.ar_qt_todocesped_pr_type_surface_other = ''
        self.ar_qt_todocesped_pr_specific_segment = []
        self.ar_qt_todocesped_pr_specific_segment_other = ''
        self.ar_qt_todocesped_pr_why_install_it = []
        self.ar_qt_todocesped_pr_why_install_it_other = ''
        self.ar_qt_todocesped_pr_who_values_more = []
        self.ar_qt_todocesped_pr_who_values_more_other = ''                        
        
        self.ar_qt_todocesped_pf_customer_type = ''
        self.ar_qt_todocesped_pf_customer_type_other = ''
        self.ar_qt_todocesped_pf_install_artificial_grass = False
        self.ar_qt_todocesped_pf_type_customers_sale = []
        self.ar_qt_todocesped_pf_stock_capacity = []
        self.ar_qt_todocesped_pf_valuation_thing = []
        self.ar_qt_todocesped_pf_valuation_thing_other = ''
        '''Arelux'''
        self.ar_qt_arelux_interest_product_1 = 0
        self.ar_qt_arelux_interest_product_2 = 0
        self.ar_qt_arelux_interest_product_3 = 0
        self.ar_qt_arelux_interest_product_4 = 0
        self.ar_qt_arelux_interest_product_all = False
                
        self.ar_qt_arelux_interest_product_not_yet = False
        self.ar_qt_arelux_valuation_thing = []
        self.ar_qt_arelux_valuation_thing_other = ''
                
        self.ar_qt_arelux_contact_form = []
        self.ar_qt_arelux_contact_form_other = ''
        
        self.ar_qt_arelux_is_recommendation = False
        self.ar_qt_arelux_recommendation_partner_id = 0
        
        self.ar_qt_arelux_pr_ql_product = []
        self.ar_qt_arelux_pr_ql_product_waterproofing = ''
        self.ar_qt_arelux_pr_ql_product_waterproofing_other = ''
        self.ar_qt_arelux_pr_ql_product_thermal_paints = ''
        self.ar_qt_arelux_pr_ql_product_thermal_paints_other = ''
        self.ar_qt_arelux_pr_ql_product_reflective_insulators = ''
        self.ar_qt_arelux_pr_ql_product_reflective_insulators_other = ''
        self.ar_qt_arelux_pr_ql_product_surface_treatment = ''
        self.ar_qt_arelux_pr_ql_product_surface_treatment_other = ''
        self.ar_qt_arelux_pr_insall_the_same = False
        self.ar_qt_arelux_pr_reason_buy = []
        self.ar_qt_arelux_pr_reason_buy_other = ''        
        
        self.ar_qt_arelux_pf_customer_type = ''
        self.ar_qt_arelux_pf_customer_type_other = ''
        self.ar_qt_arelux_pf_install = False
        self.ar_qt_arelux_pf_type_customers_sale = []
        self.ar_qt_arelux_pf_stock_capacity = []        
    
    ar_qt_activity_type = fields.Selection(
        [
            ('todocesped', 'Todocesped'),
            ('arelux', 'Arelux'),
            ('evert', 'Evert'),            
            ('both', 'Ambos'),        
        ],
        size=15, 
        string='Tipo de actividad', 
        default='todocesped'
    )

    @api.multi
    @api.onchange('ar_qt_activity_type', 'customer')
    def change_ar_qt_activity_type(self):
        for item in self:
            item._get_ar_qt_questionnaire_todocesped_show()
            item._get_ar_qt_questionnaire_arelux_show()
    
    is_potential_advertise_oniad = fields.Boolean(
        string="Potencial para OniAd"
    )            
    '''Profesional'''      
    ar_qt_pf_frequency_customer_type = fields.Selection(
        [
            ('none', 'Cliente sin ventas'),
            ('puntual', 'Cliente puntual'),
            ('loyalized', 'Cliente fidelizado'),
            ('recurrent', 'Cliente recurrente'),        
        ], 
        size=15,
        string='Tipo de cliente (frecuencia)', 
        default='puntual'
    ) 
    
    ar_qt_pf_sale_customer_type = fields.Selection(
        [
            ('bronze', 'Cliente bronce'),
            ('silver', 'Cliente plata'),
            ('gold', 'Cliente oro'),
            ('diamond', 'Cliente diamante'),        
        ], 
        size=15,
        string='Tipo de cliente (ventas)', 
        default='bronze'
    )
                                                        
    @api.multi        
    def _ar_qt_samples(self):
        for item in self:
            order_ids = self.env['sale.order'].search(
                    [
                        ('state', 'in', ('sale', 'done')),
                        ('partner_id', '=', item.id)
                    ]
                )
            if order_ids:
                for order_id in order_ids:
                    for order_line in order_id.order_line:
                        if order_line.product_id.id == 97:
                            item.ar_qt_samples = order_id.confirmation_date
                        
    @api.model
    def create(self, values):
        record = super(ResPartner, self).create(values)
        # operations
        if record.parent_id:
            if record.parent_id.ar_qt_activity_type:
                record.ar_qt_activity_type = record.parent_id.ar_qt_activity_type

            if record.parent_id.ar_qt_customer_type:
                record.ar_qt_customer_type = record.parent_id.ar_qt_customer_type                
        # return
        return record                                                                              
    
    @api.model    
    def cron_action_generate_customer_type(self):        
        current_date = datetime.today()
        start_date = current_date + relativedelta(months=-12, day=1)
        end_date = datetime(
            current_date.year,
            start_date.month,
            1
        ) + relativedelta(months=1, days=-1)
        partner_ids = self.env['res.partner'].search(
            [
                ('customer', '=', True),
                ('active', '=', True)
            ]
        )
        if partner_ids:
            partner_ids_real = partner_ids.mapped('id')
            sale_order_ids = self.env['sale.order'].search(
                [
                    ('state', 'in', ('sale','done')),
                    ('partner_id', 'in', partner_ids_real),
                    ('amount_total', '>', 0), 
                    ('confirmation_date', '>=', start_date.strftime("%Y-%m-%d")),
                    ('confirmation_date', '<=', end_date.strftime("%Y-%m-%d"))
                ]
            )
            if sale_order_ids:
                for partner_id in partner_ids:
                    # default
                    ar_qt_pf_frequency_customer_type_item = 'none'
                    ar_qt_pf_sale_customer_type_item = 'bronze'
                    # filter
                    sale_order_items = filter(lambda x : x['partner_id'] == partner_id, sale_order_ids)
                    if len(sale_order_items)>0:
                        # ar_qt_pf_frequency_customer_type_item
                        sale_order_ids_total = len(sale_order_items)
                        if sale_order_ids_total >= 1 and sale_order_ids_total <= 2:
                            ar_qt_pf_frequency_customer_type_item = 'puntual'                
                        elif sale_order_ids_total > 2 and sale_order_ids_total <= 5:
                            ar_qt_pf_frequency_customer_type_item = 'loyalized'
                        elif sale_order_ids_total >= 6:
                            ar_qt_pf_frequency_customer_type_item = 'recurrent'
                        # ar_qt_pf_sale_customer_type_item
                        amount_totals = map(lambda x : x['amount_total'],  sale_order_items)
                        partner_amount_total = sum(map(float,amount_totals))                        
                        
                        if partner_amount_total >= 6000 and partner_amount_total <= 20000:
                            ar_qt_pf_sale_customer_type_item = 'silver'
                        elif partner_amount_total > 20000 and partner_amount_total <= 40000:
                            ar_qt_pf_sale_customer_type_item = 'gold'
                        elif partner_amount_total > 40000:
                            ar_qt_pf_sale_customer_type_item = 'diamond'                                                                
                    # update
                    partner_id.ar_qt_pf_frequency_customer_type = ar_qt_pf_frequency_customer_type_item
                    partner_id.ar_qt_pf_sale_customer_type = ar_qt_pf_sale_customer_type_item
