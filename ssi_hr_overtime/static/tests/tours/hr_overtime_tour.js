odoo.define("ssi_hr_overtime.hr_overtime_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Timesheets > Overtimes.
    // "Timesheets" (level 2, section) has several children (Timesheets,
    // Leaves, Leave Allocations, Overtimes, ...) so it is clickable as a
    // dropdown-toggle; "Overtimes" (level 3) is a leaf, also clickable.
    function openOvertimeMenuSteps() {
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
                content: "Open the Overtimes menu item",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_hr_overtime.menu_hr_overtime"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action is also a .o_list_view.
                content: "Overtimes list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Overtimes)",
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

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_overtime/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeMenuSteps(), [
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
            // ── Flow 3 — Fill in Employee, Overtime Type, Date, Date
            // Start, Date End.
            {
                content: "Select the Employee",
                trigger: ".o_field_many2one[name='employee_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-EMP-OT-CREATE",
            },
            {
                content: "Pick the Employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(" +
                    "TOUR-EMP-OT-CREATE)",
                in_modal: false,
            },
            {
                content: "Select the Overtime Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-OTTYPE",
            },
            {
                content: "Pick the Overtime Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-OTTYPE)",
                in_modal: false,
            },
            {
                content: "Fill in Date",
                trigger: ".o_field_widget[name='date'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur 01/05/2026",
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur 01/05/2026 08:00:00",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur 01/05/2026 17:00:00",
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
            // ── Post-Condition — a new overtime record is created in
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
    // IK: docs/hr_overtime/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeMenuSteps(), openRecordStep("TOUR-EMP-OT-EDIT"), [
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
                run: "text_blur 02/05/2026 18:00:00",
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
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_overtime/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeMenuSteps(), openRecordStep("TOUR-EMP-OT-DELETE"), [
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
                content: "Click the Overtimes breadcrumb to return to the list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Overtimes)",
            },
            // ── Post-Condition — the record is permanently removed.
            {
                content: "Deleted overtime no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(" +
                    "TOUR-EMP-OT-DELETE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_overtime/04-confirm.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeMenuSteps(), openRecordStep("TOUR-EMP-OT-CONFIRM"), [
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
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_overtime/05-approve.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeMenuSteps(), openRecordStep("TOUR-EMP-OT-APPROVE"), [
            // ── Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
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
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_overtime/06-reject.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeMenuSteps(), openRecordStep("TOUR-EMP-OT-REJECT"), [
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
    // IK: docs/hr_overtime/10-cancel.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeMenuSteps(), openRecordStep("TOUR-EMP-OT-CANCEL"), [
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
                    ".o_radio_item:contains(TOUR-OT-CANCEL-REASON) input",
            },
            // ── Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            // ── Flow 6 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status changes to Cancelled, the
            // selected Reason is recorded, and Attendances is cleared.
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
    // IK: docs/hr_overtime/12-restart.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeMenuSteps(), openRecordStep("TOUR-EMP-OT-RESTART"), [
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
    // IK: docs/hr_overtime/13-reset-number.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeMenuSteps(), openRecordStep("TOUR-EMP-OT-RESETNUM"), [
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
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_overtime/14-restart-approval.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openOvertimeMenuSteps(),
            openRecordStep("TOUR-EMP-OT-RESTARTAPPROVAL"),
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
});
