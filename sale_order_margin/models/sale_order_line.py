from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    line_margin = fields.Float(
        string="Margin",
        compute='_compute_line_margin',
        store=True)

    @api.depends('price_unit', 'product_uom_qty', 'product_template_id')
    def _compute_line_margin(self):
        for line in self:
            if line:
                cost_price = line.product_template_id
                line.line_margin = (line.price_unit - cost_price.standard_price) * line.product_uom_qty
