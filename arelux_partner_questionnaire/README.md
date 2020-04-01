El módulo contiene el desarrollo para implementar funcionalidades relacionadas especialmente con el contacto, con el objetivo de segmentarlo mucho mejor.

Se introducen los siguientes datos por defecto en la instalación:

### res.partner.contact.form
nombre | name | filter_company | filter_ar_qt_customer_type | position | other
--- | --- | --- | --- | --- | ---
1 | Búsqueda activa de nuevos clientes | all | profesional | 0 | False
2 | Buzoneo | all | all | 1 | False
3 | Formulario web | all | all | 2 | False
4 | Llamada | all | all | 3 | False
5 | Whatsapp | all | all | 4 | False
6 | Visita a la nave | all | all | 5 | False
7 | Otro | all | all | 7 | True
8 | Redes sociales | all | all | 6 | False

### res.partner.qualification.product

<record id="res_partner_qualifiction_product_data_1" model="res.partner.qualification.product">
<field name="id">1</field>
<field name="name">Impermeabilizantes</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">0</field>
<field name="other">False</field>
</record>
<record id="res_partner_qualifiction_product_data_2" model="res.partner.qualification.product">
<field name="id">2</field>
<field name="name">Pinturas térmicas</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">1</field>
<field name="other">False</field>
</record>
<record id="res_partner_qualifiction_product_data_3" model="res.partner.qualification.product">
<field name="id">3</field>
<field name="name">Aislantes reflexivos</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">2</field>
<field name="other">False</field>
</record>
<record id="res_partner_qualifiction_product_data_4" model="res.partner.qualification.product">
<field name="id">4</field>
<field name="name">Tratamiento de superficies</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">3</field>
<field name="other">False</field>
</record>
<record id="res_partner_qualifiction_product_data_5" model="res.partner.qualification.product">
<field name="id">5</field>
<field name="name">Otro</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">4</field>
<field name="other">True</field>
</record>
 

res.partner.reason.buy

<record id="res_partner_reason_buy_1" model="res.partner.reason.buy">
<field name="id">1</field>
<field name="name">Prevención / Anticiparse a los problemas (humedades, filtraciones)</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">0</field>
<field name="other">False</field>
</record>
<record id="res_partner_reason_buy_2" model="res.partner.reason.buy">
<field name="id">2</field>
<field name="name">Problema puntual (filtraciones, humedades, etc).</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">1</field>
<field name="other">False</field>
</record>
<record id="res_partner_reason_buy_3" model="res.partner.reason.buy">
<field name="id">3</field>
<field name="name">Reforma o rehabilitación</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">2</field>
<field name="other">False</field>
</record>
<record id="res_partner_reason_buy_4" model="res.partner.reason.buy">
<field name="id">4</field>
<field name="name">Otro</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">3</field>
<field name="other">True</field>
</record>
 

res.partner.reason.install

<record id="res_partner_reason_install_data_1" model="res.partner.reason.install">
<field name="id">1</field>
<field name="name">Ahorra tiempo (regar, cortar, etc.)</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">0</field>
<field name="other">False</field>
</record>
<record id="res_partner_reason_install_data_2" model="res.partner.reason.install">
<field name="id">2</field>
<field name="name">Ahorra dinero / agua</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">1</field>
<field name="other">False</field>
</record>
<record id="res_partner_reason_install_data_3" model="res.partner.reason.install">
<field name="id">3</field>
<field name="name">Decoración</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">2</field>
<field name="other">False</field>
</record>
<record id="res_partner_reason_install_data_4" model="res.partner.reason.install">
<field name="id">4</field>
<field name="name">Seguridad (niños, zonas de juegos, etc)</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">3</field>
<field name="other">False</field>
</record>
<record id="res_partner_reason_install_data_5" model="res.partner.reason.install">
<field name="id">5</field>
<field name="name">Otro</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">4</field>
<field name="other">True</field>
</record>
 

res.partner.specific.segment

<record id="res_partner_specific_segment_data_1" model="res.partner.specific.segment">
<field name="id">1</field>
<field name="name">Comunidad de vecinos</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">0</field>
<field name="other">False</field>
</record>
<record id="res_partner_specific_segment_data_2" model="res.partner.specific.segment">
<field name="id">2</field>
<field name="name">Decoración</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">1</field>
<field name="other">False</field>
</record>
<record id="res_partner_specific_segment_data_3" model="res.partner.specific.segment">
<field name="id">3</field>
<field name="name">Mascota</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">2</field>
<field name="other">False</field>
</record>
<record id="res_partner_specific_segment_data_4" model="res.partner.specific.segment">
<field name="id">4</field>
<field name="name">Niños</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">3</field>
<field name="other">False</field>
</record>
<record id="res_partner_specific_segment_data_5" model="res.partner.specific.segment">
<field name="id">5</field>
<field name="name">Piscina (de obra, hinchable, agua salada...)</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">4</field>
<field name="other">False</field>
</record>
<record id="res_partner_specific_segment_data_6" model="res.partner.specific.segment">
<field name="id">6</field>
<field name="name">Otro</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">5</field>
<field name="other">True</field>
</record>
 

res.partner.stock.capacity

<record id="res_partner_stock_capacity_data_1" model="res.partner.stock.capacity">
<field name="id">1</field>
<field name="name">Tiene almacen (espacio)</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">0</field>
<field name="other">False</field>
</record>
<record id="res_partner_stock_capacity_data_2" model="res.partner.stock.capacity">
<field name="id">2</field>
<field name="name">Tiene capacidad finaciera (liquidez)</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">1</field>
<field name="other">False</field>
</record>
<record id="res_partner_stock_capacity_data_3" model="res.partner.stock.capacity">
<field name="id">3</field>
<field name="name">No</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">2</field>
<field name="other">False</field>
</record>
 

res.partner.type.customer.sale

<record id="res_partner_type_customer_sale_data_1" model="res.partner.type.customer.sale">
<field name="id">1</field>
<field name="name">Profesionales</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">all</field>
<field name="position">0</field>
<field name="other">False</field>
</record>
<record id="res_partner_type_customer_sale_data_2" model="res.partner.type.customer.sale">
<field name="id">2</field>
<field name="name">Particulares</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">all</field>
<field name="position">1</field>
<field name="other">False</field>
</record>
<record id="res_partner_type_customer_sale_data_3" model="res.partner.type.customer.sale">
<field name="id">3</field>
<field name="name">No vende</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">all</field>
<field name="position">2</field>
<field name="other">False</field>
</record>
 

res.partner.type.surface

<record id="res_partner_type_surface_data_1" model="res.partner.type.surface">
<field name="id">1</field>
<field name="name">Tierra</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">1</field>
<field name="other">False</field>
</record>
<record id="res_partner_type_surface_data_5" model="res.partner.type.surface">
<field name="id">5</field>
<field name="name">Cesped natural</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">2</field>
<field name="other">False</field>
</record>
<record id="res_partner_type_surface_data_2" model="res.partner.type.surface">
<field name="id">2</field>
<field name="name">Hormigón / Cemento</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">3</field>
<field name="other">False</field>
</record>
<record id="res_partner_type_surface_data_3" model="res.partner.type.surface">
<field name="id">3</field>
<field name="name">Baldosa</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">4</field>
<field name="other">False</field>
</record>
<record id="res_partner_type_surface_data_4" model="res.partner.type.surface">
<field name="id">4</field>
<field name="name">Otro</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">5</field>
<field name="other">True</field>
</record>
 

res.partner.valuation.thing

<record id="res_partner_valuation_thing_data_1" model="res.partner.valuation.thing">
<field name="id">1</field>
<field name="name">Calidad (ensayos, certificados, propiedades)</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">all</field>
<field name="position">0</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_2" model="res.partner.valuation.thing">
<field name="id">2</field>
<field name="name">Calidad - Precio</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">all</field>
<field name="position">1</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_3" model="res.partner.valuation.thing">
<field name="id">3</field>
<field name="name">Precio</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">all</field>
<field name="position">2</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_4" model="res.partner.valuation.thing">
<field name="id">4</field>
<field name="name">Servicio (muestras, rapidez, entrega, instalacion, asesoramiento...)</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">3</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_5" model="res.partner.valuation.thing">
<field name="id">5</field>
<field name="name">Valores de Empresa: RSC</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">4</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_6" model="res.partner.valuation.thing">
<field name="id">6</field>
<field name="name">Tiempo de entrega</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">5</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_7" model="res.partner.valuation.thing">
<field name="id">7</field>
<field name="name">Ensayos y certificaciones</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">6</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_8" model="res.partner.valuation.thing">
<field name="id">8</field>
<field name="name">Asesoramiento y anteción recibidos</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">7</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_9" model="res.partner.valuation.thing">
<field name="id">9</field>
<field name="name">Envío de clientes</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">8</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_10" model="res.partner.valuation.thing">
<field name="id">10</field>
<field name="name">Corte a medida</field>
<field name="filter_company">todocesped</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">9</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_11" model="res.partner.valuation.thing">
<field name="id">11</field>
<field name="name">Servicio (muestras, rapidez entrega, instalación, asesoramiento...)</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">particular</field>
<field name="position">10</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_12" model="res.partner.valuation.thing">
<field name="id">12</field>
<field name="name">Valores de Empresa: RSC</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">11</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_13" model="res.partner.valuation.thing">
<field name="id">13</field>
<field name="name">Personalización de productos (etiquetas, envases)</field>
<field name="filter_company">arelux</field>
<field name="filter_ar_qt_customer_type">profesional</field>
<field name="position">12</field>
<field name="other">False</field>
</record>
<record id="res_partner_valuation_thing_data_14" model="res.partner.valuation.thing">
<field name="id">14</field>
<field name="name">Otro</field>
<field name="filter_company">all</field>
<field name="filter_ar_qt_customer_type">all</field>
<field name="position">13</field>
<field name="other">True</field>
</record>
 

En el apartado Configuración > Técnico se añade el apartado "Arelux Partner Questionnaire" con los siguientes apartados:

- Tipos de superficie
- Razones instalacion
- Segmentos especificos
- Capacidad stock
- Tipo clientes venden
- Formas de contacto
- Cosas a valorar
- Qualification Product
- Razones compra

## Cron

### Arelux - Generar tipo cliente
Frecuencia: 1 vez al mes

Fecha: 01/xx/xxxx

Descripción: Respecto a todos los ptos > 0€ en estado "Pedido de venta" o "Bloqueado" de todos los clientes activos y de pedidos confirmados en los últimos 12 meses re-define los siguientes campos del cliente:

Tipo de cliente (frecuencia)*:

- 0 (Cliente sin ventas)
- >=1 y <=2 (Cliente puntual)
- >2 y <=5 (Cliente fidelizado)
- >=6 (Cliente recurrente)

Tipo de cliente (ventas importe)*:

- <6000 (Cliente bronce)
- >=6000 y <=20000 (Cliente plata)
- >20000 y <=40000 (Cliente oro)
- >40000 (Cliente diamante)

*Todos los datos se analizan respecto a las ventas en número (count) o importe (sum BI)

Existe un cron definido: Arelux - Generar tipo cliente que se encarga de auto-definir el tipo de cliente según las ventas + Leads - Generar ar_qt_todocesped_pf_customer_type 

### Leads - Generar ar_qt_todocesped_pf_customer_type
Frecuencia: 1 vez al día (laborable)

Descripción: Regenera el campo ar_qt_todocesped_pf_customer_type respecto al modelo crm.lead según el contacto (res.partner) correspondiente.
