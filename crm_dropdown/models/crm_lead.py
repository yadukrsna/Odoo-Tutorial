from odoo import models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_available_salesperson(self):
        salesperson = self.env['res.users'].search([('active', '=', True)])

        salesperson_ids = self.search([]).mapped('user_id').ids
        salesperson = salesperson.filtered(lambda u: u.id in salesperson_ids)

        return [{'id': sp.id, 'name': sp.name} for sp in salesperson]
