from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_doctor = fields.Boolean(string='Doctor')
    company_id = fields.Many2one('res.company', store=True, string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id, readonly=True)
    fee = fields.Monetary(string='Fee', store=True)
    op_count = fields.Integer(string="OP count", default=1)

    @api.onchange('is_doctor')
    def doctor(self):
        if self.is_doctor:
            doctor_id = self.env.ref('hospital_management.hr_job_doctor')
            # ref contains external id i.e, <modulename>.<record_id>  record id from job_position_demo.xml
            self.write({'job_id': doctor_id})
