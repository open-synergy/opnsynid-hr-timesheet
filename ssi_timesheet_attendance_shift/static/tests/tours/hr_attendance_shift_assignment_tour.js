odoo.define(
    "ssi_timesheet_attendance_shift.hr_attendance_shift_assignment_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared opening steps: Human Resource > Configurations > Attendance >
        // Attendance Shift Assignments. "Attendance" (level 3) has children of
        // its own, so it is rendered as a non-clickable dropdown header and is
        // skipped here — only the leaf "Attendance Shift Assignments" item
        // gets a step.
        function openAttendanceShiftAssignmentMenuSteps() {
            return [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
                },
                {
                    content: "Open the Configurations menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
                },
                {
                    content: "Open the Attendance Shift Assignments menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_timesheet_attendance_shift.hr_attendance_shift_assignment_menu"]',
                },
                {
                    // Gate: wait for the TARGET action, not just any list view —
                    // the app landing action is also a .o_list_view.
                    content: "Attendance Shift Assignments list is displayed",
                    trigger:
                        ".o_control_panel " +
                        ".breadcrumb-item.active:contains(Attendance Shift Assignments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // IK: docs/hr_attendance_shift_assignment/01-create.md
        tour.register(
            "ssi_timesheet_attendance_shift_hr_attendance_shift_assignment_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(openAttendanceShiftAssignmentMenuSteps(), [
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
                {
                    content: "Select the Employee",
                    trigger: ".o_field_many2one[name='employee_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR-ASSIGN-CREATE-EMPLOYEE",
                },
                {
                    content: "Pick the employee from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-ASSIGN-CREATE-EMPLOYEE)",
                    in_modal: false,
                },
                {
                    content: "Select the Pattern",
                    trigger: ".o_field_many2one[name='pattern_id'] input",
                    run: "text TOUR-ASSIGN-PATTERN",
                },
                {
                    content: "Pick the pattern from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-ASSIGN-PATTERN)",
                    in_modal: false,
                },
                {
                    content: "Fill in Cycle Offset (Days)",
                    trigger: ".o_field_widget[name='cycle_offset']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 0",
                },
                {
                    content: "Fill in Date Start",
                    trigger: ".o_field_widget[name='date_start'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 01/15/2026",
                },
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
            ])
        );

        // IK: docs/hr_attendance_shift_assignment/02-edit.md
        tour.register(
            "ssi_timesheet_attendance_shift_hr_attendance_shift_assignment_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(openAttendanceShiftAssignmentMenuSteps(), [
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR-ASSIGN-EDIT-EMPLOYEE) " +
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
                    content: "Change Cycle Offset (Days)",
                    trigger: ".o_field_widget[name='cycle_offset']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 3",
                },
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
            ])
        );

        // IK: docs/hr_attendance_shift_assignment/03-delete.md
        tour.register(
            "ssi_timesheet_attendance_shift_hr_attendance_shift_assignment_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(openAttendanceShiftAssignmentMenuSteps(), [
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR-ASSIGN-DELETE-EMPLOYEE) " +
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
                    content: "Click Delete",
                    // Action menu items are Owl components; match the exact
                    // label so "Archive" is never picked instead.
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
                    content: "Back to the Attendance Shift Assignments list",
                    trigger:
                        ".breadcrumb-item.o_back_button a:contains(Attendance Shift Assignments)",
                },
                {
                    content: "Deleted assignment no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR-ASSIGN-DELETE-EMPLOYEE)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ])
        );
    }
);
