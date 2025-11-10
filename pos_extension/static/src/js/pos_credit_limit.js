/** @odoo-module */
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { CustomPopup } from "@pos_extension/overrides/components/custom_popup";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { useService } from "@web/core/utils/hooks";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.dialog = useService("dialog");
    },

    async validateOrder() {
        const partner = this.currentOrder.get_partner();
        if (partner) {
            const creditLimit = partner.pos_credit_limit;
            const dues = partner.pos_due || 0;
            const orderTotal = this.currentOrder.get_total_with_tax();

            if (creditLimit > 0 && (dues + orderTotal) > creditLimit) {
                await makeAwaitable(this.dialog, CustomPopup, {
                    order: this.currentOrder,
                });
                return;
            }
            partner.pos_due = dues + orderTotal;
        }
        return super.validateOrder(...arguments);
    }
});
