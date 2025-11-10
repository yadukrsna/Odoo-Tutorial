from odoo import fields,models
import json

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    stock_location_ids = fields.Many2many('stock.location', string='Stock Locations')
    pos_discount_type = fields.Selection(related='pos_config_id.discount_type', readonly=False)

    def set_values(self):
        res = super().set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'pos_extension.stock_location_ids', json.dumps(self.stock_location_ids.ids)
        )
        return res

    def get_values(self):
        res = super().get_values()
        icp = self.env['ir.config_parameter'].sudo()
        value = icp.get_param('pos_extension.stock_location_ids')
        location_ids = json.loads(value) if value else []
        res.update(
            stock_location_ids=[(6, 0, location_ids)]
        )
        return res
