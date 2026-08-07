odoo.define("ssi_timesheet_attendance.hr_timesheet_attendance_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Timesheets > Attendances.
    // "Timesheets" (level 2, section) has two leaf children of its own
    // ("Timesheets" and "Attendances", both level 3, neither with further
    // children) so both levels are directly clickable.
    function openAttendancesMenuSteps() {
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
                content: "Open the Attendances menu item",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_timesheet_attendance.hr_timesheet_attendance_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action is also a .o_list_view.
                content: "Attendances list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Attendances)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet_attendance/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_timesheet_attendance_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendancesMenuSteps(), [
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
            // ── Flow 3 — Fill in Date. Check In already carries a
            // default (current date/time) so it is left as-is; Reason
            // In, Check Out and Reason Out are optional and left blank
            // (Check Out empty means the record stays Open, per
            // Post-Condition).
            {
                content: "Fill in Date",
                trigger: ".o_field_widget[name='date'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur 01/15/2026",
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
            // ── Post-Condition — a new attendance record is created.
            {
                content: "Back to the Attendances list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Attendances)",
            },
            {
                content: "New record appears in the list",
                trigger: ".o_data_row:contains(01/15/2026)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet_attendance/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_timesheet_attendance_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendancesMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit. The fixture
            // (setUpClass) has Check In filled but Check Out empty, so
            // the record starts Open.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(01/16/2026) .o_data_cell:first",
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
            // ── Flow 3 — Fill in Check Out.
            {
                content: "Fill in Check Out",
                trigger: ".o_field_widget[name='check_out'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur 01/16/2026 17:00:00",
            },
            // ── Flow 4 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — Status is recomputed to Present now
            // that both Check In and Check Out are filled.
            {
                content: "Status is Present",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='present']" +
                    ".btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet_attendance/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_timesheet_attendance_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendancesMenuSteps(), [
            // ── Flow 2-3 — select the record and delete it. Deletion is
            // driven from the record's own Action menu rather than the
            // list checkbox: the 14.0 list-selector checkbox is flaky
            // (odoo-development-ui-test skill, patterns.md §I), and this
            // reaches the same Post-Condition.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(01/20/2026) .o_data_cell:first",
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
                content: "Back to the Attendances list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Attendances)",
            },
            // ── Post-Condition — the record is permanently removed.
            {
                content: "Deleted attendance no longer appears in the list",
                trigger: ".o_list_view:not(:has(.o_data_row:contains(01/20/2026)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});
