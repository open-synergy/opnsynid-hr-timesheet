odoo.define("ssi_timesheet_attendance.hr_timesheet_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Timesheets > Timesheets.
    // Duplicated locally (rather than required from ssi_timesheet's own
    // tour module) because that module does not export it — matches the
    // convention already used by every extension tour in this repo (see
    // ssi_timesheet_attendance_shift and ssi_timesheet's own
    // hr_timesheet_computation_item_tour.js).
    function openTimesheetMenuSteps() {
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
                content: "Open the Timesheets menu item",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_timesheet.menu_hr_timesheet"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view —
                // the app landing action is also a .o_list_view.
                content: "Timesheets list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Timesheets)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    var confirmDialogStep = {
        content: "Confirm the dialog",
        trigger: ".modal-footer button.btn-primary",
        in_modal: true,
    };

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/01-create.md (delta on top of
    // ssi_timesheet/hr_timesheet/01-create.md — adds the required
    // Working Schedule field). Per the E1 extension pattern
    // (odoo-development-ui-test skill, patterns.md §O /
    // scope-and-boundaries.md §3): navigation is taken from the base
    // tour (open menu → New), then a single assertion proves the added
    // field is displayed. Does NOT continue into Save/Confirm/etc. —
    // those belong to the base ssi_timesheet create tour.
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_timesheet_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
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
            // ── Additional Fields — Working Schedule is displayed on the
            // create form. Anchored to the field's label rather than the
            // widget itself, since an empty-but-editable many2one is
            // still safe to anchor to, but the label is unambiguous and
            // matches the pattern recommended for delta tours
            // (patterns.md §O).
            {
                content: "Working Schedule field is displayed",
                trigger: ".o_form_label:contains(Working Schedule)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/15-sign-in.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_timesheet_sign_in",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record to sign in for (status On
            // Progress).
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-SIGNIN) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — On the Attendance tab, click Sign In.
            {
                content: "Open the Attendance tab",
                trigger: ".o_notebook .nav-link:contains(Attendance)",
            },
            {
                // Sign In lives inside the Attendance page's own <group>,
                // NOT the form header — so it is never wrapped in
                // .o_statusbar_buttons (that class is specific to
                // <header> buttons / the state statusbar).
                content: "Click the Sign In button",
                trigger: ".o_form_view button[name='action_sign_in']",
                extra_trigger: ".o_form_view",
            },
            // ── Post-Condition — a new hr.timesheet_attendance record is
            // created for the employee (gate: the fixture employee has no
            // attendance rows before this click), and Attendance Status
            // changes so Sign In is hidden and Sign Out becomes visible.
            {
                content: "A new attendance record is created",
                trigger: ".o_field_x2many[name='attendance_ids'] .o_data_row",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "The Sign Out button becomes available",
                trigger: ".o_form_view button[name='action_sign_out']:visible",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "The Sign In button is no longer shown",
                trigger:
                    ".o_form_view" +
                    ":not(:has(button[name='action_sign_in']:visible))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/16-sign-out.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_timesheet_sign_out",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record to sign out from (status On
            // Progress, employee currently signed in).
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-SIGNOUT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — On the Attendance tab, click Sign Out.
            {
                content: "Open the Attendance tab",
                trigger: ".o_notebook .nav-link:contains(Attendance)",
            },
            {
                // Sign Out lives inside the Attendance page's own
                // <group>, NOT the form header — see the same note on
                // Sign In above.
                content: "Click the Sign Out button",
                trigger: ".o_form_view button[name='action_sign_out']",
                extra_trigger: ".o_form_view",
            },
            // ── Post-Condition — Attendance Status changes so Sign Out
            // is hidden and Sign In becomes visible again.
            {
                content: "The Sign In button becomes available",
                trigger: ".o_form_view button[name='action_sign_in']:visible",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "The Sign Out button is no longer shown",
                trigger:
                    ".o_form_view" +
                    ":not(:has(button[name='action_sign_out']:visible))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/17-compute-schedule.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_timesheet_attendance_hr_timesheet_compute_schedule",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 2 — Open the record (status Draft or On Progress).
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-EMP-SCHEDULE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 — On the Attendance Schedules tab, click Create
            // Schedules. NOTE: the tab is rendered with the literal
            // string "Atendance Schedules" (a pre-existing typo in
            // views/hr_timesheet_views.xml, out of scope for this tour
            // per the issue's Ruang Lingkup) — the selector below
            // targets the text actually rendered in the DOM.
            {
                content: "Open the Atendance Schedules tab",
                trigger: ".o_notebook .nav-link:contains(Atendance Schedules)",
            },
            {
                content: "Click the Create Schedules button",
                trigger: ".o_form_view button[name='action_compute_schedule']",
                extra_trigger: ".o_form_view",
            },
            // ── Flow 4 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — Attendance Schedule lines are generated
            // (gate: the fixture timesheet has no schedule rows before
            // this click, and its Working Schedule covers weekdays within
            // Date Start/Date End, so at least one line is guaranteed).
            {
                content: "Attendance Schedule lines are generated",
                trigger: ".o_field_x2many[name='schedule_ids'] .o_data_row",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );
});
