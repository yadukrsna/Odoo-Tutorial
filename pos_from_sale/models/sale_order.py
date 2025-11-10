from odoo import fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pos_session_id = fields.Many2one('pos.session', string="POS Session",
                                     domain=lambda self: [('user_id', '=', self.env.uid), ('state', '=', 'opened')])
    state = fields.Selection(selection_add=[
        ('paid_at_counter', 'Paid at Counter')
    ])

    pos_order_id = fields.Many2one('pos.order', string="POS Order")

    def action_pay_at_counter(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Pay at the Counter'),
            'res_model': 'pos.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_id': self.id},
        }
