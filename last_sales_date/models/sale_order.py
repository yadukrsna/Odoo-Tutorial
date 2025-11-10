from odoo import _,fields,models
from datetime import date
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # def action_confirm(self):
    #     for order in self:
    #         partner = order.partner_id
    #
    #         overdues = self.env['account.move'].search_count([
    #             ('partner_id', '=', partner.id),
    #             ('payment_state', '=', 'not_paid')
    #         ])
    #         print(overdues)
    #         if overdues > 0:
    #             raise Warning('Customer has Overdues')
    #
    #         if partner.last_sales_date:
    #             days_since_last_sale = (date.today() - partner.last_sales_date).days
    #             if days_since_last_sale >= 90:
    #                 raise ValidationError(
    #                     _("Customer’s last sale was %d days ago.")%days_since_last_sale
    #                 )
    #         else:
    #             raise ValidationError(
    #                 _("Customer doesn't have any previous sale order")
    #             )
    #
    #         partner.last_sales_date = fields.Date.context_today(order)
    #         return super(SaleOrder, order).action_confirm()

    def server_action_uom_change(self):
        uom_dozen = self.env['uom.uom'].search([('name', '=', 'Dozens')])
        sale_order = self.env['sale.order'].search([('state', '=', 'draft')])

        sale_order.mapped('order_line').write({'product_uom': uom_dozen.id})


        print(sale_order)
        # self.mapped('order_line').write({'product_uom': uom_dozen.id})

        print(uom_dozen)
        print(self.order_line.product_uom)

        # uom_unit = self.env['uom.uom'].search([('name', '=', 'Dozen')], limit=1)
        # sale_orders = self.env['sale.order'].search([('state', '=', 'draft')])
        # for record in sale_orders:
        #     for line in record.order_line:
        #         if uom_dozen.category_id == line.product_id.uom_id.category_id:
        #             new_qty = line.product_uom_qty / 12
        #             line.write({'product_uom': uom_dozen.id, 'product_uom_qty': new_qty})
        #             line._compute_price_unit()
        #             line._compute_tax_id()
        #             line._compute_amount()
        #
        #     print("DONE")
