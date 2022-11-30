from odoo import fields, models, api, _
from datetime import datetime


class HospitalManagementOp(models.Model):
    _name = 'hospital.management.op'
    _description = 'op tickets'
    _rec_name = 'token_no'

    token_no = fields.Char(required=True, readonly=True, default=lambda self: _('New'))
    # generate sequentially regen next day
    card_id = fields.Many2one(comodel_name='hospital.management', string='Card Id', required=True)
    patient_id = fields.Many2one(string='Patient Name', related='card_id.patient_id', readonly=False)
    age = fields.Integer(related='card_id.age', string='Age', readonly=False)
    gender = fields.Selection(related='card_id.gender', string='Gender', readonly=False)
    blood_group = fields.Selection(related='card_id.blood_group', string='Blood Group', readonly=False)
    doctor_id = fields.Many2one(comodel_name='hr.employee', string='Doctor', domain="[('job_id','=','Doctor')]",
                                required=True)
    date = fields.Date(string='Date', default=datetime.today())  # today date import date time
    # print("hour", date.hour)
    company_id = fields.Many2one('res.company', store=True, string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    # company_id from res.company
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    # currency_id from res.currency related to company_id
    fee = fields.Monetary(string='Fee', required=True)
    state = fields.Selection(selection=[('draft', 'Draft'), ('op', 'OP')],
                             string='State', default='draft')  # draft&confirm

    @api.model
    def create(self, vals):
        if vals.get('token_no', _('New')) == _('New'):
            vals['token_no'] = self.env['ir.sequence'].next_by_code('hospital.token') or _('New')
        res = super(HospitalManagementOp, self).create(vals)
        return res

    def confirm(self):
        self.write({'state': "op"})

    def token_reccuring(self):
        token = self.env['ir.sequence'].search([('name', '=like', 'Hospital Management Token')])

        token.write({
            'number_next_actual': 1,
        })
