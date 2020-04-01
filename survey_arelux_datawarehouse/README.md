El módulo contiene el desarrollo que permite conectar a RDS de Postgresql (Datawarehouse) con el objetivo de "estandarizar" resultados de encuestas para obtener posteriormente estadísticas globales por empresas.
 
## Parámetros de configuración
```
survey_arelux_datawarehouse_rds_endpoint
survey_arelux_datawarehouse_rds_user
survey_arelux_datawarehouse_rds_password
survey_arelux_datawarehouse_rds_database
``` 

## Cron

Existe un cron definido: Survey User Inputs Send Datawarehouse que se encarga de enviar automáticamente los resultados a DataWarehouse.

Los códigos que se envían a RDS Datawarehouse y el mapeo de encuestas y valores de encuestas son los siguientes:
```
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
```
