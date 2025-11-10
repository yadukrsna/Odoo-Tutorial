from odoo import api,fields,models


class ResourcePartner(models.Model):
    _inherit = 'res.partner'

    associated_products = fields.Many2many('product.template', relation='partner_associated_product_rel',
                                           string='Associated Products')

    state = fields.Selection([('customer', 'Customer'), ('vendor', 'Vendor'), ('both', 'Both'), ('none', 'None')], 'State',
                             compute='_compute_partner_state')

    def _compute_partner_state(self):
        for record in self:
            if record.customer_rank > 0 and record.supplier_rank > 0:
                record.state = 'both'
            elif record.customer_rank > 0:  
                record.state = 'customer'
            elif record.supplier_rank > 0:
                record.state = 'vendor'
            else:
                record.state = 'none'
