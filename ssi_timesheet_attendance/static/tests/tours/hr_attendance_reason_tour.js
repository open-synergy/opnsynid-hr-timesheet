odoo.define("ssi_timesheet_attendance.hr_attendance_reason_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Configuration > Attendance >
    // Attendance Reasons. "Attendance" (level 3) has children of its own
    // (this menu's "Attendance Reasons" leaf, and — when installed —
    // sibling extension modules add more leaves under it), so it is
    // rendered as a non-clickable dropdown header and is skipped here —
    // only the leaf "Attendance Reasons" item gets a step (see
    // odoo-development-ui-test skill, patterns.md §A).
    function openAttendanceReasonMenuSteps() {
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
                content: "Open the Attendance Reasons menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_timesheet_attendance.hr_attendance_reason_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action is also a .o_list_view. NOTE: the
                // breadcrumb shows the ir.actions.act_window's own `name`
                // ("Attendance Reason", singular), NOT the menu item's
                // label ("Attendance Reasons", plural) — verified against
                // the actual rendered DOM in CI.
                content: "Attendance Reason list is displayed",
                trigger:
                    ".o_control_panel " +
                    ".breadcrumb-item.active:contains(Attendance Reason)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_attendance_reason/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_attendance_reason_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceReasonMenuSteps(), [
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
            // ── Flow 3 — Fill in Reason; leave Code as "/" (eligible for
            // automatic assignment).
            {
                content: "Fill in Reason",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-REASON-CREATE-UI",
            },
            {
                content: "Ensure Code is /",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur /",
            },
            // ── Flow 4 — Click Generate Code. No sequence.template is
            // configured for hr.attendance_reason in this repo, so this
            // always raises "No sequence template found" — dismiss that
            // dialog, then fill Code manually as the IK instructs for
            // that case ("Code must be filled in manually").
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
                run: "text REASON-CREATE-01",
            },
            // ── Flow 5 — Note is optional; left blank.
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
            // ── Post-Condition — a new attendance reason record is
            // created, active by default.
            {
                content: "Back to the Attendance Reason list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Attendance Reason)",
            },
            {
                content: "New record appears in the list",
                trigger: ".o_data_row:contains(TOUR-REASON-CREATE-UI)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_attendance_reason/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_attendance_reason_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceReasonMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-REASON-EDIT-UI) .o_data_cell:first",
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
            // ── Flow 3 — Change Code back to "/", so Generate Code (Flow
            // 4) has something to act on — mirrors the IK's own example
            // ("for example after resetting Code back to /").
            {
                content: "Reset the Code field to /",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur /",
            },
            // ── Flow 4 — Click Generate Code. No sequence.template is
            // configured for hr.attendance_reason in this repo, so this
            // always raises "No sequence template found" — dismiss that
            // dialog, then fill Code manually as the IK instructs.
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
                run: "text REASON-EDIT-02",
            },
            // ── Flow 5 — Click Save.
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
    // IK: docs/hr_attendance_reason/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_attendance_reason_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceReasonMenuSteps(), [
            // ── Flow 2-3 — select the record and delete it. Deletion is
            // driven from the record's own Action menu rather than the
            // list checkbox: the 14.0 list-selector checkbox is flaky
            // (odoo-development-ui-test skill, patterns.md §I), and this
            // reaches the same Post-Condition.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-REASON-DELETE-UI) .o_data_cell:first",
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
                // Action menu items are Owl components; target the <a>
                // inside .o_menu_item and match the exact label so
                // :contains(Delete) as a substring never picks "Archive".
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
                content: "Back to the Attendance Reason list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Attendance Reason)",
            },
            // ── Post-Condition — the record is permanently removed.
            {
                content: "Deleted reason no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(" +
                    ".o_data_row:contains(TOUR-REASON-DELETE-UI)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_attendance_reason/04-deactivate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_attendance_reason_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceReasonMenuSteps(), [
            // ── Flow 2-4 — select the record and archive it, from the
            // record's own form (same substitution as Delete above: the
            // list checkbox + Action menu combination is flaky in 14.0,
            // patterns.md §I).
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-REASON-DEACTIVATE-UI) " +
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
            // ── Post-Condition — the record is archived.
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
    // IK: docs/hr_attendance_reason/05-activate.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_attendance_reason_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceReasonMenuSteps(), [
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
                content: "Archived reason is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-REASON-ACTIVATE-UI)",
                extra_trigger: ".o_list_view",
            },
            // ── Flow 3-5 — select the record and unarchive it, from the
            // record's own form (same substitution as Delete above).
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-REASON-ACTIVATE-UI) " +
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
            // ── Post-Condition — the record is restored. Unarchive
            // executes immediately without a confirmation dialog.
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
    // IK: docs/hr_attendance_reason/06-reset-code.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_attendance_reason_reset_code",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceReasonMenuSteps(), [
            // ── Flow 2 — Select the record whose code will be reset. This
            // button only exists in the list header, so (unlike Delete/
            // Archive above) it must be exercised via the list checkbox.
            {
                content: "Select the record",
                trigger:
                    ".o_data_row:contains(TOUR-REASON-RESETCODE-UI) " +
                    ".o_list_record_selector input",
                run: "click",
            },
            // ── Gate — wait for the checkbox click above to actually
            // register as checked before firing the header button; without
            // this the button can act on zero selected records (race).
            {
                content: "Record is selected",
                trigger:
                    ".o_data_row:contains(TOUR-REASON-RESETCODE-UI) " +
                    ".o_list_record_selector input:checked",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — Click the Reset code button. Flow 4 ("Click OK
            // on the confirmation dialog") does not apply here: list-view
            // <header> buttons in 14.0 never honor `confirm=`
            // (web/static/src/js/views/list/list_controller.js
            // `_onHeaderButtonClicked` calls `_executeButtonAction`
            // directly and never reads `node.attrs.confirm`), so the
            // action runs immediately without a dialog.
            {
                content: "Click the Reset code button",
                trigger: ".o_control_panel button[name='action_reset_code']",
            },
            // ── Post-Condition — Code returns to "/": scoped to this
            // record's own row (matched by its stable Reason name) rather
            // than the whole list view — a transient duplicate render of
            // ``.o_list_view`` during reload can otherwise make a
            // list-wide "does not contain" check flap even after the
            // value is already correctly updated server-side. NOTE: the
            // old code must not be a substring of the Reason name itself
            // (e.g. "REASON-RESET" inside "TOUR-REASON-RESETCODE-UI"),
            // or ":not(:contains(...))" can never match regardless of
            // whether the reset actually happened — hence "OLDCODE99".
            {
                content: "Row no longer shows the old code",
                trigger:
                    ".o_data_row:contains(TOUR-REASON-RESETCODE-UI)" +
                    ":not(:contains(OLDCODE99))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});
