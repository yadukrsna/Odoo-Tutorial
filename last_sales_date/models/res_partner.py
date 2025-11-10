from odoo import api, fields, models, Command


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_round_off(self):
        invoice_ids = self.invoice_ids.filtered(lambda s: s.state == 'draft')
        for inv in invoice_ids:
            existing_line = inv.invoice_line_ids.filtered(lambda s: s.product_id == self.env.ref('last_sales_date.round_service_product'))
            total_amount = sum(inv.invoice_line_ids.filtered(lambda s: s.id not in existing_line.ids).mapped('price_subtotal'))

            rounded_total = round(total_amount)
            difference = rounded_total - total_amount

            if existing_line:
                existing_line.price_unit = difference
            else:
                inv.write({
                    'invoice_line_ids': [Command.create({
                            'product_id': self.env.ref('last_sales_date.round_service_product').id,
                            'name': 'Round off',
                            'quantity': 1,
                            'price_unit': difference,
                            'tax_ids': False,
                        })
                    ],
                })


    # # last_sales_date = fields.Date('Last Sale Date')
    # sale_order_quantities = fields.Integer('SO Quantities', compute='_compute_sale_quantities')
    # purchase_order_quantities = fields.Integer('PO Quantities', compute='_compute_sale_quantities')
    #
    # tax_ids = fields.Many2many('account.tax', string='Tax')
    # price = fields.Float('Price')
    # total_amount = fields.Float('Total Amount', compute='_compute_total')
    #
    # product_id = fields.Many2one('product.product', 'Product')
    # sale_order_line_ids = fields.Many2many('sale.order.line', 'order_partner_id', compute='_compute_sale_line')
    # # purchase_order_line_ids = fields.Many2many('purchase.order.line', 'order_partner_id', compute='_compute_sale_line')
    #
    #
    # @api.onchange('product_id')
    # def _compute_sale_line(self):
    #     for record in self:
    #         record.sale_order_line_ids = record.sale_order_ids.mapped('order_line').filtered(lambda s: s.product_id == record.product_id)
    #         # record.sale_order_line_ids = record.purchase_order_ids.mapped('order_line').filtered(lambda s: s.product_id == record.product_id)
    #
    #         # record.sale_order_line_ids = self.env['sale.order.line'].search([('order_id.partner_id', '=', record.id),
    #         #                                                                  ('product_id', '=', record.product_id.id)])
    #         #
    #         # record.purchase_order_line_ids = self.env['purchase.order.line'].search([('order_id.partner_id', '=', record.id),
    #         #                                                                  ('product_id', '=', record.product_id.id)])
    #
    # @api.onchange('tax_ids')
    # def _compute_total(self):
    #     for record in self:
    #         total_tax = record.tax_ids.compute_all(record.price)
    #         record.total_amount = total_tax['total_included']
    #
    # def _compute_sale_quantities(self):
    #     for record in self:
    #         sale_orders = self.env['sale.order'].search([('partner_id', '=', record.id)])
    #
    #         record.sale_order_quantities = sum(sale_orders.mapped('order_line.product_uom_qty'))
    #         purchase_orders = self.env['purchase.order'].search([('partner_id', '=', record.id)])
    #         record.purchase_order_quantities = sum(purchase_orders.mapped('order_line.product_qty'))

    # quantity = fields.Float('Quantity')
    # current_uom_id = fields.Many2one('uom.uom', 'Current UOM')
    # current_category_id = fields.Many2one('uom.category', compute="_compute_category")
    # target_uom_id = fields.Many2one('uom.uom', 'Target UOM', domain="[('category_id', '=', current_category_id)]")
    # converted_quantity = fields.Float('Converted Quantity', compute='_compute_converted_quantity')
    #
    # @api.depends('current_uom_id')
    # def _compute_category(self):
    #     self.current_category_id = self.current_uom_id.category_id
    #     print(self.current_category_id)
    #
    # @api.depends('target_uom_id', 'quantity')
    # def _compute_converted_quantity(self):
    #     print("FFFF")
    #     print(self.current_category_id.name)
    #     print(self.current_uom_id.category_id.name)
    #     self.converted_quantity = self.current_uom_id._compute_quantity(self.quantity, self.target_uom_id)
    #
