from odoo import fields, models, api
from datetime import date


class ResPartnerExtended(models.Model):
    """Used to add two new fields to res.partner"""
    _inherit = 'res.partner'
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    birthdate = fields.Date(string='Birthdate')
    age = fields.Integer(string="Age", compute='_compute_age', readonly=False)

    @api.depends('birthdate')
    def _compute_age(self):
        """Function used to compute age based on birthdate"""
        for record in self:
            if record.birthdate:
                today = date.today()
                age = today.year - record.birthdate.year
                if (today.month, today.day) < (record.birthdate.month, record.birthdate.day):
                    age -= 1
                record.age = age
            else:
                record.age = 0
