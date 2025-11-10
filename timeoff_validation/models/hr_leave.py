from odoo import api,models
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def action_approve(self):

        last_leave = self.search([('employee_id', '=', self.employee_id.id), ('holiday_status_id', '=', self.holiday_status_id.id),
                                  ('state', '=', 'validate')], order='request_date_from desc', limit=1)
        if last_leave:
            leave_gap = self.request_date_from - last_leave.request_date_from
            if leave_gap.days < 30:
                raise ValidationError('Already spend this type of leave in 30 days')

        return super(HrLeave, self).action_approve()




