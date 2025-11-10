from odoo import api, fields, models


class ProductLine(models.Model):
    _name = 'product.line'
    _description = 'Product Line'

    components_id = fields.Many2one('components.request', 'Components Request')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    unit_price = fields.Float(related='product_id.lst_price', string='Unit Price')
    quantity = fields.Integer('Quantity', default=1)
    route = fields.Selection([('purchase', 'Purchase Order'), ('internal', 'Internal Transfer')],
                             required=True)
    vendor_ids = fields.Many2many('res.partner', string='Vendors')
    subtotal = fields.Float('Sub Total', compute='_compute_subtotal')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.USD'))

    @api.depends('unit_price', 'quantity')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.onchange('route')
    def _onchange_vendor(self):
        for record in self:
            if record.route == 'purchase':
                record.vendor_ids = record.product_id.seller_ids.partner_id
            else:
                record.vendor_ids = False
