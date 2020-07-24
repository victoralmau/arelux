# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
import json

import logging
_logger = logging.getLogger(__name__)

class WeatherHistory(models.Model):
    _name = 'weather.history'
    _description = 'Weather History'
    
    weather_station_uuid = fields.Char(
        string='Weather Station Uuid'
    )
    date_from = fields.Date(
        string='Date From'
    )
    date_to = fields.Date(
        string='Date to'
    )

    def station_uuids(self):
        return [
            '080210-99999', '083905-99999', '084170-99999', '084490-13025', '084330-99999', '082200-99999', '080870-99999', '080530-99999', '080140-99999', '600100-99999', '083590-99999', '080143-99999',
            '083910-99999', '082100-99999', '080150-99999', '082190-99999', '083840-99999', '081120-99999', '080940-99999', '080110-99999', '603380-99999', '081480-99999', '084900-99999', '082020-99999',
            '083600-99999', '080850-99999', '082270-99999', '082010-99999', '082130-99999', '081840-99999', '082260-99999', '084510-99999', '082220-99999', '080080-99999', '600050-99999', '081710-99999',
            '082150-99999', '082230-99999', '084100-99999', '084200-99999', '082350-99999', '081400-99999', '080450-99999', '081410-99999', '084515-99999', '080270-99999', '080750-99999', '083970-99999',
            '084580-99999', '600180-99999', '083650-99999', '080010-99999', '600350-99999', '081810-99999', '080720-99999', '600070-99999', '080550-99999', '080480-99999', '600250-99999', '082800-99999',
            '600010-99999', '080290-99999', '081860-99999', '080250-99999', '080430-99999', '083060-99999', '081600-99999', '084820-99999', '082860-99999', '082240-99999', '084520-99999', '082320-99999',
            '080420-99999', '084290-99999', '082310-99999', '081570-99999', '080840-99999', '080800-99999', '083350-99999', '084300-99999', '600400-99999', '084190-99999', '084530-99999', '080910-99999',
            '080230-99999', '082210-99999', '083300-99999', '080020-99999', '083830-99999', '080440-99999', '082380-99999', '600300-99999', '084870-99999', '081170-99999', '081300-99999', '081800-99999',
            '082330-99999', '083140-99999', '084840-99999', '082720-99999', '082820-99999', '082840-99999', '083480-99999', '081763-99999', '082610-99999', '084880-99999', '083030-99999', '082850-99999',
            '081750-99999', '600150-99999', '600200-99999', '603200-99999', '083010-99999', '080144-99999', '083730-99999', '082900-99999'
        ]
    
    @api.model    
    def cron_weather_station_history_previous_month(self):
        # define
        current_date = datetime.today()
        date_from = current_date + relativedelta(months=-1, day=1)
        date_to = datetime(date_from.year, date_from.month, 1) + relativedelta(months=1, days=-1)
        
        for station_uuid in self.station_uuids():
            message = {
                "pathParameters": {
                    "uuid": str(station_uuid)
                },
                "queryStringParameters": {
                    "date_to": str(date_to.strftime("%Y-%m-%d")),
                    "date_from": str(date_from.strftime("%Y-%m-%d"))
                }
            }
            _logger.info(message)
            # sns_send
            response = self.action_weather_sns_send(message)
            if not response['send']:
                _logger.info(response['error'])
        
    @api.model    
    def cron_weather_station_history_all_years(self):
        years = [2015,2016,2017,2018,2019]
        months = ['01','02','03','04','05','06','07','08','09','10','11','12']
        for station_uuid in self.station_uuids():
            for year in years:
                for month in months:
                    # define
                    date_from = '%s-%s-01' % (year, month)
                    date_to = datetime(int(year), int(month), 1) + relativedelta(months=1, days=-1)
                    date_to = date_to.strftime("%Y-%m-%d")
                    message = {
                        "pathParameters": {
                            "uuid": str(station_uuid)
                        },
                        "queryStringParameters": {
                            "date_to": str(date_to),
                            "date_from": str(date_from)
                        }
                    }
                    _logger.info(message)
                    # sns_send
                    response = self.action_weather_sns_send(message)
                    if not response['send']:
                        _logger.info(response['error'])                                                                                           