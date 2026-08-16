odoo.define("ssi_work_log_mixin.hr_timesheet_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_timesheet/01-create.md (Extends: ssi_timesheet, model
    // hr.timesheet, aksi 01-create)
    //
    // Arketipe E1 (odoo-development-ui-test skill, scope-and-boundaries.md
    // §3 "Modul extension"): this IK only documents "## Additional Fields"
    // added to the base hr.timesheet Create IK, with no "## Modified Flow"
    // and no Post-Condition of its own. The tour is therefore delta-only:
    // navigation is taken from the base IK (open menu → New), followed by
    // a single assertion that the additional fields are rendered, then it
    // stops — it deliberately does NOT continue into Save/Confirm/etc,
    // which belong to the base tour (ssi_timesheet_hr_timesheet_create).
    //
    // docs/hr_timesheet/07-start.md (same Extends header) has no tour of
    // its own: it carries no "## Additional Fields" and no "## Modified
    // Flow" of its own, only an "## Additional Post-Condition" describing
    // that the Work Log tab's list becomes usable once On Progress — a
    // capability already exercised end-to-end by
    // ssi_work_log_mixin_hr_work_log_create's own Pre-Condition (an On
    // Progress timesheet), so a separate tour would duplicate that without
    // any Flow step of its own to map (odoo-development-ui-test skill,
    // scope-and-boundaries.md §1 aturan 1/2).
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_timesheet_create",
        {
            test: true,
            url: "/web",
        },
        [
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
                content: "Timesheets list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Timesheets)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow — Click the New button.
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
            // Open the "Work Log" tab (mixin.work_object,
            // ssi_work_log_mixin.work_log_page, auto-inserted as the LAST
            // page on hr.timesheet's form). Matched by EXACT trimmed text,
            // not :contains, because this module's own "All Work Log(s)"
            // tab (hr_timesheet_views.xml) contains "Work Log" as a
            // substring.
            {
                content: "Open the Work Log tab",
                trigger: ".o_notebook .nav-link",
                run: function () {
                    var $tab = $(".o_notebook .nav-link").filter(function () {
                        return $(this).text().trim() === "Work Log";
                    });
                    $tab[0].click();
                },
            },
            // ── Additional Fields — Estimation and Work Log Analytic
            // Account are rendered. Both are editable on this unsaved
            // record (not readonly-and-empty), so anchoring directly on
            // the field widgets is safe here (odoo-development-ui-test
            // skill, patterns.md §O).
            {
                content: "Estimation field is displayed",
                trigger: ".o_field_widget[name='work_estimation']",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Work Log Analytic Account field is displayed",
                trigger: ".o_field_widget[name='work_log_analytic_account_id']",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ]
    );
});
