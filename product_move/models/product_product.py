from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.product'

    quantity = fields.Float('Quantity')
    current_uom_id = fields.Many2one('uom.uom', 'Current UOM')
    current_category_id = fields.Many2one('uom.category', related='current_uom_id.category_id')
    target_uom_id = fields.Many2one('uom.uom', 'Target UOM', domain=lambda self: [('category_id', '=', self.current_category_id)])
    converted_quantity = fields.Float('Converted Quantity', compute='_compute_converted_quantity')

    def _compute_converted_quantity(self):
        print("FFFF")
        print(self.current_category_id.name)
        print(self.current_uom_id.category_id.name)
        self.converted_quantity = self.current_uom_id._compute_quantity(self.quantity, self.target_uom_id)