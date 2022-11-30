from odoo import fields, models
from datetime import datetime


class HospitalManagementConsultation(models.Model):
    _name = 'hospital.management.consultation'
    _description = 'hospital management consultation'
    _rec_name = 'consultation_type'

    patient_id = fields.Many2one('hospital.management', string='Patient Card', required=True)
    consultation_type = fields.Selection(selection=[('op', 'OP'), ('ip', 'IP')], string='Consultation', required=True)
    doctor = fields.Char()    # filtered by is_doctor = True
    department = fields.Char()  # related to doctor
    date = fields.Date(default=datetime.today(), string='Date')
    disease_id = fields.Many2one('hospital.management.disease', string='Disease', required=True)
    diagnose = fields.Text(string='Diagnose')
    treatment = fields.Char()
