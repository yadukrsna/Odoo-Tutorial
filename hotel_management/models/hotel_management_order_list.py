from odoo import fields,models,api


class HotelManagementOrderList(models.Model):
    _name = "hotel.management.order.list"
    _description = "Order List"

    order_id = fields.Many2one('hotel.management.order.food', string="Order")
    food_item_id = fields.Many2one('hotel.management.food.items', string="Description", required=True)
    description = fields.Char(related='food_item_id.food_description', string="Food Description")
    quantity = fields.Integer(string="Quantity", default=1)
    price_unit = fields.Monetary(string="Unit Price", related='food_item_id.food_price', store=True)
    currency_id = fields.Many2one('res.currency', related='order_id.currency_id', store=True)
    subtotal = fields.Monetary(string="Subtotal", compute="_compute_subtotal", store=True)
    uom_id = fields.Many2one("uom.uom", "UoM", related="food_item_id.uom_id")

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        """Function to compute subtotal of each item"""
        for line in self:
            line.subtotal = line.quantity * line.price_unit