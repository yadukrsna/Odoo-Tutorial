/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { GanttArchParser } from "./gantt_arch_parser";
import { GanttController } from "./gantt_controller";
import { GanttModel } from "./gantt_model";
import { GanttRenderer } from "./gantt_renderer";

const viewRegistry = registry.category("views");

export const ganttView = {
    type: "gantt",
    Controller: GanttController,
    Renderer: GanttRenderer,
    Model: GanttModel,
    ArchParser: GanttArchParser,
    props: (genericProps, view) => {
        const modelParams = {};
        let fieldName = null;

        if (genericProps.state) {
            modelParams.data = genericProps.state.data;
            modelParams.metaData = genericProps.state.metaData;
        } else {
            const { arch, fields, resModel } = genericProps;
            const archInfo = new view.ArchParser().parse(arch);
            modelParams.metaData = {
                startField: archInfo.startField,
                stopField: archInfo.stopField,
                fields,
                resModel,
                title: archInfo.title || _t("Untitled Gantt"),
            };
            fieldName = Object.keys(archInfo.fieldAttrs)[0] || null;
        }

        return {
            ...genericProps,
            Model: view.Model,
            modelParams,
            Renderer: view.Renderer,
            fieldName,
        };
    },
};

viewRegistry.add("gantt", ganttView);
