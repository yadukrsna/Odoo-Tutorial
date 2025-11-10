from odoo import models, fields

class ToleranceWarningWizard(models.TransientModel):
    _name = 'tolerance.warning.wizard'
    _description = 'Tolerance Quantity Warning'

    picking_id = fields.Many2one('stock.picking')
    move_id = fields.Many2one('stock.move')
    min_qty = fields.Float("Minimum Allowed Quantity")
    max_qty = fields.Float("Maximum Allowed Quantity")
    demand_qty = fields.Float("Actual Quantity")

    message = fields.Text("Message", default="The demand quantity for product is outside the allowed range.")

    def action_accept(self):
        return self.picking_id.with_context(tolerance_accepted=True).button_validate()

    def action_dont_accept(self):
        return {'type': 'ir.actions.act_window_close'}
