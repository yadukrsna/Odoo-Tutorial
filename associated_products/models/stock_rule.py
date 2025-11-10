from odoo import models

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values):
        if values.get('set_delivery_uom') and values.get('delivery_uom_id'):
            delivery_uom = self.env['uom.uom'].browse(values['delivery_uom_id'])
            convert_qty = product_uom._compute_quantity(product_qty, delivery_uom)
            product_uom = delivery_uom
            product_qty =  convert_qty

        return super()._get_stock_move_values(product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values)