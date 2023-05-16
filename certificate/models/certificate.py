from odoo import api, fields, models, _


class CertificateCertificate(models.Model):
    _name = 'certificate.certificate'
    _description = 'course certificates'
    _rec_name = 'name'

    name = fields.Char(readonly=True, copy=False, store=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Name", required=True,
                                 domain=[('is_course_partner', '!=', False)])
    phone = fields.Char(string="Phone", related="partner_id.phone")
    course_id = fields.Many2one('certificate.course', string="Course", required=True,
                                help='course that chosen by selected partner')
    course_status = fields.Selection(selection=[('in_progress', 'In Progress'), ('completed', 'Completed')],
                                     default='in_progress', string="Course Status", readonly=True,
                                     help='course status defined the state of course',
                                     )
    payment_status = fields.Selection(selection=[('not', 'Not Paid'), ('partial', 'Partially paid'),
                                                 ('full', 'Fully Paid')], default='not', string="Payment Status",
                                      readonly=True, help='course status defined the state of payment')
    grade = fields.Selection(selection=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], string='Grade',
                             help='provide grade of the course')
    date = fields.Date(string='Date of Pass', help='date of completion of course')

    @api.model
    def create(self, vals):
        """creating sequence"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('certificate.sequence') or _('New')
        result = super(CertificateCertificate, self).create(vals)
        return result

    @api.onchange('partner_id', 'course_id')
    def onchange_partner_id(self):
        """dynamic domain on field course w.r.t. partner"""
        if not self.course_id:
            partners = self.env['certificate.partner'].search([('partner_id', '=', self.partner_id.id)])
            return {'domain': {'course_id': [('id', 'in', partners.course_id.ids)]}}
        elif self.partner_id and self.course_id:
            partner_details = self.env['certificate.partner'].search([('partner_id', '=', self.partner_id.id),
                                                                      ('course_id', '=', self.course_id.id)])
            if partner_details.state == 'completed':
                self.write({
                    'course_status': 'completed'
                })
            if partner_details.balance_amt == partner_details.total_amt:
                self.write({'payment_status': 'not'})
            elif partner_details.balance_amt == 0:
                self.write({'payment_status': 'full'})
            else:
                self.write({'payment_status': 'partial'})

    def action_print(self):
        """for printing the reports"""
        return self.env.ref('certificate.certificate_report_action').report_action(None)
