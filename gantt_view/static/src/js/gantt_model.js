/** @odoo-module **/
import { KeepLast } from "@web/core/utils/concurrency";
import { Model } from "@web/model/model";
import { useService } from "@web/core/utils/hooks";

export class GanttModel extends Model {
    setup(params) {
        super.setup()
        this.metaData = params.metaData;
        this.orm = useService("orm");
        this.keepLast = new KeepLast();
        this.data = [];
    }

    async load() {
        const { resModel, fields } = this.metaData;
        const fieldNames = Object.keys(fields);
        this.data = await this.keepLast.add(
            this.orm.searchRead(resModel, [], fieldNames)
        );
        return this.data;
    }

    getItems() {
        return this.data || [];
    }
}
