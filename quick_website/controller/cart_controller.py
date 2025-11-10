from odoo import http
from odoo.http import request

class CartController(http.Controller):

    @http.route(['/custom_add_cart'], type='http', auth='public', website=True)
    def custom_add_cart(self, **kwargs):
        products = request.env['product.template'].sudo().search([])
        return request.render('quick_website.product_page', {
            'products': products
        })

    @http.route(['/custom_add_cart/submit'], type='http', auth='public', website=True, csrf=True)
    def custom_cart_submit(self, **post):
        product_id = int(post.get('product_id'))
        quantity = float(post.get('quantity'))



        product = request.env['product.product'].sudo().search([('product_tmpl_id', '=', product_id)], limit=1)
        if not product:
            return request.redirect('/custom_add_cart')

        order = request.website.sale_get_order(force_create=True)
        order._cart_update(product_id=product.id, add_qty=quantity)

        return request.redirect('/shop/cart')
