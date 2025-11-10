from odoo import fields, models


class HotelManagementFoodCategory(models.Model):
    """Used to create and store CATEGORIES of FOOD ITEMS available in the hotel"""
    _name = 'hotel.management.food.category'
    _description = 'Hotel Management Food Category'

    name = fields.Char("Food Category", required=True)
