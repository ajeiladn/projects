from odoo import api, models, fields, _
import requests
from requests.auth import HTTPBasicAuth
from odoo.exceptions import UserError, ValidationError


class SapIntegration(models.Model):
    _name = 'sap.integration'
    _rec_name = 'username'

    is_active = fields.Boolean(string="Active", default=False)
    hostname = fields.Char(string="Hostname", required=True)
    protocol = fields.Selection(selection=[('http', 'Http'), ('https', 'Https')],
                                string="Protocol", default='http',
                                required=True)
    port = fields.Char(string="Port", required=True)
    state = fields.Selection(selection=[('not_connected', 'Not Connected'), ('connected', 'Connected')],
                             string='State', readonly=True, copy=False, index=True,
                             default='not_connected'
                             )
    username = fields.Char(string="Username", required=True)
    password = fields.Char(string="Password", required=True)

    @api.onchange('is_active')
    def onchange_is_active(self):
        """ Only one record have active True
        """
        if self.is_active:
            exists = self.search([('is_active', '=', True)], limit=1)
            if exists:
                raise ValidationError(_('Active Record Exists: Please inactive existing record'))

    def connect_to_sap_api(self):
        """ connect Odoo to SAP with api
        """
        if self.is_active:
            url = self.protocol + "://" + self.hostname + ":" + self.port + "/b1s/v1/Login"
            auth = HTTPBasicAuth(self.username, self.password)
            try:
                response = requests.post(url, auth=auth)
                if response.status_code == 200:
                    self.write({'state': 'connected'})
                else:
                    raise UserError(_("Wrong Creditials"))
            except:
                raise UserError(_("Error"))
        else:
            raise ValidationError(_('Active not enabled!'))

    def action_sync_contacts(self):
        """ sync contacts from sap and create if it does not exist.
        """
        url = (self.protocol + "://" + self.hostname +
               ":" + self.port + "/b1s/v1/BusinessPartners?$filter=CardType eq 'C'")
        auth = HTTPBasicAuth(self.username, self.password)

        try:
            response = requests.get(url, auth=auth)
            if response.status_code == 200:
                all_contacts = response.json()['value']
                for contact in all_contacts:
                    if contact['CardCode']:
                        partner = self.env['res.partner'].search([('sap_code', '=', contact['CardCode'])])
                        if partner:
                            pass
                        else:
                            vals = {
                                'sap_code': contact['CardCode'],
                                'name': contact['CardName'] if contact['CardName'] else "Unknown Contact",
                                'mobile': contact['Cellular'] if contact['Cellular'] else False,
                                'email': contact['EmailAddress'] if contact['EmailAddress'] else False,
                            }
                            new_partner = self.env['res.partner'].create(vals)
        except:
            raise UserError(_("Error"))

    def action_sync_products(self):
        """ sync products from sap and create if it does not exist.
        """
        url = (self.protocol + "://" + self.hostname + ":" + self.port + "/b1s/v1/Items")
        auth = HTTPBasicAuth(self.username, self.password)
        try:
            response = requests.get(url, auth=auth)
            if response.status_code == 200:
                all_items = response.json()['value']
                for item in all_items:
                    if item['ItemCode']:
                        product = self.env['product.template'].search([('sap_code', '=', item['ItemCode'])])
                        if product:
                            pass
                        else:
                            default_pricelist = item['ItemPrices'][0]  # first pricelist as default
                            vals = {
                                'sap_code': item['ItemCode'],
                                'name': item['ItemName'] if item['ItemName'] else "Unknown Product",
                                'detailed_type': 'product',
                                'list_price': default_pricelist['Price'] if default_pricelist['Price'] else False,
                                'standard_price': default_pricelist['Price'] if default_pricelist['Price'] else False,
                            }
                            product = self.env['product.template'].create(vals)
                            product.write({
                                'available_in_pos': True,
                            })
                            product.product_variant_id.write({
                                'sap_code': item['ItemCode'],
                            })
                            stock_location = self.env['stock.location'].search([
                                ('company_id', '=', self.env.company.id),
                                ('usage', '=', 'internal'),
                            ], limit=1)
                            quant = self.env['stock.quant'].create({
                                'product_id': product.product_variant_id.id,
                                'location_id': stock_location.id,
                                'quantity': item['QuantityOnStock'],
                            })
                            # quant.action_apply_inventory()
        except:
            raise UserError(_("Error"))
