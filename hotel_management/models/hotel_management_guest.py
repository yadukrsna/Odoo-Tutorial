from odoo import fields,models


class HotelManagementGuest(models.Model):
    _name = 'hotel.management.guest'
    _description = 'Hotel Management Guest'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner')
    is_guest = fields.Boolean('Is Guest')
    hotel_id = fields.Many2one('hotel.management.accommodation')
    partner_age = fields.Integer(related='partner_id.age')
    partner_gender = fields.Selection(related='partner_id.gender')
