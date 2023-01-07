from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    milestone_id = fields.Many2one('sale.order', string='Milestone Id')
