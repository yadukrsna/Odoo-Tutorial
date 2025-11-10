from odoo import models,fields,api


class HotelManagementDashboard(models.Model):
    _name = 'hotel.management.dashboard'
    _description = 'Hotel Management Dashboard'

    accommodation_id = fields.Many2one('hotel.management.accommodation',"Accommodation")

    @api.model
    def get_values(self):
        data = self.search([])
        return data.read(['accommodation_id'])
