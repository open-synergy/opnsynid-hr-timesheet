odoo.define("ssi_work_log_expense.work_log_expense_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Timesheets > Work Log
    // Expenses — the "Menu:" line written in every work_log_expense IK.
    // "Timesheets" (level 2, section) has children, so it is rendered as
    // a clickable dropdown-toggle and keeps its own step; "Work Log
    // Expenses" (level 3) is a leaf, so it carries a data-menu-xmlid.
    function openWorkLogExpenseMenuSteps() {
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
                content: "Open the Work Log Expenses menu item",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_work_log_expense.work_log_expense_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action ("Employees") is also a
                // .o_list_view, and it stays on screen while this action
                // is still loading.
                content: "Work Log Expenses list is displayed",
                trigger:
                    ".o_control_panel " +
                    ".breadcrumb-item.active:contains(Work Log Expenses)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Gate for the Populate button (a type="object" button that saves the
    // record, rewrites detail_ids and reloads the form, all asynchronously).
    //
    // The gate is NOT a data delta: no hr.work_log fixture is seeded for
    // these tours, because a work log is itself a transactional document
    // that would have to be driven through confirm/approve just to exist
    // in state Done — and the lines it would produce may not be asserted
    // here anyway (this issue's Design Decision keeps value assertions in
    // the unit tests). Populate may therefore legitimately yield zero
    // lines, which rules out a data-driven gate
    // (odoo-development-ui-test skill, patterns.md §P table, third row).
    //
    // What is used instead is data-independent: Odoo 14 disables the
    // control-panel Save/Discard buttons for the WHOLE object-button cycle
    // (save -> call_button -> reload) and re-enables them only when it
    // settles, so `.o_form_button_save:enabled` cannot be true while the
    // cycle is still running (patterns.md §M).
    //
    // It must be the SAVE button, not the Populate button itself. Populate
    // lives inside the notebook page, outside the control-panel button set
    // that gets disabled, so `button[name='action_populate']:enabled` is
    // true throughout and gates nothing — CI proved it: on the edit tour it
    // succeeded 17 ms after the click, Save was clicked 11 ms later while
    // still disabled (so the click was swallowed silently), and the form
    // never left edit mode.
    var populateFinishedStep = {
        content: "Populate has finished and Save is usable again",
        trigger: ".o_form_button_save:enabled",
        run: function () {
            // Assertion only; do not trigger the default click action.
        },
    };

    var confirmDialogStep = {
        content: "Confirm the dialog",
        trigger: ".modal-footer button.btn-primary",
        in_modal: true,
    };

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/work_log_expense/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_expense_work_log_expense_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openWorkLogExpenseMenuSteps(), [
            // ── Flow 2 — Click the New button. (14.0: "Create")
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
            // ── Flow 3 — Fill in the fields. Employee gets no step of its
            // own: the IK states it is "automatically filled from the
            // current user's linked employee record", and setUpClass
            // guarantees the tour user has one. Manager, Job Position and
            // Department are filled from it and cannot be edited. Analytic
            // Account is optional and left empty, which the IK allows.
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-WLE-TYPE",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-WLE-TYPE)",
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
                run: "text_blur 01/31/2026",
            },
            {
                content: "Fill in Date",
                trigger: ".o_field_widget[name='date'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur 01/15/2026",
            },
            // ── Flow 4 — On the Details tab, click Populate.
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
            },
            {
                content: "Click Populate",
                trigger: ".o_form_view button[name='action_populate']",
            },
            {
                // Two gates at once. The trigger is the button-cycle gate
                // described above; the extra_trigger additionally proves
                // the implicit save landed: a brand-new record's
                // breadcrumb title is the literal "New" until the server
                // returns a display_name, so this cannot match earlier
                // (patterns.md §P).
                content: "Populate has finished and the record was saved",
                trigger: ".o_form_button_save:enabled",
                extra_trigger:
                    ".o_control_panel .breadcrumb-item.active:not(:contains(New))",
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
            // ── Post-Condition — a new work log expense record is created
            // in Draft status.
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
    // IK: docs/work_log_expense/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_expense_work_log_expense_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openWorkLogExpenseMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit. A record that
            // already exists opens read-only in 14.0, so Edit is clicked
            // here before any field is touched (patterns.md §E).
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-WLE-EMP-EDIT) .o_data_cell:first",
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
                run: "text_blur 02/10/2026",
            },
            // ── Flow 4 — On the Details tab, click Populate.
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
            },
            {
                content: "Click Populate",
                trigger: ".o_form_view button[name='action_populate']",
            },
            populateFinishedStep,
            // ── Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — the record is updated with the new
            // values. What a tour may assert here is that the save landed
            // and the form returned to read-only; comparing the stored
            // field values themselves belongs to the unit tests, per this
            // issue's Design Decision.
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
    // IK: docs/work_log_expense/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_expense_work_log_expense_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openWorkLogExpenseMenuSteps(), [
            // ── Flow 2-3 — Select the record and delete it via Action >
            // Delete. The selection is made by opening the record and
            // using its own Action menu rather than the list checkbox:
            // the 14.0 list-selector checkbox combined with the
            // multi-select Action menu races with Owl's async re-render
            // and sometimes leaves the dropdown unopened
            // (odoo-development-ui-test skill, patterns.md §I; same
            // treatment as ssi_timesheet and ssi_timesheet_attendance_shift
            // in this repo). The Post-Condition reached is identical.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-WLE-EMP-DELETE) .o_data_cell:first",
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
            confirmDialogStep,
            {
                content: "Back to the Work Log Expenses list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Work Log Expenses)",
            },
            // ── Post-Condition — the selected record is permanently
            // removed from the system.
            {
                content: "Deleted work log expense no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(" +
                    ".o_data_row:contains(TOUR-WLE-EMP-DELETE)))",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/work_log_expense/04-confirm.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_expense_work_log_expense_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openWorkLogExpenseMenuSteps(), [
            // ── Flow 2 — Open the record to confirm.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-WLE-EMP-CONFIRM) .o_data_cell:first",
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
            // and the Approve button becoming available is the visible
            // evidence that approval records were created for the level
            // defined by the Standard approval.template.
            //
            // The modal-closed gate is mandatory on an assertion that
            // follows a dialog: the tour engine starts polling the new
            // status the instant the modal leaves the DOM, while the form
            // behind it is still re-rendering (patterns.md §K).
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
});
