Realiza el proceso de creación de contacto, leads, presupuestos y envío de emails automático desde el lead según los formularios que se crean desde los diferentes WP.

## odoo.conf
- aws_access_key_id=xxxx
- aws_secret_key_id=xxxxx
- aws_region_name=eu-west-1
- #arelux_contact_form_submission
- sqs_contact_form_submission_url=https://sqs.eu-west-1.amazonaws.com/381857310472/arelux-odoo_dev-command-contact-form-submission-create

## Crones

### SQS Contact Form Submission 
Frecuencia: 1 vez cada 10 minutos

Descripción: 

Consulta los SQS:

nombre | Entorno
--- | ---
arelux-odoo-command-contact-form-submission-create | Prod
arelux-odoo_dev-command-contact-form-submission-create | Prod


y realiza las operaciones de creación/actualización respecto a los elementos del modelo: contact.form.submission
