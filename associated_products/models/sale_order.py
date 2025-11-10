from odoo import api,Command,fields,models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    associated_products = fields.Boolean('Associated Products')
    delivery_uom = fields.Boolean('Set Delivery UOM')

    @api.onchange('associated_products')
    def _onchange_associated_product(self):
        self.ensure_one()
        if self.associated_products:
            order_lines = []
            for order in self.partner_id.associated_products:
                order_lines.append(Command.create({
                    'product_id': order.product_variant_id.id,
                    'product_uom_qty': 1,
                    'price_unit': order.list_price,
                }))

            self.order_line = order_lines

