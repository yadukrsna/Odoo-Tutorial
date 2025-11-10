from odoo import fields,models


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    threshold = fields.Float('Product Threshold', config_parameter='product_threshold.threshold')