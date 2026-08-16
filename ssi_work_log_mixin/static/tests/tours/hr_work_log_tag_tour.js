odoo.define("ssi_work_log_mixin.hr_work_log_tag_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Configuration > Timesheets >
    // Work Log Tags.
    function openWorkLogTagMenuSteps() {
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
            // "Timesheets" (ssi_timesheet.menu_hr_timesheet_configuration) is a
            // level-3 <menuitem> WITHOUT an `action` and WITH two children
            // (ssi_timesheet's own hr_timesheet_computation_item_menu, and
            // this module's hr_work_log_tag_menu) — per 14.0's Menu.link
            // template (web/static/src/xml/menu.xml) a level-3+ item with
            // children renders as a non-clickable
            // `<div class="dropdown-header">` WITHOUT `data-menu-xmlid`, not
            // an `<a>` (odoo-development-ui-test skill, patterns.md §A "Jumlah
            // level menu di IK ≠ jumlah step tour"). Its children are
            // flattened into the SAME "Configuration" dropdown opened above,
            // so no step targets it — skip straight to the Work Log Tags leaf.
            {
                content: "Open the Work Log Tags menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_work_log_mixin.hr_work_log_tag_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view.
                content: "Work Log Tags list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Work Log Tags)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Open the control panel's "Action" menu (works both in the list view,
    // scoped to the current selection, and in a record's own form view).
    var openActionMenuStep = {
        content: "Open the Action menu",
        trigger: ".o_cp_action_menus button:contains(Action)",
    };

    // Click an item inside the (already open) Action menu, matched by its
    // exact trimmed text — its <a> is an Owl component, and substring
    // matching (:contains) can hit the wrong item (e.g. "Archive" also
    // matching "Unarchive").
    function clickActionMenuItem(label) {
        return {
            content: "Click " + label,
            trigger: ".o_cp_action_menus .o_menu_item a",
            run: function () {
                var $item = $(".o_cp_action_menus .o_menu_item a").filter(function () {
                    return $(this).text().trim() === label;
                });
                $item[0].click();
            },
        };
    }

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log_tag/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_tag_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openWorkLogTagMenuSteps(), [
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
            // ── Flow 3 — Fill in Work Log Tag.
            {
                content: "Fill in Work Log Tag",
                // No ` input` suffix: InputField.init() (basic_fields.js)
                // sets `this.tagName = 'input'` in edit mode for plain
                // Char/Float fields that don't override `start()` (unlike
                // Date/Many2one, which replace $el with a wrapping element)
                // — so `.o_field_widget[name='name']` in edit mode IS the
                // `<input>` itself, matching the working precedent in
                // ssi_timesheet_hr_timesheet_computation_item_create /
                // ssi_timesheet_attendance_shift_hr_attendance_shift_pattern_create.
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-TAG-CREATE-UI",
            },
            // `code` (mixin.master_data, ssi_master_data_mixin) carries no
            // field-level default (unlike ssi_timesheet's own
            // hr.timesheet.name), so it starts genuinely empty on a new
            // record and blocks Save until filled — same latent gap already
            // documented for ssi_timesheet_hr_timesheet_computation_item_create
            // (odoo-development-ui-test skill precedent in this repo). The
            // IK's own Flow does not mention this field; "/" is the SSI
            // convention for "assign automatically later".
            {
                content: "Ensure Code is /",
                // No ` input` suffix — see the comment on the "Fill in Work
                // Log Tag" step above.
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur /",
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
            // ── Post-Condition — a new work log tag record is created.
            {
                content: "Back to the Work Log Tags list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Work Log Tags)",
            },
            {
                content: "New record appears in the list",
                trigger: ".o_data_row:contains(TOUR-TAG-CREATE-UI)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log_tag/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_tag_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openWorkLogTagMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-TAG-EDIT) .o_data_cell:first",
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
            // ── Flow 3 — Change the Work Log Tag.
            {
                content: "Change Work Log Tag",
                // No ` input` suffix — see the comment on the create tour's
                // "Fill in Work Log Tag" step above.
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-TAG-EDITED",
            },
            // ── Flow 4 — Click Save.
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
    // IK: docs/hr_work_log_tag/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_tag_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openWorkLogTagMenuSteps(), [
            // ── Flow 2 — Select the record to delete (check the checkbox).
            {
                content: "Select the record",
                trigger:
                    ".o_data_row:contains(TOUR-TAG-DELETE) " +
                    ".o_list_record_selector input",
                run: "click",
            },
            // ── Flow 3 — Click Action > Delete.
            openActionMenuStep,
            clickActionMenuItem("Delete"),
            // ── Flow 4 — Click OK to confirm.
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            // ── Post-Condition — the selected record is permanently
            // removed.
            {
                content: "Deleted tag no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-TAG-DELETE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log_tag/04-deactivate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_tag_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openWorkLogTagMenuSteps(), [
            // ── Flow 2 — Select the record to deactivate.
            {
                content: "Select the record",
                trigger:
                    ".o_data_row:contains(TOUR-TAG-DEACTIVATE) " +
                    ".o_list_record_selector input",
                run: "click",
            },
            // ── Flow 3 — Click Action > Archive. Archive (unlike
            // Unarchive below) shows a confirmation dialog
            // (odoo-development-ui-test skill, patterns.md §"Dua
            // pengecualian").
            openActionMenuStep,
            clickActionMenuItem("Archive"),
            // ── Flow 4 — Click OK to confirm.
            {
                content: "Confirm archive",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            // ── Post-Condition — record is archived, no longer shown in
            // the default list view.
            {
                content: "Archived tag no longer appears in the default list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-TAG-DEACTIVATE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log_tag/05-activate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_tag_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openWorkLogTagMenuSteps(), [
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
                content: "Archived tag is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-TAG-ACTIVATE)",
                extra_trigger: ".o_list_view",
            },
            // ── Flow 3 — Select the record to reactivate.
            {
                content: "Select the record",
                trigger:
                    ".o_data_row:contains(TOUR-TAG-ACTIVATE) " +
                    ".o_list_record_selector input",
                run: "click",
            },
            // ── Flow 4 — Click Action > Unarchive. Unlike Archive above,
            // Unarchive executes immediately without a confirmation
            // dialog (odoo-development-ui-test skill, patterns.md §"Dua
            // pengecualian" — list_controller.js never wraps it in
            // Dialog.confirm).
            openActionMenuStep,
            clickActionMenuItem("Unarchive"),
            // ── Post-Condition — record is restored, appears again in
            // the default list view.
            {
                content: "Open the Filters menu",
                trigger: ".o_search_options .o_filter_menu button",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Disable the Archived filter",
                trigger: ".o_filter_menu .o_menu_item a:contains(Archived)",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Restored tag appears in the default list",
                trigger: ".o_data_row:contains(TOUR-TAG-ACTIVATE)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});
