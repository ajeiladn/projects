from odoo import fields, models, _, api
from datetime import datetime


class HospitalManagementAppointment(models.Model):
    _name = 'hospital.management.appointment'
    _description = 'Hospital Management Appointment'
    _rec_name = 'token_no'

    token_no = fields.Char(readonly=True, default=lambda self: _('New'))
    card_id = fields.Many2one('hospital.management', string='Patient Card', required=True)
    patient_id = fields.Many2one(string='Patient Name', related='card_id.patient_id', readonly=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', domain=[('is_doctor', '=', True)])
    department_id = fields.Many2one(related='doctor_id.department_id', string='Department')

    company_id = fields.Many2one('res.company', store=True, string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id, readonly=True)
    fee = fields.Monetary(string='Fee', related='doctor_id.fee', readonly=True)

    date = fields.Date(string='Date', default=datetime.today())
    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'), ('appointment', 'Appointment'), ('op', 'OP')],
                             default='draft')

    @api.model
    def create(self, vals):
        if vals.get('token_no', _('New')) == _('New'):
            vals['token_no'] = self.env['ir.sequence'].next_by_code('hospital.token') or _('New')
        res = super(HospitalManagementAppointment, self).create(vals)
        return res

    def action_appointment(self):
        self.write({'state': "appointment"})

    def action_op(self):
        self.write({'state': "op"})

        datas = self.env['hospital.management.op'].create({
            'card_id': self.card_id.id,
            'doctor_id': self.doctor_id.id,
            'fee': self.fee,
            'date': self.date,
            'token_no': self.token_no,
            'state': self.state
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'OP',
            'view_mode': 'form',
            'res_model': 'hospital.management.op',
            'view_id': self.env.ref('hospital_management.hospital_management_op_view_form').id,
            'res_id': datas.id,
        }

    def appointment_tab(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'view_mode': 'tree',
            'res_model': 'hospital.management.op',
            'domain': [('token_no', '=', self.token_no)],
            'context': "{'create': False}"
        }
