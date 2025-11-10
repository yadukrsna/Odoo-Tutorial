/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

publicWidget.registry.HotelGallery = publicWidget.Widget.extend({
    selector: '.hotel_img',
    start: function () {
        const self = this;

        return rpc("/hotel_gallery", {}).then(function (images) {
            self.$target.empty().html(renderToElement("hotel_management.hotel_gallery", { images }));

            const modalImage = document.getElementById('modalImage');
            self.$target.find('.gallery-card-img').each(function () {
                this.addEventListener('click', function () {
                    modalImage.src = this.src;
                    $("#imageModal").modal("show");
                });
            });
        });
    },
});
