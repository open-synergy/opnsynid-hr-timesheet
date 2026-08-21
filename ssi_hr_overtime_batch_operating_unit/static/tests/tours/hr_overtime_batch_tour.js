odoo.define("ssi_hr_overtime_batch_operating_unit.hr_overtime_batch_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Timesheets > Overtime
    // Batch.
    function openOvertimeBatchMenuSteps() {
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
                content: "Open the Overtime Batch menu item",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_hr_overtime_batch.menu_hr_overtime"]',
            },
            {
                // Gate: wait for the TARGET action, not just any
                // list view — the app landing action is also a
                // .o_list_view.
                content: "Overtime Batch list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active" +
                    ":contains(Overtime Batch)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default
                    // click action.
                },
            },
        ];
    }

    // ═══════════════════════════════════════════════════════════
    // IK: docs/hr_overtime_batch/01-create.md
    // (delta on top of
    // ssi_hr_overtime_batch/hr_overtime_batch/01-create.md — adds
    // the Operating Unit field, visible only to users in the
    // Multi Operating Unit group). Per the E1 extension pattern
    // (odoo-development-ui-test skill, patterns.md §O /
    // scope-and-boundaries.md §3): navigation is taken from the
    // base tour (open menu → Create), then a single assertion
    // proves the added field is displayed. Does NOT continue into
    // Save/Confirm/etc. — those belong to the base
    // ssi_hr_overtime_batch create tour.
    // ═══════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_batch_operating_unit_hr_overtime_batch_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openOvertimeBatchMenuSteps(), [
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
            // ── Additional Fields — Operating Unit is displayed
            // on the create form (actor is in
            // group_multi_operating_unit, see setUpClass).
            // Anchored to the field's label rather than the
            // widget itself, matching the pattern recommended for
            // delta tours (patterns.md §O).
            {
                content: "Operating Unit field is displayed",
                trigger: ".o_form_label:contains(Operating Unit)",
                run: function () {
                    // Assertion only; do not trigger the default
                    // click action.
                },
            },
        ])
    );
});
