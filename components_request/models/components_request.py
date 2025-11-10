from odoo import api, fields, models
from datetime import timedelta

class ComponentsRequest(models.Model):
    _name = 'components.request'
    _rec_name = 'employee_id'
    _description = 'Components Request'

    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    product_ids = fields.One2many('product.line', 'components_id', required=True)
    total = fields.Float('Total', compute='_compute_total')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.USD'))
    state = fields.Selection([('to submit', 'To Submit'), ('submitted', 'Submitted'),
                              ('approval head', 'Approved By Manager'), ('approved', 'Approved By Head'),('rejected', 'Rejected')],
                             default='to submit')

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    @api.depends('product_ids')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.subtotal for record in record.product_ids)

    def action_user_submit(self):
        self.state = 'submitted'
        self.sale_order_id.state = 'sale'

    def action_manager_approval(self):
        self.state = 'approval head'

    def action_head_approval(self):
        self.state = 'approved'
        for record in self:
            for line in record.product_ids:
                if line.route == 'purchase' and line.product_id:
                    for vendor in line.vendor_ids:
                        purchase_order = self.env['purchase.order'].create({
                            'partner_id': vendor.id,
                        })

                        self.env['purchase.order.line'].create({
                            'order_id': purchase_order.id,
                            'product_id': line.product_id.id,
                            'name': line.product_id.name,
                            'product_qty': line.quantity,
                            'price_unit': line.unit_price,
                        })

                if line.route == 'internal':
                    picking = self.env['stock.picking'].create({
                        'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                        'location_id': self.env.ref('stock.stock_location_stock').id,
                        'location_dest_id': self.env.ref('components_request.component_warehouse_location').id,
                        })

                    self.env['stock.move'].create({
                        'name': line.product_id.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'location_id': picking.location_id.id,
                        'location_dest_id': picking.location_dest_id.id,
                        'picking_id': picking.id,
                    })

    def action_head_rejection(self):
        self.state = 'rejected'
