from odoo import models,_

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _check_tolerance_range(self):
        for move in self.move_ids:
            if not move.tolerance or not move.sale_line_id:
                continue

            ordered_qty = move.sale_line_id.product_uom_qty
            tolerance = move.tolerance
            min_qty = tolerance - ordered_qty
            max_qty = ordered_qty + tolerance

            demand_qty = move.product_uom_qty

            if demand_qty < min_qty or demand_qty > max_qty:
                return self._show_tolerance_warning(move, min_qty, max_qty, demand_qty)
        return False

    def _show_tolerance_warning(self, move, min_qty, max_qty, demand_qty):
        view_id = self.env.ref('tolerance.tolerance_warning_wizard_view').id
        return {
            'name': _('Tolerance Warning'),
            'type': 'ir.actions.act_window',
            'res_model': 'tolerance.warning.wizard',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'context': {
                'default_picking_id': self.id,
                'default_move_id': move.id,
                'default_min_qty': min_qty,
                'default_max_qty': max_qty,
                'default_demand_qty': demand_qty,
            }
        }

    def button_validate(self):
        self.ensure_one()
        if not self.env.context.get('tolerance_accepted'):
            action = self._check_tolerance_range()
            if action:
                return action
        return super().button_validate()
