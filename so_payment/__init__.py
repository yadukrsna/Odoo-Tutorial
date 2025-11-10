from . import models

from odoo.exceptions import UserError

def action_confirm(self):
    Quant = self.env['stock.quant']
    MRP = self.env['mrp.production']
    PurchaseOrder = self.env['purchase.order']
    PurchaseOrderLine = self.env['purchase.order.line']
    StockLocation = self.env.ref('stock.stock_location_stock')

    for record in self:
        for order in record.simple_bom_id.simple_bom_line_ids:
            component = order.product_id
            required_qty = (order.product_qty / record.simple_bom_id.product_qty) * record.product_qty

            # 1️⃣ Check component stock
            if component.qty_available < required_qty:
                shortage = required_qty - component.qty_available

                # 2️⃣ Try to find BOM for this component
                bom = self.env['mrp.bom']._bom_find(products=component)
                if bom:
                    # Create a sub-manufacturing order for this component
                    sub_mrp = MRP.create({
                        'product_id': component.id,
                        'product_qty': shortage,
                    })
                    sub_mrp.action_confirm()

                    # 3️⃣ After confirming, check components of that MRP too
                    for bom_line in sub_mrp.bom_id.bom_line_ids:
                        sub_component = bom_line.product_id
                        sub_required_qty = (bom_line.product_qty / sub_mrp.bom_id.product_qty) * sub_mrp.product_qty
                        if sub_component.qty_available < sub_required_qty:
                            sub_shortage = sub_required_qty - sub_component.qty_available
                            vendor = sub_component.seller_ids[:1].name
                            if not vendor:
                                raise UserError(f"No vendor found for {sub_component.display_name}. Please define one.")
                            po = PurchaseOrder.create({
                                'partner_id': vendor.id,
                                'origin': sub_mrp.name,
                            })
                            PurchaseOrderLine.create({
                                'order_id': po.id,
                                'product_id': sub_component.id,
                                'product_qty': sub_shortage,
                                'price_unit': sub_component.standard_price,
                                'name': sub_component.name,
                                'date_planned': fields.Datetime.now(),
                            })
                else:
                    # 4️⃣ No BOM → create purchase order directly
                    vendor = component.seller_ids[:1].name
                    if not vendor:
                        raise UserError(f"No vendor found for {component.display_name}. Please define one.")
                    po = PurchaseOrder.create({
                        'partner_id': vendor.id,
                        'origin': record.name,
                    })
                    PurchaseOrderLine.create({
                        'order_id': po.id,
                        'product_id': component.id,
                        'product_qty': shortage,
                        'price_unit': component.standard_price,
                        'name': component.name,
                        'date_planned': fields.Datetime.now(),
                    })

            # 5️⃣ Consume the component stock
            Quant._update_available_quantity(component, StockLocation, -required_qty)

        # 6️⃣ Produce finished product
        Quant._update_available_quantity(record.product_id, StockLocation, record.product_qty)
        record.state = 'confirmed'
