from odoo import api, fields, models
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_invoice_lines_ids = fields.Many2many('account.move.line', compute='_compute_customer_invoice_lines',
                                                  string='Previous Invoice Lines', store=True)

    @api.depends('partner_id')
    def _compute_customer_invoice_lines(self):
        for move in self:
            all_lines = self.env['account.move.line'].search([('move_id.partner_id', '=', move.partner_id.id),
                                                              ('move_id.state', '=', 'posted')])

            product_max_price = {}
            for line in all_lines:
                pid = line.product_id.id
                if pid not in product_max_price or line.price_unit > product_max_price[pid].price_unit:
                    product_max_price[pid] = line

            move.customer_invoice_lines_ids = [(6, 0, [l.id for l in product_max_price.values()])]

    def action_add_all_invoice_lines(self):
        for move in self:
            for line in move.customer_invoice_lines_ids:
                move._create_line_from_source(line)

    def _create_line_from_source(self, source_line):
        vals = {
            'move_id': self.id,
            'product_id': source_line.product_id.id,
            'quantity': source_line.quantity or 1.0,
            'price_unit': source_line.price_unit,
        }
        self.env['account.move.line'].create(vals)



