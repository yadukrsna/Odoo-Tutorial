from odoo import fields,models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one('sale.order', 'Sale Order', domain="[('state', '!=', 'cancel')]")

    def button_confirm(self):
        res = super().button_confirm()
        for order in self:
            if order.sale_order_id:
                other_rfq = self.search([('sale_order_id', '=', order.sale_order_id.id), ('id', '!=', order.id)])
                if other_rfq:
                    other_rfq.button_cancel()
        return res