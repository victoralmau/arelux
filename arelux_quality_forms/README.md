El módulo contiene el desarrollo implementar los formularios de calidad e Informes.

## Parámetros de configuración
- maintenance_installation_job_nodriza_manager_user_id
- maintenance_installation_job_logistic_operator_user_id
 
## Informes
Se recomienda cambiar el formato del papel de los reportes a A4 Apaisado (Landscape) para una correcta visualización.

### Mantenimiento de instalaciones
Filtrando por año obtendremos un PDF todos los mantenimientos de instalaciones Hechos por fecha del año completo

### Retirada de residuos
Filtrando por fecha desde y hasta obtendremos un PDF todas las retiradas de residuos realizadas.

### maintenance.installation.need.check
id | name | job
--- | --- | ---
1 | Revision de extintores, todos en su lugar y sin obstaculos y bies | nodriza_manager
2 | Comprobacion de mercancias (Caducidad - Etiquetas - Limpieza - Rotura) | logistic_operator
3 | Comprobacion de orden y limpieza en zonas de almacenaje | logistic_operator
4 | Comprobacion de derrames en toda la nave | logistic_operator
5 | Comprobacion del sistema electronico (alumbrado), comunicar fallos a gerencia | nodriza_manager
6 | Comprobacion del sistema de calefaccion y aire acondicionado | nodriza_manager
7 | Comprobacion limpieza del rotulo exterior | nodriza_manager
8 | Comprobacion de limpieza y fugas de vestuarios y baños | logistic_operator
9 | Delimitacion de zonas y limpieza | logistic_operator
10 | Segregacion y almacenamiento de residuos | logistic_operator
11 | Comprobacion de stock de muestras y etiquetas | logistic_operator
12 | Comprobacion sistema de alumbrado carteleria y horario de los focos y luces automaticas | nodriza_manager
13 | Vehiculos de empresa (inspecciones y revisiones), y mandar al departamento de calidad | logistic_operator
14 | Revision placas del tejado (visualmente por debajo) | nodriza_manager
15 | Puesta en marcha y revision sistema contra incendios | nodriza_manager
16 | Revisar que no exista ningun producto que tenga el etiquetado antiguo, y que ponga el contenido de COVS en su etiqueta | logistic_operator
17 | Revisar que todos los productos tengan su etiqueta, incluso las muestras, y que no quede en el almacen nada absolutamente sin etiquetar | logistic_operator
18 | Revision y actualizacion del horario de la iluminacion exterior | nodriza_manager
19 | Mermas del mes, y comunicacion de las misma al departamento de administracion | logistic_operator
20 | Comprobacion de que no esten colapsados los sumideros de la azotea | nodriza_manager
21 | Comprobacion de que no este colapsado el sistema de alcantarillado de la zona de alrededor de la nave | nodriza_manager
22 | Limpieza y cepillado del cesped de la entrada y del atico | logistic_operator
23 | Revision de las placas transparentes del tejado | nodriza_manager
24 | Revision de si hay o no goteras en cualquier punto de la nave | nodriza_manager
25 | Comprobacion de que todas las lleves estan en orden y actualizadas | nodriza_manager
26 | Comprobacion de los toros y su documentacion | logistic_operator
27 | Revision del estado de cintas metricas y flexometro segun procedimiento P.7.1.02 | logistic_operator
28 | Comprobacion de que las cantidades de producto quimico no superen las maximas establecidas en el APQ | logistic_operator
29 | Comprobacion semanal del agua de las baterias de las 3 carretillas (toros) | logistic_operator

### waste.remove.product
id | name | uom
--- | --- | ---
1 | Papel | Kg
2 | RAEE | Kg
3 | Carton | Kg
4 | Envase | Uds
5 | Tinta | Uds
6 | Pilas | Uds
7 | Fluor | Uds


Se crea un apartado de "Calidad" con los siguientes elementos del menu:

- Retiradas de residuos
- Simulacros
- Mantenimiento de instalaciones
- Configuración
- Decisiones de simulacro
- Acciones a revisar mantenimiento de instalaciones
- Productos retirada de residuos
- Detalle retirada de residuos


## Crones

### Cron Autogenerate Maintenance Installation Next Month
Genera todos los mantenimientos de instalaciones respecto al mes actual

### Cron Autogenerate Maintenance Installation All this year
Genera todos los mantenimientos de instalaciones respecto a todos los meses del año actual
