from odoo import _,fields,api,models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_due_amount = fields.Monetary(string="Customer Due", currency_field='currency_id',
                                         compute="_compute_partner_due_amount")

    @api.depends('partner_id.due_amount')
    def _compute_partner_due_amount(self):
        for order in self:
            if order.partner_id and order.partner_id.due_amount > 0.0:
                order.partner_due_amount = order.partner_id.due_amount
            else:
                order.partner_due_amount = 0.0


    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id.active_credit_limit:
            due = self.partner_id.due_amount or 0.0
            warning = self.partner_id.warning_amount or 0.0
            block = self.partner_id.block_limit or 0.0

            if block > 0.0 and due >= block:
                raise ValidationError(_(
                    "The customer have exceeded credit limit"
                ))
            elif warning > 0.0 and due >= warning:
                message = _(
                    "WARNING: Customer Limit Approaching"
                )
                return {
                    'warning': {
                        'title': _("Credit Limit Warning"),
                        'message': message
                    }
                }


