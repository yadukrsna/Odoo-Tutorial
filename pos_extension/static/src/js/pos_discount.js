/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";

patch(ControlButtons.prototype, {
    async onClickDiscount() {
        const order = this.currentOrder;
        if (!order) return;

        const discountType = this.pos.config.discount_type;

        const discountValue = await makeAwaitable(this.dialog, TextInputPopup, {
            title: discountType === "percentage" ? "Enter Discount Percentage" : "Enter Discount Amount",
            startingValue: "",
        });

        if (discountValue == null) {
            return;
        }

        const orderLine = order.get_selected_orderline();
        if (!orderLine) return;

        if (discountType === "percentage") {
            orderLine.set_discount(discountValue);
        }
        else if (discountType === "amount") {
            const totalAmount = orderLine.get_unit_price() * orderLine.get_quantity();
            const discountPercent = (discountValue / totalAmount) * 100;
            orderLine.set_discount(discountPercent);
        }
    },
});
