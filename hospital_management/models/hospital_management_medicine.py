from odoo import fields, models


class HospitalManagementMedicine(models.Model):
    _name = 'hospital.management.medicine'
    _description = 'medicines'
    _rec_name = 'medicine'

    medicine = fields.Char(string='Medicine')
