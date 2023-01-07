from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_auto_po = fields.Boolean(string='Material Id', default=False)

