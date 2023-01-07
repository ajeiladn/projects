from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    margin_total = fields.Monetary(string="Margin", store=True, compute='_compute_margin_total')

    @api.depends('order_line.line_margin')
    def _compute_margin_total(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            order.margin_total = sum(order_lines.mapped('line_margin'))
