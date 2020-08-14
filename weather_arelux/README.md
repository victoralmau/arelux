El módulo implementa cosas respecto al "servicio del tiempo"

## odoo.conf
- aws_access_key_id=xxxx
- aws_secret_key_id=xxxx
- aws_region_name=eu-west-1
- weather_api_endpoint=https://api.grupoarelux.com/prod/
- weather_api_x_api_key=xxxxx

## Crones

### Cron Weather Station History Previous month 
Frecuencia: 1 vez cada mes (Día 7)

Descripción: Envía al SNS correspondiente de Weather para todas las estaciones respecto al mes completo anterior.

### Cron Weather Station History all years 
Frecuencia: Personalizado

Descripción: Envía al SNS correspondiente de Weather para todas las estaciones respecto a todos los meses de los años: 2015,2016,2017,2018 y 2019

