odoo.define("ssi_work_log_cost.work_log_rate_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Timesheets > Work Log Rates.
    // "Timesheets" (level 2, section) has children of its own but level-2
    // sections are still rendered as clickable <a data-menu-xmlid=...>;
    // only level >= 3 items with children degrade into a non-clickable
    // .dropdown-header. "Work Log Rates" is a level-3 leaf, so both get a
    // step — matching the three menu segments written in every
    // work_log_rate IK ("Menu: Human Resource > Timesheets > Work Log
    // Rates").
    function openWorkLogRateMenuSteps() {
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
                content: "Open the Work Log Rates menu item",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_work_log_cost.menu_work_log_rate"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action ("Employees") is also a
                // .o_list_view, so it would match while this action is
                // still loading.
                content: "Work Log Rates list is displayed",
                trigger:
                    ".o_control_panel " +
                    ".breadcrumb-item.active:contains(Work Log Rates)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Every draft work_log_rate still carries "/" as its document number
    // (the sequence is only assigned on the transition to Ready to Start,
    // _create_sequence_state = "ready"), so list rows are located by the
    // Employee column instead — it is present in work_log_rate_view_tree.
    function openRecordSteps(employeeName) {
        return [
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(" + employeeName + ") .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form view is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    var confirmDialogStep = {
        content: "Click OK on the confirmation dialog",
        trigger: ".modal-footer button.btn-primary",
        in_modal: true,
    };

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/work_log_rate/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_cost_work_log_rate_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openWorkLogRateMenuSteps(), [
            // ── Flow 2 — Click the New button ("Create" in 14.0).
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // ── Flow 3 — Fill in Employee, Date, Date Start, Date End.
            {
                content: "Select the Employee",
                trigger: ".o_field_many2one[name='employee_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-WLR-EMP-CREATE",
            },
            {
                content: "Pick the Employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR-WLR-EMP-CREATE)",
                in_modal: false,
            },
            {
                content: "Fill in Date",
                trigger: ".o_field_widget[name='date'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur 01/15/2026",
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
                run: "text_blur 01/31/2026",
            },
            // ── Flow 4 — On the General Rates tab, click Add a line, then
            // fill in Product and Pricelist.
            {
                content: "Open the General Rates tab",
                trigger: ".o_notebook .nav-link:contains(General Rates)",
            },
            {
                content: "Add a general rate line",
                trigger:
                    ".o_field_x2many[name='general_rate_ids'] " +
                    ".o_field_x2many_list_row_add a",
            },
            {
                content: "Select the Product",
                trigger: ".o_selected_row .o_field_widget[name='product_id'] input",
                run: "text TOUR-WLR-PRODUCT",
            },
            {
                content: "Pick the Product from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-WLR-PRODUCT)",
                in_modal: false,
            },
            {
                content: "Select the Pricelist",
                trigger: ".o_selected_row .o_field_widget[name='pricelist_id'] input",
                run: "text TOUR-WLR-PRICELIST",
            },
            {
                content: "Pick the Pricelist from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR-WLR-PRICELIST)",
                in_modal: false,
            },
            {
                // Mechanics, not a Flow step: a cell still in edit mode when
                // Save is clicked does not send its value to the record
                // (odoo-development-ui-test skill, patterns.md §C "Jebakan
                // 2"). The <td> wrapping an o2m cell carries no `name`
                // attribute in 14.0 and this is the only row, so there is no
                // sibling cell to click; clicking the notebook tab — an
                // element outside the editable list — unselects the row via
                // ListRenderer._onWindowClicked without navigating anywhere,
                // because the General Rates tab is already the active one.
                content: "Commit the general rate line",
                trigger: ".o_notebook .nav-link:contains(General Rates)",
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
                    // Assertion only; do not trigger the default click action.
                },
            },
            // ── Post-Condition — a new record is created in Draft status.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft']" +
                    ".btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/work_log_rate/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_cost_work_log_rate_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openWorkLogRateMenuSteps(),
            // ── Flow 2 — Find and open the record to edit.
            openRecordSteps("TOUR-WLR-EMP-EDIT"),
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
                // ── Flow 3 — Change Date End (the IK leaves which of
                // Employee / Date / Date Start / Date End to change up to
                // the actor: "as needed").
                {
                    content: "Change Date End",
                    trigger: ".o_field_widget[name='date_end'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text_blur 02/28/2026",
                },
                // ── Flow 4 — The General Rates tab is left as it is; the IK
                // makes changing its lines optional ("as needed"), and the
                // line mechanics are already exercised by the create tour.
                // ── Flow 5 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                // ── Post-Condition — the record is updated with the new
                // values.
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Date End shows the new value",
                    trigger:
                        ".o_form_view.o_form_readonly " +
                        ".o_field_widget[name='date_end']:contains(02/28/2026)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/work_log_rate/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_cost_work_log_rate_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openWorkLogRateMenuSteps(),
            // ── Flow 2-3 — select the record and delete it. Deletion is
            // driven from the record's own Action menu rather than the list
            // checkbox: the 14.0 list-selector checkbox is flaky
            // (odoo-development-ui-test skill, patterns.md §I), and this
            // reaches the same Post-Condition.
            openRecordSteps("TOUR-WLR-EMP-DELETE"),
            [
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Delete",
                    // Action menu items are Owl components; match the exact
                    // label so "Duplicate" is never picked instead.
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
                    content: "Back to the Work Log Rates list",
                    trigger:
                        ".breadcrumb-item.o_back_button a:contains(Work Log Rates)",
                },
                // ── Post-Condition — the selected record is permanently
                // removed from the system.
                {
                    content: "Deleted work log rate no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row" +
                        ":contains(TOUR-WLR-EMP-DELETE)))",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/work_log_rate/04-confirm.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_cost_work_log_rate_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openWorkLogRateMenuSteps(),
            // ── Flow 2 — Open the record to confirm.
            openRecordSteps("TOUR-WLR-EMP-CONFIRM"),
            [
                // ── Flow 3 — Click the Confirm button.
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },
                // ── Flow 4 — Click OK on the confirmation dialog.
                confirmDialogStep,
                // ── Post-Condition — status changes to Waiting for Approval.
                // The modal-closed gate is mandatory here: once the dialog
                // leaves the DOM the tour engine starts polling immediately
                // while the form behind it is still re-rendering, which trips
                // FieldWrapper.updateModifiersValue in 14.0
                // (odoo-development-ui-test skill, patterns.md §K).
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm']" +
                        ".btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    // Approval records were created for the single approver
                    // level of the "Standard" approval.template — the
                    // kasatmata evidence of that is the Approve button
                    // becoming available.
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
});
