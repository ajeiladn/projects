from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_doctor = fields.Boolean(string='Doctor')

    @api.onchange('is_doctor')
    def doctor(self):
        if self.is_doctor:
            doctor_id = self.env.ref('hospital_management.hr_job_doctor')
            # ref contains external id i.e, <modulename>_<record_id>  record id from demo.xml
            self.write({'job_id': doctor_id})
