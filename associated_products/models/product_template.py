from odoo import fields,models

class ProductProduct(models.Model):
    _inherit = 'product.template'

    delivery_uom_id = fields.Many2one('uom.uom', 'Deliver UOM', domain="[('category_id', '=', uom_category_id)]")
