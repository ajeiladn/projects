from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_course_partner = fields.Boolean(string='Course Partner', default=False, readonly=True,
                                       help='Identify if partner have a course')
    # field to domain for chosen partner
