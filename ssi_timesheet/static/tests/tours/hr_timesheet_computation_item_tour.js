odoo.define("ssi_timesheet.hr_timesheet_computation_item_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Configuration > Timesheets >
    // Timesheet Computation Items. "Timesheets" (level 3, under
    // Configuration) has one child of its own — the "Timesheet Computation
    // Items" leaf — so it is rendered as a non-clickable dropdown header
    // and is skipped here, exactly like the "Payroll Agreement" example in
    // the odoo-development-ui-test skill (patterns.md §A).
    function openComputationItemMenuSteps() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
            },
            {
                content: "Open the Timesheet Computation Items menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_timesheet.hr_timesheet_computation_item_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action ("Employees") is also a
                // .o_list_view.
                content: "Timesheet Computation Items list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active" +
                    ":contains(Timesheet Computation Items)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet_computation_item/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_computation_item_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openComputationItemMenuSteps(), [
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
            // ── Flow 3 — Fill in Name; leave Code as the default "/".
            {
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-COMP-CREATE-UI",
            },
            // ── Flow 4 — Click Generate Code. No sequence.template is
            // configured for this model in this repo (see the IK's own
            // caveat), so this always raises "No sequence template
            // found" — dismiss that dialog, then fill Code manually
            // with a non-"/" value as the IK instructs for that case.
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
            },
            {
                content: 'Dismiss the "No sequence template found" dialog',
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Fill in Code manually",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-CREATE-01",
            },
            // ── Flow 5 — On the Computation tab, the Python Code field is
            // shown pre-filled with the default comment template.
            {
                content: "Open the Computation tab",
                trigger: ".o_notebook .nav-link:contains(Computation)",
            },
            {
                content: "Python Code editor is displayed",
                trigger: ".o_field_widget[name='python_code'] .ace_editor",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 6 — Click Save.
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
            // ── Post-Condition — a new record is created.
            {
                content: "Back to the Timesheet Computation Items list",
                trigger:
                    ".breadcrumb-item.o_back_button a" +
                    ":contains(Timesheet Computation Items)",
            },
            {
                content: "New record appears in the list",
                trigger: ".o_data_row:contains(TOUR-COMP-CREATE-UI)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet_computation_item/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_computation_item_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openComputationItemMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-COMP-EDIT-UI) .o_data_cell:first",
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
            // ── Flow 3 — Reset Code back to "/".
            {
                content: "Reset the Code field to /",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },
            // ── Flow 4 — Click Generate Code. No sequence.template is
            // configured for this model in this repo (see the IK's own
            // caveat), so this always raises "No sequence template
            // found" — dismiss that dialog, then fill Code manually
            // with a non-"/" value as the IK instructs for that case.
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
            },
            {
                content: 'Dismiss the "No sequence template found" dialog',
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Fill in Code manually",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-EDIT-02",
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
    // IK: docs/hr_timesheet_computation_item/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_computation_item_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openComputationItemMenuSteps(), [
            // ── Flow 2-3 — select the record and delete it. Deletion is
            // driven from the record's own Action menu rather than the
            // list checkbox: the 14.0 list-selector checkbox is flaky
            // (odoo-development-ui-test skill, patterns.md §I), and this
            // reaches the same Post-Condition.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-COMP-DELETE-UI) .o_data_cell:first",
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
                content: "Back to the Timesheet Computation Items list",
                trigger:
                    ".breadcrumb-item.o_back_button a" +
                    ":contains(Timesheet Computation Items)",
            },
            // ── Post-Condition — records permanently removed.
            {
                content: "Deleted item no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-COMP-DELETE-UI)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet_computation_item/04-deactivate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_computation_item_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openComputationItemMenuSteps(), [
            // ── Flow 2-3 — select the record and archive it, from the
            // record's own form (same substitution as Delete above).
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-COMP-DEACTIVATE-UI) " +
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
            {
                content: "Uncheck Active",
                trigger: ".o_field_widget[name='active'] input",
                run: "click",
            },
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — record is archived.
            {
                content: "Archived ribbon is displayed",
                trigger: ".o_form_view .ribbon:visible:contains(Archived)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet_computation_item/05-activate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_computation_item_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openComputationItemMenuSteps(), [
            // ── Flow 2 — Enable the Archived filter.
            {
                content: "Open the Filters menu",
                trigger: ".o_search_options .o_filter_menu button",
                run: function () {
                    // Owl dropdowns in 14.0 are not always opened by a
                    // synthetic click — use a native click instead.
                    this.$anchor[0].click();
                },
            },
            {
                content: "Enable the Archived filter",
                trigger: ".o_filter_menu .o_menu_item a:contains(Archived)",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Archived item is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-COMP-ACTIVATE-UI)",
                extra_trigger: ".o_list_view",
            },
            // ── Flow 3-4 — select the record and unarchive it, from the
            // record's own form (same substitution as Delete above).
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-COMP-ACTIVATE-UI) .o_data_cell:first",
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
                content: "Click Unarchive",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $unarchive = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Unarchive";
                        }
                    );
                    $unarchive[0].click();
                },
            },
            // ── Post-Condition — record is restored. Unarchive executes
            // immediately without a confirmation dialog.
            {
                content: "Archived ribbon is no longer displayed",
                trigger: ".o_form_view:not(:has(.ribbon:visible:contains(Archived)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet_computation_item/06-reset-code.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_hr_timesheet_computation_item_reset_code",
        {
            test: true,
            url: "/web",
        },
        [].concat(openComputationItemMenuSteps(), [
            // ── Flow 2 — Select the record whose code will be reset. This
            // button only exists in the list header, so (unlike Delete/
            // Archive) it must be exercised via the list checkbox.
            {
                content: "Select the record",
                trigger:
                    ".o_data_row:contains(TOUR-COMP-RESETCODE-UI) " +
                    ".o_list_record_selector input",
                run: "click",
            },
            // ── Flow 3 — Click the Reset code button. Unlike form-view
            // buttons, list-view <header> buttons in 14.0 never honor
            // `confirm=` (web/static/src/js/views/list/list_controller.js
            // `_onHeaderButtonClicked` calls `_executeButtonAction`
            // directly and never reads `node.attrs.confirm`), so no
            // dialog appears here despite the IK's Flow step 4 — the
            // action runs immediately.
            {
                content: "Click the Reset code button",
                trigger: ".o_control_panel button[name='action_reset_code']",
            },
            // ── Post-Condition — Code returns to "/": the list reloads
            // after the action and the row no longer shows the old code.
            {
                content: "Row no longer shows the old code",
                trigger: ".o_list_view:not(:has(.o_data_row:contains(TCI-RESET)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});
