from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        icp = self.env['ir.config_parameter'].sudo()
        discount_type = icp.get_param('ecommerce_discount.ecommerce_discount_type', 'percent')
        discount_value = float(icp.get_param('ecommerce_discount.ecommerce_discount'))
        for order in self:
            if order.website_id:
                for line in order.order_line:
                    if line.is_delivery or line.display_type:
                        continue
                    if line.discount_applied == False:
                        if discount_type == 'percentage' and line.discount == 0.0:
                            print("Perper")
                            line.discount = discount_value
                        elif discount_type == 'amount' and line.discount == 0.0:
                            print('amtamt')
                            line.price_unit = (line.price_unit - discount_value)
                        line.discount_applied = True
        return res
