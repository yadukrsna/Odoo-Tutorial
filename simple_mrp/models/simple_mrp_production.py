from odoo import api, fields, models
from odoo.exceptions import ValidationError

class SimpleMRPProduction(models.Model):
    _name = 'simple.mrp.production'
    _description = 'Simple MRP Production'

    name = fields.Char('Reference', readonly=True, default='New', required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')], default='draft')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    product_qty = fields.Float('Quantity', default=1)
    simple_bom_id = fields.Many2one('simple.mrp.bom', 'Bill of Material', domain="[('product_id', '=', product_id)]")
    simple_stock_move_ids = fields.One2many('simple.stock.move', 'simple_mrp_id', 'Stock Move')
    simple_mrp_ids = fields.One2many('simple.mrp.production', 'parent_mrp_id', 'Related SMO')
    purchase_order_ids = fields.One2many('purchase.order', 'simple_mrp_id', 'Related PO')
    parent_mrp_id = fields.Many2one('simple.mrp.production', 'Parent MO')
    po_count = fields.Integer(compute='_compute_count')
    smo_count = fields.Integer(compute='_compute_count')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('simple.mrp.production') or 'New'
        return super(SimpleMRPProduction, self).create(vals)

    @api.depends('purchase_order_ids', 'simple_mrp_ids')
    def _compute_count(self):
        for rec in self:
            rec.po_count = len(rec.purchase_order_ids)
            rec.smo_count = len(rec.simple_mrp_ids)

    @api.onchange('simple_bom_id')
    def _onchange_bom_id(self):
        if not self.simple_bom_id:
            self.simple_stock_move_ids = [(5, 0, 0)]
            return

        lines = []
        for line in self.simple_bom_id.simple_bom_line_ids:
            qty = (line.product_qty / self.simple_bom_id.product_qty) * self.product_qty
            lines.append((0, 0, {
                'product_id': line.product_id.id,
                'product_qty': qty,
            }))
        self.simple_stock_move_ids = [(5, 0, 0)] + lines

    def action_confirm(self):
        for order in self.simple_bom_id.simple_bom_line_ids:
            component = order.product_id
            component_qty = (order.product_qty / self.simple_bom_id.product_qty) * self.product_qty
            if component.qty_available < component_qty:
                required_qty = component_qty - component.qty_available
                component_bom = self.env['simple.mrp.bom'].search([('product_id', '=', component.id)])
                if component_bom:
                    component_mrp = self.env['simple.mrp.production'].create({
                        'product_id': component.id,
                        'product_qty': required_qty,
                        'simple_bom_id': component_bom.id,
                        'parent_mrp_id': self.id,
                    })

                    for line in component_mrp.simple_bom_id.simple_bom_line_ids:
                        sub_component = line.product_id
                        sub_component_qty = (line.product_qty / component_mrp.simple_bom_id.product_qty) * component_mrp.product_qty
                        if sub_component.qty_available < sub_component_qty:
                            required_sub_qty = sub_component_qty - sub_component.qty_available
                            vendor = sub_component.seller_ids.partner_id
                            po = self.env['purchase.order'].create({
                                'partner_id': vendor.id,
                                'simple_mrp_id': component_mrp.id
                            })
                            self.env['purchase.order.line'].create({
                                'order_id': po.id,
                                'product_id': sub_component.id,
                                'product_qty': required_sub_qty,
                            })
        self.write({'state': 'confirmed'})

    def action_produce_all(self):
        for order in self.simple_bom_id.simple_bom_line_ids:
            component = order.product_id
            component_qty = (order.product_qty / self.simple_bom_id.product_qty) * self.product_qty
            if component.qty_available < component_qty:
                raise ValidationError("Not enough components to manufacture")
            else:
                self.env['stock.quant']._update_available_quantity(order.product_id, self.env.ref('stock.stock_location_stock'), -component_qty)

        self.env['stock.quant']._update_available_quantity(self.product_id, self.env.ref('stock.stock_location_stock'), self.product_qty)
        self.write({'state': 'done'})

    def action_view_manufacturing(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manufacture',
            'view_mode': 'list,form',
            'res_model': 'simple.mrp.production',
            'domain': [('parent_mrp_id', '=', self.id)],
            'target': 'current'
        }

    def action_view_purchase(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase',
            'view_mode': 'list,form',
            'res_model': 'purchase.order',
            'domain': [('simple_mrp_id', '=', self.id)],
            'target': 'current'
        }

