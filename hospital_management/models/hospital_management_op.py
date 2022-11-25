from odoo import fields, models


class HospitalManagementOp(models.Model):
    _name = 'hospital.management.op'
    _description = 'op tickets'

    patient_sequence = fields.Char()          #Many2one(comodel='hospital.management', string='Patient Card')
    patient_id = fields.Char()                        #Char(related='patient_sequence.patient_id')
    age = fields.Integer()                        #(related='patient_sequence.age')
    gender = fields.Char()                    #(related='patient_sequence.gender')
    blood_group = fields.Char()               #(related='patient_sequence.blood_group')
    doctor_id = fields.Char(string='Doctor')        # Many2one filtered by job posn
    date = fields.Char()            # todays day import date time
    token_no = fields.Char()        #generate sequentially regen next day
    fee = fields.Char()           #monitory field
    state = fields.Char()       #dreaft