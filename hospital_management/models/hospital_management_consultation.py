from odoo import fields, models, api
from datetime import datetime


class HospitalManagementConsultation(models.Model):
    _name = 'hospital.management.consultation'
    _description = 'hospital management consultation'
    _rec_name = 'consultation_type'

    patient_id = fields.Many2one('hospital.management', string='Patient Card', required=True)
    consultation_type = fields.Selection(selection=[('op', 'OP'), ('ip', 'IP')], string='Consultation', required=True)
    doctor = fields.Many2one('hr.employee', string='Doctor', domain=[('is_doctor', '=', True)])
    department = fields.Many2one(string='Department', related='doctor.department_id')

    date = fields.Date(default=datetime.today(), string='Date')
    disease_ids = fields.Many2many('hospital.management.disease', 'diseases_rel',  string='Disease', required=True)
    # disease_rel is the table name we provide
    diagnose = fields.Text(string='Diagnose')
    treatment_ids = fields.One2many('hospital.management.treatment', 'treatment_id', string='Treatment')

    @api.model
    def create(self, vals):
        result = super(HospitalManagementConsultation, self).create(vals)



        # access all files here from consultation
        # goto hospital mgmt

        return result


class HospitalManagementTreatment(models.Model):
    _name = 'hospital.management.treatment'
    _description = 'descriptions'

    medicine_id = fields.Many2one('hospital.management.medicine', string='Medicine')
    dose = fields.Char(string='Dose')
    days = fields.Integer(string='Days')
    description = fields.Text(string='Description')
    treatment_id = fields.Many2one('hospital.management.consultation', select=False, invisible=True)
    # treatment_id is an imaginary field for create inverse
