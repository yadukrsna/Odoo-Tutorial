from odoo import fields,models

class View(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('gantt', 'Gantt')])

    def _get_view_info(self):
        view_info = super()._get_view_info()

        view_info["gantt"] = {"icon": "oi-fw fa fa-tasks", "label": "Gantt"}
        return view_info