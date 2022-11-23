from odoo import fields, models

class HospitalManagement(models.Model):
    _name = 'hospital.management'
    _description = 'hospital management'

    patient_id = fields.Char(string='Patient Id')
    patient_name_id = fields.Many2one('res.partner', string='Patient Name')

    dob = fields.Datetime()
    age = fields.Integer()

    gender = fields.Char()

    address = fields.Text(string='Address')
    mobile = fields.Char()
    telephone = fields.Char()
    blood_group = fields.Selection(
        selection=[('a_pos', 'A+'), ('a_neg', 'A-'), ('b_pos', 'B+'), ('b_neg', 'B-'), ('o_pos', 'O+'), ('o_neg', 'O-'),
                   ('ab_pos', 'AB+'), ('ab_neg', 'AB-')]
    )
