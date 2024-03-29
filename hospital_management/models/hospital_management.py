from odoo import fields, models, api, _
from datetime import date


class HospitalManagement(models.Model):
    _name = 'hospital.management'
    _description = 'hospital management'
    _rec_name = 'patient_sequence'

    patient_sequence = fields.Char(readonly=True, copy=False, store=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('res.partner', string='Patient Name')
    dob = fields.Date(string="D.o.b", related='patient_id.d_o_b', readonly=True)
    age = fields.Integer(string="Age", readonly=True, store=True)
    gender = fields.Selection(string="Gender", related='patient_id.gender', readonly=True)
    mobile = fields.Char(string="Mobile", related='patient_id.mobile', readonly=True)
    telephone = fields.Char(string="Telephone", related='patient_id.phone', readonly=True)
    blood_group = fields.Selection(
        selection=[('a_pos', 'A+'), ('a_neg', 'A-'), ('b_pos', 'B+'), ('b_neg', 'B-'), ('o_pos', 'O+'), ('o_neg', 'O-'),
                   ('ab_pos', 'AB+'), ('ab_neg', 'AB-')],
        string="Blood Group",
    )
    history_ids = fields.One2many('hospital.management.history', 'history_id', string='OP History')

    @api.model
    def create(self, vals):
        if vals.get('patient_sequence', _('New')) == _('New'):
            vals['patient_sequence'] = self.env['ir.sequence'].next_by_code('hospital.sequence') or _('New')
        result = super(HospitalManagement, self).create(vals)
        return result

    @api.onchange('dob')
    def calc_age(self):
        if self.dob:
            today = date.today()
            self.age = today.year - self.dob.year


class HospitalManagementHistory(models.Model):
    _name = 'hospital.management.history'

    date = fields.Char(string="Date")
    token_no = fields.Char(string="Token")
    doctor = fields.Char(string="Doctor")
    department = fields.Char(string="Department")
    history_id = fields.Many2one('hospital.management')
