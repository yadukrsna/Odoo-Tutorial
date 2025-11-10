from odoo import models, fields


class HotelManagementFacility(models.Model):
    """Used to create and store FACILITIES of a hotel room offered to the CUSTOMER"""
    _name = 'hotel.management.facility'
    _description = 'Hotel Management Facility'

    name = fields.Char("Facility Name", required=True)
    color = fields.Float('color')
