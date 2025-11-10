/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";


publicWidget.registry.HotelAccommodation = publicWidget.Widget.extend({
    selector: '#wrap',
    events:{
        'change .guest_number': '_onChangeGuestNumber',
        'change .other_guest': '_onChangeGuest',
        'click  .remove_guest': '_onRemoveGuest',
        'click  .add_guest': '_onAddGuest',
        'submit .hotel_form': '_onSubmitForm'
    },

    async start() {
        this.dialog = this.bindService("dialog");
        const userInfo = await rpc('/web/session/get_session_info');
        this.$('.user_name').val(userInfo.name);
    },

    _onChangeGuestNumber: function(ev){
        let $guestNumber = $(ev.target).val();
        let $table = this.$('.add_other_guest');
        let $tableBody = this.$('#other_guest_ids tbody');

        if($guestNumber >= 2) {
            $table.show();
        }
        else if($guestNumber < 1) {
            $table.hide();
            $tableBody.empty();
        }
    },

    _onChangeGuest: function(ev){
        let age = $(ev.target).closest('tr').find('option:selected').data('age');
        let gender = $(ev.target).closest('tr').find('option:selected').data('gender');
        $(ev.target).closest('tr').find('.guest_age').val(age || '');
        $(ev.target).closest('tr').find('.guest_gender').val(gender || '');
    },

    _onRemoveGuest: function(ev){
        $(ev.target).closest('tr').remove();
    },

    _onAddGuest: function(ev) {
        ev.preventDefault();

        let $guest_detail = this.$('#other_guest_ids tbody');
        let currentGuests = $guest_detail.find('tr').length;
        let guestNumber = parseInt(this.$('.guest_number').val() || 1);
        let limit = guestNumber - 1;

        if (currentGuests >= limit) {
            this.dialog.add(AlertDialog, { body: "Cannot add more guests" });
            return;
        }

        let $newRow = $guest_detail.find('tr:first').clone();
        $newRow.find('select').val('');
        $newRow.find('.guest_age').val('');
        $newRow.find('.guest_gender').val('');
        $guest_detail.append($newRow);
    },

    _onSubmitForm: function(ev){
        let guestNumber = parseInt(this.$('.guest_number').val() || 1);
        let $guestRows = this.$('#other_guest_ids tbody tr');

        let otherGuestsCount = 0;
        $guestRows.each(function(){
            let guestId = $(this).find('.other_guest').val();
            if (guestId) {
                otherGuestsCount++;
            }
        });

        if ((otherGuestsCount + 1) !== guestNumber) {
            ev.preventDefault();
            this.dialog.add(AlertDialog, { body: "Guest Number Mismatch" });
            return false;
        }

        if (guestNumber > 1) {
            let isValid = true;
            $guestRows.each(function(){
                let guestId = $(this).find('.other_guest').val();
                let age = $(this).find('.guest_age').val();
                let gender = $(this).find('.guest_gender').val();
                if (!guestId || !age || !gender) {
                    isValid = false;
                    return false;
                }
            });
            if (!isValid) {
                ev.preventDefault();
                this.dialog.add(AlertDialog, { body: "Please fill in all details for other guests." });
                return false;
            }
        }
    },
});
