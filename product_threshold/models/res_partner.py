from odoo import fields,models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_ids =  fields.Many2many('product.product', 'Products')

    def action_recalculate(self):
        self.ensure_one()

        threshold = self.env['ir.config_parameter'].sudo().get_param('product_threshold.threshold')
        threshold = float(threshold)

        partner_so = self.env['sale.order.line'].search([('order_partner_id', '=', self.id), ('order_id.state', '=', 'sale')])

        products_to_add = []
        for line in partner_so:
            if line.product_uom_qty >= threshold and line.product_id.id not in products_to_add:
                products_to_add.append(line.product_id.id)

        if products_to_add:
            self.product_ids = [(6, 0, products_to_add)]


    def action_create_so(self):
        self.ensure_one()
        if not self.product_ids:
            raise UserError("No Products Selected")

        threshold = self.env['ir.config_parameter'].sudo().get_param(
            'product_threshold.threshold')
        threshold = float(threshold)

        sale_order = self.env['sale.order'].create({
            'partner_id': self.id,
            'state': 'draft',
        })

        for product in self.product_ids :
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': product.id,
                'product_uom_qty': threshold,
                'price_unit': product.list_price,
            })
