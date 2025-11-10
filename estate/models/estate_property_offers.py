from datetime import timedelta

from odoo import api, fields, models
import datetime


class PropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "Property Offers"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner = fields.Many2one("res.partner", "Partner")
    property = fields.Many2one("estate.property", required=True, string="Property")

    validity = fields.Integer("Validity (Days)",default=7)
    deadline = fields.Datetime(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    property_type_id = fields.Many2one(related='property.property_type',stored=True)

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.create_date = datetime.date.today()
                record.deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline-record.create_date).days


    def action_accept(self):
        self.write({'status': 'accepted'})
        for record in self:
            record.property.selling_price = record.price
            record.property.buyer = record.partner
            record.property.state = 'offer accepted'

    def action_reject(self):
        self.write({'status': 'refused'})