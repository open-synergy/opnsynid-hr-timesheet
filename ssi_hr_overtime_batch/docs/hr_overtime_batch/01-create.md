# Create Overtime Batch

> **Module:** ssi_hr_overtime_batch
>
> **Model:** `hr.overtime_batch`
>
> **Menu:** Human Resource > Timesheets > Overtime Batch
>
> **Actor:** user in group _Overtime Batch — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `confirm_ok` (state
  `draft`), `manual_number_ok` (state `draft`), `restart_approval_ok` (state `confirm`),
  `cancel_ok` (states `draft`, `confirm`, `done`), and `restart_ok` (states `cancel`,
  `reject`) to the relevant groups — see the _Standard_ `policy.template` shipped with
  this module.
- **Config:** An active `approval.template` for this model exists — see the _Standard_
  `approval.template` shipped with this module (single sequential level, approved by
  group _Overtime Batch — Validator_).
- **Config:** An active `sequence.template` for this model exists — see the _Standard_
  `sequence.template` shipped with this module.
- **Data:** Each employee to select in **Employee(s)** has an `hr.employee` record.
  Confirming this batch (`04-confirm`) creates one `hr.overtime` document per selected
  employee, so the same data prerequisites documented for a single overtime apply per
  employee — see `ssi_hr_overtime/docs/hr_overtime/01-create.md` (e.g., a matching
  `hr.timesheet` covering the batch's date range must exist for the employee).
- **Data:** None of the employees selected in **Employee(s)** may already have a
  non-cancelled, non-rejected `hr.overtime` whose **Date Start**/**Date End** range
  overlaps this batch's **Date Start**/**Date End** — otherwise confirming the batch
  fails for that employee (see `04-confirm`).
- **Access:** User is in group _Overtime Batch — User_.

## Flow

1. Open the **Human Resource > Timesheets > Overtime Batch** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Overtime Type** _(required)_: Select the type of overtime that will be applied to
     every `hr.overtime` document created for this batch.
   - **Employee(s)**: Select the employees to include in this batch. Leaving it empty
     means confirming the batch creates no `hr.overtime` documents (see `04-confirm`).
   - **Date Start** _(required)_: Enter the start date and time shared by every
     `hr.overtime` document created for this batch.
   - **Date End** _(required)_: Enter the end date and time shared by every
     `hr.overtime` document created for this batch.
4. Click **Save**.

## Post-Condition

- A new overtime batch record is created in **Draft** status.
- The **Overtime(s)** tab stays empty — the individual `hr.overtime` documents are only
  created once the batch is confirmed (see `04-confirm`).
- The document number stays **/** until the record transitions to **Done**, which
  happens automatically once approval completes (see `04-confirm`) — there is no
  separate Finish/Done button — unless the actor has _Can Input Manual Document Number_
  access (see `13-reset-number`).
