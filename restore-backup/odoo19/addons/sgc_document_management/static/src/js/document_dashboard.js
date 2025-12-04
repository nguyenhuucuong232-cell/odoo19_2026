/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, onWillStart, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";

export class SGCDocumentDashboard extends Component {
    static template = "SGCDocumentDashboard";
    
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");
        
        this.filterState = useState({
            monthFilter: 'this_month', // this_month, last_month, this_year
        });
        
        this.state = useState({
            // Incoming document stats
            incoming_total: 0,
            incoming_new: 0,
            incoming_directive: 0,
            incoming_processing: 0,
            incoming_confirmed: 0,
            incoming_archived: 0,
            
            // Outgoing document stats
            outgoing_total: 0,
            outgoing_sent_approval: 0,
            outgoing_hardcopy_signed: 0,
            outgoing_awaiting_feedback: 0,
            outgoing_archived: 0,
            outgoing_rejected: 0,
        });
        
        onWillStart(async () => await this.render_dashboard());
    }

    async update() {
        await this.render_dashboard();
    }

    async render_dashboard() {
        const today = new Date();
        let dateDomain = [];
        
        // Calculate date range based on filter
        if (this.filterState.monthFilter === 'this_month') {
            const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
            const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
            dateDomain = [
                ['received_date', '>=', firstDay.toISOString().split('T')[0]],
                ['received_date', '<=', lastDay.toISOString().split('T')[0]]
            ];
        } else if (this.filterState.monthFilter === 'last_month') {
            const firstDay = new Date(today.getFullYear(), today.getMonth() - 1, 1);
            const lastDay = new Date(today.getFullYear(), today.getMonth(), 0);
            dateDomain = [
                ['received_date', '>=', firstDay.toISOString().split('T')[0]],
                ['received_date', '<=', lastDay.toISOString().split('T')[0]]
            ];
        } else if (this.filterState.monthFilter === 'this_year') {
            const firstDay = new Date(today.getFullYear(), 0, 1);
            const lastDay = new Date(today.getFullYear(), 11, 31);
            dateDomain = [
                ['received_date', '>=', firstDay.toISOString().split('T')[0]],
                ['received_date', '<=', lastDay.toISOString().split('T')[0]]
            ];
        }

        // Get status codes for filtering
        const statusModel = await this.orm.searchRead(
            'sgc.document.status',
            [],
            ['code', 'type']
        );
        
        const statusMap = {};
        statusModel.forEach(s => {
            statusMap[s.code] = s.id;
        });

        // Incoming document counts
        const incomingDomain = [['type', '=', 'in'], ...dateDomain];
        this.state.incoming_total = await this.orm.searchCount('sgc.document', incomingDomain);
        
        // Get status IDs for incoming documents
        const incomingStatuses = statusModel.filter(s => s.type === 'in');
        const newStatus = incomingStatuses.find(s => s.code === 'new' || s.code === 'moi_den');
        const processingStatus = incomingStatuses.find(s => s.code === 'processing' || s.code === 'dang_xu_ly');
        const confirmedStatus = incomingStatuses.find(s => s.code === 'confirmed' || s.code === 'xac_nhan');
        const archivedStatus = incomingStatuses.find(s => s.code === 'archived' || s.code === 'luu_tru');

        if (newStatus) {
            this.state.incoming_new = await this.orm.searchCount('sgc.document', [
                ...incomingDomain,
                ['status_id', '=', newStatus.id]
            ]);
        }
        
        if (processingStatus) {
            this.state.incoming_processing = await this.orm.searchCount('sgc.document', [
                ...incomingDomain,
                ['status_id', '=', processingStatus.id]
            ]);
        }
        
        if (confirmedStatus) {
            this.state.incoming_confirmed = await this.orm.searchCount('sgc.document', [
                ...incomingDomain,
                ['status_id', '=', confirmedStatus.id]
            ]);
        }
        
        if (archivedStatus) {
            this.state.incoming_archived = await this.orm.searchCount('sgc.document', [
                ...incomingDomain,
                ['status_id', '=', archivedStatus.id]
            ]);
        }

        // Outgoing document counts
        const outgoingDomain = [['type', '=', 'out'], ...dateDomain];
        this.state.outgoing_total = await this.orm.searchCount('sgc.document', outgoingDomain);
        
        const outgoingStatuses = statusModel.filter(s => s.type === 'out');
        const sentApprovalStatus = outgoingStatuses.find(s => s.code === 'sent_approval' || s.code === 'gui_duyet');
        const hardcopySignedStatus = outgoingStatuses.find(s => s.code === 'hardcopy_signed' || s.code === 'ky_ban_cung');
        const awaitingFeedbackStatus = outgoingStatuses.find(s => s.code === 'awaiting_feedback' || s.code === 'cho_phan_hoi');
        const outgoingArchivedStatus = outgoingStatuses.find(s => s.code === 'archived' || s.code === 'luu_tru');
        const rejectedStatus = outgoingStatuses.find(s => s.code === 'rejected' || s.code === 'tu_choi');

        if (sentApprovalStatus) {
            this.state.outgoing_sent_approval = await this.orm.searchCount('sgc.document', [
                ...outgoingDomain,
                ['status_id', '=', sentApprovalStatus.id]
            ]);
        }
        
        if (hardcopySignedStatus) {
            this.state.outgoing_hardcopy_signed = await this.orm.searchCount('sgc.document', [
                ...outgoingDomain,
                ['status_id', '=', hardcopySignedStatus.id]
            ]);
        }
        
        if (awaitingFeedbackStatus) {
            this.state.outgoing_awaiting_feedback = await this.orm.searchCount('sgc.document', [
                ...outgoingDomain,
                ['status_id', '=', awaitingFeedbackStatus.id]
            ]);
        }
        
        if (outgoingArchivedStatus) {
            this.state.outgoing_archived = await this.orm.searchCount('sgc.document', [
                ...outgoingDomain,
                ['status_id', '=', outgoingArchivedStatus.id]
            ]);
        }
        
        if (rejectedStatus) {
            this.state.outgoing_rejected = await this.orm.searchCount('sgc.document', [
                ...outgoingDomain,
                ['status_id', '=', rejectedStatus.id]
            ]);
        }
    }

    onMonthFilterChange(ev) {
        this.filterState.monthFilter = ev.target.value;
        this.update();
    }

    async navigateToDocuments(type, statusCode = null) {
        const domain = [['type', '=', type]];
        if (statusCode) {
            // Find status by code
            const statuses = await this.orm.searchRead('sgc.document.status', [['code', '=', statusCode]], ['id']);
            if (statuses.length > 0) {
                domain.push(['status_id', '=', statuses[0].id]);
            }
        }
        this.action.doAction({
            name: type === 'in' ? _t("Công văn đến") : _t("Công văn đi"),
            type: 'ir.actions.act_window',
            res_model: 'sgc.document',
            view_mode: 'list,form',
            domain: domain,
            views: [[false, 'list'], [false, 'form']],
            target: 'current'
        });
    }
}

registry.category("actions").add("sgc_document_dashboard", SGCDocumentDashboard);

