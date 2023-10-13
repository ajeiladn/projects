from odoo import models, fields, api, _
import requests
from requests.auth import HTTPBasicAuth
from odoo.exceptions import UserError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    doc_entry = fields.Char(string="DocEntry", help="Field which indicate DocEntry in SAP")
    doc_num = fields.Char(string="DocNum", help="Field which indicate DocNum in SAP")

    @api.model
    def _process_order(self, order, draft, existing_order):
        pos_order_id = super(PosOrder, self)._process_order(order, draft, existing_order)
        pos_order = self.browse(pos_order_id)
        doc_lines = []
        for line in pos_order.lines:
            product = self.env['product.product'].browse(line.product_id.id)
            data = {
                "ItemCode": product.sap_code,
                "Quantity": str(line.qty),
                "UnitPrice": str(line.price_unit),
            }
            doc_lines.append(data)

        body = {
            "DocDueDate": pos_order.create_date.strftime('%Y-%m-%d'),
            "CardCode": pos_order.partner_id.sap_code,
            "DocumentLines": doc_lines
        }
        api_cred = self.env['sap.integration'].search([('is_active', '=', True)])
        url = api_cred.protocol + "://" + api_cred.hostname + ":" + api_cred.port + "/b1s/v1/Orders"
        auth = HTTPBasicAuth(api_cred.username, api_cred.password)
        try:
            response = requests.post(url, json=body, auth=auth)
            if response.status_code == 201:
                response_data = response.json()
                pos_order.write({
                    'doc_entry': response_data['DocEntry'],
                    'doc_num': response_data['DocNum']
                })
        except:
            raise UserError(_("Error"))
        return pos_order_id
