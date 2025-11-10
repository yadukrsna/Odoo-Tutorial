from odoo import api,fields,models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    active_credit_limit = fields.Boolean('Activate Credit Limit', default=False)
    warning_amount = fields.Monetary('Warming Amount', currency_field='currency_id')
    block_limit = fields.Monetary('Block Limit', currency_field='currency_id')
    due_amount = fields.Monetary('Due Amount', compute='_compute_due_amount', currency_field='currency_id')

    def _compute_due_amount(self):
        for partner in self:
            print("FFFGGGGG")
            lines = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
            ])
            partner.due_amount = sum(lines.mapped('amount_residual_signed'))
            print(partner.due_amount)