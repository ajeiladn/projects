from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_doctor = fields.Boolean(string='Doctor')

    @api.onchange('is_doctor')
    def doctor(self):
        if self.is_doctor:
            pass
            # print("hello world")
            # print("self.job_id---------------", self.job_id)
            # print("self.job_id.id------------", self.job_id.id)
            # print("self.job_id.id.name-------", self.job_id.id)
            # self.write({'job_id': "Doctor"})
