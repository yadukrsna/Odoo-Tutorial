from odoo import models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def action_add_invoice_line(self):
        self.ensure_one()
        partner = self.move_id.partner_id
        parent_invoice = self.env['account.move'].search([('partner_id', '=', partner.id), ('state', '=', 'draft')])
        parent_invoice._create_line_from_source(self)
