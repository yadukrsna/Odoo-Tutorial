/** @odoo-module **/
import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class GanttRenderer extends Component {
    static template = "gantt_view.GanttRenderer";
    static props = ["model", "fieldName"];

    setup() {
        this.actionService = useService("action");
        this.orm = useService("orm");
        this.items = this.props.model.getItems();
        this.state = useState({
            scale: "weeks",
            currentDate: new Date(),
            showTaskPopup: false,
            selectedDate: null,
            selectedProjectId: null,
            availableTasks: [],
            resizingTask: null,
            resizeType: null,
            resizeStartX: 0,
        });

        this.onSetDays = () => this.setScale("days");
        this.onSetWeeks = () => this.setScale("weeks");
        this.onSetMonths = () => this.setScale("months");
        this.onNext = () => this.navigate(1);
        this.onPrev = () => this.navigate(-1);

        onWillUpdateProps(() => { this.items = this.props.model.getItems(); });
    }

    groupBy() {
        const grouped = {};

        this.items.forEach(item => {
            let projectId, projectName;
            if (item.project_id && Array.isArray(item.project_id)) {
                projectId = item.project_id[0];
                projectName = item.project_id[1];
            }
            else if (item.project_id) {
                projectId = item.project_id;
                projectName = `Project ${item.project_id}`;
            }
            else {
                projectId = 'no_project';
                projectName = 'Private';
            }

            if (!grouped[projectId]) {
                grouped[projectId] = {
                    id: projectId,
                    name: projectName,
                    tasks: []
                };
            }

            grouped[projectId].tasks.push(item);
        });

        return Object.values(grouped);
    }

    getFieldValue(item) {
        if (!this.props.fieldName) return item.name || "Unnamed";

        if (this.props.fieldName === 'project_id' && item.project_id) {
            if (Array.isArray(item.project_id)) {
                return item.project_id[1];
            }
            return item.project_id;
        }

        return item[this.props.fieldName] || "";
    }

    setScale(scale) {
        this.state.scale = scale;
    }

    navigate(direction) {
        const date = new Date(this.state.currentDate);
        if (this.state.scale === "days") date.setDate(date.getDate() + direction);
        else if (this.state.scale === "weeks") date.setDate(date.getDate() + 7 * direction);
        else if (this.state.scale === "months") date.setMonth(date.getMonth() + direction);
        this.state.currentDate = date;
    }

    async onBarClick(task, event) {
        if (this.state.resizingTask) return;

        await this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "project.task",
            res_id: task.id,
            views: [[false, "form"]],
            target: "new",
        });
    }

    onResizeStart(task, scale, type, event) {
        event.stopPropagation();
        event.preventDefault();

        this.state.resizingTask = {
            task: task,
            scale: scale,
            originalStartDate: new Date(task.start_date),
            originalEndDate: new Date(task.end_date),
        };
        this.state.resizeType = type;
        this.state.resizeStartX = event.clientX;

        document.addEventListener('mousemove', this.onResizeMove.bind(this));
        document.addEventListener('mouseup', this.onResizeEnd.bind(this));
    }

    onResizeMove(event) {
        if (!this.state.resizingTask) return;

        const { scale, task } = this.state.resizingTask;
        const movedX = event.clientX - this.state.resizeStartX;

        const timeScale = this.getTimeScale(this.state.scale);
        const cellWidth = this.state.scale === 'days' ? 60 : (this.state.scale === 'weeks' ? 200 : 50);
        const totalCells = timeScale[0].sub.length;
        const timelineWidth = cellWidth * totalCells;

        const scaleStart = new Date(scale.start).getTime();
        const scaleEnd = new Date(scale.end).getTime();
        const scaleDuration = scaleEnd - scaleStart;
        const movedPercent = (movedX / timelineWidth) * 100;
        const addDate = (movedPercent / 100) * scaleDuration;

        if (this.state.resizeType === 'start') {
            const newStartTime = this.state.resizingTask.originalStartDate.getTime() + addDate;
            const newStart = new Date(newStartTime);
            const endTime = new Date(task.end_date).getTime();

            if (newStartTime < endTime) {
                task.start_date = this.formatDateForDisplay(newStart);
            }
        } else if (this.state.resizeType === 'end') {
            const newEndTime = this.state.resizingTask.originalEndDate.getTime() + addDate;
            const newEnd = new Date(newEndTime);
            const startTime = new Date(task.start_date).getTime();

            if (newEndTime > startTime) {
                task.end_date = this.formatDateForDisplay(newEnd);
            }
        }
    }

    async onResizeEnd(event) {
        document.removeEventListener('mousemove', this.onResizeMove.bind(this));
        document.removeEventListener('mouseup', this.onResizeEnd.bind(this));

        if (!this.state.resizingTask) return;

        const task = this.state.resizingTask.task;

        await this.orm.write('project.task', [task.id], {
            start_date: task.start_date,
            end_date: task.end_date,
        });

        await this.props.model.load();
        this.items = this.props.model.getItems();

        this.state.resizingTask = null;
        this.state.resizeType = null;
    }

    formatDateForDisplay(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    async onCellClick(date, projectId) {
        let domain = [
            ['start_date', '=', false],
            ['end_date', '=', false]
        ];

        if (projectId && projectId !== 'no_project') {
            domain.push(['project_id', '=', projectId]);
        } else if (projectId === 'no_project') {
            domain.push(['project_id', '=', false]);
        }

        const tasks = await this.orm.searchRead(
            'project.task',
            domain,
            ['name', 'id', 'project_id']
        );

        this.state.availableTasks = tasks;
        this.state.selectedDate = date;
        this.state.selectedProjectId = projectId;
        this.state.showTaskPopup = true;
    }

    closePopup() {
        this.state.showTaskPopup = false;
        this.state.availableTasks = [];
        this.state.selectedDate = null;
        this.state.selectedProjectId = null;
    }

    async onTaskSelect(taskId) {
        const startDate = new Date(this.state.selectedDate);
        const endDate = new Date(this.state.selectedDate);
        endDate.setDate(endDate.getDate() + 1);

        await this.orm.write('project.task', [taskId], {
            start_date: this.formatDateForDisplay(startDate),
            end_date: this.formatDateForDisplay(endDate),
        });

        await this.props.model.load();
        this.items = this.props.model.getItems();

        this.closePopup();
    }

    getTimeScale(scale = "days") {
        const base = new Date(this.state.currentDate);
        const result = [];

        if (scale === "days") {
            const hours = [];
            const dayStart = new Date(base);
            dayStart.setHours(0, 0, 0, 0);
            const dayEnd = new Date(base);
            dayEnd.setHours(23, 59, 59, 999);

            for (let h = 0; h < 24; h++) {
                const hourDate = new Date(dayStart);
                hourDate.setHours(h);
                hours.push({ label: `${h}:00`, date: hourDate });
            }
            result.push({
                label: base.toDateString(),
                sub: hours,
                start: dayStart,
                end: dayEnd
            });
        }
        else if (scale === "weeks") {
            const start = new Date(base);
            start.setDate(base.getDate() - base.getDay() + 1);
            start.setHours(0, 0, 0, 0);
            const end = new Date(start);
            end.setDate(start.getDate() + 6);
            end.setHours(23, 59, 59, 999);

            const days = [];
            const dayNames = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];
            for (let i = 0; i < 7; i++) {
                const d = new Date(start);
                d.setDate(start.getDate() + i);
                days.push({ label: `${dayNames[i]}, ${d.getDate()}`, date: d });
            }

            const getWeekNumber = (date) => {
                const d = new Date(date);
                let yearStart = +new Date(d.getFullYear(),0,1);
                let today = +new Date(d.getFullYear(), d.getMonth(), d.getDate());
                let dayOfYear = ((today - yearStart + 1)/86400000);
                return Math.ceil(dayOfYear / 7);
            };

            const weekNumber = getWeekNumber(start);
            const weekLabel = `Week ${weekNumber}`;
            result.push({ label: weekLabel, sub: days, start, end });
        }
        else if (scale === "months") {
            const start = new Date(base.getFullYear(), base.getMonth(), 1);
            start.setHours(0, 0, 0, 0);
            const end = new Date(base.getFullYear(), base.getMonth() + 1, 0);
            end.setHours(23, 59, 59, 999);

            const days = [];
            for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
                days.push({ label: d.getDate(), date: new Date(d) });
            }
            const monthLabel = `${start.toLocaleString("default", { month: "long" })} ${start.getFullYear()}`;
            result.push({ label: monthLabel, sub: days, start, end });
        }

        return result;
    }

    computeBarPosition(item, scaleItem) {
        if (!item.start_date || !item.end_date) {
            return { left: 0, width: 0, hidden: true };
        }

        const scaleStart = new Date(scaleItem.start).getTime();
        const scaleEnd = new Date(scaleItem.end).getTime();

        const itemStart = new Date(item.start_date);
        itemStart.setHours(0, 0, 0, 0);
        const itemEnd = new Date(item.end_date);
        itemEnd.setHours(23, 59, 59, 999);

        const start = Math.max(itemStart.getTime(), scaleStart);
        const end = Math.min(itemEnd.getTime(), scaleEnd);

        if (end < scaleStart || start > scaleEnd) {
            return { left: 0, width: 0, hidden: true };
        }

        const total = scaleEnd - scaleStart;
        const left = ((start - scaleStart) / total) * 100;
        const width = ((end - start) / total) * 100;

        return { left: Math.max(0, left), width: Math.max(0.5, width), hidden: false };
    }
}