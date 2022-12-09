from odoo import fields, models
from datetime import datetime


class HospitalManagementConsultation(models.Model):
    _name = 'hospital.management.consultation'
    _description = 'hospital management consultation'
    _rec_name = 'consultation_type'

    token_id = fields.Many2one('hospital.management.op', string='Token', required=True,
                               domain=[('date', '=', datetime.today())])
    card_id = fields.Many2one(related='token_id.card_id', string='Patient Card', readonly=False)
    consultation_type = fields.Selection(selection=[('op', 'OP'), ('ip', 'IP')], string='Consultation', required=True)
    doctor_id = fields.Many2one(related='token_id.doctor_id', string='Doctor', store=True, readonly=True)
    department_id = fields.Many2one(string='Department', related='token_id.department_id', store=True, readonly=True)
    date = fields.Date(string='Date', default=datetime.today())
    disease_ids = fields.Many2many('hospital.management.disease', 'diseases_rel', string='Disease', required=True)
    # disease_rel is the table name we provide attr of Many2many
    diagnose = fields.Text(string='Diagnose')
    treatment_ids = fields.One2many('hospital.management.treatment', 'treatment_id', string='Treatment')
    is_save = fields.Boolean(default=False)

    def confirm(self):
        self.env['hospital.management.history'].create({
            'date': self.date,
            'token': self.token_id.token_no,
            'doctor': self.doctor_id.name,
            'department': self.department_id.name,
            'history_id': self.card_id.id
            })
        self.is_save = True


class HospitalManagementTreatment(models.Model):
    _name = 'hospital.management.treatment'
    _description = 'descriptions'

    medicine_id = fields.Many2one('hospital.management.medicine', string='Medicine', required=True)
    dose = fields.Char(string='Dose')
    days = fields.Integer(string='Days')
    description = fields.Text(string='Description')
    treatment_id = fields.Many2one('hospital.management.consultation', select=False, invisible=True)

    # treatment_id is an imaginary field for create inverse
