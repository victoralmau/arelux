# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models, tools
from dateutil.relativedelta import relativedelta
from datetime import datetime
import json
import requests

import logging
_logger = logging.getLogger(__name__)

class ResCityZip(models.Model):
    _inherit = 'res.city.zip'
    
    weather_station_uuid = fields.Char(
        string='Weather Station Uuid'
    )
        
    def api_call_postal_code(self, country_code, postal_code):
        return_response = {
            'statusCode': 500,
            'body': '',
        }
        headers = {
            'x-api-key': str(tools.config.get('weather_api_x_api_key'))
        }         
        
        url = str(tools.config.get('weather_api_endpoint'))
        uuid = str(country_code)+'-'+str(postal_code)
        url += 'weather/postal_code/'+str(uuid) 
        response = requests.get(url, headers=headers)
        if response.status_code!=200:        
            return_response['statusCode'] = response.status_code
            if response.status_code!=204:
                return_response['body'] =  response.json()        
        else:
            return_response['statusCode'] = 200
            return_response['body'] =  response.json()
            
        return return_response
    
    def api_call_weather_history(self, weather_station_uuid, date_from, date_to):
        return_response = {
            'statusCode': 500,
            'body': '',
        }
        headers = {
            'x-api-key': str(tools.config.get('weather_api_x_api_key'))
        } 
        url = str(tools.config.get('weather_api_endpoint'))
        url += 'weather/station/'+str(weather_station_uuid)+'/history?date_from='+str(date_from)+'&date_to='+str(date_to)
        _logger.info(url) 
        response = requests.get(url, headers=headers)
        if response.status_code!=200:        
            return_response['statusCode'] = response.status_code
            if response.status_code!=204:
                return_response['body'] =  response.json()        
        else:
            return_response['statusCode'] = 200
            return_response['body'] =  response.json()
            
        return return_response                                               
    
    @api.model    
    def cron_set_all_weather_stations(self):
        country_codes = ['ES', 'AD', 'GB', 'FR']
        for country_code in country_codes:
            res_city_zip_ids = self.env['res.city.zip'].search(
                [
                    ('city_id.country_id.code', '=', country_code),
                    ('weather_station_uuid', '=', False)                                
                 ], limit=1000
            )
            if len(res_city_zip_ids)>0:
                weather_station_uuids = {}
                                                        
                for res_city_zip_id in res_city_zip_ids:
                    zip_item = str(res_city_zip_id.name)                 
                    _logger.info(zip_item)
                    #api_call
                    if zip_item not in weather_station_uuids:
                        response = self.api_call_postal_code(country_code, zip_item)
                        if response['statusCode']!=200:
                            _logger.info(response)
                        else:
                            if 'weather_station_uuid' in response['body']:
                                if response['body']['weather_station_uuid']!='0':
                                    weather_station_uuids[zip_item] = str(response['body']['weather_station_uuid'])
                    #update
                    if zip_item in weather_station_uuids:
                        weather_station_uuid_item = str(weather_station_uuids[zip_item])
                        res_city_zip_id.weather_station_uuid = weather_station_uuid_item                                                        
    
    def get_weather_station_uuids(self, country_code):
        weather_station_uuids = []
        res_city_zip_ids = self.env['res.city.zip'].search(
            [
                ('city_id.country_id.code', '=', country_code),
                ('weather_station_uuid', '!=', False)
            ]
        )
        if len(res_city_zip_ids)>0:
            for res_city_zip_id in res_city_zip_ids:
                weather_station_uuid = str(res_city_zip_id.weather_station_uuid)
                if weather_station_uuid not in weather_station_uuids:
                    weather_station_uuids.append(weather_station_uuid)
                    
        return weather_station_uuids
    
    @api.model    
    def cron_weather_station_history_previous_month(self):        
        #define
        current_date = datetime.today()
        date_from = current_date + relativedelta(months=-1, day=1)
        date_to = datetime(date_from.year, date_from.month, 1) + relativedelta(months=1, days=-1)
        #define strftime
        date_from = date_from.strftime("%Y-%m-%d")
        date_to = date_to.strftime("%Y-%m-%d")
        #all
        country_codes = ['ES']
        for country_code in country_codes:
            weather_station_uuids = self.get_weather_station_uuids(country_code)
            _logger.info(len(weather_station_uuids))
            if len(weather_station_uuids)>0:
                for weather_station_uuid in weather_station_uuids:
                    #get_all_items and sort
                    weather_history_items = []
                    weather_history_ids = self.env['weather.history'].search([('weather_station_uuid', '=', str(weather_station_uuid))])
                    if len(weather_history_ids)>0:
                        for weather_history_id in weather_history_ids:
                            new_key = str(weather_history_id.date_from)+'-'+str(weather_history_id.date_to)
                            weather_history_items.append(new_key)
                    #api_call
                    new_key = str(date_from)+'-'+str(date_to)                                        
                    if new_key not in weather_history_items:
                        response = self.api_call_weather_history(weather_station_uuid, date_from, date_to)
                        if response['statusCode']!=200:
                            _logger.info(response)
                        if response['statusCode']==200:
                            #save_weather_history
                            weather_history_vals = {                    
                                'weather_station_uuid': weather_station_uuid,
                                'date_from': date_from,
                                'date_to': date_to                                                                                                                                                                                           
                            }
                            weather_history_obj = self.env['weather.history'].sudo().create(weather_history_vals)            
        
    @api.model    
    def cron_weather_station_history_all_years(self):
        #define
        years = [2015,2016,2017,2018,2019]
        months = ['01','02','03','04','05','06','07','08','09','10','11','12']
        #all
        country_codes = ['ES']
        for country_code in country_codes:
            weather_station_uuids = self.get_weather_station_uuids(country_code)
            if len(weather_station_uuids)>0:
                for weather_station_uuid in weather_station_uuids:
                    #get_all_items and sort
                    weather_history_items = []
                    weather_history_ids = self.env['weather.history'].search([('weather_station_uuid', '=', weather_station_uuid)])
                    if len(weather_history_ids)>0:
                        for weather_history_id in weather_history_ids:
                            new_key = str(weather_history_id.date_from)+'-'+str(weather_history_id.date_to)
                            weather_history_items.append(new_key)
                    #all_years
                    for year in years:
                        for month in months:
                            #define                
                            date_from = str(year)+'-'+str(month)+'-01'
                            date_to = datetime(int(year), int(month), 1) + relativedelta(months=1, days=-1)
                            date_to = date_to.strftime("%Y-%m-%d")
                            #define strftime
                            date_from = date_from.strftime("%Y-%m-%d")
                            date_to = date_to.strftime("%Y-%m-%d")                    
                            #api_call
                            new_key = str(date_from)+'-'+str(date_to)
                            if new_key not in weather_history_items:
                                response = self.api_call_weather_history(weather_station_uuid, date_from, date_to)
                                if response['statusCode']==200:
                                    #save_weather_history
                                    weather_history_vals = {                    
                                        'weather_station_uuid': weather_station_uuid,
                                        'date_from': date_from,
                                        'date_to': date_to                                                                                                                                                                                           
                                    }
                                    weather_history_obj = self.env['weather.history'].sudo().create(weather_history_vals)                                                                                                               