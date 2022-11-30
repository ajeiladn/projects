from odoo import fields, models, api, _

from dateutil.relativedelta import relativedelta
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
    age = fields.Integer(string="Age", readonly=True, compute="_compute_age")
    # _compute_age is a standard fn name "_compute_<fieldname>"
    gender = fields.Selection(string="Gender", related='patient_id.gender', readonly=False)
    mobile = fields.Char(string="Mobile", related='patient_id.mobile', readonly=False)
    telephone = fields.Char(string="Telephone", related='patient_id.phone', readonly=False)
    blood_group = fields.Selection(
        selection=[('a_pos', 'A+'), ('a_neg', 'A-'), ('b_pos', 'B+'), ('b_neg', 'B-'), ('o_pos', 'O+'), ('o_neg', 'O-'),
                   ('ab_pos', 'AB+'), ('ab_neg', 'AB-')],
        string="Blood Group",
    )

    @api.model
    def create(self, vals):
        if vals.get('patient_sequence', _('New')) == _('New'):
            vals['patient_sequence'] = self.env['ir.sequence'].next_by_code('hospital.sequence') or _('New')
        result = super(HospitalManagement, self).create(vals)
        return result

    @api.depends('dob')
    def _compute_age(self):      # _ represents private method
        for i in self:     # FOR loop because SELF may have multiple values "SINGLETON ERROR"
            i.age = False   # compute doesn't work on empty fields so assign a false init
            if i.dob:
                d1 = i.dob
                d2 = date.today()
                i.age = relativedelta(d2, d1).years
