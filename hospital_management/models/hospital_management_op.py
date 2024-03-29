from odoo import fields, models, api, _
from datetime import datetime


class HospitalManagementOp(models.Model):
    _name = 'hospital.management.op'
    _description = 'op tickets'
    _rec_name = 'token_no'

    sequence_no = fields.Char(readonly=True, copy=False, default=lambda self: _('New'))
    card_id = fields.Many2one('hospital.management', string='Card Id', required=True)
    patient_id = fields.Many2one(string='Patient Name', related='card_id.patient_id', readonly=True)
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
    # invoice_ids = fields.Many2many('account.move', string="Invoices")
    token_no = fields.Char(string='Token', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', _('New')) == _('New'):
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('hospital.sequence.op') or _('New')
        res = super(HospitalManagementOp, self).create(vals)
        return res

    def action_confirm(self):
        self.write({'state': "op"})
        self.patient_id.is_op_created = True

        doc = self.env['hr.employee'].browse(self.doctor_id.id)
        doc.op_count += 1

        token = self.env['hospital.management.appointment'].search_count([('date', '=', self.date),
                                                                          ('doctor_id', '=', self.doctor_id.id)])
        token += 1
        self.token_no = token

        # token = self.search_count([('date', '=', self.date), ('doctor_id', '=', self.doctor_id.id)])
        #
        # appointment_token = self.env['hospital.management.appointment'].search(
        #     [('date', '=', self.date), ('doctor_id', '=', self.doctor_id.id)], limit=1,  order='id desc')
        #
        # appointment_token = int(appointment_token)
        #
        # if token == appointment_token:
        #     self.token_no = token + 1
        #
        # elif token > appointment_token:
        #     self.token_no = token
        #
        # elif token < appointment_token:
        #     self.token_no = appointment_token
        #
        # else:
        #     self.token_no = appointment_token


    def action_fee_payment(self):
        vals = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.id,
            'invoice_date': self.date,
            'date': self.date,
            'ref': self.sequence_no,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.env.ref('hospital_management.product_template_product').id,
                # inside ref is <modulename>.<record_id>
                'quantity': 1.0,
                'name': "Doctor's Fee",
                'price_unit': self.fee,
                'tax_ids': [],
            })]
        })

        # self.write({'invoice_ids': [(4, vals.id)]})
        # here pass the vals id to that many2one field

        return {
            'type': 'ir.actions.act_window',
            'name': 'Fee',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_id': vals.id,
        }


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.constrains('payment_state')
    def constrains_payment_state(self):
        for i in self:
            if i.payment_state == 'paid':
                ref = i.env['hospital.management.op'].search([('sequence_no', '=', i.ref)])
                # ref = i.env['hospital.management.op'].search([('invoice_ids', '=', i.self.id)])
                ref.write({'state': "paid"})
