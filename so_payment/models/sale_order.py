from odoo import models,fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_paid = fields.Boolean('Invoice Paid', compute='_compute_paid_invoice')

    def action_so_payment(self):
        for record in self:
            invoice = record.invoice_ids.filtered(lambda inv: inv.state == 'posted')
            return invoice.action_register_payment()

    def _compute_paid_invoice(self):
        for record in self:
            invoice = record.invoice_ids.filtered(lambda inv: inv.state == 'posted')

            if not invoice:
                record.invoice_paid = False
            else:
                record.invoice_paid = all(inv.payment_state == 'paid' for inv in invoice)