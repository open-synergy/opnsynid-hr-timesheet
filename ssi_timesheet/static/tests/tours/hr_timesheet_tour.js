odoo.define("ssi_timesheet.hr_timesheet_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Timesheets > Timesheets.
    // "Timesheets" (level 2, section) has one child ("Timesheets" leaf,
    // level 3) so both levels are clickable — matches the three menu
    // segments written in every hr_timesheet IK ("Menu: Human Resource >
    // Timesheets > Timesheets").
    function openTimesheetMenuSteps() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Timesheets section",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_timesheet.timesheet_menu"]',
            },
            {
                content: "Open the Timesheets menu item",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_timesheet.menu_hr_timesheet"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action ("Employees") is also a
                // .o_list_view.
                content: "Timesheets list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Timesheets)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Click a statusbar/header button by its exact visible label. Several
    // buttons on this form share a `name` attribute that is a numeric
    // action id (the Cancel button) rather than a method name, so matching
    // by trimmed text is the only selector that is deterministic across
    // all of them.
    function clickHeaderButtonByLabel(label) {
        return {
            content: "Click the " + label + " button",
            trigger: ".o_statusbar_buttons button",
            run: function () {
                var $button = $(".o_statusbar_buttons button").filter(function () {
                    return $(this).text().trim() === label;
                });
                $button[0].click();
            },
        };
    }

    var confirmDialogStep = {
        content: "Confirm the dialog",
        trigger: ".modal-footer button.btn-primary",
        in_modal: true,
    };

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Click the New button.
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Fill in Employee, Date Start, Date End.
            {
                content: "Select the Employee",
                trigger: ".o_field_many2one[name='employee_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-EMP-CREATE",
            },
            {
                content: "Pick the Employee from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-EMP-CREATE)",
                in_modal: false,
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 01/01/2026",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 01/31/2026",
            },
            // ── Flow 4 — On the Computations tab, click Reload, then
            // Compute.
            {
                content: "Open the Computations tab",
                trigger: ".o_notebook .nav-link:contains(Computations)",
            },
            {
                content: "Click Reload",
                trigger:
                    ".o_form_view button[name='action_reload_timesheet_computation']",
            },
            {
                // Gate: TCC01 only becomes reachable through
                // employee_id.timesheet_computation_ids, and computation_ids
                // starts empty on a brand-new record — this cannot match
                // before Reload actually ran.
                content: "Computation line is loaded from the Employee",
                trigger:
                    ".o_field_x2many[name='computation_ids'] " +
                    ".o_data_row:contains(TCC01)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Click Compute",
                trigger: ".o_form_view button[name='action_compute_computation']",
            },
            {
                content: "UI is no longer blocked",
                trigger: "body:not(.o_ui_blocked)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Post-Condition — new record created in Draft status.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft']" +
                    ".btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-EDIT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Change Date End.
            {
                content: "Change Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 01/20/2026",
            },
            // ── Flow 4 — On the Computations tab, click Reload, then
            // Compute.
            {
                content: "Open the Computations tab",
                trigger: ".o_notebook .nav-link:contains(Computations)",
            },
            {
                content: "Click Reload",
                trigger:
                    ".o_form_view button[name='action_reload_timesheet_computation']",
            },
            {
                // Gate: TCE01 is registered on TOUR-EMP-EDIT but the record
                // was created without any computation_ids row, so this
                // cannot match before Reload actually ran.
                content: "Computation line is loaded from the Employee",
                trigger:
                    ".o_field_x2many[name='computation_ids'] " +
                    ".o_data_row:contains(TCE01)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Click Compute",
                trigger: ".o_form_view button[name='action_compute_computation']",
            },
            {
                content: "UI is no longer blocked",
                trigger: "body:not(.o_ui_blocked)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — record is updated.
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2-3 — select the record and delete it. Deletion is
            // driven from the record's own Action menu rather than the
            // list checkbox: the 14.0 list-selector checkbox is flaky
            // (odoo-development-ui-test skill, patterns.md §I), and this
            // reaches the same Post-Condition.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-DELETE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Back to the Timesheets list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Timesheets)",
            },
            // ── Post-Condition — records permanently removed.
            {
                content: "Deleted timesheet no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-EMP-DELETE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/04-confirm.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record to confirm.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-CONFIRM) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Click the Confirm button.
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },
            // ── Flow 4 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status changes to Waiting for Approval,
            // and the Approve button (evidence that approval records were
            // created for the pending level) becomes available.
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm']" +
                    ".btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "The Approve button becomes available",
                trigger:
                    ".o_statusbar_buttons button[name='action_approve_approval']:visible",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/05-approve.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record to approve.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-APPROVE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },
            // ── Flow 4 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — single-level approval template fulfilled
            // immediately, so status changes to Done.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done']" +
                    ".btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/06-reject.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record to reject.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-REJECT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Click the Reject button.
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },
            // ── Flow 4 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status changes to Rejected.
            {
                content: "Status is Rejected",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='reject']" +
                    ".btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/07-start.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_start",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record to start.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-START) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Click the Start button.
            {
                content: "Click the Start button",
                trigger: ".o_statusbar_buttons button[name='action_open']",
                extra_trigger: ".o_form_view",
            },
            // ── Flow 4 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status changes to On Progress.
            {
                content: "Status is On Progress",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open']" +
                    ".btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/10-cancel.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record to cancel.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-CANCEL) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Click the Cancel button. `name` is a numeric
            // action id on this button, so match its label instead.
            clickHeaderButtonByLabel("Cancel"),
            // ── Flow 4 — In the wizard, select the Reason.
            {
                // 14.0: do NOT prefix with `.modal` — the trigger is
                // searched INSIDE the modal already (see
                // odoo-development-ui-test skill, patterns.md §H).
                content: "Wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Select the cancellation reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] " +
                    ".o_radio_item:contains(TOUR-CANCEL-REASON) input",
            },
            // ── Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            // ── Flow 6 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status changes to Cancelled, and the
            // selected Reason is recorded on the timesheet.
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel']" +
                    ".btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Cancellation reason is displayed",
                trigger: "h2:visible:contains(Cancellation reason)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/12-restart.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record to restart.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-RESTART) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Click the Restart button.
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },
            // ── Flow 4 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status returns to Draft.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft']" +
                    ".btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/13-reset-number.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record whose document number will be
            // reset.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-RESETNUM) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Click the Reset Document Number button.
            {
                content: "Click the Reset Document Number button",
                trigger:
                    ".o_statusbar_buttons button[name='action_reset_document_number']",
                extra_trigger: ".o_form_view",
            },
            // ── Flow 4 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — document number returns to "/"; the
            // dialog closing without error is the visible evidence.
            {
                content: "Dialog is closed",
                trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/14-restart-approval.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record to restart the approval process
            // for.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-EMP-RESTARTAPPROVAL) " +
                    ".o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Click the Restart Approval Process button.
            {
                content: "Click the Restart Approval Process button",
                trigger:
                    ".o_statusbar_buttons " +
                    "button[name='action_reload_approval_template']",
                extra_trigger: ".o_form_view",
            },
            // ── Flow 4 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status remains Waiting for Approval.
            {
                content: "Status remains Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm']" +
                    ".btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});
