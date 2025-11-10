from odoo import fields,models


class ProjectTasks(models.Model):
    _inherit = 'project.task'

    sale_order_id = fields.Many2one('sale.order', 'Related Sale Order')