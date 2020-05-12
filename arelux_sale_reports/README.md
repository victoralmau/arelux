El módulo contiene el desarrollo que permite crear y gestionar plantillas de reportes y crear reportes automáticamente en base a ellas.

## Parámetros de configuración
```
arelux_sale_report_mail_template_id
``` 

### arelux.sale.report.template
id | name | active | custom_type | show_in_table_format
--- | --- | --- | --- | ---
1 | TodoCESPED Ventas Online | True | weekly | True
2 | TodoCESPED Ventas Offline | True | weekly | True 

### arelux.sale.report.template.line

id | arelux_sale_report_template_id | arelux_sale_report_type_id | position | ar_qt_activity_type | ar_qt_customer_type | group_by_user | show_in_table_format
--- | --- | --- | --- | --- | --- | --- | ---
1 | 1 | 1 | 1 | todocesped | particular | True | True
2 | 1 | 2 | 2 | todocesped | particular | True | True
3 | 1 | 3 | 3 | todocesped | particular | True | True
4 | 1 | 4 | 4 | todocesped | particular | True | True
5 | 1 | 5 | 5 | todocesped | particular | True | True
6 | 1 | 6 | 6 | todocesped | particular | False | False
7 | 1 | 7 | 7 | todocesped | particular | False | False
8 | 2 | 1 | 1 | todocesped | profesional | True | True
9 | 2 | 2 | 2 | todocesped | profesional | True | True
10 | 2 | 3 | 3 | todocesped | profesional | True | True
11 | 2 | 8 | 4 | todocesped | profesional | True | True
12 | 2 | 9 | 5 | todocesped | profesional | True | True
12 | 2 | 10 | 6 | todocesped | profesional | False | False
13 | 2 | 11 | 7 | todocesped | profesional | False | False
 

### arelux.sale.report.type

id | name | custom_type | group_by_user
--- | --- | --- | ---
1 | Ventas (Base Imponible) | sale_order_done_amount_untaxed | True
2 | Ventas (Cuenta) | sale_order_done_count | True
3 | Ventas (Ticket medio) | sale_order_ticket_medio | True
4 | Ptos realizados (Cuenta) | sale_order_sent_count | True
5 | Muestras enviadas (Cuenta) | sale_order_done_muestras | True
6 | Ratio muestras | ratio_muestras | True
7 | Ratio calidad | ratio_calidad | True
8 | Contactos pontenciales (Cuenta) | res_partner_potencial_count | True
9 | Cartera Actual activa (Cuenta) | cartera_actual_activa_count | True
10 | Cartera Actual (Cuenta) | cartera_actual_count | True
11 | Nuevos clientes con ventas | nuevos_clientes_con_ventas | False
12 | Salto de linea | line_break | False


En el apartado Ventas > Configuración se añade el apartado "Arelux Reporte de ventas" con los siguientes apartados:

- Reportes
- Tipos de reporte
- Plantillas de reporte

## Crones

### Cron generate automatic arelux sale report 
Frecuencia: 1 vez a la semana

Día de la semana: Lunes

Descripción: Revisa todas las plantillas de reportes de ventas activas y se generan los reportes de ventas con las líneas definidas segun la frecuencia establecida que correspondan generarse (si existen reportes anuales, mensuales, etc solo se generaran cuando corresponde si es que previamente no se han definido), se recalcularan todos los datos y se enviará por email el PDF del reporte a todos los seguidores definidos en la plantilla de reporte de ventas
