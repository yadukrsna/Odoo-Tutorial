from email.policy import default

from odoo import fields,models


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    ecommerce_discount_type = fields.Selection([('percentage', 'Percentage'), ('amount', 'Amount')], 'Discount Type',
                                               config_parameter="ecommerce_discount.ecommerce_discount_type", default='percentage')
    ecommerce_discount = fields.Float('Ecommerce Discount', default=0,
                                      config_parameter="ecommerce_discount.ecommerce_discount")
