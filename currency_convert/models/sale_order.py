from odoo import api,fields,models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    convert_currency_id = fields.Many2one('res.currency', 'Convert Currency',
                                          domain="[('active', '=', True), ('id', '!=', currency_id)]")

    converted_total = fields.Monetary   ('Converted Total', compute='_compute_converted_total',currency_field="convert_currency_id")

    @api.depends('amount_total', 'convert_currency_id', 'currency_id')
    def _compute_converted_total(self):
        for record in self:
            if record.convert_currency_id:
                record.converted_total = record.currency_id._convert(record.amount_total, record.convert_currency_id,
                                                                     self.env.company, fields.Date.today())
            else:
                record.converted_total = 0.0
