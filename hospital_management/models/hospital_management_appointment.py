from odoo import fields, models, _, api
from datetime import datetime


class HospitalManagementAppointment(models.Model):
    _name = 'hospital.management.appointment'
    _description = 'Hospital Management Appointment'
    _rec_name = 'sequence_no'

    sequence_no = fields.Char(readonly=True, copy=False, default=lambda self: _('New'))
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
    token_no = fields.Char(string="Token", readonly=True)
    is_backend = fields.Boolean(string="Is Backend", default=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', _('New')) == _('New'):
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('hospital.sequence.appointment') or _('New')
        res = super(HospitalManagementAppointment, self).create(vals)
        return res

    def action_appointment(self):
        self.write({'state': "appointment"})

        token = self.env['hospital.management.op'].search_count([('date', '=', self.date),
                                                                 ('doctor_id', '=', self.doctor_id.id)])
        token += 1
        self.token_no = token

        # token = self.search_count([('date', '=', self.date), ('doctor_id', '=', self.doctor_id.id)])
        # op_token = self.env['hospital.management.op'].search(
        #     [('date', '=', self.date), ('doctor_id', '=', self.doctor_id.id)], limit=1, order='id desc')
        # op_token = int(op_token)
        #
        # if token == op_token:
        #     self.token_no = token+1
        #
        # elif token > op_token:
        #     self.token_no = token
        #
        # elif token < op_token:
        #     self.token_no = op_token
        #
        # else:
        #     self.token_no = op_token

    def action_op(self):
        self.write({'state': "op"})

        datas = self.env['hospital.management.op'].create({
            'card_id': self.card_id.id,
            'doctor_id': self.doctor_id.id,
            'date': self.date,
            'state': self.state,
            'token_no': self.token_no
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
            'view_mode': 'tree,form',
            'res_model': 'hospital.management.op',
            'domain': [('token_no', '=', self.token_no)],
            'context': "{'create': False}"
        }

    def patient_name(self, card):
        var = self.browse(int(card))
        p_name = var.patient_id.name
        return p_name

    def doctor_details(self, doctor):
        var = self.env['hr.employee'].browse(int(doctor))
        dept = var.department_id.name
        print("FEEEEEEEEEEE", var.fee)
        fee = var.fee
        return dept, fee
