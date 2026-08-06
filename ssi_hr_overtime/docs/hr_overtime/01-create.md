# Create Overtime

> **Module:** ssi_hr_overtime
>
> **Model:** `hr.overtime`
>
> **Menu:** Human Resource > Timesheets > Overtimes
>
> **Actor:** user in group _Overtime — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `confirm_ok` (state
  `draft`), `manual_number_ok` (state `draft`), `restart_approval_ok` (state `confirm`),
  `cancel_ok` (states `draft`, `confirm`, `done`), and `restart_ok` (states `cancel`,
  `reject`) to the relevant groups — see the _Standard_ `policy.template` shipped with
  this module.
- **Config:** An active `approval.template` for this model exists — see the _Standard_
  `approval.template` shipped with this module.
- **Config:** An active `sequence.template` for this model exists — see the _Standard
  Overtime_ `sequence.template` shipped with this module.
- **Data:** The **Employee** to select has an `hr.employee` record, and has an
  `hr.timesheet` record whose **Date Start**/**Date End** range covers this overtime's
  **Date** (see `ssi_timesheet/docs/hr_timesheet/01-create.md`) — an overtime cannot be
  saved without a matching timesheet.
- **Data:** If **Overtime Type** has **Apply Limit Per Days** checked, the sum of
  **Planned Hours** across this employee's other (non-cancelled, non-rejected) overtimes
  on the same **Date** and **Overtime Type** must not exceed **Limit Per Days** —
  otherwise saving fails (see `Limit Per Days` on
  `ssi_hr_overtime/docs/hr_overtime_type/01-create.md`).
- **Access:** User is in group _Overtime — User_.

## Flow

1. Open the **Human Resource > Timesheets > Overtimes** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Employee**: Automatically filled from the current user's linked employee record,
     if any. Change if needed.
   - **Department**, **Manager**, **Job Position**: Automatically filled from
     **Employee**. Read-only.
   - **Overtime Type** _(required)_: Select the type of overtime being requested.
     **Apply Limit Per Days** and **Limit Per Days** are displayed read-only, copied
     from the selected type.
   - **Date** _(required)_: Enter the date this overtime covers. Defaults to today.
   - **Date Start** _(required)_: Enter the start date and time of the overtime. Must
     fall on the same calendar day as **Date**. Defaults to the current date and time;
     changing **Date** while this field is still empty fills it with midnight of that
     date.
   - **Date End** _(required)_: Enter the end date and time of the overtime. Must not be
     earlier than **Date Start**, and the difference between **Date End** and **Date
     Start** must not exceed 24 hours. Must not overlap the date/time range of another
     (non-cancelled, non-rejected) overtime for the same **Employee**.
4. Click **Save**.

## Post-Condition

- A new overtime record is created in **Draft** status.
- **# Timesheet** is automatically linked to the `hr.timesheet` whose date range covers
  this overtime's **Date**; saving fails if no matching timesheet is found.
- **Planned Hours** is automatically computed as the difference between **Date Start**
  and **Date End**. **Realized Hours** is computed the same way at this point, since no
  **Attendances** are linked yet — see `04-confirm` for how **Attendances** get linked
  and **Realized Hours** subsequently narrows to the overlapping check-in/check-out
  time.
- The document number stays **/** until the record transitions to **Done**, which
  happens automatically once approval completes (see `04-confirm`) — there is no
  separate Finish/Done button — unless the actor has _Can Input Manual Document Number_
  access (see `13-reset-number`).
