/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.FoodModal = publicWidget.Widget.extend({
    selector: '.portal_hotel',

    events: {
        'click .portal_img': '_onClickImage',
        'click #addToCart': '_onClickCart',
        'click #confirmOrder': '_onClickConfirm',
        'click .plus-btn': '_onClickPlus',
        'click .minus-btn': '_onClickMinus',
    },

    start: function () {
        this.cart = [];
        this.modalTitle = document.getElementById("modalFoodTitle");
        this.modalImage = document.getElementById("modalFoodImage");
        this.modalCategory = document.getElementById("modalFoodCategory");
        this.modalDescription = document.getElementById("modalDescription");
        this.modalPrice = document.getElementById("modalFoodPrice");
    },

    _onClickImage: function (ev) {
        const el = ev.currentTarget;
        this.currentItem = {
            id: el.dataset.id,
            name: el.dataset.food,
            category: el.dataset.category,
            description: el.dataset.description,
            price: parseFloat(el.dataset.price),
            currency: el.dataset.currency,
            src: el.src,
            qty: 1
        };

        this.modalTitle.textContent = this.currentItem.name;
        this.modalImage.src = this.currentItem.src;
        this.modalCategory.textContent = this.currentItem.category;
        this.modalDescription.textContent = this.currentItem.description;
        this.modalPrice.textContent = this.currentItem.currency + " " + this.currentItem.price;

        $('#foodModal').modal('show');
    },

    _onClickCart: function () {
        if (!this.currentItem) return;

        this.cart.push({...this.currentItem});
        this._renderCart();
        $('#foodModal').modal('hide');
    },

    _onClickConfirm: function () {
        fetch("/hotel/order", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cart: this.cart }),
        }).then(() => {
            window.location.href = "/contactus-thank-you";
            this.cart = [];
            this._renderCart();
        });
    },

    _onClickPlus: function (ev) {
        const idx = parseInt(ev.currentTarget.dataset.index);
        this.cart[idx].qty += 1;
        this._renderCart();
    },

    _onClickMinus: function (ev) {
        const idx = parseInt(ev.currentTarget.dataset.index);
        if (this.cart[idx].qty > 1) {
            this.cart[idx].qty -= 1;
            this._renderCart();
        }
    },

    _renderCart: function () {
        const cartTableBody = document.querySelector("#cartTable tbody");
        const cartTotal = document.getElementById("cartTotal");
        cartTableBody.innerHTML = '';
        let total = 0;

        this.cart.forEach((item, i) => {
            const subtotal = item.price * item.qty;
            total += subtotal;

            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.name}</td>
                <td class="text-center">
                    <div class="input-group input-group-sm" style="width:100px; margin:auto;">
                        <button class="btn btn-sm minus-btn" type="button" data-index="${i}">-</button>
                        <input type="text" class="form-control text-center" value="${item.qty}" readonly/>
                        <button class="btn btn-sm plus-btn" type="button" data-index="${i}">+</button>
                    </div>
                </td>
                <td class="text-end">${item.price}</td>
                <td class="text-end">${subtotal}</td>
            `;
            cartTableBody.appendChild(row);
        });

        cartTotal.textContent = total;
    }
});
