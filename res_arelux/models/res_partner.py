# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields, tools, _
from odoo.exceptions import Warning as UserError
from odoo.exceptions import ValidationError
from validate_email import validate_email


class ResPartner(models.Model):
    _inherit = 'res.partner'

    whatsapp = fields.Boolean(
        string='Whatsapp'
    )
    proposal_bring_a_friend = fields.Boolean(
        string='Propuesta trae a un amigo'
    )

    @api.constrains("email")
    def _check_email_valid(self):
        for item in self:
            if not item.email:
                continue
            test_condition = tools.config["test_enable"] and not self.env.context.get(
                "test_email"
            )
            if test_condition:
                continue

            if item.email:
                is_valid = validate_email(
                    item['email'],
                    check_regex=False,
                    check_mx=False,
                    use_blacklist=False
                )
                if not is_valid:
                    raise ValidationError(
                        _("Email &s incorrect'") % item.email
                    )

    @api.multi
    def write(self, vals):
        allow_write = True
        # check_dni
        for item in self:
            if item.type == 'contact' and item.parent_id.id == 0:
                if 'vat' in vals:
                    if vals['vat']:
                        vals['vat'] = vals['vat'].strip().replace(' ', '').upper()

                        if item.country_id and item.country_id.code == 'ES':
                            if '-' in vals['vat']:
                                allow_write = False
                                raise UserError(
                                    _('The NIF does not allow the character -')
                                )

                        if allow_write:
                            if item.supplier:
                                partner_ids = self.env['res.partner'].search(
                                    [
                                        ('id', 'not in', (1, str(item.id))),
                                        ('type', '=', 'contact'),
                                        ('parent_id', '=', False),
                                        ('supplier', '=', True),
                                        ('vat', '=', vals['vat'])
                                    ]
                                )
                            else:
                                partner_ids = self.env['res.partner'].search(
                                    [
                                        ('id', 'not in', (1, str(item.id))),
                                        ('type', '=', 'contact'),
                                        ('parent_id', '=', False),
                                        ('supplier', '=', False),
                                        ('vat', '=', vals['vat'])
                                    ]
                                )

                            if partner_ids:
                                allow_write = False
                                raise UserError(
                                    _('The NIF already exists for another contact')
                                )
        # return
        if allow_write:
            return super(ResPartner, self).write(vals)

    @api.model
    def cron_res_partners_fix_customer(self):
        self.env.cr.execute("""
            UPDATE res_partner
            SET customer = True
            WHERE id IN (
            SELECT rp.id
            FROM res_partner AS rp
            WHERE rp.id > 1 AND rp.type = 'contact' AND rp.active = True
            AND rp.customer = False
            AND ((
            SELECT COUNT(cl.id)
            FROM crm_lead AS cl
            WHERE cl.type = 'opportunity' AND cl.partner_id = rp.id
            ) > 0
            OR (
            SELECT COUNT(so.id)
            FROM sale_order AS so
            WHERE so.partner_id = rp.id) > 0))
        """)
