from odoo import models, fields, api


class HotelManagementOrderFood(models.Model):
    """This Model generated order for accommodations"""
    _name = "hotel.management.order.food"
    _description = "Hotel Management Order Food"
    _rec_name = "accommodation_id"

    accommodation_id = fields.Many2one('hotel.management.accommodation', required=True,
                                       string="Accommodation", store=True, ondelete="cascade")
    room_id = fields.Many2one('hotel.management.room', compute='_compute_room_id', store=True)
    guest_id = fields.Many2one("res.partner", string="Guest", related='accommodation_id.guest_id',
                               readonly=True, store=True)
    order_time = fields.Datetime("Order Time", default=lambda self: fields.Datetime.now(), store=True)
    category_ids = fields.Many2many("hotel.management.food.category", string="Food Category")
    food_items_ids = fields.Many2many("hotel.management.food.items", compute="_compute_items")
    order_list_ids = fields.One2many('hotel.management.order.list', 'order_id', store=True)
    total_amount = fields.Monetary(string="Total", compute="_compute_total", store=True, currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.ref('base.USD'))
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft', store=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company.id)

    @api.depends('accommodation_id')
    def _compute_room_id(self):
        for record in self:
            record.room_id = record.accommodation_id.room_id

    @api.depends('category_ids')
    def _compute_items(self):
        """Function to select food items based on their categories"""
        for record in self:
            if record.category_ids:
                record.food_items_ids = self.env['hotel.management.food.items'].search(
                    [('category_id', 'in', record.category_ids.ids)])
            else:
                record.food_items_ids = False

    @api.depends('order_list_ids.subtotal')
    def _compute_total(self):
        """Function to compute total amount in each order"""
        for record in self:
            record.total_amount = sum(line.subtotal for line in record.order_list_ids)

    def action_confirm_order(self):
        """Button Action to Confirm Orders"""
        restaurant_cost_product = self.env.ref('hotel_management.default_hotel_management_product_restaurant')
        for record in self:
            record.state = 'confirmed'
            record.accommodation_id.write({
                'payment_ids': [(0, 0, {
                    'product_id': restaurant_cost_product.id,
                    'quantity': 1,
                    'unit_price': self.total_amount,
                    'uom_id': self.env.ref('uom.product_uom_unit').id
                })]
            })
