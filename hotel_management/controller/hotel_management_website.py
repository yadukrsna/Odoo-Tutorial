from odoo import Command, http
from odoo.http import request
from datetime import datetime
import json


class WebsiteHotelForm(http.Controller):
    @http.route(['/hotel_room'], type='json', auth='public', website=True, csrf=False)
    def get_hotel_room(self):
        rooms = request.env['hotel.management.room'].sudo().search([])
        room_data = []
        for room in rooms:
            room_data.append({
                'id': room.id,
                'name': room.name,
                'image_1920': room.image_1920,
                'bed': room.bed.title(),
                'rent': "{:,.2f}".format(room.rent),
                'state': room.state.title(),
                'available': room.available_beds,
                'currency_symbol': room.currency_id.symbol,
                'facilities': room.facility_ids.mapped('name'),
            })
        return room_data

    @http.route(['/hotel_gallery'], type='json', auth='public', website=True, csrf=False)
    def hotel_gallery(self):
        images = request.env['hotel.gallery'].sudo().search([])
        image_data = []

        for image in images:
            for i in range(1, 19):
                img = getattr(image, f'image_{i}')
                if img:
                    image_data.append({'image': img})
        return image_data

    @http.route(['/hotel/accommodation'], type='http', auth='public', website=True, csrf=False)
    def create_accommodation(self, **post):
        guest_number = int(post.get('guest_number'))
        hotel_facility = request.httprequest.form.getlist('facility[]')
        facility_ids = []
        order = []
        for facility in hotel_facility:
            if facility:
                facility_ids.append(int(facility))
        if guest_number >= 2:
            guest_ids = request.httprequest.form.getlist('guest_ids[]')
            for guest in range(len(guest_ids)):
                if guest_ids[guest]:
                    order.append({
                        'partner_id': int(guest_ids[guest]),
                    })
        check_in_str = post.get("check_in")
        if check_in_str:
            check_in_dt = datetime.strptime(check_in_str, "%Y-%m-%dT%H:%M")
            request.env['hotel.management.accommodation'].sudo().create({
                'guest_id': request.env.user.partner_id.id,
                'bed_type': post.get('bed'),
                'check_in': check_in_dt,
                'guest_number': guest_number,
                'expected_days': post.get('expected_days'),
                'other_guest_ids': [Command.create(rec) for rec in order],
                'facility_id': [(6, 0, facility_ids)],
                'website_id': request.website.id
            })
        return request.redirect('/contactus-thank-you')

    @http.route(['/hotel/order'], type='http', auth="user", website=True, csrf=False)
    def portal_food_order(self, **kwargs):
        if request.httprequest.method == 'POST':
            data = json.loads(request.httprequest.data)
            cart = data.get("cart")
            if cart:
                partner = request.env.user.partner_id
                accommodation = request.env['hotel.management.accommodation'].sudo().search([
                    ('guest_id', '=', partner.id)
                ])

                if accommodation:
                    order = request.env['hotel.management.order.food'].sudo().create({
                        'accommodation_id': accommodation.id,
                    })
                    for item in cart:
                        request.env['hotel.management.order.list'].sudo().create({
                            'order_id': order.id,
                            'food_item_id': int(item['id']),
                            'quantity': int(item['qty']),
                        })
                    return request.redirect('/contactus-thank-you')

        items = request.env['hotel.management.food.items'].sudo().search([])
        food_item = [{
            'id': item.id,
            'food': item.name,
            'image': item.food_image,
            'description': item.food_description,
            'price': item.food_price,
            'category': item.category_id.name if item.category_id else '',
            'currency_symbol': item.currency_id.symbol if item.currency_id else '',
        } for item in items]

        return request.render("hotel_management.portal_hotel_food_order", {'food': food_item})
