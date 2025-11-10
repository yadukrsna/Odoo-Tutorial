from odoo import api,fields,models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    state = fields.Selection([('onboarding', 'Onboarding'), ('offboarding', 'Offboarding')], compute="_compute_state", store=True)

    @api.depends('resource_calendar_id')
    def _compute_state(self):
        print("jjj")
        if self.resource_calendar_id:
            self.write({
                'state':'onboarding'
            })
            self.action_unarchive()
        else:
            self.write({
              'state':'offboarding'
            })
            self.action_archive()



    # transfer_requested = fields.Boolean(default=False)
    # transfer_company_id = fields.Many2one('res.company')
    #
    # def action_employee_transfer(self):
    #
    #     return {
    #         'type':'ir.actions.act_window',
    #         'name':'Employee Transfer',
    #         'res_model':'employee.transfer.wizard',
    #         'view_mode':'form',
    #         'target':'new',
    #         'context':{
    #             'default_employee_id': self.id,
    #             'default_current_company_id': self.company_id.id,
    #         }
    #     }
    #
    # def action_approve_transfer(self):
    #     self.ensure_one()
    #
    #     new_company = self.transfer_company_id
    #     self.write({
    #         'company_id': new_company.id,
    #         'transfer_company_id': False,
    #     })
    #
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Employees',
    #         'res_model': 'hr.employee',
    #         'view_mode': 'kanban',
    #         'domain': [('company_id', '=', self.env.company.id)],
    #         'target': 'main',
    #     }
    #
    #