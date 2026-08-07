# Create Leave Allocation Request Batch

> **Module:** ssi_hr_leave_allocation_request_batch
>
> **Model:** `hr.leave_allocation_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Allocation Request Batch
>
> **Actor:** user in group _Leave Allocation Request Batch — User_
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
  group _Leave Allocation Request Batch — Validator_).
- **Config:** An active `sequence.template` for this model exists — see the _Standard_
  `sequence.template` shipped with this module.
- **Data:** Each employee to select in **Employee(s)** has an `hr.employee` record.
  Approving this batch to **Done** (`05-approve`) creates one `hr.leave_allocation`
  document per selected employee that does not already have a clashing allocation, so
  the same data prerequisites documented for a single leave allocation apply per
  employee — see `ssi_hr_holiday/docs/hr_leave_allocation/01-create.md` (e.g., the
  selected **Type** must have **Need Allocation** checked, and the employee must not
  already have an active `hr.leave_allocation` whose date range overlaps this batch's
  **Date Start**/**Date End**).
- **Access:** User is in group _Leave Allocation Request Batch — User_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocation Request Batch** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Type** _(required)_: Select the leave type that will be applied to every
     `hr.leave_allocation` document created for this batch. Only leave types with **Need
     Allocation** checked can be selected.
   - **Number Of Days** _(required)_: Enter the number of leave days granted by every
     `hr.leave_allocation` document created for this batch.
   - **Employee(s)** _(required)_: Select the employees to include in this batch.
   - **Date Start** _(required)_: Enter the start date shared by every
     `hr.leave_allocation` document created for this batch.
   - **Date End** _(required)_: Enter the end date shared by every `hr.leave_allocation`
     document created for this batch.
   - **Can be Extended**: Check to allow **Date Extended** to be set later than **Date
     End**. Leave unchecked to keep **Date Extended** equal to **Date End**.
   - **Date Extended**: Automatically filled from **Date End**. If **Can be Extended**
     is checked, change it to a later date; entering a date earlier than **Date End**
     triggers a warning and it is reset back to **Date End**.
4. Click **Save**.

## Post-Condition

- A new leave allocation request batch record is created in **Draft** status.
- The **Leave Allocation Request** tab stays empty — the individual
  `hr.leave_allocation` documents are only created once the batch's approval completes
  and it reaches **Done** (see `05-approve`), not when it is confirmed (see
  `04-confirm`).
- The document number stays **/** until the record transitions to **Done**, which
  happens automatically once approval completes — there is no separate Finish/Done
  button — unless the actor has _Can Input Manual Document Number_ access (see
  `13-reset-number`).
