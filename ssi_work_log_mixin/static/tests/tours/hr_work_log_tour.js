odoo.define("ssi_work_log_mixin.hr_work_log_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Human Resource > Timesheets > Timesheets. Every
    // hr_work_log IK is written starting from a timesheet's Work Log tab
    // (docs/hr_work_log/01-create.md note), so all tours below share this
    // navigation plus the same fixture timesheet (employee TOUR-EMP-WORKLOG).
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
                // the app landing action ("Employees") is also a
                // .o_list_view.
                content: "Timesheets list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Timesheets)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Open the fixture timesheet",
                trigger: ".o_data_row:contains(TOUR-EMP-WORKLOG) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ];
    }

    // Open the auto-inserted "Work Log" tab (mixin.work_object,
    // ssi_work_log_mixin.work_log_page). Matched by EXACT trimmed text, not
    // :contains, because the sibling "All Work Log(s)" tab (registered by
    // this module's own hr_timesheet_views.xml) contains "Work Log" as a
    // substring — :contains would match both nav-links non-deterministically.
    var openWorkLogTabStep = {
        content: "Open the Work Log tab",
        trigger: ".o_notebook .nav-link",
        run: function () {
            var $tab = $(".o_notebook .nav-link").filter(function () {
                return $(this).text().trim() === "Work Log";
            });
            $tab[0].click();
        },
    };

    // Click a statusbar/header button by its exact visible label — needed
    // for the Cancel button, whose `name` attribute is a numeric action id
    // (base_select_cancel_reason_action) rather than a method name.
    //
    // The `run` callback below is a PLAIN jQuery query, not a web_tour
    // trigger — it is never routed through web_tour's own
    // `$modal_displayed.find(...)` scoping, so it is NOT covered by the
    // in_modal auto-scoping used elsewhere in this file. Left unscoped,
    // `$(".o_statusbar_buttons button")` matches globally: the underlying
    // hr.timesheet form (also using mixin.transaction_cancel, so it has
    // its OWN "Cancel" button) is still in the DOM behind the work log
    // dialog, and `[0]` can pick that wrong, hidden button instead of the
    // one inside the currently open modal — confirmed via CI (PR #245,
    // run 31925098655): the click silently canceled the TIMESHEET
    // ("Document Type: timesheet" in the policy error), which the
    // fixture's timesheet policy rejects, so the work log itself never
    // transitioned and "Status is Cancelled" timed out. Scope the query
    // to the topmost open modal explicitly.
    function clickHeaderButtonByLabel(label) {
        return {
            content: "Click the " + label + " button",
            trigger: ".o_statusbar_buttons button",
            run: function () {
                var $scope = $(".modal:visible").last();
                if (!$scope.length) {
                    $scope = $(document);
                }
                var $button = $scope
                    .find(".o_statusbar_buttons button")
                    .filter(function () {
                        return $(this).text().trim() === label;
                    });
                $button[0].click();
            },
        };
    }

    var confirmDialogStep = {
        content: "Confirm the dialog",
        trigger: ".modal-footer button.btn-primary",
        in_modal: true,
    };

    // Click the primary Save button of the currently open one2many-line
    // FormViewDialog. Its LABEL depends on `multi_select`
    // (view_dialogs.js FormViewDialog.init): a brand-new record (no
    // `res_id` yet, e.g. "Add a line") gets "Save & Close" (+ a separate
    // "Save & New"), while an EXISTING record (`res_id` set, e.g. "click
    // the line to edit") is single-select and gets plain "Save" instead —
    // confirmed via CI (PR #245, run 31925098655): the edit tour's
    // "Save & Close" text match found zero buttons on the edit dialog
    // (label there is just "Save"), causing `$button[0].click()` to throw
    // "Cannot read properties of undefined". Match either label.
    var clickDialogSaveStep = {
        content: "Click Save (or Save & Close)",
        trigger: ".modal-footer button",
        run: function () {
            var $button = $(".modal-footer button").filter(function () {
                var t = $(this).text().trim();
                return t === "Save & Close" || t === "Save";
            });
            $button[0].click();
        },
    };

    // Post-condition gate for state transitions that happen INSIDE the
    // work log line's own dialog (opened via the non-editable
    // `work_log_ids` one2many — see openWorkLogLineSteps below). Unlike a
    // top-level record, that dialog never fully closes after the
    // "Are you sure?" confirmation: it stays open (still a `.modal`) while
    // only the confirmation dialog stacked on top of it closes. The
    // documented `body:not(:has(.modal))` gate (odoo-development-ui-test
    // skill, patterns.md §K) therefore never becomes true here. This is
    // its nested-dialog equivalent: wait until at most ONE `.modal` is
    // still on screen (the work log dialog itself), i.e. the confirmation
    // dialog stacked on top of it (and, for Cancel, the reason wizard
    // beneath it) has fully closed — the same FieldWrapper re-render race
    // (patterns.md §K) can otherwise hit the statusbar widget inside that
    // still-open dialog.
    var nestedDialogSettledExtraTrigger = "body:not(:has(.modal:eq(1)))";

    // Small safety margin over the web_tour step default (10000ms, 14.0,
    // odoo-development-ui-test skill tour-14.md): the hr.work_log form
    // dialog is assembled by several ssi_decorator hooks (multiple-approval
    // page, status-check page, header buttons per _header_button_order,
    // plus this module's own Cost tab) on top of an RPC fetch of the full
    // view, so it is reasonable for it to render slightly slower than a
    // bare form. This is NOT the fix for the dialog-never-detected CI
    // failure (PR #245, rounds 3-5) — see the trigger selector note below.
    var WORK_LOG_DIALOG_TIMEOUT = 15000;

    // Open the fixture work log line identified by its Description, from
    // inside the (already open) Work Log tab. Used by every state
    // transition tour (04-confirm through 14-restart-approval): clicking a
    // row of a non-editable one2many list always opens the record's own
    // form in a dialog, regardless of the parent form's edit/view mode, so
    // no "Click Edit" step is needed here (unlike Create/Edit/Delete below).
    function openWorkLogLineSteps(description) {
        return [
            openWorkLogTabStep,
            {
                content: "Open the work log line",
                trigger:
                    ".o_field_x2many[name='work_log_ids'] " +
                    ".o_data_row:contains(" +
                    description +
                    ") .o_data_cell:first",
            },
            {
                content: "Work log dialog is open",
                // NOT ".modal .o_form_view". 14.0's web_tour, when a step
                // doesn't set `in_modal: false` (default true), resolves
                // the trigger via `$modal_displayed.find(tip.trigger)` —
                // already scoped to the currently open modal. Prefixing
                // the selector with `.modal` then asks it to find a
                // SECOND, nested `.modal` ancestor inside the modal that's
                // already the search root, which never exists — the
                // trigger silently never matches, no matter how long the
                // timeout is (odoo-development-ui-test skill, patterns.md
                // §H: "14.0 — JANGAN prefiks trigger in-modal dengan
                // `.modal`"). Confirmed locally: with this exact fix, the
                // dialog (which — per CI failure screenshots, PR #245,
                // run 31921263812 — was already rendering correctly the
                // whole time) is detected immediately.
                trigger: ".o_form_view",
                timeout: WORK_LOG_DIALOG_TIMEOUT,
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ];
    }

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
            // ── Flow 3 — On the Work Log tab, click Add a line. Adding a
            // line (and Delete below) needs the timesheet FORM itself in
            // edit mode — a non-editable one2many hides "Add a line" and
            // the row delete icon while the parent form is read-only, the
            // same mechanic that already forces every other IK in this
            // repo to click "Edit" before touching a field (see
            // odoo-development-ui-test skill precedent, e.g.
            // ssi_timesheet_hr_timesheet_edit). The IK's own Flow omits
            // this click; it is added here as the minimum bridging step
            // the tour cannot run without.
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
            openWorkLogTabStep,
            {
                content: "Click Add a line",
                trigger:
                    ".o_field_x2many[name='work_log_ids'] " +
                    ".o_field_x2many_list_row_add a",
            },
            {
                content: "Work log dialog is open in edit mode",
                // No ".modal" prefix — see the comment on
                // openWorkLogLineSteps's "Work log dialog is open" step.
                trigger: ".o_form_view.o_form_editable",
                timeout: WORK_LOG_DIALOG_TIMEOUT,
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 3 (repeat) — Fill in Description, Date, Analytic
            // Account, Duration.
            {
                content: "Fill in Description",
                // No ` input` suffix: InputField.init() (basic_fields.js)
                // sets `this.tagName = 'input'` in edit mode for plain
                // Char/Float fields that don't override `start()` (unlike
                // Date/Many2one below, which replace $el with a wrapping
                // element) — so `.o_field_widget[name='description']` in
                // edit mode IS the `<input>` itself.
                trigger: ".o_field_widget[name='description']",
                run: "text TOUR-WL-CREATE-UI",
            },
            {
                content: "Fill in Date",
                trigger: ".o_field_widget[name='date'] input",
                run: "text_blur 01/15/2026",
            },
            {
                content: "Select the Analytic Account",
                trigger: ".o_field_many2one[name='analytic_account_id'] input",
                run: "text TOUR-WORKLOG-AA",
            },
            {
                content: "Pick the Analytic Account from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-WORKLOG-AA)",
                in_modal: false,
            },
            {
                content: "Fill in Duration",
                // No ` input` suffix — float_time (FieldFloatTime) extends
                // FieldFloat/NumericField, which never overrides `start()`,
                // so the same InputField edit-mode rule applies.
                trigger: ".o_field_widget[name='amount']",
                run: "text_blur 4:00",
            },
            // ── Flow 3 (repeat) — Click Save & Close.
            clickDialogSaveStep,
            {
                // Gate: dialog fully closed before touching the parent
                // form again (odoo-development-ui-test skill, patterns.md
                // §K — same FieldWrapper re-render race applies to the
                // one2many list widget).
                content: "New line is added to the Work Log tab",
                trigger:
                    ".o_field_x2many[name='work_log_ids'] " +
                    ".o_data_row:contains(TOUR-WL-CREATE-UI)",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 4 — Click Save on the timesheet form.
            {
                content: "Save the timesheet",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — new work log record created in Draft
            // status, visible on the timesheet's Work Log tab.
            {
                content: "Timesheet is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
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
            openWorkLogTabStep,
            // ── Flow 3 — On the Work Log tab, click the line to edit.
            {
                content: "Open the work log line",
                trigger:
                    ".o_field_x2many[name='work_log_ids'] " +
                    ".o_data_row:contains(TOUR-WL-EDIT) .o_data_cell:first",
            },
            {
                content: "Work log dialog is open in edit mode",
                // No ".modal" prefix — see the comment on
                // openWorkLogLineSteps's "Work log dialog is open" step.
                trigger: ".o_form_view.o_form_editable",
                timeout: WORK_LOG_DIALOG_TIMEOUT,
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 4 — Change Description.
            {
                content: "Change Description",
                // No ` input` suffix — see the comment on the create tour's
                // "Fill in Description" step above.
                trigger: ".o_field_widget[name='description']",
                run: "text TOUR-WL-EDITED",
            },
            // ── Flow 5 — Click Save & Close.
            clickDialogSaveStep,
            {
                content: "Line shows the new Description",
                trigger:
                    ".o_field_x2many[name='work_log_ids'] " +
                    ".o_data_row:contains(TOUR-WL-EDITED)",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 6 — Click Save on the timesheet form.
            {
                content: "Save the timesheet",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — record is updated.
            {
                content: "Timesheet is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), [
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
            openWorkLogTabStep,
            // ── Flow 3 — On the Work Log tab, select the line to delete
            // and click the row's delete (trash) icon.
            {
                content: "Delete the work log line",
                trigger:
                    ".o_field_x2many[name='work_log_ids'] " +
                    ".o_data_row:contains(TOUR-WL-DELETE) .o_list_record_remove",
            },
            {
                content: "Line no longer appears on the Work Log tab",
                trigger:
                    ".o_field_x2many[name='work_log_ids']" +
                    ":not(:has(.o_data_row:contains(TOUR-WL-DELETE)))",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            // ── Flow 4 — Click Save on the timesheet form.
            {
                content: "Save the timesheet",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — work log record permanently removed.
            {
                content: "Timesheet is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log/04-confirm.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), openWorkLogLineSteps("TOUR-WL-CONFIRM"), [
            // ── Flow 4 — Click the Confirm button.
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
            },
            // ── Flow 5 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status changes to Waiting for Approval.
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm']" +
                    ".btn-primary",
                extra_trigger: nestedDialogSettledExtraTrigger,
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log/05-approve.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), openWorkLogLineSteps("TOUR-WL-APPROVE"), [
            // ── Flow 4 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
            },
            // ── Flow 5 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — single-level approval template
            // fulfilled immediately, so status changes to Done.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done']" +
                    ".btn-primary",
                extra_trigger: nestedDialogSettledExtraTrigger,
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log/06-reject.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), openWorkLogLineSteps("TOUR-WL-REJECT"), [
            // ── Flow 4 — Click the Reject button.
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
            },
            // ── Flow 5 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status changes to Rejected.
            {
                content: "Status is Rejected",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='reject']" +
                    ".btn-primary",
                extra_trigger: nestedDialogSettledExtraTrigger,
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log/10-cancel.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), openWorkLogLineSteps("TOUR-WL-CANCEL"), [
            // ── Flow 4 — Click the Cancel button. `name` is a numeric
            // action id on this button, so match its label instead.
            clickHeaderButtonByLabel("Cancel"),
            // ── Flow 5 — In the wizard, select the Reason.
            {
                // 14.0: do NOT prefix with `.modal` — the trigger is
                // searched INSIDE the (topmost) modal already.
                content: "Wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Select the cancellation reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] " +
                    ".o_radio_item:contains(TOUR-WORKLOG-CANCEL-REASON) input",
            },
            // ── Flow 6 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            // ── Flow 7 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status changes to Cancelled, and the
            // selected Reason is recorded on the work log.
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel']" +
                    ".btn-primary",
                extra_trigger: nestedDialogSettledExtraTrigger,
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Cancellation reason is displayed",
                // No ".modal:visible" prefix — same in_modal scoping
                // reason as the dialog-open steps above; $modal_displayed
                // already IS the currently open modal, so the trigger is
                // written relative to its content.
                trigger: "h2:contains(Cancellation reason)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log/12-restart.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), openWorkLogLineSteps("TOUR-WL-RESTART"), [
            // ── Flow 4 — Click the Restart button.
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
            },
            // ── Flow 5 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — status returns to Draft.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft']" +
                    ".btn-primary",
                extra_trigger: nestedDialogSettledExtraTrigger,
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log/13-reset-number.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTimesheetMenuSteps(), openWorkLogLineSteps("TOUR-WL-RESETNUM"), [
            // ── Flow 4 — Click the Reset Document Number button.
            {
                content: "Click the Reset Document Number button",
                trigger:
                    ".o_statusbar_buttons " +
                    "button[name='action_reset_document_number']",
            },
            // ── Flow 5 — Click OK on the confirmation dialog.
            confirmDialogStep,
            // ── Post-Condition — document number returns to "/".
            {
                content: "Document number is reset to /",
                // `name` (mixin_transaction_view_form's <h1>) carries
                // class="oe_edit_only" — hidden by CSS whenever the form
                // is in READONLY mode, which this dialog is (no "Click
                // Edit" step in this Flow). Its read-only counterpart,
                // shown instead, is `display_name` (class="oe_read_only")
                // — confirmed via CI (PR #245, run 31925098655): the
                // "name" element existed in the DOM (trigger count 1) but
                // was never :visible, hence the timeout. No ".modal:
                // visible" prefix either — same in_modal scoping reason as
                // the dialog-open steps above.
                trigger: ".o_field_widget[name='display_name']:contains(/)",
                extra_trigger: nestedDialogSettledExtraTrigger,
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/hr_work_log/14-restart-approval.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_work_log_mixin_hr_work_log_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openTimesheetMenuSteps(),
            openWorkLogLineSteps("TOUR-WL-RESTARTAPPROVAL"),
            [
                // ── Flow 4 — Click the Restart Approval Process button.
                {
                    content: "Click the Restart Approval Process button",
                    trigger:
                        ".o_statusbar_buttons " +
                        "button[name='action_reload_approval_template']",
                },
                // ── Flow 5 — Click OK on the confirmation dialog.
                confirmDialogStep,
                // ── Post-Condition — status remains Waiting for Approval.
                {
                    content: "Status remains Waiting for Approval",
                    trigger:
                        ".o_statusbar_status " +
                        ".o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: nestedDialogSettledExtraTrigger,
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );
});
