# Create Work Log

> **Module:** ssi_work_log_mixin
>
> **Model:** `hr.work_log`
>
> **Menu:** Human Resource > Timesheets > Timesheets (open a timesheet, then use its
> **Work Log** tab)
>
> **Actor:** user in group _Work log — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Record:** A `hr.timesheet` exists and its status is **On Progress** (see
  `ssi_timesheet/docs/hr_timesheet/07-start.md`), covering the **Date** to be logged for
  the same **Employee**. A work log cannot be saved otherwise — its **Timesheet** field
  is resolved automatically from **Employee** and **Date**, and saving fails with an
  error if no matching **On Progress** timesheet is found.
- **Config:** An active `policy.template` for this model grants `confirm_ok` (state
  `draft`), `manual_number_ok` (state `draft`), `cancel_ok` (states `draft`, `confirm`,
  `done`), and `restart_ok` (states `cancel`, `reject`) to the relevant groups — see the
  _Standard_ `policy.template` shipped with this module.
- **Config:** An active `approval.template` for this model exists — see the _Standard_
  `approval.template` shipped with this module.
- **Config:** An active `sequence.template` for this model exists — see the _Standard_
  `sequence.template` shipped with this module.
- **Data:** The allowed **Analytic Account** list is configured on the **Document Type**
  (the `ir.model` record for `hr.timesheet`) — either a fixed list or a Python-evaluated
  list. This configuration is set up by a developer/administrator and is out of scope
  for this Work Instruction.
- **Access:** User is in group _Work log — User_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the timesheet (status **On Progress**) to log work against.
3. On the **Work Log** tab, click **Add a line**. Repeat the following steps as many
   times as needed:
   - Fill in the required fields:
     - **Description** _(required)_: Enter a short description of the work performed.
     - **Date** _(required)_: Defaults to today. Must fall within the **On Progress**
       timesheet's date range for the same **Employee**.
     - **Analytic Account** _(required)_: Select from the accounts allowed for the
       **Timesheet** document type.
     - **Duration** _(required)_: Enter the hours logged. Defaults to `0.0`.
   - **Tags**: Select one or more tags (see `docs/hr_work_log_tag/01-create.md`).
     Optional.
   - Click **Save & Close**.
4. Click **Save** on the timesheet form to persist the new work log(s).

## Post-Condition

- A new work log record is created in **Draft** status, linked to the timesheet used in
  step 2 as both its **Document** (the `hr.timesheet` record) and its **Timesheet**.
- The document number stays **/** until the record is **Done**, unless the actor has
  _Can Input Manual Document Number_ access (see `13-reset-number`).
- The timesheet's **Total Work Log** is recalculated automatically.

> **Note:** `hr.work_log` also has a standalone **Human Resource > Timesheets > Work
> Logs** menu (group _Work log — Viewer_). That menu is for browsing/reporting across
> all work logs and cannot be used to create a new one — its form permanently hides the
> required **Document ID** field, so a new record can never be completed from there. All
> `hr.work_log` Work Instructions (this one and `02-edit` through `14-restart-approval`)
> are written starting from the timesheet's **Work Log** tab instead.
