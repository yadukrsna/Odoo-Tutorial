/** @odoo-module */
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component } from "@odoo/owl";

export class CustomPopup extends Component {
    static template = "pos_custom_popup.CustomPopup";

    setup() {
        this.pos = usePos();
        const partner = this.props.order.get_partner();
        this.dues = partner.pos_due;
        this.creditLimit = partner.pos_credit_limit;
    }

    closeModal() {
        if (this.props.close) {
            this.props.close();
        }
    }
}
