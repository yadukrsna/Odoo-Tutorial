from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    tolerance = fields.Float(string="Tolerance")

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            if move.sale_line_id:
                move.tolerance = move.sale_line_id.tolerance
        return moves