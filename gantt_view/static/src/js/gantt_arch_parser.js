/** @odoo-module **/
import { visitXML } from "@web/core/utils/xml";

export class GanttArchParser {
    parse(arch) {
        const archInfo = {
            fieldAttrs: {},
            startField: "start_date",
            stopField: "end_date",
            title: "Gantt",
        };

        visitXML(arch, (node) => {
            switch (node.tagName) {
                case "gantt":
                    if (node.hasAttribute("string")) {
                        archInfo.title = node.getAttribute("string");
                    }
                    if (node.hasAttribute("start_date")) {
                        archInfo.startField = node.getAttribute("start_date");
                    }
                    if (node.hasAttribute("end_date")) {
                        archInfo.stopField = node.getAttribute("end_date");
                    }
                    break;
                case "field":
                    const fieldName = node.getAttribute("name");
                    archInfo.fieldAttrs[fieldName] = {};
                    break;
            }
        });

        return archInfo;
    }
}
