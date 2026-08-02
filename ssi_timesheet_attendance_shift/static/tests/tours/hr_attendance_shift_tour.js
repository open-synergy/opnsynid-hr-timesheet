odoo.define("ssi_timesheet_attendance_shift.hr_attendance_shift_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Configurations > Attendance >
    // Attendance Shifts. "Attendance" (level 3) has children of its own, so
    // it is rendered as a non-clickable dropdown header and is skipped here
    // — only the leaf "Attendance Shifts" item gets a step.
    function openAttendanceShiftMenuSteps() {
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
                content: "Open the Attendance Shifts menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_timesheet_attendance_shift.hr_attendance_shift_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action is also a .o_list_view.
                content: "Attendance Shifts list is displayed",
                trigger:
                    ".o_control_panel " +
                    ".breadcrumb-item.active:contains(Attendance Shifts)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/hr_attendance_shift/01-create.md
    tour.register(
        "ssi_timesheet_attendance_shift_hr_attendance_shift_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceShiftMenuSteps(), [
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
                run: "text TOUR-SHIFT-CREATE",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },
            {
                content: "Fill in Work From",
                trigger: ".o_field_widget[name='hour_start']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 18",
            },
            {
                content: "Fill in Duration (Hours)",
                trigger: ".o_field_widget[name='duration']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 12",
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

    // IK: docs/hr_attendance_shift/02-edit.md
    tour.register(
        "ssi_timesheet_attendance_shift_hr_attendance_shift_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceShiftMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-SHIFT-EDIT) .o_data_cell:first",
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
                content: "Change Duration (Hours)",
                trigger: ".o_field_widget[name='duration']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 9",
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

    // IK: docs/hr_attendance_shift/03-delete.md
    tour.register(
        "ssi_timesheet_attendance_shift_hr_attendance_shift_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceShiftMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-SHIFT-DELETE) .o_data_cell:first",
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
                content: "Back to the Attendance Shifts list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Attendance Shifts)",
            },
            {
                content: "Deleted shift no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-SHIFT-DELETE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // IK: docs/hr_attendance_shift/04-deactivate.md
    tour.register(
        "ssi_timesheet_attendance_shift_hr_attendance_shift_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceShiftMenuSteps(), [
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-SHIFT-DEACTIVATE) .o_data_cell:first",
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

    // IK: docs/hr_attendance_shift/05-activate.md
    tour.register(
        "ssi_timesheet_attendance_shift_hr_attendance_shift_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceShiftMenuSteps(), [
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
                content: "Archived shift is displayed in the list",
                trigger: ".o_data_row:contains(TOUR-SHIFT-ACTIVATE)",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Select the archived record",
                // Click the checkbox CONTAINER, not the nested <input>: in
                // 14.0, clicking the input directly bypasses
                // ListRenderer._onToggleCheckbox's delegated handler
                // (`$(ev.target).find(...)` finds nothing when ev.target
                // IS the input, since find() only searches descendants),
                // relying on native checkbox toggling instead — which is
                // fragile and was observed opening the record's form
                // instead of just selecting the row.
                trigger:
                    ".o_data_row:contains(TOUR-SHIFT-ACTIVATE) " +
                    ".o_list_record_selector",
                run: "click",
            },
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
                run: function () {
                    // Owl dropdowns in 14.0 are not always opened by a
                    // synthetic click — use a native click instead.
                    this.$anchor[0].click();
                },
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
            {
                content: "Confirm unarchive",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Shift is restored and stays in the archived view",
                trigger: ".o_data_row:contains(TOUR-SHIFT-ACTIVATE)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});
