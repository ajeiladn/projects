from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sap_code = fields.Char(string="Sap Code", help="Field which indicate Business partner CardCode in SAP")
