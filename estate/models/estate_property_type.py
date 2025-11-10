from odoo import fields,models,api

class PropertyType(models.Model):
    _name="estate.property.type"
    _description="Property Type"
    _order = "name desc"

    name = fields.Char("Types", required=True)
    sequence = fields.Integer('Sequence')
    _sql_constraints = [('check_property_type', 'UNIQUE(name)', 'Property Type Already Exists')]

    property_type_line_ids = fields.One2many("estate.property", "property_type")

    property_offer_ids = fields.One2many('estate.property.offers', 'property_type_id')

    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")
    @api.depends('property_offer_ids.price')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.property_offer_ids.mapped("price"))