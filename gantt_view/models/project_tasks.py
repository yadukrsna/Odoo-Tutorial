from odoo import models,fields


class ProjectTasks(models.Model):
    _inherit = 'project.task'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('Last Date')