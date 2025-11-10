from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project', string='Projects', domain="[('partner_id', '=', partner_id)]")
    task_ids = fields.One2many('project.task', 'sale_order_id', 'Related Tasks')
    task_created = fields.Boolean(default=False)

    def action_create_task(self):
        for order in self:
            if order.task_created:
                raise UserError("Tasks have already been created for this order.")

            if not order.project_id:
                raise UserError("Please select a project before creating tasks.")

            main_task = self.env['project.task'].create({
                'name': f"SO/{order.name} - {order.partner_id.name}",
                'project_id': order.project_id.id,
                'sale_order_id': order.id,
                'description': f"Created from Sale Order {order.name}\n Customer: {order.partner_id.name}\n Total: {order.amount_total}"
            })

            subtotals = order.order_line.mapped('price_subtotal')
            avg_subtotal = sum(subtotals) / len(subtotals) if subtotals else 0

            for line in order.order_line:
                priority = '1' if line.price_subtotal >= avg_subtotal else '0'

                self.env['project.task'].create({
                    'name': f"{line.product_id.display_name} - Qty: {line.product_uom_qty}",
                    'parent_id': main_task.id,
                    'project_id': order.project_id.id,
                    'sale_order_id': order.id,
                    'priority': priority,
                    'description': f"Product: {line.product_id.display_name}\nQuantity: {line.product_uom_qty}\nSubtotal: {line.price_subtotal}",
                })
            order.task_created = True

    def action_view_tasks(self):
        self.ensure_one()
        return {
            'name': 'Tasks',
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'list,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {'default_sale_order_id': self.id}
        }
