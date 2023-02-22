from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # payment_ref = fields.Char(String="Payment Reference", related="move_id.payment_reference", store=True)
    payment_ref = fields.Char(String="Payment Reference", store=True)


