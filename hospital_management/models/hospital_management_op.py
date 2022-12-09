from odoo import fields, models, api, _
from datetime import datetime


class HospitalManagementOp(models.Model):
    _name = 'hospital.management.op'
    _description = 'op tickets'
    _rec_name = 'token_no'

    token_no = fields.Char(readonly=True, default=lambda self: _('New'))
    card_id = fields.Many2one('hospital.management', string='Card Id', required=True)
    patient_id = fields.Many2one(string='Patient Name', related='card_id.patient_id', readonly=True)  # true
    age = fields.Integer(related='card_id.age', string='Age', readonly=True)
    gender = fields.Selection(related='card_id.gender', string='Gender', readonly=True)
    blood_group = fields.Selection(related='card_id.blood_group', string='Blood Group', readonly=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', domain=[('is_doctor', '=', True)],
                                required=True)
    department_id = fields.Many2one(related='doctor_id.department_id', readonly=True)
    date = fields.Date(string='Date', default=datetime.today())
    company_id = fields.Many2one('res.company', store=True, string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id, readonly=True)
    fee = fields.Monetary(string='Fee', related='doctor_id.fee', readonly=True)
    state = fields.Selection(selection=[('draft', 'Draft'), ('op', 'OP'), ('paid', 'Paid')],
                             string='State', default='draft')

    @api.model
    def create(self, vals):
        if vals.get('token_no', _('New')) == _('New'):
            vals['token_no'] = self.env['ir.sequence'].next_by_code('hospital.token') or _('New')
        res = super(HospitalManagementOp, self).create(vals)
        return res

    def token_reccuring(self):
        token = self.env['ir.sequence'].search([('name', '=like', 'Hospital Management Token')])
        token.write({
            'number_next_actual': 1,
        })

    def action_confirm(self):
        self.write({'state': "op"})

    def action_fee_payment(self):
        vals = self.env['account.move'].create({
            'move_type': 'out_invoice',
            # 'journal_id': journal.id,
            'partner_id': self.patient_id.id,
            'invoice_date': self.date,
            'date': self.date,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.env.ref('hospital_management.product_template_product').id,
                # inside ref is <modulename>.<record_id>
                'quantity': 1.0,
                'name': "Doctor's Fee",
                'price_unit': self.fee,
                'tax_ids': [],
            })]
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Fee',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_id': vals.id,
        }
