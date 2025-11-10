/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

function chunk(array, size) {
    if (!array || !array.length) return [];
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

publicWidget.registry.hotelRoom = publicWidget.Widget.extend({
    selector: '.hotel_section',
    start: function () {
        const self = this;
        return rpc("/hotel_room", {}).then(function (result) {

            const chunks = chunk(result, 3);

            if (chunks.length > 0) {
                chunks[0].is_active = true;
            }
            self.$target.empty().html(renderToElement("hotel_management.hotel_data", { chunks }));
        });
    },
});

