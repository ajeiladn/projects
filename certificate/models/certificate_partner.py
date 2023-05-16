from datetime import datetime
from odoo import fields, models, api, _


class CertificatePartner(models.Model):
    _name = 'certificate.partner'
    _description = 'payments'
    _rec_name = 'partner_id'

    name = fields.Char(readonly=True, copy=False, store=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Name", required=True)
    phone = fields.Char(string="Phone", related="partner_id.phone")
    course_id = fields.Many2one('certificate.course', string="Course", required=True,
                                help='select course name')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    total_amt = fields.Monetary(string="Total Amount", related="course_id.fee", help='total amount to paid')
    state = fields.Selection(selection=[('draft', 'Draft'), ('to_inv', 'To Invoice'),
                                        ('invoiced', 'Invoiced'), ('paid', 'Paid'), ('completed', 'Completed')],
                             default='draft')
    invoice_id = fields.Many2one('account.move', string='Invoice Id')
    balance_amt = fields.Monetary(string='Balance Amount', compute='_compute_balance_amt', help='balance amount to pay')

    @api.model
    def create(self, vals):
        """for creating sequence number"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('partner.sequence') or _('New')
        result = super(CertificatePartner, self).create(vals)
        return result

    def action_confirm(self):
        """when confirming the record state changes and course partner field in res.partner become True"""
        self.write({
            'state': 'to_inv'
        })
        self.partner_id.is_course_partner = True

    def action_payment(self):
        """creating invoice"""
        product = self.course_id.product_id
        vals = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': datetime.today().date(),
            'date': datetime.today().date(),
            'certificate_partner_id': self.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'quantity': 1.0,
                'name': "Course Fee",
                'price_unit': product.lst_price,
                'tax_ids': [],
            })]
        })
        self.write({
            'invoice_id': vals.id,
            'state': 'invoiced'
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fee',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_id': vals.id,
        }

    def action_invoice_view(self):
        """smart tab for invoice"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('id', '=', self.invoice_id.id)],
            'context': "{'create': False}"
        }

    def action_complete(self):
        """for changing state to completed"""
        self.write({
            'state': 'completed'
        })

    def _compute_balance_amt(self):
        """for calculating balance amount tobe paid"""
        for rec in self:
            if rec:
                rec.balance_amt = rec.invoice_id.amount_residual

    def unlink(self):
        """when deleting a partner also removes is_course_partner in res.partner"""
        self.partner_id.write({
            'is_course_partner': False
        })
        return super(CertificatePartner, self).unlink()
