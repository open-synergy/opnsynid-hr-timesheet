odoo.define(
    "ssi_timesheet_attendance_operating_unit.hr_timesheet_attendance_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/hr_timesheet_attendance/01-create.md (E1 delta --
        // Additional Fields)
        // Navigation (open menu -> New) is retraced from the base IK
        // ssi_timesheet_attendance/docs/hr_timesheet_attendance/01-create.md
        // Flow steps 1-2 -- see skill odoo-development-ui-test,
        // scope-and-boundaries.md §3 ("Backing dua file: tour extension =
        // base IK ∪ delta IK"). The delta assertion comes from this
        // module's own IK: the Operating Unit field is visible on the
        // create form for a user in the
        // operating_unit.group_multi_operating_unit group. The tour stops
        // there; it does not fill, save, or confirm (E1 delta-only).
        tour.register(
            "ssi_timesheet_attendance_operating_unit_hr_timesheet_attendance_create",
            {
                test: true,
                url: "/web",
            },
            [
                // ── Base Flow 1 — Open the Human Resource > Timesheets >
                // Attendances menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
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
                    // Gate: wait for the TARGET action, not just any list
                    // view — the app landing action is also a
                    // .o_list_view.
                    content: "Attendances list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Attendances)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // ── Base Flow 2 — Click the New button. (14.0: "Create")
                {
                    content: "Click Create",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default
                        // click action.
                    },
                },

                // ── Delta assertion — the Operating Unit field is
                // visible on the create form for a user in the multi
                // operating unit group. The tour stops here (E1
                // delta-only).
                {
                    content: "Operating Unit field is visible on the form",
                    trigger:
                        ".o_form_view.o_form_editable " +
                        ".o_field_widget[name='operating_unit_id']",
                    run: function () {
                        // Assertion only; do not trigger the default
                        // click action.
                    },
                },
            ]
        );
    }
);
