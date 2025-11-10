/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { loadJS } from "@web/core/assets";

publicWidget.registry.HotelFacilityTags = publicWidget.Widget.extend({
    selector: ".hotel_form",

    init: function () {
        this._super.apply(this, arguments);

        loadJS("https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js").then(() => {
                $(this.el).find("select.facility_tags").select2({
                    placeholder: "Select Facilities",
                    allowClear: true,
                    width: '100%',
                    tags: true
                });
            }).catch(err => console.error("Error loading Select2:", err));
    },
});
