import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';
const { Component } = owl;

export class HotelDashboard extends Component {
    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.data = [];
        this.loadData();
    }

    loadData() {
        this.rpc.query({
            model: 'hotel.management.dashboard',
            method: 'get_values',
            args: []
        }).then((result) => {
            this.data = result;
            this.render();
        });
    }
}
registry.category("actions").add("hotel_dashboard", HotelDashboard);
