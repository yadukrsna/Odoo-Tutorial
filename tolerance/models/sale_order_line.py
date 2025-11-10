from odoo import api,fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tolerance = fields.Float(string="Tolerance", default=0)

    @api.onchange('product_id')
    def _onchange_product(self):
        tolerance = self.order_id.partner_id.tolerance
        if tolerance:
            self.tolerance = tolerance

