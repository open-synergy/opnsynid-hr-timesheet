odoo.define("ssi_hr_overtime.hr_overtime_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Configuration > Timesheets >
    // Overtime Types. "Timesheets" (level 3, under Configurations) always
    // has more than one child in this repo (this module's own "Overtime
    // Types" plus "ssi_timesheet"'s "Computation Item"), so it renders as
    // a non-clickable dropdown header and is skipped here — only the leaf
    // "Overtime Types" item gets a step.
    function openOvertimeTypeMenuSteps() {
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
                content: "Open the Overtime Types menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_hr_overtime.hr_overtime_type_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action is also a .o_list_view.
                content: "Overtime Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(" +
                    "Overtime Types)",
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
    // IK: docs/hr_overtime_type/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_type_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeTypeMenuSteps(), [
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
            // ── Flow 3 — Fill in Type.
            {
                content: "Fill in Type",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-OTTYPE-CREATE",
            },
            // Code is not part of this IK's Flow — it is a required field
            // inherited from `mixin.master_data` (present on every SSI
            // master data model, e.g. hr.leave_type), and "/" is its
            // documented sentinel for "auto-assign a sequence" (see the
            // field's own help text). Same precedent as
            // ssi_hr_holiday.hr_leave_type_tour's create tour.
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
            // ── Post-Condition — a new overtime type record is created.
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
    // IK: docs/hr_overtime_type/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_type_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeTypeMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-OTTYPE-EDIT) .o_data_cell:first",
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
            // ── Flow 3 — Change Type.
            {
                content: "Change Type",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-OTTYPE-EDITED",
            },
            // ── Flow 4 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — the record is updated with the new value.
            {
                content: "Type shows the new value",
                trigger:
                    ".o_form_view.o_form_readonly " +
                    ".o_field_widget[name='name']:contains(TOUR-OTTYPE-EDITED)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_overtime_type/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_type_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openOvertimeTypeMenuSteps(),
            // ── Flow 2-3 — Select the record and click Action > Delete.
            selectRowAndClickActionMenuItem("TOUR-OTTYPE-DELETE", "Delete"),
            [
                // ── Flow 4 — Click OK to confirm.
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                // ── Post-Condition — the record is permanently removed.
                {
                    content: "Deleted overtime type no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(" +
                        "TOUR-OTTYPE-DELETE)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_overtime_type/04-deactivate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_type_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openOvertimeTypeMenuSteps(),
            // ── Flow 2-3 — Select the record and click Action > Archive.
            selectRowAndClickActionMenuItem("TOUR-OTTYPE-DEACTIVATE", "Archive"),
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
                    content: "Archived overtime type no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(" +
                        "TOUR-OTTYPE-DEACTIVATE)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_overtime_type/05-activate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_hr_overtime_type_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeTypeMenuSteps(), [
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
                // Gate: `aria-checked` on the filter's <a> is the real,
                // synchronously-toggled signal that the Archived facet was
                // applied (web/static/src/xml/base.xml:
                // `t-att-aria-checked="props.isActive ? 'true' : 'false'"`).
                // Without this, the list can briefly re-render with a stale
                // domain before the facet lands, making the next steps
                // (select row, Unarchive) race against an in-flight search
                // and leaving the row stuck in the Archived list afterwards
                // (odoo-development-ui-test skill, patterns.md §J).
                content: "Archived filter is applied",
                trigger:
                    ".o_filter_menu .o_menu_item a:contains(Archived)" +
                    "[aria-checked='true']",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                // Gate: the archived TOUR-OTTYPE-ACTIVATE record is only
                // reachable once the Archived filter is actually applied.
                //
                // This step's trigger matches the row itself (via
                // `:contains`), so it MUST declare an explicit no-op
                // `run` like every other assertion-only gate in this
                // file. Without it, the tour engine's default action
                // for a step with no `run` is to CLICK the matched
                // trigger element — which opens TOUR-OTTYPE-ACTIVATE's
                // FORM view (the same default-click behavior the "Open
                // the record" step in the edit tour above relies on
                // *intentionally*). That accidental navigation away
                // from the list would leave the final Post-Condition
                // step below polling for `.o_list_view` on a DOM that
                // no longer had one, timing out even though the
                // Unarchive RPC itself succeeded immediately.
                content: "Archived overtime type is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-OTTYPE-ACTIVATE)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3-4 — Select the record and click Action > Unarchive.
            {
                content: "Select the TOUR-OTTYPE-ACTIVATE row",
                trigger:
                    ".o_data_row:contains(TOUR-OTTYPE-ACTIVATE) " +
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
            // (odoo-development-ui-test skill, patterns.md §G/§J). Same
            // discrepancy already reported for
            // ssi_hr_holiday/docs/hr_leave_type/05-activate.md — out of
            // scope for this tour-writing item.
            //
            // ── Post-Condition — the record is restored: it no longer
            // matches the still-active Archived filter.
            {
                content: "Reactivated overtime type leaves the Archived list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(" +
                    "TOUR-OTTYPE-ACTIVATE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});
