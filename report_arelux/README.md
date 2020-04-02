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
