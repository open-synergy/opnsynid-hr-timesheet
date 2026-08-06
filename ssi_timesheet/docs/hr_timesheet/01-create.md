# Create Timesheet

> **Module:** ssi_timesheet
>
> **Model:** `hr.timesheet`
>
> **Menu:** Human Resource > Timesheets > Timesheets
>
> **Actor:** user in group _Timesheets — User_
>
> **State:** `—` → `draft`
>
> **Inline Actions:** `action_reload_timesheet_computation` (Reload),
> `action_compute_computation` (Compute)

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `open_ok` (state
  `draft`), `confirm_ok` (state `open`), `manual_number_ok` (state `draft`), `cancel_ok`
  (states `draft`, `confirm`, `done`), and `restart_ok` (states `cancel`, `reject`) to
  the relevant groups — see the _Standard Timesheet_ `policy.template` shipped with this
  module.
- **Config:** An active `approval.template` for this model exists — see the _Standard -
  Timesheet_ `approval.template` shipped with this module.
- **Config:** An active `sequence.template` for this model exists — see the _Standard
  Timesheet_ `sequence.template` shipped with this module.
- **Data:** The **Employee** to select has an `hr.employee` record, and optionally has
  **Timesheet Computations** registered on it (see the _Timesheet Computation Item_
  configuration).
- **Access:** User is in group _Timesheets — User_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Employee**: Automatically filled from the current user's linked employee record,
     if any. Change if needed.
   - **Department**, **Manager**, **Job Position**: Automatically filled from
     **Employee**. Read-only.
   - **Date Start** _(required)_: Enter the first date this timesheet covers.
   - **Date End** _(required)_: Enter the last date this timesheet covers. Must not be
     earlier than **Date Start**, and must not overlap the date range of another
     timesheet for the same **Employee**.
4. On the **Computations** tab, click **Reload** to populate the computation lines from
   the **Timesheet Computation Items** registered on **Employee**. Existing lines whose
   item is still registered keep their **Correction Amount**; lines whose item is no
   longer registered are removed. You may then click **Compute** to re-evaluate each
   line's **Amount** and **Final Amount**. Both steps also run automatically when the
   record is **Started** or **Confirmed**, so results still populate even if skipped
   here — use them to preview or adjust corrections beforehand.
5. Click **Save**.

## Post-Condition

- A new timesheet record is created in **Draft** status.
- The document number stays **/** until the record is **Started** (see `07-start`),
  unless the actor has _Can Input Manual Document Number_ access (see
  `13-reset-number`).
