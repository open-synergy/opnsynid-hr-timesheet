odoo.define(
    "ssi_timesheet_attendance_shift.hr_attendance_shift_pattern_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared opening steps: Human Resource > Configurations > Attendance >
        // Attendance Shift Patterns. "Attendance" (level 3) has children of its
        // own, so it is rendered as a non-clickable dropdown header and is
        // skipped here — only the leaf "Attendance Shift Patterns" item gets a
        // step.
        function openAttendanceShiftPatternMenuSteps() {
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
                    content: "Open the Attendance Shift Patterns menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_timesheet_attendance_shift.hr_attendance_shift_pattern_menu"]',
                },
                {
                    // Gate: wait for the TARGET action, not just any list view —
                    // the app landing action is also a .o_list_view.
                    content: "Attendance Shift Patterns list is displayed",
                    trigger:
                        ".o_control_panel " +
                        ".breadcrumb-item.active:contains(Attendance Shift Patterns)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // IK: docs/hr_attendance_shift_pattern/01-create.md
        tour.register(
            "ssi_timesheet_attendance_shift_hr_attendance_shift_pattern_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(openAttendanceShiftPatternMenuSteps(), [
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
                    content: "Fill in Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR-PATTERN-CREATE",
                },
                {
                    content: "Fill in Code",
                    trigger: ".o_field_widget[name='code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text /",
                },
                {
                    content: "Fill in Cycle Length (Days)",
                    trigger: ".o_field_widget[name='cycle_length']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 7",
                },
                {
                    content: "Fill in Cycle Anchor Date",
                    trigger: ".o_field_widget[name='date_anchor'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 01/15/2026",
                },
                {
                    content: "Open the Cycle Days tab",
                    trigger: ".o_notebook .nav-link:contains(Cycle Days)",
                },
                {
                    content: "Add a cycle day line",
                    trigger:
                        ".o_field_widget[name='detail_ids'] " +
                        ".o_field_x2many_list_row_add a",
                },
                {
                    content: "Fill in Day Index",
                    trigger: ".o_selected_row .o_field_widget[name='day_index']",
                    run: "text 1",
                },
                {
                    content: "Select the Shift",
                    trigger: ".o_selected_row .o_field_widget[name='shift_id'] input",
                    run: "text TOUR-PATTERN-SHIFT",
                },
                {
                    content: "Pick the shift from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-PATTERN-SHIFT)",
                    in_modal: false,
                },
                {
                    // The <td> wrapping an o2m cell carries no `name`
                    // attribute in 14.0 (only the field widget itself
                    // does — abstract_field.js sets it on `this.$el`,
                    // not on the surrounding cell), and there is only
                    // one row here so there is no sibling cell to click
                    // instead. Blur the still-open row by clicking the
                    // always-visible Name field above the notebook
                    // instead — a plain click does not change its text.
                    content: "Commit the cycle day line",
                    trigger: ".o_field_widget[name='name']",
                    run: function () {
                        this.$anchor[0].click();
                    },
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

        // IK: docs/hr_attendance_shift_pattern/02-edit.md
        tour.register(
            "ssi_timesheet_attendance_shift_hr_attendance_shift_pattern_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(openAttendanceShiftPatternMenuSteps(), [
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR-PATTERN-EDIT) .o_data_cell:first",
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
                    content: "Change Cycle Length (Days)",
                    trigger: ".o_field_widget[name='cycle_length']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 14",
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

        // IK: docs/hr_attendance_shift_pattern/03-delete.md
        tour.register(
            "ssi_timesheet_attendance_shift_hr_attendance_shift_pattern_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(openAttendanceShiftPatternMenuSteps(), [
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR-PATTERN-DELETE) .o_data_cell:first",
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
                    content: "Back to the Attendance Shift Patterns list",
                    trigger:
                        ".breadcrumb-item.o_back_button a:contains(Attendance Shift Patterns)",
                },
                {
                    content: "Deleted pattern no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR-PATTERN-DELETE)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ])
        );
    }
);
