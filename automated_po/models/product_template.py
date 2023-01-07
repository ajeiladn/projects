from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_automated_po(self):
        print("self.name>>>>>", self.name)
        wizard = self.env['product.template.wizard'].create({
            'product_name': self.name,
            'price': self.list_price
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.template.wizard',
            'view_mode': 'form',
            # 'view_type': 'form',
            'res_id': wizard.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
