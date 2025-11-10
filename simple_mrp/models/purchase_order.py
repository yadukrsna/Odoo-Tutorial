from odoo import fields,models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    simple_mrp_id = fields.Many2one('simple.mrp.production', 'Simple MRP')