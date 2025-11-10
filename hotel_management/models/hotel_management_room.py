from odoo import models, fields


class HotelManagementRoom(models.Model):
    """This model is used to create and store ROOMS in a hotel"""
    _name = "hotel.management.room"
    _description = "Hotel Management Room"

    name = fields.Char("Room No.", required=True)
    bed = fields.Selection([('single', 'Single'), ('double', 'Double'), ('dormitory', 'Dormitory')])
    available_beds = fields.Integer('Available Beds')
    rent = fields.Monetary("Rent", currency_field='currency_id')
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.ref('base.USD'))
    state = fields.Selection([('available', 'Available'), ('not available', 'Not Available')], default='available')
    uom_id = fields.Many2one('uom.uom', string="UoM ", default=lambda self: self.env.ref('uom.product_uom_day'))
    facility_ids = fields.Many2many("hotel.management.facility", string="Facility")
    company_id = fields.Many2one('res.company', 'Company')
    image_1920 = fields.Image('Room Image')
