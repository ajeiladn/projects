from odoo import fields, models, _, api
from datetime import datetime


class MaterialRequest(models.Model):
    _name = 'material.request'
    _description = 'material request'
    _rec_name = 'sequence'

    sequence = fields.Char(string="Sequence No", readonly=True, copy=False, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Employee Name', required=True)
    date = fields.Date(string='Date', default=datetime.today())
    state = fields.Selection(selection=[('to_submit', 'To Submit'),
                                        ('submitted', 'Submitted'),
                                        ('verified', 'Verified'),
                                        ('approved', 'Approved'),
                                        ('refused', 'Refused')],
                             default='to_submit')

    request_ids = fields.One2many('request.lines', 'request_id', string='Request')
    is_po = fields.Boolean(default=False)
    is_internal = fields.Boolean(default=False)

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('material.sequence') or _('New')
        res = super(MaterialRequest, self).create(vals)
        return res

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_verify(self):
        self.write({'state': 'verified'})

    def action_refuse(self):
        self.write({'state': 'refused'})

    def action_approve(self):
        self.write({'state': 'approved'})
        for line in self.request_ids:
            if line.product_transfer == 'po':
                for rec in line.product_id.seller_ids:
                    x = self.env['purchase.order'].search([('state', '=', 'draft'),
                                                           ('partner_id', '=', rec.partner_id.id),
                                                           ('material_id', '=', self.id)],
                                                          limit=1, order='id desc')
                    if x:
                        x.update({
                            "order_line": [(0, 0, {
                                'product_id': line.product_id.id,
                                'name': line.product_id.name,
                                'product_qty': line.product_qty,
                                'price_unit': line.product_id.list_price,
                            })],
                        })
                    else:
                        self.env['purchase.order'].create({
                            'partner_id': rec.partner_id.id,
                            'material_id': self.id,
                            "order_line": [(0, 0, {
                                'product_id': line.product_id.id,
                                'name': line.product_id.name,
                                'product_qty': line.product_qty,
                                'price_unit': line.product_id.list_price,
                            })],
                        })
                self.is_po = True
            if line.product_transfer == 'internal':
                self.env['stock.picking'].create({
                    'partner_id': self.partner_id.id,
                    'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                    'location_id': self.env.ref('stock.stock_location_stock').id,
                    'location_dest_id': self.env.ref('stock.stock_location_stock').id,
                    'origin': self.sequence,
                    'move_ids': [(0, 0, {
                        'name': '/',
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_qty,
                        'location_id': self.env.ref('stock.stock_location_stock').id,
                        'location_dest_id': self.env.ref('stock.stock_location_stock').id,
                    })],
                })
                self.is_internal = True

    def internal_tab(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Internal Transfer',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('origin', '=', self.sequence)],
            'context': "{'create': False}"
        }

    def po_tab(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'RFQ',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('material_id', '=', self.id)],
            'context': "{'create': False}"
        }


class RequestLines(models.Model):
    _name = 'request.lines'

    request_id = fields.Many2one('material.request', string='Request Reference')
    product_id = fields.Many2one('product.product', string='Product')
    product_qty = fields.Float(string='Quantity', default=1.0)
    product_transfer = fields.Selection(string="Transfer",
                                        selection=[('internal', 'Internal Transfer'), ('po', 'Purchase Order')])
