from odoo import models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self:
            partner_orders = self.env['sale.order'].search([('partner_id', '=', order.partner_id.id),
                                                            ('state', 'in', ['sale', 'done']), ('id', '!=', order.id)])

            confirmed_order_count = len(partner_orders)
            confirmed_order_amount = sum(partner_orders.mapped('amount_total'))
            first_order = (min(partner_orders.mapped('date_order')) if partner_orders else False)
            six_month_check = datetime.now() - timedelta(days=180)

            date_check = bool(not first_order or first_order <= six_month_check)

            if date_check:
                raise ValidationError('Customer doesnt have a sale order confirmed for 6 months')
            if not(confirmed_order_count >= 2):
                raise ValidationError('Customer must have 2 or more confirmed previous orders')
            if not(confirmed_order_amount > 10000):
                raise ValidationError('Customer must have a sale amount of 10000$')

        return super(SaleOrder, self).action_confirm()


