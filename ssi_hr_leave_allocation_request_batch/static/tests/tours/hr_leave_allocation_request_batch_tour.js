odoo.define(
    "ssi_hr_leave_allocation_request_batch.hr_leave_allocation_request_batch_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared opening steps: Human Resource > Timesheets > Leave Allocation
        // Request Batch. "Timesheets" (level 2, section) has several children
        // (Timesheets, Leaves, Leave Allocations, Leave Allocation Request
        // Batch, ...) so it is clickable as a dropdown-toggle; "Leave
        // Allocation Request Batch" (level 3) is a leaf, also clickable.
        function openLeaveAllocationRequestBatchMenuSteps() {
            return [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
                },
                {
                    content: "Open the Timesheets section",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_timesheet.timesheet_menu"]',
                },
                {
                    content: "Open the Leave Allocation Request Batch menu item",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_hr_leave_allocation_request_batch.' +
                        'menu_hr_leave_allocation_request_batch"]',
                },
                {
                    // Gate: wait for the TARGET action, not just any list view —
                    // the app landing action is also a .o_list_view.
                    content: "Leave Allocation Request Batch list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(" +
                        "Leave Allocation Request Batch)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // Click a statusbar/header button by its exact visible label. The
        // Cancel button shares this form's statusbar but its `name` attribute
        // is a numeric action id (the Select Cancel Reason wizard action)
        // rather than a method name, so matching by trimmed text is the only
        // selector that is deterministic.
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

        var openLeaveAllocationRequestTabStep = {
            content: "Open the Leave Allocation Request tab",
            trigger: ".o_notebook .nav-link:contains(Leave Allocation Request)",
        };

        // ═══════════════════════════════════════════════════════════════
        // IK: docs/hr_leave_allocation_request_batch/01-create.md
        // ═══════════════════════════════════════════════════════════════
        tour.register(
            "ssi_hr_leave_allocation_request_batch_hr_leave_allocation_request_batch_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(openLeaveAllocationRequestBatchMenuSteps(), [
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
                // ── Flow 3 — Fill in Type, Number Of Days, Employee(s), Date
                // Start, Date End. (Can be Extended / Date Extended are
                // optional and left at their auto-filled default.)
                {
                    content: "Select the Type",
                    trigger: ".o_field_many2one[name='type_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR-BATCH-LTYPE-CREATE",
                },
                {
                    content: "Pick the Type from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(" +
                        "TOUR-BATCH-LTYPE-CREATE)",
                    in_modal: false,
                },
                {
                    content: "Fill in Number Of Days",
                    trigger: ".o_field_widget[name='number_of_days']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 12",
                },
                // Employee(s) lives on the "Employee" notebook tab, which is
                // not the tab active by default when the form opens — it must
                // be opened before its field is interactable (odoo-
                // development-ui-test skill, patterns.md §E).
                {
                    content: "Open the Employee tab",
                    trigger: ".o_notebook .nav-link:contains(Employee)",
                },
                // `employee_ids` has no `widget=` attribute in the view, so it
                // renders as the default FieldMany2Many — an embedded list
                // with an "Add a line" control that opens a
                // SelectCreateDialog, not a tag-input with a free-type
                // autocomplete (verified against web/static/src/js/fields/
                // relational_fields.js FieldMany2Many.onAddRecordOpenDialog
                // and web/static/src/js/views/view_dialogs.js
                // SelectCreateDialog: a single click on a dialog row fires
                // `select_record`, which selects that record and closes the
                // dialog immediately).
                {
                    content: "Add an Employee line",
                    trigger:
                        ".o_field_widget[name='employee_ids'] " +
                        ".o_field_x2many_list_row_add a",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    content: "Search for the Employee in the dialog",
                    trigger: ".o_searchview_input",
                    run: "text TOUR-BATCH-EMP-CREATE",
                },
                {
                    content: "Validate the search",
                    trigger: ".o_searchview_autocomplete li.o_menu_item:first",
                },
                {
                    content: "Select the Employee from the dialog list",
                    trigger:
                        ".o_data_row:contains(TOUR-BATCH-EMP-CREATE) " +
                        ".o_data_cell:first",
                },
                {
                    content: "Fill in Date Start",
                    trigger: ".o_field_widget[name='date_start'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text_blur 01/05/2026",
                },
                {
                    content: "Fill in Date End",
                    trigger: ".o_field_widget[name='date_end'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text_blur 01/31/2026",
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
                // ── Post-Condition — a new leave allocation request batch
                // record is created in Draft.
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
        // IK: docs/hr_leave_allocation_request_batch/02-edit.md
        // ═══════════════════════════════════════════════════════════════
        tour.register(
            "ssi_hr_leave_allocation_request_batch_hr_leave_allocation_request_batch_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openLeaveAllocationRequestBatchMenuSteps(),
                openRecordStep("TOUR-BATCH-LTYPE-EDIT"),
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
                    // ── Flow 3 — Change Number Of Days.
                    {
                        content: "Change Number Of Days",
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
        // IK: docs/hr_leave_allocation_request_batch/03-delete.md
        // ═══════════════════════════════════════════════════════════════
        tour.register(
            "ssi_hr_leave_allocation_request_batch_hr_leave_allocation_request_batch_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openLeaveAllocationRequestBatchMenuSteps(),
                openRecordStep("TOUR-BATCH-LTYPE-DELETE"),
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
                            "Click the Leave Allocation Request Batch breadcrumb to " +
                            "return to the list",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(" +
                            "Leave Allocation Request Batch)",
                    },
                    // ── Post-Condition — the record is permanently removed.
                    {
                        content:
                            "Deleted leave allocation request batch no longer " +
                            "appears in the list",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(" +
                            "TOUR-BATCH-LTYPE-DELETE)))",
                        run: function () {
                            // Assertion only; do not trigger the default click
                            // action.
                        },
                    },
                ]
            )
        );

        // ═══════════════════════════════════════════════════════════════
        // IK: docs/hr_leave_allocation_request_batch/04-confirm.md
        // ═══════════════════════════════════════════════════════════════
        tour.register(
            "ssi_hr_leave_allocation_request_batch_hr_leave_allocation_request_batch_confirm",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openLeaveAllocationRequestBatchMenuSteps(),
                openRecordStep("TOUR-BATCH-LTYPE-CONFIRM"),
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
                    // pending level (evidenced by the Approve button becoming
                    // available).
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
                    // ── Post-Condition — the Leave Allocation Request tab
                    // still stays empty: confirming the batch does not create
                    // any hr.leave_allocation document yet (unlike Confirm, it
                    // is Approve/Done that creates them — see 05-approve.md).
                    openLeaveAllocationRequestTabStep,
                    {
                        content: "The Leave Allocation Request tab stays empty",
                        trigger:
                            ".o_field_widget[name='leave_allocation_request_ids']" +
                            ":not(:has(.o_data_row))",
                        run: function () {
                            // Assertion only; do not trigger the default click
                            // action.
                        },
                    },
                ]
            )
        );

        // ═══════════════════════════════════════════════════════════════
        // IK: docs/hr_leave_allocation_request_batch/05-approve.md
        // ═══════════════════════════════════════════════════════════════
        tour.register(
            "ssi_hr_leave_allocation_request_batch_hr_leave_allocation_request_batch_approve",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openLeaveAllocationRequestBatchMenuSteps(),
                openRecordStep("TOUR-BATCH-LTYPE-APPROVE"),
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
                    // ── Post-Condition — reaching Done creates one
                    // hr.leave_allocation document per employee, which appears
                    // in the Leave Allocation Request tab.
                    openLeaveAllocationRequestTabStep,
                    {
                        content:
                            "The created hr.leave_allocation document appears in " +
                            "the Leave Allocation Request tab",
                        trigger: ".o_data_row:contains(TOUR-BATCH-EMP-APPROVE)",
                        run: function () {
                            // Assertion only; do not trigger the default click
                            // action.
                        },
                    },
                ]
            )
        );

        // ═══════════════════════════════════════════════════════════════
        // IK: docs/hr_leave_allocation_request_batch/06-reject.md
        // ═══════════════════════════════════════════════════════════════
        tour.register(
            "ssi_hr_leave_allocation_request_batch_hr_leave_allocation_request_batch_reject",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openLeaveAllocationRequestBatchMenuSteps(),
                openRecordStep("TOUR-BATCH-LTYPE-REJECT"),
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
                    // ── Post-Condition — no hr.leave_allocation document is
                    // created; the Leave Allocation Request tab stays empty.
                    openLeaveAllocationRequestTabStep,
                    {
                        content: "The Leave Allocation Request tab stays empty",
                        trigger:
                            ".o_field_widget[name='leave_allocation_request_ids']" +
                            ":not(:has(.o_data_row))",
                        run: function () {
                            // Assertion only; do not trigger the default click
                            // action.
                        },
                    },
                ]
            )
        );

        // ═══════════════════════════════════════════════════════════════
        // IK: docs/hr_leave_allocation_request_batch/10-cancel.md
        // ═══════════════════════════════════════════════════════════════
        tour.register(
            "ssi_hr_leave_allocation_request_batch_hr_leave_allocation_request_batch_cancel",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openLeaveAllocationRequestBatchMenuSteps(),
                openRecordStep("TOUR-BATCH-LTYPE-CANCEL"),
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
                            ".o_radio_item:contains(TOUR-BATCH-CANCEL-REASON) input",
                    },
                    // ── Flow 5 — Click Confirm.
                    {
                        content: "Confirm the wizard",
                        trigger: ".modal-footer button[name='action_confirm']",
                    },
                    // ── Flow 6 — Click OK on the confirmation dialog.
                    confirmDialogStep,
                    // ── Post-Condition — status changes to Cancelled, and the
                    // selected Reason is recorded.
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
        // IK: docs/hr_leave_allocation_request_batch/12-restart.md
        // ═══════════════════════════════════════════════════════════════
        tour.register(
            "ssi_hr_leave_allocation_request_batch_hr_leave_allocation_request_batch_restart",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openLeaveAllocationRequestBatchMenuSteps(),
                openRecordStep("TOUR-BATCH-LTYPE-RESTART"),
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
        // IK: docs/hr_leave_allocation_request_batch/13-reset-number.md
        // ═══════════════════════════════════════════════════════════════
        tour.register(
            "ssi_hr_leave_allocation_request_batch_hr_leave_allocation_request_batch_reset_number",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openLeaveAllocationRequestBatchMenuSteps(),
                openRecordStep("TOUR-BATCH-LTYPE-RESETNUM"),
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
        // IK: docs/hr_leave_allocation_request_batch/14-restart-approval.md
        // ═══════════════════════════════════════════════════════════════
        tour.register(
            "ssi_hr_leave_allocation_request_batch_hr_leave_allocation_request_batch_" +
                "restart_approval",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openLeaveAllocationRequestBatchMenuSteps(),
                openRecordStep("TOUR-BATCH-LTYPE-REAPPROVAL"),
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
                ]
            )
        );
    }
);
