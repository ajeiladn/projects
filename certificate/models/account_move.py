from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    certificate_partner_id = fields.Many2one('certificate.partner', string="Certificate Partner")
    # field has connection with certificate partner

    @api.constrains('payment_state')
    def constrains_payment_state(self):
        """when invoice get paid then state change in certificate partner"""
        for rec in self:
            ref = rec.env['certificate.partner'].browse(self.certificate_partner_id.id)
            if rec.payment_state == 'paid':
                ref.write({'state': "paid"})
