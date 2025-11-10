from odoo import api,fields,models


class SimpleBom(models.Model):
    _name = 'simple.mrp.bom'
    _description = 'Simple BOM'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', 'Product', required=True)
    product_qty = fields.Float('Quantity', default=1)
    simple_bom_line_ids = fields.One2many('simple.bom.line', 'simple_bom_id','Simple BOM Line')
