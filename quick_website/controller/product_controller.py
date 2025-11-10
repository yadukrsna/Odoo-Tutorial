import base64

from odoo import http
from odoo.http import request

class ProductController(http.Controller):
    @http.route(['/custom_product'], type='http', auth='public', website=True)
    def custom_product_page(self, **kwargs):
        return request.render('quick_website.custom_product')
    @http.route(['/custom_create_product/submit'], type='http', auth='public', website=True, csrf=True, methods=['POST'])
    def custom_product_submit(self, **post):
        name = post.get('name')
        price = float(post.get('price'))
        image = post.get('image')

        website = request.website

        vals = {
            'name': name,
            'list_price': price,
            'website_id': website.id,
            'website_published': True,
            'image_1920': base64.b64encode(image.read())
        }
        print(post)
        print(image)
        request.env['product.template'].sudo().create(vals)

        return request.redirect('/custom_product?success=1')


