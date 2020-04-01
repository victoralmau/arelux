# -*- coding: utf-8 -*-
from openerp import _, api, exceptions, fields, models

import logging
_logger = logging.getLogger(__name__)

import psycopg2

class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'
    
    datawarehouse_question_answer_id = fields.Integer(        
        string='Datawarehouse Question Answer Id',
    )
        
    def connect_postgresql_datawarehouse_rds(self):
        try:
            connection = psycopg2.connect(
                user = self.env['ir.config_parameter'].sudo().get_param('survey_arelux_datawarehouse_rds_user'),
                password = self.env['ir.config_parameter'].sudo().get_param('survey_arelux_datawarehouse_rds_password'),
                host = self.env['ir.config_parameter'].sudo().get_param('survey_arelux_datawarehouse_rds_endpoint'),
                port = "5432",
                database = self.env['ir.config_parameter'].sudo().get_param('survey_arelux_datawarehouse_rds_database')
            )
            return {
                'connection': connection,
                'errors': False,
                'error': ''
            }            
        except (psycopg2.Error) as error :
            return {
                'connection': False,
                'errors': True,
                'error': error
            }                                   
    
    @api.multi    
    def cron_survey_user_inputs_send_datawarehouse(self, cr=None, uid=False, context=None):
        #connect_postgresql_datawarehouse_rds
        return_connection = self.connect_postgresql_datawarehouse_rds()
                                                
        if return_connection['errors']==True:
            _logger.info(return_connection['error'])
        else:
            #question_codes        
            question_codes = {
                'ATC.01.GLO.General': {
                    'survey_ids': {
                        '6': {
                            'company': 'Todocesped',
                            'question_id': 12,
                            'label_id': 70
                        },
                        '7': {
                            'company': 'Todocesped',
                            'question_id': 19,
                            'label_id': 117
                        },
                        '8': {
                            'company': 'Arelux',
                            'question_id': 24,
                            'label_id': 149
                        }
                    }
                },
                'CX.01.GLO.Satisfacción': {
                    'survey_ids': {
                        '6': {
                            'company': 'Todocesped',                                
                            'question_id': 12,
                            'label_id': 75
                        },
                        '7': {
                            'company': 'Todocesped',
                            'question_id': 19,
                            'label_id': 122
                        },
                        '8': {
                            'company': 'Arelux',
                            'question_id': 24,
                            'label_id': 154
                        }
                    }
                },
                'PRO.01.GLO.General': {
                    'survey_ids': {
                        '6': {
                            'company': 'Todocesped',
                            'question_id': 12,
                            'label_id': 72
                        },
                        '7': {
                            'company': 'Todocesped',
                            'question_id': 19,
                            'label_id': 119
                        },
                        '8': {
                            'company': 'Arelux',
                            'question_id': 24,
                            'label_id': 151
                        }
                    }
                },
                'CX.02.GLO.NPS': {
                    'survey_ids': {
                        '6': {
                            'company': 'Todocesped',
                            'question_id': 16,
                            'label_id': 0
                        },
                        '7': {
                            'company': 'Todocesped',
                            'question_id': 20,
                            'label_id': 0
                        },
                        '8': {
                            'company': 'Arelux',
                            'question_id': 25,
                            'label_id': 0
                        }
                    }
                }
            }                
            for question_code in question_codes:
                question_code_item = question_codes[question_code]                        
                for survey_id in question_code_item['survey_ids']:
                    survey_id_item = question_code_item['survey_ids'][survey_id]                
                    
                    if survey_id_item['label_id']>0:                                                                    
                        survey_user_input_line_ids = self.env['survey.user_input_line'].search(
                            [                            
                                ('user_input_id.test_entry', '=', False),
                                ('user_input_id.survey_id', '=', int(survey_id)),                
                                ('user_input_id.state', '=', 'done'),
                                ('question_id', '=', int(survey_id_item['question_id'])), 
                                ('datawarehouse_question_answer_id', '=', False),
                                ('value_suggested_row', '=', int(survey_id_item['label_id']))
                             ]
                        )                                                
                    else:                        
                        survey_user_input_line_ids = self.env['survey.user_input_line'].search(
                            [                            
                                ('user_input_id.test_entry', '=', False),
                                ('user_input_id.survey_id', '=', int(survey_id)),                
                                ('user_input_id.state', '=', 'done'),
                                ('question_id', '=', int(survey_id_item['question_id'])), 
                                ('datawarehouse_question_answer_id', '=', False)
                             ]
                        )
                    #result ids                        
                    if len(survey_user_input_line_ids)>0:
                        cursor = return_connection['connection'].cursor()
                        
                        for survey_user_input_line_id in survey_user_input_line_ids:
                            postgres_insert_query = """ INSERT INTO question_answer (company, code, create_date, value, value_int, odoo_survey_id, odoo_survey_question_id, odoo_survey_label_id, odoo_survey_user_input_id, odoo_survey_user_input_line_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning id"""
                            record_to_insert = (
                                survey_id_item['company'], 
                                question_code, 
                                survey_user_input_line_id.user_input_id.date_done, 
                                str(survey_user_input_line_id.value_suggested.value), 
                                int(survey_user_input_line_id.value_suggested.value),
                                survey_user_input_line_id.survey_id.id,
                                survey_user_input_line_id.question_id.id,
                                survey_user_input_line_id.value_suggested_row.id,
                                survey_user_input_line_id.user_input_id.id,
                                survey_user_input_line_id.id
                            )
                            #_logger.info(record_to_insert)
                            cursor.execute(postgres_insert_query, record_to_insert)                                                                              
                            
                            return_connection['connection'].commit()
                            
                            return_id = cursor.fetchone()[0]
                            #_logger.info(return_id)
                            
                            survey_user_input_line_id.datawarehouse_question_answer_id = return_id
            #connect_close
            cursor = return_connection['connection'].cursor()
            cursor.close()
            return_connection['connection'].close()                                