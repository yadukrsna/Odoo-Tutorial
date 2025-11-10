from odoo import fields,models

class HotelGallery(models.Model):
    _name = 'hotel.gallery'
    _description = 'Hotel Gallery'

    image_1 = fields.Image('Reception')
    image_2 = fields.Image('Corridor')
    image_3 = fields.Image('Pool')
    image_4 = fields.Image('Pool 2')
    image_5 = fields.Image('Garden')
    image_6 = fields.Image('Gym')
    image_7 = fields.Image('room 1')
    image_8 = fields.Image('Room 2')
    image_9 = fields.Image('Room 3')
    image_10 = fields.Image('Room 4')
    image_11 = fields.Image('Room 5')
    image_12 = fields.Image('Room 6')
    image_13 = fields.Image('Food 1')
    image_14 = fields.Image('Food 2')
    image_15 = fields.Image('Food 3')
    image_16 = fields.Image('Food 4')
    image_17 = fields.Image('Food 5')
    image_18 = fields.Image('Food 6')

