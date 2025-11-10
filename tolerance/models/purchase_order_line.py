from odoo import models, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    tolerance = fields.Float(string="Tolerance")

    def _prepare_purchase_order_line(self, product_qty, product, partner, date_order, fiscal_position, name, price_unit,
                                     taxes, move):
        vals = super()._prepare_purchase_order_line(
            product_qty, product, partner, date_order, fiscal_position, name, price_unit, taxes, move)
        if move.sale_line_id and move.sale_line_id.tolerance:
            vals['tolerance'] = move.sale_line_id.tolerance

        return vals