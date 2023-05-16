from odoo import fields, models, api


class CertificateCourse(models.Model):
    _name = 'certificate.course'
    _description = 'courses'
    _rec_name = 'name'

    name = fields.Char(string="Course Name")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    fee = fields.Monetary(string='Fee', required=True, help='specify course fee')
    product_id = fields.Many2one('product.product', string='Product ID')

    @api.constrains('name')
    def constrains_name(self):
        """creating product (course) for invoicing"""
        product = self.env['product.product'].create({
                'name': self.name,
                'lst_price': self.fee,
                'detailed_type': 'service'
            })
        self.product_id = product.id
