from odoo import fields, models, api, _

from dateutil.relativedelta import relativedelta
import datetime


class HospitalManagement(models.Model):
    _name = 'hospital.management'
    _description = 'hospital management'

    patient_sequence = fields.Char(readonly=True, required=True, copy=False, index=True, default=lambda self: _('New'))

    patient_id = fields.Many2one(comodel_name='res.partner', string='Patient Name')
    # comodel is target model

    dob = fields.Date(string="D.o.b", related='patient_id.d_o_b')
    # patient_id is an object connects res.partner

    age = fields.Integer(string="Age", readonly=True, compute="_compute_age")
    # _compute_age is a standard fn name "_compute_<fieldname>"

    gender = fields.Selection(string="Gender", related='patient_id.gender')
    mobile = fields.Char(string="Mobile", related='patient_id.mobile')
    telephone = fields.Char(string="Telephone", related='patient_id.phone')
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

        # super() is used to change the workflow of existing fn
        # @api.model
        # def create(self, vals):
        #     if vals.get('name', _('New')) == _('New'):
        #         vals['name'] = self.env['ir.sequence'].next_by_code('test_seq') or _('New')
        #     res = super(Class_Name, self).create(vals)
        #     return res

    @api.depends('dob')
    def _compute_age(self):      # _ represents private method private method
        for i in self:     # FOR loop because SELF may have multiple values "SINGLETON ERROR"
            i.age = False   # compute doesn't work on empty fields so assign a false init
            if i.dob:
                d1 = i.dob
                d2 = datetime.date.today()
                i.age = relativedelta(d2, d1).years
