from odoo import _,models
from datetime import date
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for line in self:
            expiry_date = self.env['stock.move.line'].search


        return super().button_validate()