    # from odoo import fields,models
    #
    #
    # class ResConfigSettings(models.TransientModel):
    #     _inherit = 'res.config.settings'
    #
    #     stock_location_id = fields.Many2one('stock.location', 'Stock Location',
    #                                         config_parameter='web_location_quantity.stock_location_id')
    #
    #
    #
    # from odoo import http
    # from odoo.http import request
    #
    # class WebsiteAddToCart(http.Controller):
    #
    #     @http.route(['/custom_add_to_cart'], type='http', auth='public', website=True)
    #     def custom_add_to_cart(self, **kwargs):
    #         # Render the page
    #         products = request.env['product.template'].sudo().search([('sale_ok', '=', True)])
    #         return request.render('your_module_name.template_add_to_cart_page', {
    #             'products': products,
    #         })
    #
    #     @http.route(['/custom_add_to_cart/submit'], type='http', auth='public', website=True, csrf=True)
    #     def custom_add_to_cart_submit(self, **post):
    #         product_id = int(post.get('product_id'))
    #         quantity = float(post.get('quantity', 1))
    #         product = request.env['product.product'].sudo().search([('product_tmpl_id', '=', product_id)], limit=1)
    #
    #         if not product:
    #             return request.redirec  ('/shop')  # fallback
    #
    #         order = request.website.sale_get_order(force_create=True)
    #         order._cart_update(
    #             product_id=product.id,
    #             add_qty=quantity
    #         )
    #         return request.redirect('/shop/cart')
    # <odoo>
    #     <template id="template_add_to_cart_page" name="Custom Add to Cart Page" inherit_id="website.layout">
    #         <xpath expr="//main" position="inside">
    #             <section class="container my-5">
    #                 <h2>Add Product to Cart</h2>
    #                 <form action="/custom_add_to_cart/submit" method="post">
    #                     <div class="form-group mt-3">
    #                         <label for="product_id">Select Product</label>
    #                         <select name="product_id" id="product_id" class="form-control" required>
    #                             <option value="">-- Choose a product --</option>
    #                             <t t-foreach="products" t-as="product">
    #                                 <option t-att-value="product.id"><t t-esc="product.name"/></option>
    #                             </t>
    #                         </select>
    #                     </div>
    #
    #                     <div class="form-group mt-3">
    #                         <label for="quantity">Quantity</label>
    #                         <input type="number" name="quantity" id="quantity" class="form-control" min="1" value="1" required/>
    #                     </div>
    #
    #                     <div class="form-group mt-4">
    #                         <button type="submit" class="btn btn-primary">Add to Cart</button>
    #                     </div>
    #                 </form>
    #             </section>
    #         </xpath>
    #     </template>
    # </odoo>
# addons/quick_website/controllers/main.py
from odoo import http
from odoo.http import request
import base64

class CustomProductController(http.Controller):

    @http.route(['/custom_product'], type='http', auth='user', website=True)
    def custom_product_page(self, **kwargs):
        """Display the product creation page."""
        return request.render('quick_website.custom_product')

    @http.route(['/custom_create_product/submit'], type='http', auth='user', website=True, csrf=True, methods=['POST'])
    def custom_create_product_submit(self, **post):
        """Handle form submission to create a product visible in shop."""
        name = post.get('name')
        price = float(post.get('price', 0.0))
        description = post.get('description', '')
        image = post.get('image')

        website = request.website

        vals = {
            'name': name,
            'list_price': price,
            'description_sale': description,
            'website_published': True,
            'sale_ok': True,
            'website_id': website.id,  # restrict to current website
        }

        # Handle image upload
        if image and hasattr(image, 'read'):
            vals['image_1920'] = base64.b64encode(image.read())

        # Create product
        request.env['product.template'].sudo().create(vals)

        return request.redirect('/custom_product?success=1')
