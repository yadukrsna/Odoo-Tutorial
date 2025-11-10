from odoo import api, fields,models
from odoo.exceptions import ValidationError

class ProjectProject(models.Model):
    _inherit = 'project.task'

    @api.constrains('user_ids')
    def _check_assignees(self):
        if len(self.user_ids) > 1:
            raise ValidationError("Cannot add another assignee")



   # project_progress = fields.Float('Progress', compute='_compute_project_progress', store=True)
    # @api.depends('task_ids.stage_id')
    # def _compute_project_progress(self):
    #     for project in self:
    #         total_tasks = self.env['project.task'].search_count([('project_id', '=', project.id)])
    #         print(total_tasks)
    #
    #         completed_tasks = self.env['project.task'].search_count([
    #             ('project_id', '=', project.id),
    #             (''),
    #             ('stage_id.name', '=', 'Done')
    #         ])
    #         print(completed_tasks)
    #         project.project_progress = (completed_tasks / total_tasks) * 100
    #         print(project.project_progress)



