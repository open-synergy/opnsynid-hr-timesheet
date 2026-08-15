odoo.define("ssi_hr_holiday.hr_leave_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Configuration > Timesheets >
    // Leave Type. "Timesheets" (level 3, under Configurations) always has
    // more than one child in this repo (this module's own "Leave Type" plus
    // "ssi_timesheet"'s "Computation Item"), so it renders as a
    // non-clickable dropdown header and is skipped here — only the leaf
    // "Leave Type" item gets a step.
    function openLeaveTypeMenuSteps() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Configurations menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
            },
            {
                content: "Open the Leave Type menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_hr_holiday.hr_leave_type_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action is also a .o_list_view.
                content: "Leave Type list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Leave Type)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Select the checkbox on the row matching `label`, wait for the Action
    // menu to become available (it only renders once a row is selected —
    // web/static/src/js/components/action_menus.js: `t-if="actionItems.
    // length"`, and list_controller.js only populates actionItems once
    // `selectedRecords.length` is non-zero — so this step cannot match
    // before the checkbox is actually ticked), then click the named menu
    // item by its exact visible label.
    function selectRowAndClickActionMenuItem(label, menuLabel) {
        return [
            {
                content: "Select the " + label + " row",
                trigger:
                    ".o_data_row:contains(" + label + ") .o_list_record_selector input",
                run: "click",
            },
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click " + menuLabel,
                // Action menu items are Owl components; target the <a>
                // inside .o_menu_item and match the exact label —
                // :contains() as a substring could pick the wrong item
                // (e.g. "Archive" vs "Unarchive").
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $item = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === menuLabel;
                        }
                    );
                    $item[0].click();
                },
            },
        ];
    }

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_type/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_type_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openLeaveTypeMenuSteps(), [
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
            // ── Flow 3 — Fill in Leave Type (name) and Code.
            {
                content: "Fill in Leave Type",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-LTYPE-CREATE",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },
            // ── Flow 4 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — a new leave type record is created.
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
    // IK: docs/hr_leave_type/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_type_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openLeaveTypeMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-LTYPE-EDIT) .o_data_cell:first",
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
            // ── Flow 3 — Change Leave Type.
            {
                content: "Change Leave Type",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-LTYPE-EDITED",
            },
            // ── Flow 4 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — the record is updated with the new value.
            {
                content: "Leave Type shows the new value",
                trigger:
                    ".o_form_view.o_form_readonly " +
                    ".o_field_widget[name='name']:contains(TOUR-LTYPE-EDITED)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_type/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_type_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveTypeMenuSteps(),
            // ── Flow 2-3 — Select the record and click Action > Delete.
            selectRowAndClickActionMenuItem("TOUR-LTYPE-DELETE", "Delete"),
            [
                // ── Flow 4 — Click OK to confirm.
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                // ── Post-Condition — the record is permanently removed.
                {
                    content: "Deleted leave type no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(" +
                        "TOUR-LTYPE-DELETE)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_type/04-deactivate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_type_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openLeaveTypeMenuSteps(),
            // ── Flow 2-3 — Select the record and click Action > Archive.
            selectRowAndClickActionMenuItem("TOUR-LTYPE-DEACTIVATE", "Archive"),
            [
                // ── Flow 4 — Click OK to confirm. Archive (unlike
                // Unarchive) opens a Dialog.confirm before applying
                // (web/static/src/js/views/list/list_controller.js:485).
                {
                    content: "Confirm archiving",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                // ── Post-Condition — the record is archived and no longer
                // appears in the default list view.
                {
                    content: "Archived leave type no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(" +
                        "TOUR-LTYPE-DEACTIVATE)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_leave_type/05-activate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_holiday_hr_leave_type_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openLeaveTypeMenuSteps(), [
            // ── Flow 2 — Enable the Archived filter in the search bar.
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
                // Gate: the archived TOUR-LTYPE-ACTIVATE record is only
                // reachable once the Archived filter is actually applied.
                content: "Archived leave type is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-LTYPE-ACTIVATE)",
                extra_trigger: ".o_list_view",
            },
            // ── Flow 3-4 — Select the record and click Action > Unarchive.
            {
                content: "Select the TOUR-LTYPE-ACTIVATE row",
                trigger:
                    ".o_data_row:contains(TOUR-LTYPE-ACTIVATE) " +
                    ".o_list_record_selector input",
                run: "click",
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
            // NOTE: the IK's Flow step 5 ("Click OK to confirm.") has no
            // counterpart here on purpose. Unlike Archive, the list view's
            // Unarchive action calls `_toggleArchiveState(false)` directly
            // without a `Dialog.confirm` wrapper (web/static/src/js/views/
            // list/list_controller.js:490) — no dialog is ever shown, so a
            // step waiting for one would time out
            // (odoo-development-ui-test skill, patterns.md §G/§J). This is
            // a discrepancy in docs/hr_leave_type/05-activate.md, reported
            // separately rather than patched here (out of scope for this
            // tour-writing item — IK edits belong to issue #124).
            //
            // ── Post-Condition — the record is restored: it no longer
            // matches the still-active Archived filter.
            {
                content: "Reactivated leave type leaves the Archived list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(" +
                    "TOUR-LTYPE-ACTIVATE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});
