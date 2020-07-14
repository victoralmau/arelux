El módulo contiene el desarrollo que permite implementar cosas respecto a Res

## Crones

### Res partner fix customer
Frecuencia: 1 vez al día

Descripción: 

Se define como customer=True todos los contactos que corresponden segun los filtros:
Contactos de tipo 'contacto' activos que estén definidos como customer=False y tengan un lead asociado o un pto asociado

Motivo: Este cron se realiza por si se "quita" el check de cliente a contactos de los cuales NO se debería quitar el check
