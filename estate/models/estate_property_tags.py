from odoo import fields,models

class PropertyTag(models.Model):
    _name="estate.property.tags"
    _order = "name desc"

    name = fields.Char('Property Tags', required=True)
    color = fields.Integer('Color')
    _sql_constraints = [('check_property_tag', 'UNIQUE(name)', 'Property Tag Already Exists')]

