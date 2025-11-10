from odoo import fields,models


class SimpleStockMove(models.Model):
    _name = 'simple.stock.move'
    _description = 'Simple Stock Move'

    product_id = fields.Many2one('product.product', 'Product')
    product_qty = fields.Integer('Quantity')
    simple_mrp_id = fields.Many2one('simple.mrp.production', 'MRP Production')