# Start Timesheet

> **Module:** ssi_timesheet
>
> **Model:** `hr.timesheet`
>
> **Menu:** Human Resource > Timesheets > Timesheets
>
> **Actor:** user in group _Timesheets — User_
>
> **State:** `draft` → `open`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `open_ok` for state
  `draft` to the actor's group (see the _Standard Timesheet_ `policy.template`).
- **Config:** An active `sequence.template` for this model exists (see the _Standard
  Timesheet_ `sequence.template`) — the document number is assigned automatically at
  this step.
- **Access:** User is in group _Timesheets — User_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the record to start.
3. Click the **Start** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **On Progress**.
- The **Computations** tab is reloaded and recomputed automatically (same effect as the
  **Reload** and **Compute** buttons described in `01-create`).
- If the document number is still **/**, it is assigned automatically from the sequence
  configured by the matching `sequence.template`.
