import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";

patch(ProductCard, {
    props: {
        ...ProductCard.props,
        pos_quantities: { type: String, optional: true },
    },
});