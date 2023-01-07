from odoo import fields, models


class ProductTemplateWizard(models.TransientModel):
    _name = 'product.template.wizard'
    _description = 'product template wizard'

    product_name = fields.Char(string='Product')
    quantity = fields.Float(string="Quantity", default=1.0)
    price = fields.Char(string="Unit Price", readonly=True)

    def action_confirm(self):
        vendors = []
        product = self.env['product.product'].search([('name', '=', self.product_name)])

        for seller in product.seller_ids:
            vendors.append(seller)
        if vendors:
            vendor = vendors[0]

            x = self.env['purchase.order'].search([('state', '=', 'draft'),
                                                   ('partner_id', '=', vendor.partner_id.id),
                                                   ('is_auto_po', '=', True)])
            if x:
                x.order_line = [(0, 0, {
                        'product_id': product.id,
                        'product_qty': self.quantity,
                        'price_unit': self.price,
                    })]

            else:
                datas = self.env['purchase.order'].create({
                    'partner_id': vendor.partner_id.id,
                    'is_auto_po': True,
                    "order_line": [(0, 0, {
                        'product_id': product.id,
                        'product_qty': self.quantity,
                        'price_unit': self.price,
                    })],
                })
            return {
                'type': 'ir.actions.act_window',
                'name': 'RFQ',
                'view_mode': 'form',
                'res_model': 'purchase.order',
                'view_id': self.env.ref('purchase.purchase_order_form').id,
                'res_id': x.id if x else datas.id,
            }
