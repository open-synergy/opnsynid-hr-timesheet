# Create Leave

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave`
>
> **Menu:** Human Resource > Timesheets > Leaves
>
> **Actor:** user in group _Leave — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `confirm_ok` (state
  `draft`), `manual_number_ok` (state `draft`), and `cancel_ok` (states `draft`,
  `confirm`, `done`) to the relevant groups — see the _Standard_ `policy.template`
  shipped with this module.
- **Config:** An active `approval.template` for this model exists — see the _Standard_
  `approval.template` shipped with this module.
- **Config:** An active `sequence.template` for this model exists — see the _Standard
  Leave_ `sequence.template` shipped with this module.
- **Data:** The **Employee** to select has an `hr.employee` record, and has an
  `hr.timesheet` record whose **Date Start**/**Date End** range covers this leave's
  **Date Start**/**Date End** (see `ssi_timesheet/docs/hr_timesheet/01-create.md`) — a
  leave cannot be saved without a matching timesheet.
- **Data:** If the selected **Leave Type** has **Need Allocation** checked, an
  `hr.leave_allocation` record in status **In Progress** must exist for the same
  **Employee** and **Leave Type**, covering this leave's date range, with enough
  **Available Days** (see `ssi_hr_holiday/docs/hr_leave_allocation/01-create.md`) —
  otherwise confirming this leave will fail (see `04-confirm`).
- **Access:** User is in group _Leave — User_.

## Flow

1. Open the **Human Resource > Timesheets > Leaves** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Employee**: Automatically filled from the current user's linked employee record,
     if any. Change if needed.
   - **Department**, **Manager**, **Job Position**: Automatically filled from
     **Employee**. Read-only.
   - **Leave Type** _(required)_: Select the type of leave being requested.
   - **Date Start** _(required)_: Enter the first date of the leave. Must not overlap
     the date range of another (non-cancelled, non-rejected) leave for the same
     **Employee**.
   - **Date End** _(required)_: Enter the last date of the leave. Must not be earlier
     than **Date Start**.
   - **Number of Days** _(required)_: Automatically filled from **Duration** once **Date
     Start**/**Date End** are set. Change if a different value is needed (for example a
     half-day leave).
4. Click **Save**.

## Post-Condition

- A new leave record is created in **Draft** status.
- **# Timesheet** is automatically linked to the `hr.timesheet` whose date range covers
  this leave; saving fails if no matching timesheet is found.
- **Duration** is automatically computed from the **Schedules** tab, which lists the
  attendance schedules matching **Employee**/**Date Start**/**Date End** — public
  holidays within that range are excluded from **Duration** (see the note on
  `ssi_hr_holiday/docs/hr_leave_type/01-create.md`).
- **# Leave Allocation** is automatically linked to a matching, available leave
  allocation for **Employee**/**Leave Type**, if one exists.
- The document number stays **/** until the record transitions to **Done**, which
  happens automatically once approval completes (see `04-confirm`) — there is no
  separate Finish/Done button — unless the actor has _Can Input Manual Document Number_
  access (see `13-reset-number`).
