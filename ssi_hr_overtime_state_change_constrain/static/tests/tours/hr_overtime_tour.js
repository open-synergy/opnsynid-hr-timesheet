// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_hr_overtime_state_change_constrain.hr_overtime_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_overtime/01-create.md (delta — Modified Flow)
    //
    // Delta-only: this tour reuses the base ssi_hr_overtime Flow (open
    // menu, click New) up to the point of change, asserts the Status
    // Checks tab this module adds, then stops — it does not continue
    // into Save/Confirm (odoo-development-ui-test skill,
    // scope-and-boundaries.md §3, arketipe E2a).
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_hr_overtime_state_change_constrain_hr_overtime_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 (base) — Open the Human Resource > Timesheets >
            // Overtimes menu.
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
                content: "Open the Overtimes menu item",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_hr_overtime.menu_hr_overtime"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list
                // view — the app landing action is also a
                // .o_list_view.
                content: "Overtimes list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Overtimes)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },

            // ── Flow 2 (base) — Click the New button. (14.0: "Create")
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

            // ── Delta — Modified Flow: the Status Checks tab, added by
            // this module's mixin.status_check, is shown on the form.
            {
                content: "Open the Status Checks tab",
                trigger: ".o_notebook .nav-link:contains(Status Checks)",
            },
            {
                // Gate: the tab content only exists once the tab above
                // is actually selected, so this cannot match before
                // the click above ran. Odoo 14 wraps the active page in
                // `.tab-pane.active` (Bootstrap tabs) — there is no
                // `.o_notebook_content` class in this series.
                content: "Status Checks tab content is rendered",
                trigger: ".tab-pane.active .o_field_x2many[name='status_check_ids']",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action. Delta-only tour: stop here, do not
                    // continue into Save/Confirm.
                },
            },
        ]
    );
});
