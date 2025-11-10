from odoo import fields, models
import json

class ProductProduct(models.Model):
    _inherit = ["product.product"]

    pos_quantities = fields.Char(compute="_compute_stock_quantities")

    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result += ["pos_quantities"]
        return result

    def _compute_stock_quantities(self):
        icp_sudo = self.env["ir.config_parameter"].sudo()
        param = icp_sudo.get_param("pos_extension.stock_location_ids")
        location_ids = json.loads(param) if param else []

        locations = self.env["stock.location"].browse(location_ids)

        for product in self:
            qty_info = []
            for loc in locations:
                quant = self.env['stock.quant'].search(
                    [('product_id', '=', product.id), ('location_id', '=', loc.id)])
                qty = quant.quantity
                if qty > 0:
                    qty_info.append(f"{loc.display_name}: {qty}\n")
            product.pos_quantities = " ".join(qty_info)

    from odoo import fields, models

    class Website(models.Model):
        _inherit = 'website'

        stock_location_id = fields.Many2one(
            'stock.location',
            string='Website Stock Location',
            domain=[('usage', '=', 'internal')],
            help="Select a stock location whose quantities will be shown on the website."
        )


from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def format_product_stock_values(self, product, wh_id=None, free_qty=None):
        """Override: Show website stock based on website's configured location."""
        website = self.env['website'].get_current_website()
        location = website.stock_location_id

        if product.is_product_variant and location:
            # Get free qty only from that location
            if free_qty is None:
                qty_data = self.env['stock.quant'].sudo().read_group(
                    [('product_id', '=', product.id), ('location_id', '=', location.id)],
                    ['quantity:sum'],
                    []
                )
                free_qty = qty_data and qty_data[0].get('quantity', 0.0) or 0.0

            # Reuse Odoo’s built-in availability flags
            return {
                'in_stock': free_qty > 0,
                'show_quantity': product.show_availability and product.available_threshold >= free_qty,
                'quantity': free_qty,
            }

        # fallback to normal behavior
        return super().format_product_stock_values(product, wh_id=wh_id, free_qty=free_qty)

