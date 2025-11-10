from odoo import models


class HotelReport(models.AbstractModel):
    _name = 'report.hotel_management.report_hotel_management'
    _description = 'Hotel Management Report Abstract'

    def _get_report_values(self, docids, data=None):
        return {
            'docs' : data
        }
