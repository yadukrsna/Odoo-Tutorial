from . import models
from . import wizard
from . import report
from . import controller

def create_hotel_management_values(env):
    facility_a = env['hotel.management.facility'].create({
        'name': 'A/C'
    })
    facility_b = env['hotel.management.facility'].create({
        'name': 'Wash Room'
    })
    facility_c = env['hotel.management.facility'].create({
        'name': 'Hot Water'
    })
    facility_d = env['hotel.management.facility'].create({
        'name': 'Wifi'
    })
    env['hotel.management.room'].create({
        'name': '101A',
        'facility_ids' : [(6, 0, [facility_a.id, facility_b.id, facility_c.id, facility_d.id])],
        'bed': 'double',
        'rent': '1200',
        'image_1920': 'hotel_management/static/src/img/room1.jpg'
        })
    env['hotel.management.room'].create({
        'name': '101B',
        'facility_ids': [(6, 0, [facility_a.id, facility_b.id, facility_d.id])],
        'bed': 'single',
        'rent': '1000',
        'image_1920': 'hotel_management/static/src/img/room2.jpg'
    })
    env['hotel.management.room'].create({
        'name': '101C',
        'facility_ids': [(6, 0, [facility_b.id, facility_c.id, facility_d.id])],
        'bed': 'dormitory',
        'available_beds': 5,
        'rent': '800',
    })
