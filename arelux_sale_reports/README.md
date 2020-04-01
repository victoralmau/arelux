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

<record id="arelux_sale_report_type_data_1" model="arelux.sale.report.type">
<field name="id">1</field>
<field name="name">Ventas (Base Imponible)</field>
<field name="custom_type">sale_order_done_amount_untaxed</field>
<field name="group_by_user">True</field>
</record>
<record id="arelux_sale_report_type_data_2" model="arelux.sale.report.type">
<field name="id">2</field>
<field name="name">Ventas (Cuenta)</field>
<field name="custom_type">sale_order_done_count</field>
<field name="group_by_user">True</field>
</record>
<record id="arelux_sale_report_type_data_3" model="arelux.sale.report.type">
<field name="id">3</field>
<field name="name">Ventas (Ticket medio)</field>
<field name="custom_type">sale_order_ticket_medio</field>
<field name="group_by_user">True</field>
</record>
<record id="arelux_sale_report_type_data_4" model="arelux.sale.report.type">
<field name="id">4</field>
<field name="name">Ptos realizados (Cuenta)</field>
<field name="custom_type">sale_order_sent_count</field>
<field name="group_by_user">True</field>
</record>
<record id="arelux_sale_report_type_data_5" model="arelux.sale.report.type">
<field name="id">5</field>
<field name="name">Muestras enviadas (Cuenta)</field>
<field name="custom_type">sale_order_done_muestras</field>
<field name="group_by_user">True</field>
</record>
<record id="arelux_sale_report_type_data_6" model="arelux.sale.report.type">
<field name="id">6</field>
<field name="name">Ratio muestras</field>
<field name="custom_type">ratio_muestras</field>
<field name="group_by_user">True</field>
</record>
<record id="arelux_sale_report_type_data_7" model="arelux.sale.report.type">
<field name="id">7</field>
<field name="name">Ratio calidad</field>
<field name="custom_type">ratio_calidad</field>
<field name="group_by_user">True</field>
</record>
<record id="arelux_sale_report_type_data_8" model="arelux.sale.report.type">
<field name="id">8</field>
<field name="name">Contactos pontenciales (Cuenta)</field>
<field name="custom_type">res_partner_potencial_count</field>
<field name="group_by_user">True</field>
</record>
<record id="arelux_sale_report_type_data_9" model="arelux.sale.report.type">
<field name="id">9</field>
<field name="name">Cartera Actual activa (Cuenta)</field>
<field name="custom_type">cartera_actual_activa_count</field>
<field name="group_by_user">True</field>
</record>
<record id="arelux_sale_report_type_data_10" model="arelux.sale.report.type">
<field name="id">10</field>
<field name="name">Cartera Actual (Cuenta)</field>
<field name="custom_type">cartera_actual_count</field>
<field name="group_by_user">True</field>
</record>
<record id="arelux_sale_report_type_data_11" model="arelux.sale.report.type">
<field name="id">11</field>
<field name="name">Nuevos clientes con ventas</field>
<field name="custom_type">nuevos_clientes_con_ventas</field>
<field name="group_by_user">False</field>
</record>
<record id="arelux_sale_report_type_data_12" model="arelux.sale.report.type">
<field name="id">12</field>
<field name="name">Salto de linea</field>
<field name="custom_type">line_break</field>
<field name="group_by_user">False</field>
</record>


En el apartado Ventas > Configuración se añade el apartado "Arelux Reporte de ventas" con los siguientes apartados:

- Reportes
- Tipos de reporte
- Plantillas de reporte

## Crones

### Cron generate automatic arelux sale report 
Frecuencia: 1 vez a la semana

Día de la semana: Lunes

Descripción: Revisa todas las plantillas de reportes de ventas activas y se generan los reportes de ventas con las líneas definidas segun la frecuencia establecida que correspondan generarse (si existen reportes anuales, mensuales, etc solo se generaran cuando corresponde si es que previamente no se han definido), se recalcularan todos los datos y se enviará por email el PDF del reporte a todos los seguidores definidos en la plantilla de reporte de ventas