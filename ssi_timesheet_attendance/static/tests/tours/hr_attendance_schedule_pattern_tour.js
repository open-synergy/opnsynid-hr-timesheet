odoo.define("ssi_timesheet_attendance.hr_attendance_schedule_pattern_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Configuration > Attendance >
    // Attendance Schedule Patterns. "Attendance" (level 3) has children of
    // its own, so it is rendered as a non-clickable dropdown header and is
    // skipped here — only the leaf "Attendance Schedule Patterns" item gets
    // a step.
    function openSchedulePatternMenuSteps() {
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
                content: "Open the Attendance Schedule Patterns menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_timesheet_attendance.hr_attendance_schedule_pattern_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action is also a .o_list_view.
                content: "Attendance Schedule Patterns list is displayed",
                trigger:
                    ".o_control_panel " +
                    ".breadcrumb-item.active:contains(Attendance Schedule Patterns)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/hr_attendance_schedule_pattern/01-create.md
    tour.register(
        "ssi_timesheet_attendance_hr_attendance_schedule_pattern_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openSchedulePatternMenuSteps(), [
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
                run: "text TOUR-SCHED-PATTERN-CREATE",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },
            {
                content: "Open the Pattern Lines tab",
                trigger: ".o_notebook .nav-link:contains(Pattern Lines)",
            },
            {
                content: "Add a pattern line",
                trigger:
                    ".o_field_widget[name='line_ids'] " +
                    ".o_field_x2many_list_row_add a",
            },
            {
                content: "Select the Frequency",
                trigger: ".o_selected_row .o_field_widget[name='frequency_id'] input",
                run: "text TOUR-SCHED-PATTERN-FREQ",
            },
            {
                content: "Pick the frequency from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR-SCHED-PATTERN-FREQ)",
                in_modal: false,
            },
            {
                content: "Fill in Hour From",
                trigger: ".o_selected_row .o_field_widget[name='hour_from']",
                run: "text 8:00",
            },
            {
                content: "Fill in Hour To",
                trigger: ".o_selected_row .o_field_widget[name='hour_to']",
                run: "text 16:00",
            },
            {
                // The <td> wrapping an o2m cell carries no `name`
                // attribute in 14.0, so blur the still-open row by clicking
                // the always-visible Name field above the notebook — a
                // plain click does not change its text.
                content: "Commit the pattern line",
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

    // IK: docs/hr_attendance_schedule_pattern/02-edit.md
    tour.register(
        "ssi_timesheet_attendance_hr_attendance_schedule_pattern_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openSchedulePatternMenuSteps(), [
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-SCHED-PATTERN-EDIT) .o_data_cell:first",
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
                content: "Change Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-SCHED-PATTERN-EDITED",
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

    // IK: docs/hr_attendance_schedule_pattern/03-delete.md
    tour.register(
        "ssi_timesheet_attendance_hr_attendance_schedule_pattern_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openSchedulePatternMenuSteps(), [
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-SCHED-PATTERN-DELETE) .o_data_cell:first",
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
                content: "Back to the Attendance Schedule Patterns list",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Attendance Schedule Patterns)",
            },
            {
                content: "Deleted pattern no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-SCHED-PATTERN-DELETE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});
