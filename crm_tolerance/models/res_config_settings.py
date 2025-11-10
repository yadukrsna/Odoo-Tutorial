from odoo import fields,models
from datetime import datetime, timedelta


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    crm_tolerance_time = fields.Integer('CRM Tolerance', config_parameter="crm_tolerance.crm_tolerance")\

