from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SalePayAtCounterWizard(models.TransientModel):
    _name = 'pos.payment.wizard'
    _description = 'Wizard for Pay at Counter'

    sale_id = fields.Many2one('sale.order', required=True)
    payment_line_ids = fields.One2many('pos.payment.line', 'payment_wizard_id', string="Payments")

    total_amount = fields.Monetary(related="sale_id.amount_total", string="Total", readonly=True)
    paid_amount = fields.Monetary(compute='_compute_paid', string="Paid", readonly=True)
    remaining_amount = fields.Monetary(compute='_compute_paid', string="Remaining", readonly=True)
    currency_id = fields.Many2one(related="sale_id.currency_id")

    @api.depends('payment_line_ids.amount')
    def _compute_paid(self):
        for rec in self:
            rec.paid_amount = sum(rec.payment_line_ids.mapped('amount'))
            rec.remaining_amount = rec.total_amount - rec.paid_amount

    def action_confirm_payment(self):
        self.ensure_one()
        sale = self.sale_id
        pos_session = sale.pos_session_id
        if not pos_session:
            raise UserError(_("No active POS session found for this user."))

        order_lines_data = []
        for line in sale.order_line:
            order_lines_data.append((0, 0, {
                'product_id': line.product_id.id,
                'qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'tax_ids': [(6, 0, line.tax_id.ids)],
                'price_subtotal': line.price_subtotal,
                'price_subtotal_incl': line.price_total,
            }))
        pos_order = self.env['pos.order'].create({
            'name': f'POS/{pos_session.id}/{sale.name}',
            'session_id': pos_session.id,
            'partner_id': sale.partner_id.id,
            'lines': order_lines_data,
            'amount_tax': sale.amount_tax or 0.0,
            'amount_total': sale.amount_total or 0.0,
            'amount_paid': self.paid_amount or 0.0,
            'amount_return': 0.0,
            'pricelist_id': sale.pricelist_id.id,
            'currency_id': sale.currency_id.id,
            'state': 'paid'
        })

        for pay in self.payment_line_ids:
            self.env['pos.payment'].create({
                'pos_order_id': pos_order.id,
                'payment_method_id': pay.payment_method_id.id,
                'amount': pay.amount or 0.0,
                'session_id': pos_session.id,
            })
        sale.write({
            'state': 'paid_at_counter',
            'pos_order_id': pos_order.id,
        })

        return {'type': 'ir.actions.act_window_close'}


class SalePayAtCounterLine(models.TransientModel):
    _name = 'pos.payment.line'
    _description = 'Pay at Counter Payment Line'

    payment_wizard_id = fields.Many2one('pos.payment.wizard', required=True, ondelete='cascade')
    payment_method_id = fields.Many2one(
        'pos.payment.method',
        string="Payment Method",
        required=True,
        domain="[('id', 'in', available_payment_method_ids)]"
    )
    available_payment_method_ids = fields.Many2many('pos.payment.method', compute='_compute_available_methods')
    amount = fields.Monetary(string="Amount", required=True)
    currency_id = fields.Many2one(related="payment_wizard_id.sale_id.currency_id")

    @api.depends('payment_wizard_id')
    def _compute_available_methods(self):
        for record in self:
            session = record.payment_wizard_id.sale_id.pos_session_id
            if session:
                record.available_payment_method_ids = session.config_id.payment_method_ids
            else:
                record.available_payment_method_ids = self.env['pos.payment.method']
