from odoo import models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_procurement_values(self, group_id=False):
        res = super()._prepare_procurement_values(group_id=group_id )

        if self.order_id.delivery_uom and self.product_id.delivery_uom_id:
            res.update({
                'set_delivery_uom':True,
                'delivery_uom_id': self.product_id.delivery_uom_id.id
            })
        return res

        # delivery_uom = self.product_id.delivery_uom_id

        # 'product_uom': delivery_uom.id,
        # 'product_qty': self.product_uom._compute_quantity(self.product_uom_qty, delivery_uom)
        # })
        # else:
        #     res.update({
        #         'product_uom': self.product_uom.id,
        #         'product_qty': self.product_uom_qty
        #     })