from odoo import fields,models


class SimpleBomLine(models.Model):
    _name = 'simple.bom.line'
    _description = 'Simple BOM Line'

    product_id = fields.Many2one('product.product', 'Components', required=True)
    product_qty = fields.Float('Quantity', default=1)
    simple_bom_id = fields.Many2one('simple.mrp.bom', 'Simple BOM')