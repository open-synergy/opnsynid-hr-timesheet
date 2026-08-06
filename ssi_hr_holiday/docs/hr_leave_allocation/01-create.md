# Create Leave Allocation

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_allocation`
>
> **Menu:** Human Resource > Timesheets > Leave Allocations
>
> **Actor:** user in group _Leave Allocation — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `confirm_ok` (state
  `draft`), `manual_number_ok` (state `draft`), `cancel_ok` (states `draft`, `confirm`,
  `open`, `done`, `reject`), `restart_ok` (state `cancel`), and `terminate_ok` (state
  `done`) to the relevant groups — see the _Standard_ `policy.template` shipped with
  this module.
- **Config:** An active `approval.template` for this model exists — see the _Standard_
  `approval.template` shipped with this module.
- **Config:** An active `sequence.template` for this model exists — see the _Standard
  Leave Allocation_ `sequence.template` shipped with this module.
- **Data:** The **Employee** to select has an `hr.employee` record.
- **Data:** A **Leave Type** exists with **Need Allocation** checked (see
  `ssi_hr_holiday/docs/hr_leave_type/01-create.md`) — only leave types with **Need
  Allocation** checked can be selected as **Leave Type** here.
- **Access:** User is in group _Leave Allocation — User_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocations** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Leave Type** _(required)_: Select a leave type that has **Need Allocation**
     checked.
   - **Employee**: Automatically filled from the current user's linked employee record,
     if any. Change if needed.
   - **Department**, **Manager**, **Job Position**: Automatically filled from
     **Employee**. Read-only.
   - **Date Start** _(required)_: Enter the first date this allocation is valid from.
   - **Date End** _(required)_: Enter the last date this allocation is valid until. Must
     not be earlier than **Date Start**, and must not overlap the date range of another
     leave allocation for the same **Employee**.
   - **Number of Days** _(required)_: Enter the number of leave days granted by this
     allocation.
   - **Can be Extended**: Check to allow **Date Extended** to be set later than **Date
     End**. Leave unchecked to keep **Date Extended** equal to **Date End**.
   - **Date Extended** _(required)_: Defaults to **Date End**. If **Can be Extended** is
     checked, enter a later date until which leaves may still be taken from this
     allocation.
4. Click **Save**.

## Post-Condition

- A new leave allocation record is created in **Draft** status.
- The document number stays **/** until the record transitions to **In Progress**, which
  happens automatically once approval completes (see `04-confirm`) — there is no
  separate Open/Start button — unless the actor has _Can Input Manual Document Number_
  access (see `13-reset-number`).
- **Used Days**, **Plannned Days**, and **Available Days** are computed from the linked
  **Leaves** tab and initially show **0** and the full **Number of Days**, respectively.
