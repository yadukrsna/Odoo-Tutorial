/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { onWillStart, useState } from "@odoo/owl";

patch(ListController.prototype, {
    setup() {
        super.setup();
        if (this.props.resModel === 'crm.lead') {
            this.orm = useService("orm");
            this.state = useState({
                salesperson: [],
                selectedSalesperson: '',
            });

            onWillStart(async () => {
                await this.loadSalesperson();
            });
        }
    },

    async loadSalesperson() {
            const salesperson = await this.orm.call(
                'crm.lead',
                'get_available_salesperson',
            );
            this.state.salesperson = salesperson;
    },

    async onSalespersonChange(ev) {
        const salespersonId = ev.target.value ? parseInt(ev.target.value) : null;
        this.state.selectedSalesperson = ev.target.value;

        let domain = [];

        if (this.props.domain) {
            domain = JSON.parse(JSON.stringify(this.props.domain));
        }

        if (salespersonId) {
            domain.push(['user_id', '=', salespersonId]);
        }

        await this.model.root.load({ domain });
    },
});
