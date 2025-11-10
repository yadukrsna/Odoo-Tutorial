from odoo import fields,models

class PosDiscount(models.Model):
    _inherit = 'pos.config'

    discount_type = fields.Selection([('percentage', 'Percentage'), ('amount', 'Amount')],
                                    'POS Discount', default='percentage')

    def get_pos_ui_settings(self):
        res = super().get_pos_ui_settings()
        res['discount_type'] = self.discount_type
        return res


