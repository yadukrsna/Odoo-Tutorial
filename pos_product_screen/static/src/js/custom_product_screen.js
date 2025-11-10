import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class CustomProductScreen extends Component {
    static template = "pos_product_screen.CustomProductScreen";

    setup() {
        this.pos = usePos();
        this.products = this.pos.models["product.product"].getAll();
    }

    closeCustomProductScreen() {
        this.pos.showScreen('ProductScreen');
    }

    showProducts() {
        return this.products;
    }

    editProduct(product) {
        this.pos.editProduct(product);
    }
}

registry.category("pos_screens").add("CustomProductScreen", CustomProductScreen);