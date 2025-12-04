/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, onWillStart, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";

export class SGCActivityDashboard extends Component {
    static template = "SGCActivityDashboard";
    
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");
        
        this.filterState = useState({
            resUsersId: null, 
            hrDepartmentsId: null, 
            startDate: null, 
            endDate: null, 
            resUsersValue: null, 
            hrDepartmentsValue: null
        });
        
        this.domain = {
            domain_all_activities: [],
            domain_planned_activity: [],
            domain_today_activity: [],
            domain_overdue_activity: [],
            domain_done_activity: [],
        };
        
        this.state = useState({
            len_all: 0,
            len_planned: 0,
            len_done: 0,
            len_today: 0,
            len_overdue: 0,
            done_activity: [],
            planned_activity: [],
            today_activity: [],
            overdue_activity: [],
            activity_type: 0,
            res_users: [],
            hr_departments: [],
        });
        
        onWillStart(async () => await this.render_dashboards());
    }

    async update() {
        await this.render_dashboards();
    }

    async render_dashboards() {
        // Update domain with filterState
        this.domain.domain_planned_activity = [["state", "=", 'planned']];
        this.domain.domain_today_activity = [["state", "=", 'today']];
        this.domain.domain_overdue_activity = [["state", "=", 'overdue']];
        this.domain.domain_done_activity = [["state", "=", 'done'], ['active', 'in', [true, false]]];
        this.domain.domain_all_activities = [['active', 'in', [true, false]]];

        if (this.filterState.resUsersId) {
            const resUsersId = parseInt(this.filterState.resUsersId, 10);
            this.domain.domain_planned_activity.push(["user_id", "=", resUsersId]);
            this.domain.domain_today_activity.push(["user_id", "=", resUsersId]);
            this.domain.domain_overdue_activity.push(["user_id", "=", resUsersId]);
            this.domain.domain_done_activity.push(["user_id", "=", resUsersId]);
            this.domain.domain_all_activities.push(["user_id", "=", resUsersId]);
        }

        if (this.filterState.hrDepartmentsId) {
            const hrDepartmentsId = parseInt(this.filterState.hrDepartmentsId, 10);
            this.domain.domain_planned_activity.push(["user_id.employee_ids.department_id", "=", hrDepartmentsId]);
            this.domain.domain_today_activity.push(["user_id.employee_ids.department_id", "=", hrDepartmentsId]);
            this.domain.domain_overdue_activity.push(["user_id.employee_ids.department_id", "=", hrDepartmentsId]);
            this.domain.domain_done_activity.push(["user_id.employee_ids.department_id", "=", hrDepartmentsId]);
            this.domain.domain_all_activities.push(["user_id.employee_ids.department_id", "=", hrDepartmentsId]);
        }

        if (this.filterState.startDate && this.filterState.endDate) {
            const dateFilters = [
                ["date_deadline", ">=", this.filterState.startDate],
                ["date_deadline", "<=", this.filterState.endDate]
            ];
            for (const domain of Object.values(this.domain)) {
                domain.push(...dateFilters);
            }
        }

        // Fetch data asynchronously
        const [planned_activity, today_activity, overdue_activity, done_activity, activity_type, res_users, hr_departments] = await Promise.all([
            this.orm.call('mail.activity', 'search_read', [], {domain: this.domain.domain_planned_activity}),
            this.orm.call('mail.activity', 'search_read', [], {domain: this.domain.domain_today_activity}),
            this.orm.call('mail.activity', 'search_read', [], {domain: this.domain.domain_overdue_activity}),
            this.orm.call('mail.activity', 'search_read', [], {domain: this.domain.domain_done_activity}),
            this.orm.call('mail.activity.type', 'search_count', [], {domain: []}),
            this.orm.call('res.users', 'search_read', [], {fields: ['id', 'name']}),
            this.orm.call('hr.department', 'search_read', [], {fields: ['id', 'name']}),
        ]);

        // Calculate activity counts
        this.state.len_all = planned_activity.length + done_activity.length + today_activity.length + overdue_activity.length;
        this.state.len_planned = planned_activity.length;
        this.state.len_done = done_activity.length;
        this.state.len_today = today_activity.length;
        this.state.len_overdue = overdue_activity.length;

        // Assign data to component state
        this.state.done_activity = done_activity.slice(0, 10);
        this.state.planned_activity = planned_activity.slice(0, 10);
        this.state.today_activity = today_activity.slice(0, 10);
        this.state.overdue_activity = overdue_activity.slice(0, 10);
        this.state.activity_type = activity_type;
        this.state.res_users = res_users;
        this.state.hr_departments = hr_departments;
    }

    onUserChange(ev) {
        const resUsersId = ev.target.value || null;
        this.filterState.resUsersValue = resUsersId;
        this.filterState.resUsersId = resUsersId === '0' ? null : resUsersId;
        this.update();
    }

    onChangeHrDepartments(ev) {
        const hrDepartmentsId = ev.target.value || null;
        this.filterState.hrDepartmentsValue = hrDepartmentsId;
        this.filterState.hrDepartmentsId = hrDepartmentsId === '0' ? null : hrDepartmentsId;
        this.update();
    }

    onDateChange(ev) {
        const inputType = ev.target.classList.contains("o_date_range_picker_input_start") ? "startDate" : "endDate";
        this.filterState[inputType] = ev.target.value || null;

        const {startDate, endDate} = this.filterState;
        if (startDate && endDate) {
            const startDateObj = new Date(startDate);
            const endDateObj = new Date(endDate);

            if (endDateObj < startDateObj) {
                this.notification.add(_t("Ngày kết thúc không thể nhỏ hơn ngày bắt đầu!"), {type: "danger"});
                ev.target.value = "";
                this.filterState[inputType] = null;
                return;
            }
        }
        this.update();
    }

    show_all_activities(e) {
        e.stopPropagation();
        e.preventDefault();
        this.action.doAction({
            name: _t("Tất cả hoạt động"),
            type: 'ir.actions.act_window',
            res_model: 'mail.activity',
            view_mode: 'tree,form',
            domain: this.domain.domain_all_activities,
            views: [[false, 'list'], [false, 'form']],
            target: 'current'
        });
    }

    show_planned_activities(e) {
        e.stopPropagation();
        e.preventDefault();
        this.action.doAction({
            name: _t("Hoạt động đã lên kế hoạch"),
            type: 'ir.actions.act_window',
            res_model: 'mail.activity',
            domain: this.domain.domain_planned_activity,
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],
            target: 'current'
        });
    }

    show_completed_activities(e) {
        e.stopPropagation();
        e.preventDefault();
        this.action.doAction({
            name: _t("Hoạt động hoàn thành"),
            type: 'ir.actions.act_window',
            res_model: 'mail.activity',
            domain: this.domain.domain_done_activity,
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],
            target: 'current'
        });
    }

    show_today_activities(e) {
        e.stopPropagation();
        e.preventDefault();
        this.action.doAction({
            name: _t("Hoạt động hôm nay"),
            type: 'ir.actions.act_window',
            res_model: 'mail.activity',
            domain: this.domain.domain_today_activity,
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],
            target: 'current'
        });
    }

    show_overdue_activities(e) {
        e.stopPropagation();
        e.preventDefault();
        this.action.doAction({
            name: _t("Hoạt động quá hạn"),
            type: 'ir.actions.act_window',
            res_model: 'mail.activity',
            domain: this.domain.domain_overdue_activity,
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],
            target: 'current'
        });
    }

    show_activity_types(e) {
        e.stopPropagation();
        e.preventDefault();
        this.action.doAction({
            name: _t("Loại hoạt động"),
            type: 'ir.actions.act_window',
            res_model: 'mail.activity.type',
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],
            target: 'current'
        });
    }

    click_view(e) {
        const id = e.target.value;
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Chi tiết hoạt động'),
            res_model: 'mail.activity',
            res_id: parseInt(id),
            views: [[false, 'form']],
            view_mode: 'form',
            target: 'current'
        });
    }

    async click_origin(e) {
        const id = e.target.value;
        const result = await this.orm.call('mail.activity', 'get_activity', [parseInt(id)]);
        if (result && result.model && result.res_id) {
            this.action.doAction({
                type: 'ir.actions.act_window',
                name: _t('Nguồn gốc'),
                res_model: result.model,
                res_id: result.res_id,
                views: [[false, 'form']],
                view_mode: 'form',
                target: 'current'
            });
        }
    }
}

registry.category("actions").add("sgc_activity_dashboard", SGCActivityDashboard);
