Se modificand las siguientes vistas

### [report_arelux] external_layout_header
Original > https://github.com/odoo/odoo/blob/10.0/addons/report/views/layout_templates.xml#L95

#### Original
```
<?xml version="1.0"?>
<t t-name="report.external_layout_header">
    <div class="header">
        <div class="row">
            <div class="col-xs-3">
                <img t-if="company.logo" t-att-src="'data:image/png;base64,%s' % company.logo" style="max-height: 45px;"/>
            </div>
            <div class="col-xs-9 text-right" style="margin-top:20px;" t-field="company.rml_header1"/>
        </div>
        <div class="row zero_min_height">
            <div class="col-xs-12">
                <div style="border-bottom: 1px solid black;"/>
            </div>
        </div>
        <div class="row">
            <div class="col-xs-6" name="company_address">
                <span t-field="company.partner_id" t-field-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;], &quot;no_marker&quot;: true}" style="border-bottom: 1px solid black; display:inline-block;"/>
            </div>
        </div>
    </div>
</t>
```

#### Modificado
```
<?xml version="1.0"?>
<t t-name="report.external_layout_header">
    <div class="header">
        <div class="row">
            <t t-set="ar_qt_activity_type_global" t-value="arelux" ></t>                    
            <t t-if="ar_qt_activity_type_global=='arelux'">                
                <t t-set="custom_color_1" t-value="'#195660'" />
            </t>
            <t t-else="">
                <t t-set="custom_color_1" t-value="'#12575E'" />
            </t>
            <div class='title_bar' t-att-style="'background:'+custom_color_1+';width:100%;height:20px;margin-bottom:10px;'"></div>
            <t t-if="doc_model!='purchase.order'">
                <t t-if="o and 'ar_qt_activity_type' in o">
                    <t t-set="ar_qt_activity_type_global" t-value="o.ar_qt_activity_type"></t>
                </t>                    
                <t t-elif="o and 'partner_id' in o">                                        
                    <t t-set="ar_qt_activity_type_global" t-value="o.partner_id.ar_qt_activity_type"></t>
                </t>
                <t t-if="ar_qt_activity_type_global=='arelux'">                
                    <t t-set="custom_color_1" t-value="'#195660'" />
                </t>
                <t t-else="">
                    <t t-set="custom_color_1" t-value="'#12575E'" />
                </t>
                <div class="col-xs-4">
                     <t t-if="ar_qt_activity_type_global=='todocesped'">
                        <img src="/account_arelux/static/src/img/todocesped_vector.png" style="height: 40px;" />
                    </t>
                    <t t-elif="ar_qt_activity_type_global=='evert'">
                        <img src="/account_arelux/static/src/img/logo_evert.png" style="height: 40px;" />
                    </t>
                    <t t-elif="ar_qt_activity_type_global=='arelux'">
                        <img src="/account_arelux/static/src/img/arelux_top_chemicals.png" style="height: 40px;" />
                    </t>
                    <t t-else="">
                        <img src="/account_arelux/static/src/img/todocesped_vector.png" style="height: 40px;" />
                    </t>
                    <div class='company_data' style="line-height: 15px;font-size: 13px;margin-top: 10px;">
                        <p t-field="company.partner_id.name" style="margin-bottom:0px;" />
                        <p t-field="company.partner_id.vat" style="margin-bottom:0px;" />
                        <p t-field="company.partner_id.street" style="margin-bottom:0px;" />
                        <p style="margin-bottom: 0px;"><span t-field="company.partner_id.zip" /> <span t-field="company.partner_id.city" /></p>
                        <p style="margin-bottom: 0px;">(<span t-field="company.partner_id.state_id" />) <span t-field="company.partner_id.country_id" /></p>
                    </div>
                </div>
                <div class="col-xs-5 col-xs-offset-3" style="text-align:center;">
                    <img src="/account_arelux/static/src/img/arelux_logo.png" style="height:60px;margin-top: 10px;" /><br/>
                    <img src="/account_arelux/static/src/img/logos_empresas_grises.png" style="width: 70%;margin-top: 30px;" />
                </div>
            </t>
            <t t-else="">
                <div class="col-xs-4">
                    <img src="/account_arelux/static/src/img/grupo_arelux.png" style="height: 70px;" /><br/>
                    <img src="/account_arelux/static/src/img/logos_empresas_grises.png" style="width: 100%;margin-top: 20px;" />
                </div>
                <div class="col-xs-5 col-xs-offset-3"></div>
            </t>
        </div>
    </div>
</t>
```

### [report_arelux] external_layout_footer
Original > https://github.com/odoo/odoo/blob/10.0/addons/report/views/layout_templates.xml#L118

#### Original
```
<?xml version="1.0"?>
<t t-name="report.external_layout_footer">
    <div class="footer">
        <div class="text-center" style="border-top: 1px solid black;">
            <ul t-if="not company.custom_footer" class="list-inline">
                <t t-set="company" t-value="company.sudo()"/>
                <li t-if="company.phone">Phone: <span t-field="company.phone"/></li>

                <li t-if="company.fax and company.phone">&amp;bull;</li>
                <li t-if="company.fax">Fax: <span t-field="company.fax"/></li>

                <li t-if="company.email and company.fax or company.email and company.phone">&amp;bull;</li>
                <li t-if="company.email">Email: <span t-field="company.email"/></li>

                <li t-if="company.website and company.email or company.website and company.fax or company.website and company.phone">&amp;bull;</li>
                <li t-if="company.website">Website: <span t-field="company.website"/></li>
            </ul>

            <ul t-if="not company.custom_footer" class="list-inline" name="financial_infos">
                <li t-if="company.vat">TIN: <span t-field="company.vat"/></li>
                <li stle="font-size:9px">Inscrita en el Registro Mercantil de Zaragoza al Tomo 4163, Folio 182, Sección 8, Hoja Z-59796</li>
            </ul>

            <t t-if="company.custom_footer">
                <span t-raw="company.rml_footer"/>
            </t>

            <ul class="list-inline">
                <li>Page:</li>
                <li><span class="page"/></li>
                <li>/</li>
                <li><span class="topage"/></li>
            </ul>
        </div>
    </div>      
</t>
```

#### Modificado
```
<?xml version="1.0"?>
<t t-name="report.external_layout_footer">
    <div class="footer" style="margin-top: 10px;">
        <t t-if="o and 'pack_operation_ids' in o">
            <p style="font-size:10px;">Según RD 728/1998 establece el artículo 18 punto 1 que "El responsable de la entrega del residuo de envase usado para su correcta gestión medioambiental, será el poseedor final". Rogamos se gestionen según normativa vigente Condiciones de venga en www.grupoarelux.com/condiciones-generales-venta/</p>
        </t>
        <t t-if="doc_model=='sale.order'">
            <p style="font-size:10px;font-weight:bold">Te recordamos que el precio de la instalación no está incluido en el presente presupuesto</p>
            <t t-if="o.partner_id.ar_qt_customer_type=='particular'">
                <p style="font-size:10px;">Portes incluidos en entregas a pie de calle.</p>
            </t>
        </t>
        <p style="font-size:10px;">Sus datos son tratados por ARELUX, S.L. para presentarle los servicios solicitados y su facturación, estando legitimados por un contrato. No se cederán datos a terceros, salvo obligación legal. Puedes ejercer sus derechos y solicitar la información completa contactando con info@arelux.com</p>
        <div class="row" style="margin-bottom:10px;">
            <div class="col-xs-3">
                <p style="line-height: 50px;font-weight: bold;color: #e7ad36;font-size: 20px;">Calidad global</p>
            </div>
            <div class="col-xs-8 col-xs-offset-1">
                <t t-if="doc_model=='account.invoice'">
                    <img src="/account_arelux/static/src/img/cesce_mini.jpg" style="height:80px;" />
                </t>
                <img src="/account_arelux/static/src/img/sello_rsa_2017.png" style="height:50px;margin-right: 30px;" />
                <img src="/account_arelux/static/src/img/iso_9001_2015.png" style="height:50px;margin-right: 30px;" />
                <img src="/account_arelux/static/src/img/conformite_europeenn.svg.png" style="height:50px;margin-right: 30px;" />
                <img src="/account_arelux/static/src/img/eco_friendly.png" style="height:50px;" />
            </div>
        </div>
        <div class="row">
            <t t-set="ar_qt_activity_type_global" t-value="arelux" ></t>                    
            <t t-if="o and 'ar_qt_activity_type' in o">
                <t t-set="ar_qt_activity_type_global" t-value="o.ar_qt_activity_type"></t>
            </t>                    
            <t t-elif="o and 'partner_id' in o">                                        
                <t t-set="ar_qt_activity_type_global" t-value="o.partner_id.ar_qt_activity_type"></t>
            </t>
            <t t-if="ar_qt_activity_type_global=='arelux'">                
                <t t-set="custom_color_1" t-value="'#195660'" />
            </t>
            <t t-else="">
                <t t-set="custom_color_1" t-value="'#12575E'" />
            </t>
            <div class="text-center" t-att-style="'background:'+custom_color_1+';color:white;width:100%;font-size:9px;margin-bottom:10px;line-height: 25px;'">
                <ul t-if="not company.custom_footer" class="list-inline" style="list-style-type: none;margin-bottom: 0px;">
                    <t t-set="company" t-value="company.sudo()"/>
                    <li t-if="company.phone">Phone: <span t-field="company.phone"/></li>
                    <!--<li t-if="company.fax and company.phone">&amp;bull;</li>!-->
                    <li t-if="company.fax">Fax: <span t-field="company.fax"/></li>
                    <!--<li t-if="company.email and company.fax or company.email and company.phone">&amp;bull;</li>!-->
                    
                    <t t-if="ar_qt_activity_type_global=='todocesped'">
                        <li t-if="company.email">Email: info@todocesped.es</li>
                    </t>
                    <t t-elif="ar_qt_activity_type_global=='evert'">
                        <li t-if="company.email">Email: info@evert.es</li>
                    </t>
                    <t t-elif="ar_qt_activity_type_global=='arelux'">
                        <li t-if="company.email">Email: info@arelux.com</li>
                    </t>
                    <t t-else="">
                        <li t-if="company.email">Email: info@arelux.com</li>
                    </t>
                    <t t-if="ar_qt_activity_type_global=='todocesped'">
                        <li>www.todocesped.es</li>
                    </t>
                    <t t-elif="ar_qt_activity_type_global=='evert'">
                        <li>www.evert.es</li>
                    </t>
                    <t t-elif="ar_qt_activity_type_global=='arelux'">
                        <li>www.arelux.com</li>
                    </t>
                    <t t-else="">
                        <li>www.arelux.com</li>
                    </t>
                    <li t-if="company.street"><span t-field="company.street"/> <span t-field="company.zip"/> <span t-field="company.city"/></li>
                    <li t-if="company.vat">TIN: <span t-field="company.vat"/></li>
                </ul>
                <t t-if="doc_model=='account.invoice'">
                    <div class="infi_mercantil" style="border-top:1px solid white;">
                        <p>Inscrito en Registro Mercantil de Zaragoza al Tomo 3542, Folio 4, Seccion 8, Hoja Z-44463</p>
                    </div>
                </t>
                <ul t-if="not company.custom_footer" name="financial_infos"></ul>
                <t t-if="company.custom_footer">
                    <span t-raw="company.rml_footer"/>
                </t>
            </div>
        </div>
        <!--
        <ul class="list-inline">
            <li>Page:</li>
            <li><span class="page"/></li>
            <li>/</li>
            <li><span class="topage"/></li>
        </ul>
        !-->
    </div>      
</t>
```
