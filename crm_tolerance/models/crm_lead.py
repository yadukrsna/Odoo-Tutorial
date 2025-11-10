from odoo import fields,models
from datetime import datetime, timedelta


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _archive_lead(self):
        tolerance_time = int(self.env['ir.config_parameter'].sudo().get_param('crm_tolerance.crm_tolerance_time'))
        leads = self.env['crm.lead'].search([])

        for lead in leads:
            message = self.env['mail.message'].search([('res_id', '=', lead.id),
                                                       ('model', '=', 'crm.lead')], order="date desc", limit=1)

            last_message = fields.Datetime.from_string(message.date)
            if(datetime.now() - last_message) > timedelta(minutes=tolerance_time):
                lead.action_archive()