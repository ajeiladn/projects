from odoo import fields, models


class HospitalManagementDisease(models.Model):
    _name = 'hospital.management.disease'
    _description = 'diseases'
    _rec_name = 'disease'

    disease = fields.Char(string='Disease')
