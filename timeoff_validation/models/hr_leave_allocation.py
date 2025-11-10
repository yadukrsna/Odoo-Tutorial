from odoo import models
from datetime import date

class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'


    def _allocation_expiry_mail(self):
        leave_allocation = self.search([('date_to', '=', date.today()), ('state', '=', 'validate')])
        for record in leave_allocation:
            template = self.env.ref('timeoff_validation.email_template_allocation', raise_if_not_found=False)
            if template:
                template.send_mail(record.id, force_send=True)