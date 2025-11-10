from odoo import api,models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.constrains('unit_amount')
    def _check_time_spend(self):
        for record in self:
            # total_time_spend = sum(record.task_id.timesheet_ids.mapped('unit_amount'))
            # if total_time_spend > record.task_id.allocated_hours:
            #     raise ValidationError("Time spend is greater than allocated hours")
            # for record in self:
            working_hours = record.employee_id.resource_calendar_id.hours_per_day
            print(working_hours)
            total_time_spend = sum(self.search([('employee_id', '=', record.employee_id.id),
                                                ('date', '=', record.date)]).mapped('unit_amount'))
            print(total_time_spend)

            if total_time_spend > working_hours:
                raise ValidationError("Working hours exceeding for this date")

