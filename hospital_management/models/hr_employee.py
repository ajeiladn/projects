from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_doctor = fields.Boolean(string='Doctor')
