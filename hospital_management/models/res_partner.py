from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'  # is to add fields to res.partner model

    d_o_b = fields.Date(string="D.o.b")
    gender = fields.Selection(selection=[('male', "Male"), ('female', "Female")], string="Gender")
    is_op_created = fields.Boolean(default=False)
