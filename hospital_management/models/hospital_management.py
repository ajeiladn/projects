from odoo import fields, models, api, _
from datetime import date


class HospitalManagement(models.Model):
    _name = 'hospital.management'
    _description = 'hospital management'
    _rec_name = 'patient_sequence'  # for identify the object name coz we didn't give the name field

    patient_sequence = fields.Char(readonly=True, copy=False, default=lambda self: _('New'))
    patient_id = fields.Many2one(comodel_name='res.partner', string='Patient Name')
    # comodel is target model
    dob = fields.Date(string="D.o.b", related='patient_id.d_o_b', readonly=False)
    # patient_id is an object connects res.partner
    age = fields.Integer(string="Age", readonly=True)
    gender = fields.Selection(string="Gender", related='patient_id.gender', readonly=False)
    mobile = fields.Char(string="Mobile", related='patient_id.mobile', readonly=False)
    telephone = fields.Char(string="Telephone", related='patient_id.phone', readonly=False)
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

    date = fields.Char()
    token = fields.Char()
    doctor = fields.Char()
    department = fields.Char()
    history_id = fields.Many2one('hospital.management')

    # using .create() give data to history fields
