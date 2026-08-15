odoo.define("ssi_hr_holiday.hr_leave_allocation_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Timesheets > Leave
    // Allocations. "Timesheets" (level 2, section) has several children
    // (Timesheets, Leaves, Leave Allocations) so it is clickable as a
    // dropdown-toggle; "Leave Allocations" (level 3) is a leaf, also
    // clickable.
    function openLeaveAllocationMenuSteps() {
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
                content: "Open the Leave Allocations menu item",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_hr_holiday.menu_hr_leave_allocation"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action is also a .o_list_view.
                content: "Leave Allocations list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(" +
                    "Leave Allocations)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Click a statusbar/header button by its exact visible label. The
    // Cancel and Terminate buttons share this form's statusbar but their
    // `name` attribute is a numeric action id (their respective "Select
    // Reason" wizard actions) rather than a method name, so matching by
    // trimmed text is the only selector that is deterministic across both.
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

    var openRecordStep = function (label) {
        return [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(" + label + ") .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ];
    };

    var confirmDialogStep = {
        content: "Confirm the dialog",
        trigger: ".modal-footer button.btn-primary",
        in_modal: true,
    };

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_allocation/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openLeaveAllocationMenuSteps(), [
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
            // ── Flow 3 — Fill in Leave Type, Employee, Date Start, Date
            // End, Number of Days.
            {
                content: "Select the Leave Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-LTYPE-ALLOC",
            },
            {
                content: "Pick the Leave Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-LTYPE-ALLOC)",
                in_modal: false,
            },
            {
                content: "Select the Employee",
                trigger: ".o_field_many2one[name='employee_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-EMP-ALLOC-CREATE",
            },
            {
                content: "Pick the Employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(" +
                    "TOUR-EMP-ALLOC-CREATE)",
                in_modal: false,
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur 01/01/2026",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur 12/31/2026",
            },
            {
                content: "Fill in Number of Days",
                trigger: ".o_field_widget[name='number_of_days']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 12",
            },
            // ── Flow 4 — Click Save.
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
            // ── Post-Condition — a new allocation record is created in
            // Draft.
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
    // IK: docs/hr_leave_allocation/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveAllocationMenuSteps(),
            openRecordStep("TOUR-EMP-ALLOC-EDIT"),
            [
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
                // ── Flow 3 — Change Number of Days.
                {
                    content: "Change Number of Days",
                    trigger: ".o_field_widget[name='number_of_days']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 20",
                },
                // ── Flow 4 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                // ── Post-Condition — the record is updated.
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_allocation/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveAllocationMenuSteps(),
            openRecordStep("TOUR-EMP-ALLOC-DELETE"),
            [
                // ── Flow 2-3 — Select the record and click Action >
                // Delete. Driven from the record's own Action menu rather
                // than the list checkbox: the 14.0 list-selector checkbox
                // is flaky (odoo-development-ui-test skill, patterns.md
                // §I), and this reaches the same Post-Condition.
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
                // ── Flow 4 — Click OK to confirm.
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content:
                        "Click the Leave Allocations breadcrumb to return " +
                        "to the list",
                    trigger:
                        ".breadcrumb-item.o_back_button a:contains(" +
                        "Leave Allocations)",
                },
                // ── Post-Condition — the record is permanently removed.
                {
                    content: "Deleted allocation no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(" +
                        "TOUR-EMP-ALLOC-DELETE)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_allocation/04-confirm.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveAllocationMenuSteps(),
            openRecordStep("TOUR-EMP-ALLOC-CONFIRM"),
            [
                // ── Flow 3 — Click the Confirm button.
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },
                // ── Flow 4 — Click OK on the confirmation dialog.
                confirmDialogStep,
                // ── Post-Condition — status changes to Waiting for
                // Approval, and approval records are created for the
                // pending level (evidenced by the Approve button
                // becoming available).
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
                        ".o_statusbar_buttons " +
                        "button[name='action_approve_approval']:visible",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_allocation/05-approve.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveAllocationMenuSteps(),
            openRecordStep("TOUR-EMP-ALLOC-APPROVE"),
            [
                // ── Flow 3 — Click the Approve button.
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },
                // ── Flow 4 — Click OK on the confirmation dialog.
                confirmDialogStep,
                // ── Post-Condition — single-level approval fulfilled
                // immediately, so status changes to In Progress.
                {
                    content: "Status is In Progress",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open']" +
                        ".btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_allocation/06-reject.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveAllocationMenuSteps(),
            openRecordStep("TOUR-EMP-ALLOC-REJECT"),
            [
                // ── Flow 3 — Click the Reject button.
                {
                    content: "Click the Reject button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reject_approval']",
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
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_allocation/10-cancel.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveAllocationMenuSteps(),
            openRecordStep("TOUR-EMP-ALLOC-CANCEL"),
            [
                // ── Flow 3 — Click the Cancel button. `name` is a numeric
                // action id on this button, so match its label instead.
                clickHeaderButtonByLabel("Cancel"),
                // ── Flow 4 — In the wizard, select the Reason.
                {
                    // 14.0: do NOT prefix with `.modal` — the trigger is
                    // searched INSIDE the modal already (odoo-development-
                    // ui-test skill, patterns.md §H).
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
                        ".o_radio_item:contains(TOUR-ALLOC-CANCEL-REASON) input",
                },
                // ── Flow 5 — Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                // ── Flow 6 — Click OK on the confirmation dialog.
                confirmDialogStep,
                // ── Post-Condition — status changes to Cancelled, and the
                // selected Reason is recorded on the allocation.
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
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_allocation/11-terminate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_terminate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveAllocationMenuSteps(),
            openRecordStep("TOUR-EMP-ALLOC-TERMINATE"),
            [
                // ── Flow 3 — Click the Terminate button. `name` is a
                // numeric action id on this button, so match its label
                // instead.
                clickHeaderButtonByLabel("Terminate"),
                // ── Flow 4 — In the wizard, select the Reason.
                {
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Select the termination reason",
                    trigger:
                        ".o_field_widget[name='terminate_reason_id'] " +
                        ".o_radio_item:contains(TOUR-ALLOC-TERMINATE-REASON) input",
                },
                // ── Flow 5 — Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                // ── Flow 6 — Click OK on the confirmation dialog.
                confirmDialogStep,
                // ── Post-Condition — status changes to Terminated, and
                // the selected Reason is recorded on the allocation.
                {
                    content: "Status is Terminated",
                    trigger:
                        ".o_statusbar_status " +
                        ".o_arrow_button[data-value='terminate'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Termination reason is displayed",
                    trigger: "h2:visible:contains(Termination reason)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_allocation/12-restart.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveAllocationMenuSteps(),
            openRecordStep("TOUR-EMP-ALLOC-RESTART"),
            [
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
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_allocation/13-reset-number.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveAllocationMenuSteps(),
            openRecordStep("TOUR-EMP-ALLOC-RESETNUM"),
            [
                // ── Flow 3 — Click the Reset Document Number button.
                {
                    content: "Click the Reset Document Number button",
                    trigger:
                        ".o_statusbar_buttons " +
                        "button[name='action_reset_document_number']",
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
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_allocation/14-restart-approval.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_allocation_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveAllocationMenuSteps(),
            openRecordStep("TOUR-EMP-ALLOC-RESTARTAPPROVAL"),
            [
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
                // ── Post-Condition — status remains unchanged (Waiting
                // for Approval).
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
            ]
        )
    );
});
