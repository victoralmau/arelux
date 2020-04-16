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
7 | Otro | all | all | 8 | True
8 | Redes sociales | all | all | 6 | False
9 | Tienda online | all | all | 7 | False

### res.partner.qualification.product
nombre | name | filter_company | filter_ar_qt_customer_type | position | other
--- | --- | --- | --- | --- | ---
1 | Impermeabilizantes | arelux | particular | 0 | False
2 | Pinturas térmicas | arelux | particular | 1 | False
3 | Aislantes reflexivos | arelux | particular | 2 | False
4 | Tratamiento de superficies | arelux | particular | 3 | False
5 | Otro | arelux | particular | 4 | True

### res.partner.reason.buy
nombre | name | filter_company | filter_ar_qt_customer_type | position | other
--- | --- | --- | --- | --- | ---
1 | Prevención / Anticiparse a los problemas (humedades, filtraciones) | arelux | profesional | 0 | False
2 | Problema puntual (filtraciones, humedades, etc) | arelux | profesional | 1 | False
3 | Reforma o rehabilitación | arelux | profesional | 2 | False
4 | Otro | arelux | profesional | 3 | False

### res.partner.reason.install
nombre | name | filter_company | filter_ar_qt_customer_type | position | other
--- | --- | --- | --- | --- | ---
1 | Ahorra tiempo (regar, cortar, etc.) | todocesped | particular | 0 | False
2 | Ahorra dinero / agua | todocesped | particular | 1 | False
3 | Decoración | todocesped | particular | 2 | False
4 | Seguridad (niños, zonas de juegos, etc) | todocesped | particular | 3 | False
5 | Otro | todocesped | particular | 4 | True

### res.partner.specific.segment
nombre | name | filter_company | filter_ar_qt_customer_type | position | other
--- | --- | --- | --- | --- | ---
1 | Comunidad de vecinos | todocesped | particular | 0 | False
2 | Decoración | todocesped | particular | 1 | False
3 | Mascota | todocesped | particular | 2 | False
4 | Niños | todocesped | particular | 3 | False
5 | Piscina (de obra, hinchable, agua salada...) | todocesped | particular | 4 | False
6 | Otro | todocesped | particular | 5 | True

### res.partner.stock.capacity
nombre | name | filter_company | filter_ar_qt_customer_type | position | other
--- | --- | --- | --- | --- | ---
1 | Tiene almacen (espacio) | all | profesional | 0 | False
2 | Tiene capacidad finaciera (liquidez) | all | profesional | 1 | False
3 | No | all | profesional | 2 | False

### res.partner.type.customer.sale
nombre | name | filter_company | filter_ar_qt_customer_type | position | other
--- | --- | --- | --- | --- | ---
1 | Profesionales | all | all | 0 | False
2 | Particulares | all | all | 1 | False
3 | No vende | all | all | 2 | False

### res.partner.type.surface
nombre | name | filter_company | filter_ar_qt_customer_type | position | other
--- | --- | --- | --- | --- | ---
1 | Tierra | todocesped | particular | 1 | False
2 | Hormigón / Cemento | todocesped | particular | 3 | False
3 | Baldosa | todocesped | particular | 4 | False
4 | Otro | todocesped | particular | 5 | True
5 | Cesped natural | todocesped | particular | 2 | False

### res.partner.valuation.thing
nombre | name | filter_company | filter_ar_qt_customer_type | position | other
--- | --- | --- | --- | --- | ---
1 | Calidad (ensayos, certificados, propiedades) | all | all | 0 | False
2 | Calidad - Precio | all | all | 1 | False
3 | Precio | all | all | 2 | False
4 | Servicio (muestras, rapidez, entrega, instalacion, asesoramiento...) | all | all | 3 | False
5 | Valores de Empresa: RSC | all | all | 4 | False
6 | Tiempo de entrega | all | profesional | 5 | False
7 | Ensayos y certificaciones | all | profesional | 6 | False
8 | Asesoramiento y anteción recibidos | all | profesional | 7 | False
9 | Envío de clientes | all | profesional | 8 | False
10 | Corte a medida | all | profesional | 9 | False
11 | Servicio (muestras, rapidez entrega, instalación, asesoramiento...) | all | profesional | 10 | False
12 | Valores de Empresa: RSC | all | profesional | 11 | False
13 | Personalización de productos (etiquetas, envases) | all | profesional | 12 | False
14 | Otro | all | profesional | 13 | True
 

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
