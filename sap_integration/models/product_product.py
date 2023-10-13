from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    sap_code = fields.Char(string="Sap Code", help="Field which indicate product ItemCode in SAP")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sap_code = fields.Char(string="Sap Code", help="Field which indicate product ItemCode in SAP")
