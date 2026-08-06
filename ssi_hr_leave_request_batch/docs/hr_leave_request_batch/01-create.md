# Create Leave Request Batch

> **Module:** ssi_hr_leave_request_batch
>
> **Model:** `hr.leave_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Request Batch
>
> **Actor:** user in group _Leave Request Batch — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `confirm_ok` (state
  `draft`), `manual_number_ok` (state `draft`), `restart_approval_ok` (states `confirm`,
  `reject`), `cancel_ok` (states `draft`, `confirm`, `done`, `reject`), and `restart_ok`
  (state `cancel`) to the relevant groups — see the _Standard_ `policy.template` shipped
  with this module.
- **Config:** An active `approval.template` for this model exists — see the _Standard_
  `approval.template` shipped with this module (single sequential level, approved by
  group _Leave Request Batch — Validator_).
- **Config:** An active `sequence.template` for this model exists — see the _Standard_
  `sequence.template` shipped with this module.
- **Data:** Each employee to select in **Employee(s)** has an `hr.employee` record.
  Confirming this batch (`04-confirm`) creates one `hr.leave` document per selected
  employee, so the same data prerequisites documented for a single leave apply per
  employee — see `ssi_hr_holiday/docs/hr_leave/01-create.md` (e.g., a matching
  `hr.timesheet` covering the batch's date range, and, if the selected **Type** has
  **Need Allocation** checked, an available `hr.leave_allocation` for that employee).
- **Access:** User is in group _Leave Request Batch — User_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Request Batch** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Type** _(required)_: Select the type of leave that will be applied to every
     `hr.leave` document created for this batch.
   - **Employee(s)**: Select the employees to include in this batch. Leaving it empty
     means confirming the batch creates no `hr.leave` documents (see `04-confirm`).
   - **Date Start** _(required)_: Enter the start date shared by every `hr.leave`
     document created for this batch.
   - **Date End** _(required)_: Enter the end date shared by every `hr.leave` document
     created for this batch.
4. Click **Save**.

## Post-Condition

- A new leave request batch record is created in **Draft** status.
- The **Leave Request** tab stays empty — the individual `hr.leave` documents are only
  created once the batch is confirmed (see `04-confirm`).
- The document number stays **/** until the record transitions to **Done**, which
  happens automatically once approval completes (see `04-confirm`) — there is no
  separate Finish/Done button — unless the actor has _Can Input Manual Document Number_
  access (see `13-reset-number`).
