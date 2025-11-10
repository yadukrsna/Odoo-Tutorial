from odoo import models, fields, api

class HotelManagementPayment(models.Model):
    """This model creates payment details of accommodations"""
    _name = 'hotel.management.payment'
    _description = 'Hotel Management Payment'

    accommodation_id = fields.Many2one('hotel.management.accommodation', ondelete="cascade")
    order_list_ids = fields.Many2one('hotel.management.order.list')
    product_id = fields.Many2one('product.product', 'Product Description')
    quantity = fields.Integer('Quantity')
    uom_id = fields.Many2one('uom.uom', 'UoM')
    unit_price = fields.Monetary('Unit Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.INR'))
    subtotal = fields.Monetary('Sub Total', compute='_compute_subtotal', currency_field='currency_id')

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        """Function to compute subtotal of each order"""
        for record in self:
            record.subtotal = record.quantity * record.unit_price

