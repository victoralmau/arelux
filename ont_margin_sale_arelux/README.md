Tomando como referencia el addon ont_margin_sale se realiza lo siguiente (sobrescribiendo) a la función de calcular el coste de cada línea.

El precio de compra (purchase_price) que se define en las líneas de ptos se calcula de la siguiente manera:

Se revisan todas las lineas de pedido y para cada una de ellas se especifica lo siguiente:

is_delivery (es el envio)
purchase_price (precio de compra)
standar_price (precio estándar definido en la ficha de cada producto)

Se buscan todos los AV en estado "hecho" y se recorren todas las líneas
Para cada una de las lineas del AV se revisan los "quant_ids" y de cada uno de ellos se busca si el "valor de inventario" es > 0€
En caso de que se > 0€ se calcula el precio unitario del inventario, para ello (valor de inventario)/cantidad y con este valor unitario se suma al "purchase_price" de ese producto (por si se ha "sacado" de varios quant_ids con precios diferentes)

Una vez realizadas todas las opciones y en caso de que el 'purchase_price' de algún producto sea 0€ se define como 'purchase_price' el 'standar_price' inicial

Calculado ya el 'purchase_price' correcto de todos las líneas de pedido del pto que corresponde, recorremos ahora todas las líneas para calcular el margen del pedido:
Omitimos el producto (277) > Mer4
Definimos el margen por línea de pedido: price_subtotal - (purchase_price * qty_invoiced)
Sumamos el margen de la línea al margen del pedido

* Solo se calcula para los ptos con importe > 0€ y con estado 'Pedido de venta' o 'Bloqueado'
