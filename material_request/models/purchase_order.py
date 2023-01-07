from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    material_id = fields.Many2one('material.request', string='Material Id')
