from odoo import api, models, fields, exceptions
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = 'id desc'

    name = fields.Char("Name", required=True)
    description = fields.Text()
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From",default= datetime.date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Float("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float("Garden Area (sqm)")
    garden_orientation = fields.Selection( [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ])
    buyer = fields.Many2one("res.partner", string="Buyer")
    seller = fields.Many2one("res.users", "Sales Person", default=lambda self:self.env.user)
    active = fields.Boolean(active=False)
    total_area = fields.Float("Total Area (sqm)", compute="_compute_area")
    state = fields.Selection( [
        ('new', 'New'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ],default='new', copy=False)

    property_type = fields.Many2one('estate.property.type', string="Property Type", no_create_edit=True)
    property_tags = fields.Many2many('estate.property.tags')
    property_offers = fields.One2many('estate.property.offers', "property", string="Property Offers")
    best_offers = fields.Float("Best Offer", compute="_compute_best_offers")

    sale_order_id = fields.Many2one('sale.order', 'Sale Order')
    partner_id = fields.Many2one(related='sale_order_id.partner_id')
    product_id = fields.Many2one('product.product')

    product_price = fields.Char('Product Price')

    @api.depends("garden_area", "living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("property_offers.price")
    def _compute_best_offers(self):
        for record in self:
            if record.property_offers:
                record.best_offers = max(record.property_offers.mapped('price'))

            else:
                record.best_offers=0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = ""
            self.garden_area = 0

    def sold_action(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Cancelled Property Cannot be Sold")
            else:
                record.state = 'sold'

            if record.product_id and record.partner_id:
                pricelist = record.partner_id.property_product_pricelist
                price = pricelist._get_product_price(record.product_id, 1, record.partner_id)
                record.product_price = price

    def cancel_action(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Sold Property Cannot be Cancelled")
            else:
                record.state = 'cancelled'


    @api.constrains('selling_price', 'expected_price', 'best_offers')
    def _check_price(self):
        for record in self:
            if record.selling_price<0.0 or record.expected_price<0.0 or record.best_offers<0.0:
                raise ValidationError('Selling Price must be positive')


    @api.constrains('selling_price')
    def _check_price_percentage(self):
        for record in self:
            price_compare = 0.9*record.expected_price
            if float_compare(record.selling_price, price_compare, precision_digits=2) == -1:
                raise ValidationError('Selling Price must be 90% expected Price. Reduce your expected price to accept this offer.')
