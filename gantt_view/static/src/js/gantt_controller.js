/** @odoo-module **/

import { Layout } from "@web/search/layout";
import { useModelWithSampleData } from "@web/model/model";
import { standardViewProps } from "@web/views/standard_view_props";
import { useSetupAction } from "@web/search/action_hook";
import { Component, useRef } from "@odoo/owl";
import { SearchBar } from "@web/search/search_bar/search_bar";
import { useSearchBarToggler } from "@web/search/search_bar/search_bar_toggler";

export class GanttController extends Component {
    static template = "gantt_view.GanttController";
    static components = { Layout, SearchBar };
    static props = {
        ...standardViewProps,
        Model: Function,
        modelParams: Object,
        Renderer: Function,
        fieldName: String,
    };

    setup() {

        this.model = useModelWithSampleData(this.props.Model, this.props.modelParams);

        useSetupAction({
            rootRef: useRef("root"),
            getLocalState: () => ({ metaData: this.model.metaData }),
            getContext: () => this.getContext(),
        });

        this.searchBarToggler = useSearchBarToggler();
    }
}
