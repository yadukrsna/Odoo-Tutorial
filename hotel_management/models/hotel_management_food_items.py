from odoo import models, fields, api


class HotelManagementFoodItems(models.Model):
    """Used to create and store FOOD ITEMS available in the hotel"""
    _name = "hotel.management.food.items"
    _description = "Hotel Management Food Items"

    name = fields.Char("Name", required=True)
    category_id = fields.Many2one("hotel.management.food.category", "Food Category")
    food_price = fields.Monetary("Price", currency_field='currency_id')
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.ref('base.USD'))
    food_description = fields.Char("Description")
    food_image = fields.Image("Image")
    food_quantity = fields.Integer("Quantity", default=1)
    uom_id = fields.Many2one("uom.uom", "UoM",
                             default=lambda self: self.env.ref('uom.product_uom_unit'))
    order_id = fields.Many2one('hotel.management.order.list')
    product_ids = fields.Many2one('lunch.product')

    def action_open_food(self):
        """Button Action to open form view of food items in order food"""
        self.ensure_one()
        order_food = self.env.context.get('order_id')
        view_id = self.env.ref('hotel_management.hotel_management_food_card').id
        return {
            'name': 'Food Items',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.management.food.items',
            'view_mode': 'form',
            'view_id': view_id,
            'res_id': self.id,
            'target': 'new',
            'context': {
                'default_order_id': order_food,
                'default_name': self.name,
                'default_food_description': self.food_description,
                'default_category_id': self.category_id.id,
                'default_food_quantity': self.food_quantity,
                'default_food_image': self.food_image,
                'default_food_price': self.food_price,
            }
        }

    def action_add_to_list(self):
        """Add selected food item to order list."""
        self.ensure_one()
        order_id = self.env.context.get('order_id')
        order = self.env['hotel.management.order.food'].browse(order_id)
        order.write({
            'order_list_ids': [(0, 0, {
                'food_item_id': self.id,
                'description': self.food_description,
                'quantity': self.food_quantity,
                'price_unit': self.food_price,
                'uom_id': self.uom_id
            })]
        })

    def server_action_lunch(self):
        for record in self:
            self.env['lunch.product'].create({
                'name': record.name,
                'price': record.food_price,
                'description': record.food_description,
                'supplier_id': 5,
                'category_id': 8,
            })
