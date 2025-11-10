from odoo import fields,models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pos_credit_limit = fields.Monetary('POS Credit Limit')
    pos_due = fields.Float(string="POS Outstanding")

    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result += ['pos_credit_limit', 'pos_due']
        return result

