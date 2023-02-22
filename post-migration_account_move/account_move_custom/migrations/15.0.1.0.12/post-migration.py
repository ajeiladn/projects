import logging
from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    account_move = env['account.move'].search([])
    for move_line in account_move:
        for line in move_line.invoice_line_ids:
            if not line.payment_ref:
                line.payment_ref = move_line.payment_reference

