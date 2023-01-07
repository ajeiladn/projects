from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    similar_so_ids = fields.Many2many('sale.order', string='Similar SO', ondelete='restrict')

    @api.onchange('similar_so_ids')
    def _onchange_similar_so_ids(self):
        self.invoice_line_ids = False
        for so_id in self.similar_so_ids.ids:
            invoice_object = self.env['sale.order'].browse(so_id)
            for line in invoice_object.order_line:
                vals = self.update({
                    'invoice_line_ids': [(0, 0, {
                        'product_id': line.product_id.id,
                        'quantity': line.product_uom_qty,
                    })]
                })
